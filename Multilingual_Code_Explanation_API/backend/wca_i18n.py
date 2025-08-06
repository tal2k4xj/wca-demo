import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import wca_backend as wca
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI without lifespan
app = FastAPI(
    title="Code Explanation API",
    description="API for explaining code in multiple languages",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    message: str
    code: str
    history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    answer: str
    context: List[str] = []

class CodeExplainRequest(BaseModel):
    code: str

class CodeExplainResponse(BaseModel):
    explanation: str
    analysis: List[str] = []

def get_language_prompt(language: str, code: str, context: list) -> str:
    """Get language-specific prompt."""
    prompts = {
        "traditional_chinese": f"""請用繁體中文詳細解釋以下程式碼：
要求：
1. 用自然的語言解釋程式碼的主要功能
2. 以淺顯易懂的方式分析實現原理
3. 說明重要的參數和返回值
4. 如果有特殊的演算法或設計模式，請用生活化的例子解釋
<<SYS>>
程式碼：
```
{code}
```

相關上下文：
```
{chr(10).join(context) if context else '無'}
```
<</SYS>>
繁體中文詳細解釋:
""",
        "simplified_chinese": f"""请用简体中文详细解释以下代码：
要求：
1. 用自然的语言解释代码的主要功能
2. 以通俗易懂的方式分析实现原理
3. 说明重要的参数和返回值
4. 如果有特殊的算法或设计模式，请用生活化的例子解释
<<SYS>>
代码：
```
{code}
```

相关上下文：
```
{chr(10).join(context) if context else '无'}
```
<</SYS>>
简体中文详细解释:
""",
        "english": f"""Please explain the following code in detail:
Requirements:
1. Explain the main functionality of the code in natural language
2. Analyze the implementation principles in an easy-to-understand way
3. Explain key parameters and return values
4. If there are special algorithms or design patterns, explain with real-life examples
<<SYS>>
Code:
```
{code}
```

Related context:
```
{chr(10).join(context) if context else 'None'}
```
<</SYS>>
explanation code in detail:
""",
        "korean": f"""다음 코드를 한국어로 자세히 설명해주세요:
요구사항:
1. 각 메서드와 함수의 주요 기능을 자연스러운 언어로 설명
2. 구현된 알고리즘과 동작 원리를 이해하기 쉽게 분석
3. 함수의 매개변수와 반환값의 역할 설명
4. 특별한 알고리즘이나 디자인 패턴이 있다면 실생활 예시로 설명
<<SYS>>
코드:
```
{code}
```

관련 컨텍스트:
```
{chr(10).join(context) if context else '없음'}
```
<</SYS>>
각 메서드와 함수의 동작을 상세히 설명해주세요:
""",
        "thai": f"""กรุณาอธิบายโค้ดต่อไปนี้เป็นภาษาไทยโดยละเอียด:
ข้อกำหนด:
1. อธิบายฟังก์ชันหลักของโค้ดด้วยภาษาที่เป็นธรรมชาติ
2. วิเคราะห์หลักการทำงานในแบบที่เข้าใจง่าย
3. อธิบายพารามิเตอร์สำคัญและค่าที่ส่งคืน
4. หากมีอัลกอริทึมหรือรูปแบบการออกแบบพิเศษ ให้อธิบายด้วยตัวอย่างในชีวิตประจำวัน
<<SYS>>
โค้ด:
```
{code}
```

บริบทที่เกี่ยวข้อง:
```
{chr(10).join(context) if context else 'ไม่มี'}
```
<</SYS>>
คำอธิบายโดยละเอียดเป็นภาษาไทย:
""",
        "indonesian": f"""Mohon jelaskan kode berikut dalam Bahasa Indonesia secara detail:
Persyaratan:
1. Jelaskan fungsi utama kode dalam bahasa yang natural
2. Analisis prinsip implementasi dengan cara yang mudah dipahami
3. Jelaskan parameter penting dan nilai return
4. Jika ada algoritma atau pola desain khusus, jelaskan dengan contoh kehidupan sehari-hari
<<SYS>>
Kode:
```
{code}
```

Konteks terkait:
```
{chr(10).join(context) if context else 'Tidak ada'}
```
<</SYS>>
Penjelasan detail dalam Bahasa Indonesia:
""",
        "vietnamese": f"""Vui lòng giải thích chi tiết mã sau bằng tiếng Việt:
Yêu cầu:
1. Giải thích chức năng chính của mã bằng ngôn ngữ tự nhiên
2. Phân tích nguyên lý thực hiện một cách dễ hiểu
3. Giải thích các tham số quan trọng và giá trị trả về
4. Nếu có thuật toán hoặc mẫu thiết kế đặc biệt, hãy giải thích bằng ví dụ thực tế
<<SYS>>
Mã:
```
{code}
```

Ngữ cảnh liên quan:
```
{chr(10).join(context) if context else 'Không có'}
```
<</SYS>>
Giải thích chi tiết bằng tiếng Việt:
"""
    }
    return prompts.get(language, prompts["english"])

async def explain_code(code: str, language: str) -> dict:
    """Explain code in specified language."""
    try:
        prompt = get_language_prompt(language, code, [])
        if not prompt:
            logger.warning(f"Unsupported language: {language}, falling back to English")
            prompt = get_language_prompt("english", code, [])

        try:
            api_key = os.getenv("API_KEY")
            if not api_key:
                logger.error("API key not found in environment variables")
                raise ValueError("API key not found in environment variables")
            
            # Check authentication first
            if not wca.check_auth(api_key):
                logger.error("Authentication failed")
                return {
                    "explanation": "Authentication failed. Please check your API key.",
                    "analysis": []
                }
            
            logger.info(f"Calling WCA API with language: {language}")
            logger.info(f"Prompt: {prompt}")
            
            try:
                # Call explain function with the prompt
                response = wca.explain(
                    source_file=code,  # Pass code directly
                    prompt=prompt,
                    api_key=api_key
                )
                
                if not response:
                    raise ValueError("Empty response from WCA API")

                logger.info(f"Processed Response: {response.strip()}")
                logger.info(f"Language: {language}")
                logger.info(f"Prompt:\n{prompt}")
                logger.info(f"Response:\n{response}")

                return {
                    "explanation": response.strip(),
                    "analysis": []
                }
            except Exception as api_error:
                logger.error(f"WCA API call error: {str(api_error)}")
                return {
                    "explanation": f"An error occurred while processing your request: {str(api_error)}",
                    "analysis": []
                }

        except Exception as e:
            logger.error(f"WCA API setup error: {str(e)}")
            return {
                "explanation": "Error setting up API call. Please check your configuration.",
                "analysis": []
            }

    except Exception as e:
        logger.error(f"General error explaining code: {str(e)}")
        return {
            "explanation": "An unexpected error occurred. Please try again later.",
            "analysis": []
        }

async def process_chat(chat_data: dict) -> dict:
    """Process chat messages and return response."""
    try:
        message = chat_data.get("message", "")
        code = chat_data.get("code", "")

        # Detect language from message
        language = None
        if "請用繁體中文" in message or "traditional" in message.lower():
            language = "traditional_chinese"
        elif "请用简体中文" in message or "simplified" in message.lower():
            language = "simplified_chinese"
        elif "한국어" in message or "korean" in message.lower():
            language = "korean"
        elif "ภาษาไทย" in message or "thai" in message.lower():
            language = "thai"
        elif "bahasa indonesia" in message.lower() or "indonesian" in message.lower():
            language = "indonesian"
        elif "tiếng việt" in message or "vietnamese" in message.lower():
            language = "vietnamese"

        # Use the detected language or default to English
        response = await explain_code(code, language or "english")
        return {
            "answer": response["explanation"],
            "context": response["analysis"]
        }

    except Exception as e:
        logger.error(f"Error in process_chat: {str(e)}")
        raise

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint for code explanation."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        return await process_chat(request.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat: {str(e)}"
        )

@app.post("/explain/{language}", response_model=CodeExplainResponse)
async def explain_code_endpoint(language: str, request: CodeExplainRequest):
    """Analyze and explain code in specified language."""
    if not request.code.strip():
        error_messages = {
            "traditional_chinese": "程式碼不能為空",
            "simplified_chinese": "代码不能为空",
            "korean": "코드가 비어있습니다",
            "thai": "โค้ดต้องไม่ว่างเปล่า",
            "indonesian": "Kode tidak boleh kosong",
            "vietnamese": "Mã không được để trống",
            "english": "Code cannot be empty"
        }
        raise HTTPException(
            status_code=400, 
            detail=error_messages.get(language, "Code cannot be empty")
        )
    
    try:
        return await explain_code(request.code, language)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing code: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)