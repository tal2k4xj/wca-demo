from fastapi import FastAPI
from app.webhooks.github_webhook import github_webhook
import uvicorn
import os

app = FastAPI()

# Include the GitHub webhook router
app.include_router(github_webhook)

if __name__ == "__main__":
    # Load environment variables
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key.replace("export ", "")] = value.strip().strip("'").strip('"')

    # Run with auto-reload enabled
    uvicorn.run(
        "main:app", 
        host="localhost", 
        port=8000, 
        reload=True,  # Enable auto-reload
        reload_dirs=["app"]  # Watch the app directory for changes
    )
