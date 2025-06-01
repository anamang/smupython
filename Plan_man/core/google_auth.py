# core/google_auth.py
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 이 SCOPES를 수정하면 token.json 파일을 삭제해야 합니다.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'] # 읽기 전용 범위
CREDENTIALS_FILE = 'credentials.json'  # API 인증 정보 파일 경로
TOKEN_FILE = 'token.json'  # 생성된 토큰 저장 파일 경로

def get_calendar_service():
    """구글 캘린더 API의 기본 사용법을 보여줍니다.
    사용자 캘린더에서 다음 10개 이벤트의 시작 시간과 이름을 출력합니다.
    성공 시 calendar service 객체를, 실패 시 None을 반환합니다.
    """
    creds = None
    # token.json 파일은 사용자의 액세스 및 새로고침 토큰을 저장하며,
    # 인증 흐름이 처음 완료될 때 자동으로 생성됩니다.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 유효한 인증 정보가 없으면 사용자가 로그인하도록 합니다.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"토큰 새로고침 실패: {e}")
                # 새로고침 실패 시 재인증으로 대체
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0) # 사용 가능한 포트에서 로컬 서버 실행
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"오류: {CREDENTIALS_FILE} 파일을 찾을 수 없습니다. Google Cloud Console에서 다운로드하세요.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # 다음 실행을 위해 인증 정보를 저장합니다.
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(f"캘린더 서비스 빌드 중 오류 발생: {e}")
        return None

if __name__ == '__main__':
    # 이 스크립트를 직접 실행하여 인증 흐름을 테스트합니다.
    service = get_calendar_service()
    if service:
        print("성공적으로 인증되었고 캘린더 서비스를 가져왔습니다.")
    else:
        print("캘린더 서비스 가져오기에 실패했습니다.")