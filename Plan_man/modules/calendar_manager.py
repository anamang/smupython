# modules/calendar_manager.py
import datetime
from calendar import monthrange # 해당 월의 날짜 수를 가져오기 위해 import
from core.google_auth import get_calendar_service

# 기존 get_upcoming_events 함수는 그대로 두거나 필요 없다면 삭제할 수 있습니다.
# def get_upcoming_events(max_results=10): ...

def get_events_for_month(year, month):
    """
    지정된 연도와 월에 해당하는 모든 Google Calendar 이벤트를 가져옵니다.
    날짜(date 객체)를 키로, 해당 날짜의 이벤트 요약 문자열 리스트를 값으로 하는 딕셔너리를 반환합니다.
    오류 발생 시 {"error": "에러 메시지"} 형태의 딕셔너리를 반환합니다.
    """
    service = get_calendar_service()
    if not service:
        return {"error": "Google Calendar 서비스에 연결할 수 없습니다. 인증 상태를 확인하세요."}

    try:
        year = int(year)
        month = int(month)
    except ValueError:
        return {"error": "연도와 월은 숫자로 입력해야 합니다."}

    # 해당 월의 첫째 날과 마지막 날 계산
    try:
        first_day_of_month = datetime.datetime(year, month, 1, 0, 0, 0)
        # monthrange(year, month)는 (요일, 해당 월의 날짜 수) 튜플을 반환합니다.
        num_days_in_month = monthrange(year, month)[1]
        last_day_of_month = datetime.datetime(year, month, num_days_in_month, 23, 59, 59)
    except ValueError: # 잘못된 날짜(예: 2월 30일) 입력 방지
        return {"error": f"{year}년 {month}월은 유효한 날짜가 아닙니다."}


    # Google Calendar API가 요구하는 RFC3339 형식으로 변환 ('Z'는 UTC를 의미)
    time_min_str = first_day_of_month.isoformat() + 'Z'
    time_max_str = last_day_of_month.isoformat() + 'Z'

    events_by_date = {}  # {datetime.date 객체: [이벤트1 요약, 이벤트2 요약, ...]}
    try:
        events_result = service.events().list(
            calendarId='primary',       # 기본 캘린더
            timeMin=time_min_str,
            timeMax=time_max_str,
            singleEvents=True,          # 반복 이벤트를 개별 이벤트로 확장
            orderBy='startTime'         # 시작 시간 순으로 정렬
        ).execute()
        google_api_events = events_result.get('items', [])

        if not google_api_events:
            return {}  # 해당 월에 이벤트 없음

        for event in google_api_events:
            start_info = event['start']
            # 이벤트 시작 날짜/시간 문자열 가져오기
            start_str = start_info.get('dateTime', start_info.get('date'))
            
            # ISO 8601 형식의 날짜/시간 문자열을 datetime.date 객체로 변환
            # 'dateTime'은 'YYYY-MM-DDTHH:MM:SS...' 형식, 'date'는 'YYYY-MM-DD' 형식
            if 'T' in start_str:  # 'dateTime' 형식인 경우 (시간 정보 포함)
                # 시간대 정보를 고려하여 datetime 객체로 변환 후 date 부분만 사용
                event_date_obj = datetime.datetime.fromisoformat(start_str.replace('Z', '+00:00')).date()
            else:  # 'date' 형식인 경우 (종일 이벤트)
                event_date_obj = datetime.date.fromisoformat(start_str)
            
            summary = event.get('summary', '제목 없음') # 이벤트 제목
            
            if event_date_obj not in events_by_date:
                events_by_date[event_date_obj] = []
            events_by_date[event_date_obj].append(summary)
            
        return events_by_date

    except Exception as e:
        print(f"{year}년 {month}월 이벤트 가져오기 중 오류 발생: {e}")
        return {"error": f"이벤트 가져오기 중 오류 발생: {e}"}

if __name__ == '__main__':
    # 테스트용: 현재 월의 이벤트를 가져와서 출력
    today = datetime.date.today()
    print(f"--- {today.year}년 {today.month}월 캘린더 일정 테스트 ---")
    monthly_events = get_events_for_month(today.year, today.month)
    if "error" in monthly_events:
        print(monthly_events["error"])
    elif not monthly_events:
        print("이번 달에는 예정된 이벤트가 없습니다.")
    else:
        for event_date, summaries in sorted(monthly_events.items()):
            print(f"\n{event_date.strftime('%Y-%m-%d (%a)')}:") # 날짜와 요일 출력
            for summary in summaries:
                print(f"  - {summary}")