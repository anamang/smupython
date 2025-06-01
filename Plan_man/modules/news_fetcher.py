# modules/news_fetcher.py
import requests
from bs4 import BeautifulSoup

CATEGORY_RSS = {
    "정치": "https://www.yna.co.kr/rss/politics.xml",
    "경제": "https://www.yna.co.kr/rss/economy.xml",
    "사회/문화": "https://rss.etnews.com/Section904.xml", # 전자신문 사회
    "산업/과학": "https://rss.etnews.com/Section903.xml", # 전자신문 IT/과학
    "세계": "https://www.yna.co.kr/rss/international.xml"
}

def get_news_items_by_category(category):
    """
    지정된 카테고리의 뉴스 항목(제목, 링크)을 가져옵니다.
    뉴스 항목 딕셔너리의 리스트 또는 오류 메시지 딕셔너리의 리스트를 반환합니다.
    """
    url = CATEGORY_RSS.get(category)
    if not url:
        return [{"title": f"❌ '{category}' 카테고리에 대한 RSS가 없습니다.", "link": ""}]

    # 웹사이트가 자동화된 요청을 차단하는 것을 피하기 위해 User-Agent 설정
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 PlanManApp/1.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10) # 타임아웃 시간 증가
        res.raise_for_status() # HTTP 오류 발생 시 예외 발생

        # 인코딩 문제 해결을 위해 utf-8로 먼저 디코딩 시도, 실패 시 apparent_encoding 사용
        try:
            content = res.content.decode('utf-8')
        except UnicodeDecodeError:
            content = res.content.decode(res.apparent_encoding, 'ignore') # 디코딩 오류 발생 시 해당 문자 무시

        soup = BeautifulSoup(content, "xml") # RSS는 XML 형식이므로 "xml" 파서 사용
        items = soup.find_all("item")
        if not items: # 일부 RSS 피드는 'item' 대신 'entry'를 사용할 수 있음
            items = soup.find_all("entry")

        news_list = []
        for item in items[:10]: # 최대 10개 항목으로 제한
            title_tag = item.find("title")
            link_tag = item.find("link")

            title = title_tag.text.strip() if title_tag else "제목 없음"
            
            link = ""
            if link_tag:
                if link_tag.text: # 연합뉴스 스타일
                    link = link_tag.text.strip()
                elif link_tag.get('href'): # 전자신문 등 다른 스타일 (link 태그의 href 속성)
                    link = link_tag.get('href').strip()
            
            news_list.append({"title": title, "link": link})

        return news_list if news_list else [{"title": "✅ 해당 카테고리에 표시할 뉴스가 없습니다.", "link": ""}]

    except requests.exceptions.RequestException as e: # 네트워크 관련 예외 처리
        return [{"title": f"❌ 뉴스 로드 실패 (네트워크 오류): {str(e)}", "link": ""}]
    except Exception as e: # 그 외 모든 예외 처리
        print(f"피드 {url} 처리 중 오류 발생: {e}") # 디버깅을 위해 상세 오류 로깅
        return [{"title": f"❌ 뉴스 처리 중 오류 발생: {str(e)}", "link": ""}]

if __name__ == '__main__':
    # 테스트용 함수 호출
    for cat in CATEGORY_RSS.keys():
        print(f"\n--- {cat} 뉴스 ---")
        news = get_news_items_by_category(cat)
        for n in news:
            print(f"  {n['title']} ({n['link']})")