from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
import os
import json
from datetime import datetime
from colorama import init, Fore, Style
from github import Github
from app.services.code_review_service import trigger_code_review

# Initialize colorama
init(autoreset=True)

github_webhook = APIRouter()

def verify_github_signature(request_data: bytes, signature_header: str) -> bool:
    """Verify that the webhook is from GitHub using the secret token"""
    webhook_secret = os.environ.get('GITHUB_WEBHOOK_SECRET', '')
    
    # Skip verification if no secret is set
    if not webhook_secret:
        return True
        
    if not signature_header:
        return False
    
    try:
        expected_signature = hmac.new(
            key=webhook_secret.encode(),
            msg=request_data,
            digestmod=hashlib.sha256
        ).hexdigest()
        
        expected_header = f'sha256={expected_signature}'
        is_valid = hmac.compare_digest(expected_header, signature_header)
        return is_valid
        
    except Exception as e:
        print(f"{Fore.RED}Error verifying signature: {str(e)}{Style.RESET_ALL}")
        return False

def format_file_changes(commit):
    """Format file changes in a readable way"""
    changes = []
    if commit.get('modified'):
        changes.append(f"{Fore.YELLOW}Modified:{Style.RESET_ALL} {', '.join(commit['modified'])}")
    if commit.get('added'):
        changes.append(f"{Fore.GREEN}Added:{Style.RESET_ALL} {', '.join(commit['added'])}")
    if commit.get('removed'):
        changes.append(f"{Fore.RED}Removed:{Style.RESET_ALL} {', '.join(commit['removed'])}")
    return '\n  '.join(changes) if changes else "No files changed"

def get_commit_diff(repo_name: str, commit_sha: str) -> str:
    """Get the code diff for a specific commit"""
    try:
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            return "Unable to fetch diff: GITHUB_TOKEN not set"
            
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        commit = repo.get_commit(commit_sha)
        
        diff_output = []
        for file in commit.files:
            diff_output.append(f"\n{Fore.CYAN}=== {file.filename} ==={Style.RESET_ALL}")
            
            # Show status with color
            status_color = {
                'modified': Fore.YELLOW,
                'added': Fore.GREEN,
                'removed': Fore.RED,
                'renamed': Fore.BLUE
            }.get(file.status, Fore.WHITE)
            diff_output.append(f"{status_color}Status: {file.status}{Style.RESET_ALL}")
            
            # Show the actual diff
            if file.patch:
                for line in file.patch.split('\n'):
                    if line.startswith('+'):
                        diff_output.append(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
                    elif line.startswith('-'):
                        diff_output.append(f"{Fore.RED}{line}{Style.RESET_ALL}")
                    else:
                        diff_output.append(line)
                        
        return '\n'.join(diff_output)
    except Exception as e:
        return f"{Fore.RED}Error fetching diff: {str(e)}{Style.RESET_ALL}"

def get_file_content(repo_name: str, commit_sha: str, file_path: str) -> str:
    """Get the full content of a file at a specific commit"""
    try:
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            return None
            
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        # Get the file content at this commit
        content = repo.get_contents(file_path, ref=commit_sha)
        if content:
            return content.decoded_content.decode('utf-8')
        return None
    except Exception as e:
        print(f"{Fore.RED}Error fetching file content: {str(e)}{Style.RESET_ALL}")
        return None

@github_webhook.post('/webhook/github')
async def handle_github_webhook(request: Request):
    # Get raw body for signature verification
    body = await request.body()
    
    # Verify webhook signature if secret is set
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_github_signature(body, signature):
        raise HTTPException(status_code=401, detail='Invalid signature')

    event_type = request.headers.get('X-GitHub-Event')
    if event_type != 'push':
        return {'message': f'Event {event_type} ignored'}

    try:
        # Parse the payload
        if isinstance(body, bytes):
            body_str = body.decode('utf-8')
        payload = json.loads(body_str)
        
        # Handle nested JSON from smee.io
        if 'payload' in payload and isinstance(payload['payload'], str):
            payload = json.loads(payload['payload'])

        repo_name = payload.get('repository', {}).get('full_name')
        
        # Process each commit
        commits = payload.get('commits', [])
        for commit in commits:
            # Print commit information with colors
            print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{Style.BRIGHT}Commit Message:{Style.RESET_ALL} {commit.get('message')}")
            print(f"\n{Fore.BLUE}Author:{Style.RESET_ALL} {commit.get('author', {}).get('name')} ({commit.get('author', {}).get('email')})")
            print(f"{Fore.BLUE}Time:{Style.RESET_ALL} {commit.get('timestamp')}")
            
            print(f"\n{Fore.MAGENTA}Changes:{Style.RESET_ALL}")
            print(f"  {format_file_changes(commit)}")
            
            # Get code diff and full file contents
            diff = get_commit_diff(repo_name, commit.get('id'))
            
            # Get full content of modified and added files
            file_contents = {}
            for file_path in commit.get('modified', []) + commit.get('added', []):
                content = get_file_content(repo_name, commit.get('id'), file_path)
                if content:
                    file_contents[file_path] = content
            
            print(f"\n{Fore.MAGENTA}Code Changes:{Style.RESET_ALL}")
            print(diff)
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            
            # Trigger code review with diff and full file contents
            trigger_code_review({
                'repository': repo_name,
                'commit_sha': commit.get('id'),
                'commit_message': commit.get('message'),
                'modified_files': commit.get('modified', []),
                'added_files': commit.get('added', []),
                'removed_files': commit.get('removed', []),
                'code_diff': diff,
                'file_contents': file_contents  # Add full file contents
            })
        
        return {'message': 'Webhook processed successfully'}
        
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error parsing JSON: {str(e)}{Style.RESET_ALL}")
        raise HTTPException(status_code=400, detail='Invalid JSON payload')
    except Exception as e:
        print(f"{Fore.RED}Error processing webhook: {str(e)}{Style.RESET_ALL}")
        raise HTTPException(status_code=500, detail='Internal server error')