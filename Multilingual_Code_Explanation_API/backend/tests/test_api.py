import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add the root directory to Python path
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from backend.wca_i18n import app, ChatRequest, CodeExplainRequest

client = TestClient(app)

# API Tests
def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_chat_empty_message():
    """Test chat endpoint with empty message"""
    chat_data = {
        "message": "",
        "code": "print('hello')"
    }
    response = client.post("/chat", json=chat_data)
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

def test_chat_missing_fields():
    """Test chat endpoint with missing required fields"""
    # Missing message
    response = client.post("/chat", json={"code": "print('hello')"})
    assert response.status_code == 422

    # Missing both fields
    response = client.post("/chat", json={})
    assert response.status_code == 422

def test_chat_invalid_json():
    """Test chat endpoint with invalid JSON"""
    response = client.post(
        "/chat",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_chat_success():
    """Test successful chat response"""
    request = ChatRequest(
        message="Please explain this code",
        code="def hello(): return 'world'",
        history=[]
    )
    
    response = client.post("/chat", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    print(f"\nChat Response:\n{data['answer']}")
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert "context" in data
    assert isinstance(data["context"], list)
    assert len(data["context"]) == 0

def test_chat_wrong_method():
    """Test chat endpoint with wrong HTTP method"""
    response = client.get("/chat")
    assert response.status_code == 405  # Method not allowed

def test_chat_wrong_content_type():
    """Test chat endpoint with wrong content type"""
    response = client.post(
        "/chat",
        data="plain text",
        headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 422

def test_nonexistent_endpoint():
    """Test accessing non-existent endpoint"""
    response = client.get("/nonexistent")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_explain_code_traditional_chinese():
    """Test code explanation in Traditional Chinese"""
    request = CodeExplainRequest(
        code="def hello(): return 'world'"
    )
    
    # Test empty code
    empty_request = CodeExplainRequest(code="")
    response = client.post("/explain/traditional_chinese", json=empty_request.model_dump())
    assert response.status_code == 400
    assert "程式碼不能為空" in response.json()["detail"]
    
    # Test actual code explanation
    response = client.post("/explain/traditional_chinese", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    print(f"\nTraditional Chinese Explanation:\n{data['explanation']}")
    assert "explanation" in data
    assert isinstance(data["explanation"], str)
    assert "analysis" in data
    assert isinstance(data["analysis"], list)
    assert len(data["analysis"]) == 0

@pytest.mark.asyncio
async def test_explain_code_simplified_chinese():
    """Test code explanation in Simplified Chinese"""
    request = CodeExplainRequest(
        code="def hello(): return 'world'"
    )
    
    # Test empty code
    empty_request = CodeExplainRequest(code="")
    response = client.post("/explain/simplified_chinese", json=empty_request.model_dump())
    assert response.status_code == 400
    assert "代码不能为空" in response.json()["detail"]
    
    # Test actual code explanation
    response = client.post("/explain/simplified_chinese", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    print(f"\nSimplified Chinese Explanation:\n{data['explanation']}")
    assert "explanation" in data
    assert isinstance(data["explanation"], str)
    assert "analysis" in data
    assert isinstance(data["analysis"], list)
    assert len(data["analysis"]) == 0

@pytest.mark.asyncio
async def test_explain_code_korean():
    """Test code explanation in Korean"""
    request = CodeExplainRequest(
        code="def hello(): return 'world'"
    )
    
    # Test empty code
    empty_request = CodeExplainRequest(code="")
    response = client.post("/explain/korean", json=empty_request.model_dump())
    assert response.status_code == 400
    assert "코드가 비어있습니다" in response.json()["detail"]
    
    # Test actual code explanation
    response = client.post("/explain/korean", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    print(f"\nKorean Explanation:\n{data['explanation']}")
    assert "explanation" in data
    assert isinstance(data["explanation"], str)
    assert "analysis" in data
    assert isinstance(data["analysis"], list)
    assert len(data["analysis"]) == 0

@pytest.mark.asyncio
async def test_explain_code_thai():
    """Test code explanation in Thai"""
    request = CodeExplainRequest(
        code="def hello(): return 'world'"
    )
    
    # Test empty code
    empty_request = CodeExplainRequest(code="")
    response = client.post("/explain/thai", json=empty_request.model_dump())
    assert response.status_code == 400
    assert "โค้ดต้องไม่ว่างเปล่า" in response.json()["detail"]
    
    # Test actual code explanation
    response = client.post("/explain/thai", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert isinstance(data["explanation"], str)
    assert "analysis" in data
    assert isinstance(data["analysis"], list)
    assert len(data["analysis"]) == 0

@pytest.mark.asyncio
async def test_explain_code_indonesian():
    """Test code explanation in Indonesian"""
    request = CodeExplainRequest(
        code="def hello(): return 'world'"
    )
    
    # Test empty code
    empty_request = CodeExplainRequest(code="")
    response = client.post("/explain/indonesian", json=empty_request.model_dump())
    assert response.status_code == 400
    assert "Kode tidak boleh kosong" in response.json()["detail"]
    
    # Test actual code explanation
    response = client.post("/explain/indonesian", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert isinstance(data["explanation"], str)
    assert "analysis" in data
    assert isinstance(data["analysis"], list)
    assert len(data["analysis"]) == 0

@pytest.mark.asyncio
async def test_explain_code_vietnamese():
    """Test code explanation in Vietnamese"""
    request = CodeExplainRequest(
        code="def hello(): return 'world'"
    )
    
    # Test empty code
    empty_request = CodeExplainRequest(code="")
    response = client.post("/explain/vietnamese", json=empty_request.model_dump())
    assert response.status_code == 400
    assert "Mã không được để trống" in response.json()["detail"]
    
    # Test actual code explanation
    response = client.post("/explain/vietnamese", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert isinstance(data["explanation"], str)
    assert "analysis" in data
    assert isinstance(data["analysis"], list)
    assert len(data["analysis"]) == 0

@pytest.mark.asyncio
async def test_explain_complex_code_traditional_chinese():
    """Test complex code explanation in Traditional Chinese"""
    complex_code = """
class BinarySearchTree:
    def __init__(self):
        self.root = None
        
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
            
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
    """
    
    request = CodeExplainRequest(code=complex_code)
    response = client.post("/explain/traditional_chinese", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    print("\n=== Complex Traditional Chinese Explanation ===")
    print(f"Code:\n{complex_code}")
    print(f"Explanation:\n{data['explanation']}")
    print("=" * 50)
    
    # More flexible term checking with alternative terms
    chinese_terms = [
        ["二元搜尋樹", "二元樹", "二叉樹", "搜索樹"],  # Binary search tree alternatives
        ["遞迴", "遞歸", "循環"],  # Recursion alternatives
        ["節點", "結點", "node"]   # Node alternatives
    ]
    
    # Check if at least one term from each group is present
    for term_group in chinese_terms:
        assert any(term in data["explanation"] for term in term_group), \
            f"Expected one of {term_group} in explanation"

@pytest.mark.asyncio
async def test_explain_complex_code_simplified_chinese():
    """Test complex code explanation in Simplified Chinese"""
    complex_code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
    """
    
    request = CodeExplainRequest(code=complex_code)
    response = client.post("/explain/simplified_chinese", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    print("\n=== Complex Simplified Chinese Explanation ===")
    print(f"Code:\n{complex_code}")
    print(f"Explanation:\n{data['explanation']}")
    print("=" * 50)
    
    # More flexible term checking with alternative terms
    chinese_terms = [
        # Sort related terms
        ["快速排序", "快排", "排序", "排列", "sort", "分类", "顺序"],
        # Recursion related terms
        ["递归", "遍历", "循环", "recursive", "重复", "调用自身"],
        # Pivot/Partition related terms
        ["基准", "枢轴", "pivot", "中值", "分区", "分割", "划分"]
    ]
    
    # Check if at least one term from each concept group is present
    matched_terms = []
    for term_group in chinese_terms:
        found = False
        for term in term_group:
            if term.lower() in data["explanation"].lower():
                matched_terms.append(term)
                found = True
                break
        assert found, f"Expected one of {term_group} in explanation. Found terms: {matched_terms}"

@pytest.mark.asyncio
async def test_explain_complex_code_korean():
    """Test complex code explanation in Korean"""
    complex_code = """
class Stack:
    def __init__(self):
        self.items = []
        
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        
    def is_empty(self):
        return len(self.items) == 0
        
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
    """
    
    request = CodeExplainRequest(code=complex_code)
    response = client.post("/explain/korean", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    print("\n=== Complex Korean Explanation ===")
    print(f"Code:\n{complex_code}")
    print(f"Explanation:\n{data['explanation']}")
    print("=" * 50)
    
    # More flexible term checking with alternative terms
    korean_terms = [
        # Method/Function related terms
        ["메서드", "함수", "기능", "method", "function", "메소드"],
        # Data structure related terms
        ["스택", "자료구조", "데이터", "stack", "리스트", "배열"],
        # Implementation/Operation related terms
        ["구현", "동작", "처리", "저장", "추가", "삭제", "확인"]
    ]
    
    # Check if at least one term from each concept group is present
    matched_terms = []
    for term_group in korean_terms:
        found = False
        for term in term_group:
            if term.lower() in data["explanation"].lower():
                matched_terms.append(term)
                found = True
                break
        assert found, f"Expected one of {term_group} in explanation. Found terms: {matched_terms}"

@pytest.mark.asyncio
async def test_explain_complex_code_thai():
    """Test complex code explanation in Thai"""
    complex_code = """
class Stack:
    def __init__(self):
        self.items = []
        
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        
    def is_empty(self):
        return len(self.items) == 0
        
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
    """
    
    request = CodeExplainRequest(code=complex_code)
    response = client.post("/explain/thai", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    print("\n=== Complex Thai Explanation ===")
    print(f"Code:\n{complex_code}")
    print(f"Explanation:\n{data['explanation']}")
    print("=" * 50)
    
    # More flexible term checking with alternative terms
    thai_terms = [
        # Method/Function/Class related terms
        ["เมธอด", "ฟังก์ชัน", "method", "function", "คลาส", "class", "โปรแกรม"],
        # Data structure related terms
        ["สแตก", "stack", "อาร์เรย์", "array", "ลิสต์", "list", "ข้อมูล", "data"],
        # Operation related terms
        ["เพิ่ม", "ลบ", "ตรวจสอบ", "push", "pop", "peek", "ทำงาน"]
    ]
    
    matched_terms = []
    for term_group in thai_terms:
        found = False
        for term in term_group:
            if term.lower() in data["explanation"].lower():
                matched_terms.append(term)
                found = True
                break
        assert found, f"Expected one of {term_group} in explanation. Found terms: {matched_terms}"

@pytest.mark.asyncio
async def test_explain_complex_code_indonesian():
    """Test complex code explanation in Indonesian"""
    complex_code = """
class Stack:
    def __init__(self):
        self.items = []
        
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        
    def is_empty(self):
        return len(self.items) == 0
        
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
    """
    
    request = CodeExplainRequest(code=complex_code)
    response = client.post("/explain/indonesian", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    print("\n=== Complex Indonesian Explanation ===")
    print(f"Code:\n{complex_code}")
    print(f"Explanation:\n{data['explanation']}")
    print("=" * 50)
    
    # More flexible term checking with alternative terms
    indonesian_terms = [
        # Method/Function/Class related terms
        ["metode", "fungsi", "method", "function", "kelas", "class", "program"],
        # Data structure related terms
        ["stack", "tumpukan", "array", "larik", "list", "daftar", "data"],
        # Operation related terms
        ["tambah", "hapus", "periksa", "push", "pop", "peek", "operasi"]
    ]
    
    matched_terms = []
    for term_group in indonesian_terms:
        found = False
        for term in term_group:
            if term.lower() in data["explanation"].lower():
                matched_terms.append(term)
                found = True
                break
        assert found, f"Expected one of {term_group} in explanation. Found terms: {matched_terms}"

@pytest.mark.asyncio
async def test_explain_complex_code_vietnamese():
    """Test complex code explanation in Vietnamese"""
    complex_code = """
class Stack:
    def __init__(self):
        self.items = []
        
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        
    def is_empty(self):
        return len(self.items) == 0
        
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
    """
    
    request = CodeExplainRequest(code=complex_code)
    response = client.post("/explain/vietnamese", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    print("\n=== Complex Vietnamese Explanation ===")
    print(f"Code:\n{complex_code}")
    print(f"Explanation:\n{data['explanation']}")
    print("=" * 50)
    
    # More flexible term checking with alternative terms
    vietnamese_terms = [
        # Method/Function/Class related terms
        ["phương thức", "hàm", "method", "function", "lớp", "class", "chương trình"],
        # Data structure related terms
        ["ngăn xếp", "stack", "mảng", "array", "danh sách", "list", "dữ liệu"],
        # Operation related terms
        ["thêm", "xóa", "kiểm tra", "push", "pop", "peek", "hoạt động"]
    ]
    
    matched_terms = []
    for term_group in vietnamese_terms:
        found = False
        for term in term_group:
            if term.lower() in data["explanation"].lower():
                matched_terms.append(term)
                found = True
                break
        assert found, f"Expected one of {term_group} in explanation. Found terms: {matched_terms}"
        