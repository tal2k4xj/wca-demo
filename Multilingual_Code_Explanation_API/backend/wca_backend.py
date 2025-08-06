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
import logging

console = Console()
app = typer.Typer()

# Default WCA API endpoints
DEFAULT_BASE_URL = "https://api.dataplatform.cloud.ibm.com/v2/wca/core/chat/text/generation"
DEFAULT_IBM_IAM_URL = "https://iam.cloud.ibm.com/identity/token"
IAM_APIKEY = "IAM_APIKEY"

logger = logging.getLogger(__name__)

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

def call_wca_api(payload, file_dict=[], url=os.getenv("BASE_URL", DEFAULT_BASE_URL), request_id=str(uuid.uuid4()), apikey=None):
    """Call the Watson Code Assistant API with streaming support."""
    console = Console()
    
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
            raise
    
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

def check_auth(api_key: str) -> bool:
    """Check if authentication is valid."""
    try:
        get_bearer_token(api_key)
        return True
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        return False

def explain(
    source_file: str = typer.Argument(..., help="The source code to explain"),
    prompt: str = typer.Option("Please explain this code in detail:", help="Custom prompt for explanation"),
    api_key: str = typer.Option(None, envvar=IAM_APIKEY, help="IBM Cloud API key"),
):
    """Explain the provided source code in detail with custom prompt."""
    # Check authentication first
    if not check_auth(api_key):
        raise ValueError("Authentication failed. Please check your API key.")

    # Format the prompt with the code
    formatted_prompt = f"{prompt}\n\n{source_file}"
    
    # Prepare the payload
    payload = {
        "message_payload": {
            "messages": [{
                "content": formatted_prompt,
                "role": "USER"
            }]
        }
    }
    
    # Call API and get response
    response = call_wca_api(payload, [], apikey=api_key)
    
    # Process the response without file writing
    buffer = ""
    for chunk in response.iter_lines():
        if chunk:
            try:
                chunk_data = json.loads(chunk.decode('utf-8'))
                if 'response' in chunk_data and 'message' in chunk_data['response']:
                    content = chunk_data['response']['message'].get('content', '')
                    if content:
                        buffer += content
            except json.JSONDecodeError:
                continue
    
    return buffer.strip()

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
