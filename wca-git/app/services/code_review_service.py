import os
from github import Github
import json
import requests
import base64
import uuid
import time
from rich.console import Console
from rich.markdown import Markdown
import typer

console = Console()
app = typer.Typer()

# Default WCA API endpoints
DEFAULT_BASE_URL = "https://api.dataplatform.cloud.ibm.com/v2/wca/core/chat/text/generation"
DEFAULT_IBM_IAM_URL = "https://iam.cloud.ibm.com/identity/token"
IAM_APIKEY = "IAM_APIKEY"

def get_bearer_token(apikey=None):
    """Get IBM Cloud bearer token for authentication."""
    if not apikey:
        apikey = os.getenv(IAM_APIKEY)
        if not apikey:
            raise ValueError(f"No API key provided. Set the {IAM_APIKEY} environment variable.")
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'urn:ibm:params:oauth:grant-type:apikey', 'apikey': apikey}
    response = requests.post(DEFAULT_IBM_IAM_URL, headers=headers, data=data, timeout=30)
    
    if not response.ok:
        raise Exception(f'Status code: {response.status_code}, Error: {json.loads(response.content)}')
    return response.json()['access_token']

def analyze_code_changes(commit_data):
    """Analyze code changes using WCA API"""
    try:
        # Format the code changes for analysis
        changes_description = []
        
        # Add commit message and metadata
        changes_description.append(f"Commit Message: {commit_data['commit_message']}\n")
        
        # Add file changes summary
        if commit_data['modified_files']:
            changes_description.append("Modified files:")
            changes_description.extend([f"- {file}" for file in commit_data['modified_files']])
        if commit_data['added_files']:
            changes_description.append("\nAdded files:")
            changes_description.extend([f"- {file}" for file in commit_data['added_files']])
        if commit_data['removed_files']:
            changes_description.append("\nRemoved files:")
            changes_description.extend([f"- {file}" for file in commit_data['removed_files']])
            
        # Add code diff for context
        if 'code_diff' in commit_data:
            changes_description.append("\nCode Changes (Diff):")
            changes_description.append(commit_data['code_diff'])
        
        # Add full file contents for comprehensive review
        if 'file_contents' in commit_data:
            changes_description.append("\nFull File Contents:")
            for file_path, content in commit_data['file_contents'].items():
                changes_description.append(f"\n=== {file_path} ===")
                changes_description.append(content)
        
        # Create prompt for WCA
        prompt = f"""you are a senior code reviewer with extensive experience in analyzing code changes. 
-please be keeping high standards of professionalism
-dont be nice or easy going, just direct to the point
-please be clear and concise in your responses
-please be specific and provide detailed information
-please provide examples and context where appropriate
-please analyze this code commit and provide a detailed review focusing on:
1. Summary of the changes
2. Detailed review of each modified file
3. Impact on the codebase
4. Specific recommendations for improvement

For modified files, please review both the changes made and how they fit into the overall file context.

<<SYS>>
changes to review: `{'\n'.join(changes_description)}`
<</SYS>>

Please generate a comprehensive analysis in markdown format, including:
1. Summary of the changes
2. Detailed review of each modified file
3. Impact on the codebase
4. Specific recommendations for improvement
"""

        # Call WCA API
        payload = {
            "message_payload": {
                "messages": [{
                    "content": prompt,
                    "role": "USER"
                }]
            }
        }
        
        response = call_wca_api(payload)
        analysis = stream_response(response, action="Analyzing code")
        return analysis
        
    except Exception as e:
        console.print(f"[red]Error analyzing code changes: {str(e)}[/red]")
        return None

def trigger_code_review(commit_data):
    """
    Trigger a code review for the given commit.
    
    Args:
        commit_data: Dictionary containing:
            - repository: Repository full name (e.g., "owner/repo")
            - commit_sha: Commit SHA
            - commit_message: Commit message
            - modified_files: List of modified files
            - added_files: List of added files
            - removed_files: List of removed files
            - code_diff: Optional, formatted code diff
    """
    try:
        # Get GitHub token
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
            
        g = Github(github_token)
        repo = g.get_repo(commit_data['repository'])
        
        # Get code analysis from WCA
        analysis = analyze_code_changes(commit_data)
        
        # Create issue title
        commit_summary = commit_data['commit_message'].split('\n')[0][:50]
        issue_title = f"Code Review: {commit_summary}..."
        
        # Create issue body
        issue_body = f"""## Code Review for Commit [{commit_data['commit_sha'][:7]}](https://github.com/{commit_data['repository']}/commit/{commit_data['commit_sha']})

### Commit Details
- **Message:** {commit_data['commit_message']}
- **Files Changed:** 
  - Modified: {len(commit_data['modified_files'])}
  - Added: {len(commit_data['added_files'])}
  - Removed: {len(commit_data['removed_files'])}

### WCA Analysis
{analysis if analysis else "No analysis available"}

### Changed Files
"""
        # Add links to changed files
        for file in commit_data['modified_files']:
            issue_body += f"- 📝 [{file}](https://github.com/{commit_data['repository']}/blob/{commit_data['commit_sha']}/{file})\n"
        for file in commit_data['added_files']:
            issue_body += f"- ✨ [{file}](https://github.com/{commit_data['repository']}/blob/{commit_data['commit_sha']}/{file})\n"
        for file in commit_data['removed_files']:
            issue_body += f"- 🗑️ [{file}](https://github.com/{commit_data['repository']}/blob/{commit_data['commit_sha']}/{file})\n"

        # Create the issue
        labels = ['code-review', 'automated']
        issue = repo.create_issue(
            title=issue_title,
            body=issue_body,
            labels=labels
        )
        
        console.print(f"[green]Created code review issue: {issue.html_url}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error triggering code review: {str(e)}[/red]")

