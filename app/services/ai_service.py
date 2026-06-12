# app/services/ai_service.py
import httpx
from bs4 import BeautifulSoup
from google import genai

# API 키 설정 (나중에 .env로 분리 권장)
GEMINI_API_KEY = "API키는 꼭 빼도록 합시다 깃허브가 차단하기전에..."

client = genai.Client(api_key=GEMINI_API_KEY)

# 관심사 태그 목록 (member_schema.py의 VALID_INTERESTS와 동일)
INTERESTS = ["차(tea)", "아웃도어", "아이와 함께", "반려", "건축", "해외여행", "맛집", "인테리어"]

async def crawl_url(url: str) -> str:
    """URL 접속해서 본문 텍스트 추출"""
    try:
        async with httpx.AsyncClient(timeout=10) as http_client:
            response = await http_client.get(url)
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
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print("요약 오류:", e)
    return ""
    # except Exception as e:
    #     return ""  # 요약 실패해도 서버 정상 응답

async def classify_interest(text: str) -> str:
    """
    크롤링한 본문을 보고 관심사 태그 중 가장 적합한 것 하나 반환.
    매칭되는 게 없으면 빈 문자열 반환.
    """
    if not text:
        return ""
    try:
        tags = ", ".join(INTERESTS)
        prompt = (
            f"다음 텍스트를 읽고 아래 카테고리 중 가장 잘 맞는 것 하나만 골라줘. "
            f"반드시 아래 목록 중 하나만 답해. 다른 말은 하지 마.\n\n"
            f"카테고리: {tags}\n\n"
            f"텍스트: {text[:1000]}"
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        result = response.text.strip()

        # 응답이 목록 안에 있는 값인지 확인
        if result in INTERESTS:
            return result
        
        # 혹시 문장으로 답했을 경우 포함 여부 확인
        for interest in INTERESTS:
            if interest in result:
                return interest
        return ""
    
    except Exception as e:
        print("분류 오류:", e)
        return ""

async def crawl_and_summarize(url: str) -> str:
    text = await crawl_url(url)
    summary = await summarize(text)
    return summary

async def crawl_summarize_classify(url: str) -> tuple[str, str]:
    """
    URL 크롤링 + 요약 + 관심사 분류 한 번에.
    반환: (요약문, 관심사 태그)
    """
    text = await crawl_url(url)
    summary = await summarize(text)
    interest = await classify_interest(text)
    return summary, interest