from fastapi import FastAPI
from app.webhooks.github_webhook import github_webhook

app = FastAPI(title="Code Review Bot")

# Include the github webhook router
app.include_router(github_webhook)

def create_app():
    # ... existing code ...
    
    return app 