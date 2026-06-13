# app/services/ai_service.py
import httpx
from bs4 import BeautifulSoup
from google import genai
import os


# API 키 설정 (나중에 .env로 분리 권장)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# 관심사 태그 목록 (member_schema.py의 VALID_INTERESTS와 동일)
INTERESTS = ["차(tea)", "아웃도어", "아이와 함께", "반려", "건축", "해외여행", "맛집", "인테리어", "기타"]

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


async def extract_og_image(url: str) -> str:
    """URL에서 og:image 태그 추출 → 썸네일 URL 반환"""
    try:
        async with httpx.AsyncClient(timeout=10, headers={"User-Agent": "Mozilla/5.0"}) as http_client:
            response = await http_client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # og:image 태그 찾기
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
            
        return ""
    except Exception as e:
        print("썸네일 오류:", e)
        return ""

async def summarize(text: str) -> str:
    if not text:
        return ""
    try:
        prompt = f"다음 내용을 한국어로 핵심 요약해줘, 명사형 어미로 1줄 내외의 핵심 헤드라인을 넣고 개행한 후에 키워드: 라고 적고 앞줄엔 들어가지 않았지만 북마크 내용에 포함되거나 관련되는 핵심 키워드를 나열해줘 (예시: 파리 주요 관광지를 3일 동안 여행하는 일정 \n키워드: 프랑스, 여행, 루트):\n\n{text}"
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
    매칭되는 게 없으면 기타 폴더에 저장.
    """
    if not text:
        return ""
    try:
        tags = ", ".join(INTERESTS)
        prompt = (
            f"다음 텍스트를 읽고 아래 카테고리 중 가장 잘 맞는 것 하나만 골라줘. "
            f"반드시 아래 목록 중 하나만 답해. 다른 말은 하지 마. "
            f"적합한 카테고리가 없으면 반드시 기타 카테고리를 선택해.\n\n"
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

async def crawl_summarize_classify(url: str) -> tuple[str, str, str]:
    """
    반환: (요약문, 관심사 태그, 썸네일 URL)
    """
    text = await crawl_url(url)
    summary = await summarize(text)
    interest = await classify_interest(text)
    image_url = await extract_og_image(url)  # 추가
    return summary, interest, image_url