def call_wca_api(payload, file_dict=[], url=os.getenv("BASE_URL", DEFAULT_BASE_URL), request_id=str(uuid.uuid4()), apikey=None):
    """Call the Watson Code Assistant API with streaming support."""
    headers = {
        'Authorization': f'Bearer {get_bearer_token(apikey)}',
        'Request-Id': request_id,
        'Origin': 'vscode',
        'Accept': 'text/event-stream'
    }

    files = []
    files.append(('message', (None, json.dumps(payload))))
    for a_file in file_dict:
        file_name = a_file.split("/")[-1]
        with open(a_file, 'rb') as file:
            encoded_content = base64.b64encode(file.read()).decode('utf-8')
        files.append(('files', (file_name, encoded_content, 'text/plain')))

    try:
        response = requests.post(url=url, headers=headers, files=files, timeout=180, stream=True)
        if not response.ok:
            error_msg = f"Error {response.status_code}: {response.text}"
            console.print(f"[red]{error_msg}[/red]")
            response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        console.print("[red]Request timed out. Please try again.[/red]")
        raise
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error connecting to the API: {str(e)}[/red]")
        raise

def stream_response(response, to_file=None, action="Processing"):
    """Stream API response and return the complete response text."""
    buffer = ""
    first_chunk = True
    start_time = time.time()
    
    with console.status(f"[bold blue]{action}...", spinner="dots") as status:
        try:
            for chunk in response.iter_lines():
                if chunk:
                    elapsed = int(time.time() - start_time)
                    if elapsed > 10 and first_chunk:
                        status.update(f"[bold yellow]{action} (taking longer than usual)...")
                    
                    try:
                        chunk_data = json.loads(chunk.decode('utf-8'))
                        if 'response' in chunk_data and 'message' in chunk_data['response']:
                            content = chunk_data['response']['message'].get('content', '')
                            if content:
                                if first_chunk:
                                    first_chunk = False
                                buffer += content
                                if to_file:
                                    to_file.write(content)
                                    to_file.flush()
                                else:
                                    console.print(content, end='')
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            console.print(f"\n[red]Error processing response: {str(e)}[/red]")
    
    return buffer.strip()

def format_as_markdown(content, language=None):
    """Format content as markdown with optional code blocks."""
    # If the content looks like code (has indentation or common code characters)
    if any(char in content for char in '{([;=+-%*/') or '\n ' in content:
        # Wrap it in a code block with the specified language
        lang_spec = language if language else 'python'
        formatted = f"```{lang_spec}\n{content}\n```"
    else:
        # Otherwise, treat it as regular markdown
        formatted = content
    
    return Markdown(formatted)

def explain(
    source_file: typer.FileText = typer.Argument(..., help="The source code file to explain"),
    api_key: str = typer.Option(None, envvar=IAM_APIKEY, help="IBM Cloud API key"),
    to_file: typer.FileTextWrite = typer.Option(None, help="File to write the explanation to")
):
    """Explain the provided source code in detail."""
    content = source_file.read()
    prompt = f"Please explain this code in detail:\n\n{content}"
    payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
    response = call_wca_api(payload, [source_file.name], apikey=api_key)
    stream_response(response, to_file, "Analyzing code")

def document(
    source_file: typer.FileText = typer.Argument(..., help="The source code file to document"),
    api_key: str = typer.Option(None, envvar=IAM_APIKEY, help="IBM Cloud API key"),
    to_file: typer.FileTextWrite = typer.Option(None, help="File to write the documentation to")
):
    """Generate comprehensive documentation for the provided source code."""
    content = source_file.read()
    prompt = f"Please generate comprehensive documentation for this code in markdown format, including function descriptions, parameters, return values, and examples:\n\n{content}"
    payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
    response = call_wca_api(payload, [source_file.name], apikey=api_key)
    stream_response(response, to_file, "Generating documentation")
