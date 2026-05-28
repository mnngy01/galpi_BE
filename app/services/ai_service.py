# app/services/ai_service.py
import os
import httpx
from bs4 import BeautifulSoup
from google import genai

# API 키 설정 (나중에 .env로 분리 권장)
GEMINI_API_KEY = "API 키 여기에"
client = genai.Client(api_key=GEMINI_API_KEY)


async def crawl_url(url: str) -> str:
    """URL 접속해서 본문 텍스트 추출"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # 불필요한 태그 제거
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:3000]  # 앞 3000자만 사용
    
    except Exception as e:
        print("크롤링 오류:", e)
    return ""
    # except Exception as e:
    #     return ""  # 크롤링 실패해도 일단 정상 응답


async def summarize(text: str) -> str:
    if not text:
        return ""
    try:
        prompt = f"다음 내용을 한국어로 2~3줄로 요약해줘:\n\n{text}"
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print("요약 오류:", e)
    return ""
    # except Exception as e:
    #     return ""  # 요약 실패해도 서버 정상 응답 ㅅㅂ이러면안되지


async def crawl_and_summarize(url: str) -> str:
    text = await crawl_url(url)
    summary = await summarize(text)
    return summary