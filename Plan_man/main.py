# main.py
from ui.interface import launch_gui
import tkinter as tk # Tkinter의 TclError 예외 처리를 위해 import

if __name__ == "__main__":
    try:
        launch_gui()
    except tk.TclError as e:
        # 애플리케이션이 정상적으로 닫힐 때 발생하는 "application has been destroyed" 오류는 무시
        if "application has been destroyed" in str(e):
            print("애플리케이션이 정상적으로 종료되었습니다.")
        else:
            # 그 외 Tkinter 관련 오류는 출력
            print(f"예기치 않은 Tkinter 오류가 발생했습니다: {e}")
    except Exception as e:
        # 기타 모든 예외 처리
        print(f"예기치 않은 오류가 발생했습니다: {e}")