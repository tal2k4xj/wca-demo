import pytest
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

@pytest.fixture(scope="session")
def test_data_dir():
    """Create and clean up test data directory"""
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    
    # Create sample test files
    with open(test_dir / "sample.pdf", "wb") as f:
        f.write(b"Sample PDF content")
    
    with open(test_dir / "invalid.txt", "w") as f:
        f.write("Invalid file content")
    
    yield test_dir
    
    # Clean up
    shutil.rmtree(test_dir)

@pytest.fixture(autouse=True)
def clean_temp_files():
    """Clean up temporary files before and after each test"""
    temp_dir = Path("temp")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    yield
    shutil.rmtree(temp_dir)

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Set test environment
    os.environ["TESTING"] = "true"
    
    # Set default test values if not present
    if not os.getenv("API_KEY"):
        os.environ["API_KEY"] = "test_api_key"
    if not os.getenv("IAM_APIKEY"):
        os.environ["IAM_APIKEY"] = "test_api_key"
    if not os.getenv("BASE_URL"):
        os.environ["BASE_URL"] = "https://api.dataplatform.cloud.ibm.com/v2/wca/core/chat/text/generation"
    if not os.getenv("PROJECT_ID"):
        os.environ["PROJECT_ID"] = "test_project_id"

    yield
    
    # Clean up
    os.environ.pop("TESTING", None) 