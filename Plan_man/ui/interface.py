# ui/interface.py
import tkinter as tk
from tkinter import ttk, messagebox # messagebox 임포트 추가
from tkcalendar import Calendar     # tkcalendar 임포트
from datetime import date           # date 객체 사용을 위해 임포트
from modules import news_fetcher    # 모듈 자체를 임포트하여 사용
from modules import calendar_manager # 모듈 자체를 임포트하여 사용
import webbrowser # 뉴스 링크 연결에 필요
import traceback # 오류 상세 출력을 위해 추가

class PlanManApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Plan Man")
        self.setup_main_window()
        self.create_main_menu_buttons()
        self.current_view_frame = None
        self.monthly_events_cache = {} # 월별 이벤트 캐시용
        self.cal = None # Calendar 위젯을 저장할 변수 초기화

    def setup_main_window(self):
        window_width = 800
        window_height = 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(700, 600)

        title_label = tk.Label(self.root, text="📚 PLAN MAN", font=("Arial", 28, "bold"), pady=10)
        title_label.pack()

        self.nav_frame = tk.Frame(self.root, pady=10)
        self.nav_frame.pack(fill=tk.X)
        
        self.content_frame = tk.Frame(self.root, pady=10, padx=10)
        self.content_frame.pack(expand=True, fill=tk.BOTH)

    def create_main_menu_buttons(self):
        buttons_info = [
            ("📅 일정 관리", self.show_calendar_view_new),
            ("📰 오늘의 뉴스", self.show_news_view),
            ("✍️ 시험 공부 계획", lambda: self.show_placeholder_view("시험 공부 계획")),
            ("☀️ 날씨 보기", lambda: self.show_placeholder_view("날씨 보기")),
            ("🚪 종료", self.root.quit)
        ]
        for text, command in buttons_info:
            btn = ttk.Button(self.nav_frame, text=text, command=command, style="Nav.TButton")
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, ipady=5)
        style = ttk.Style()
        style.configure("Nav.TButton", font=("Arial", 12))

    def clear_content_frame(self):
        if self.current_view_frame:
            self.current_view_frame.destroy()
        self.current_view_frame = tk.Frame(self.content_frame)
        self.current_view_frame.pack(expand=True, fill=tk.BOTH)

    def show_placeholder_view(self, feature_name):
        self.clear_content_frame()
        label = tk.Label(self.current_view_frame, text=f"{feature_name} 기능은 추후 연결 예정입니다.", font=("Arial", 16))
        label.pack(pady=50, padx=20, expand=True, anchor=tk.CENTER)
        
    def show_news_view(self):
        self.clear_content_frame()
        news_view_container = tk.Frame(self.current_view_frame)
        news_view_container.pack(expand=True, fill=tk.BOTH)
        category_buttons_frame = tk.Frame(news_view_container)
        category_buttons_frame.pack(fill=tk.X, pady=(0, 5))
        self.news_listbox = tk.Listbox(
            news_view_container, font=("Arial", 12), activestyle='dotbox',
            selectbackground="#a6a6a6", selectforeground="white"
        )
        news_scrollbar = ttk.Scrollbar(news_view_container, orient=tk.VERTICAL, command=self.news_listbox.yview)
        self.news_listbox.config(yscrollcommand=news_scrollbar.set)
        news_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.news_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.news_items_cache = []

        def load_news_for_category(category):
            self.news_listbox.delete(0, tk.END)
            self.news_items_cache.clear()
            items = news_fetcher.get_news_items_by_category(category)
            if items:
                for i, item in enumerate(items):
                    self.news_listbox.insert(tk.END, f"{i+1}. {item['title']}")
                    self.news_items_cache.append(item)
                    if "❌" in item['title'] or "✅" in item['title']:
                        self.news_listbox.itemconfig(tk.END, {'fg': 'gray'})
            else:
                self.news_listbox.insert(tk.END, "뉴스를 불러오지 못했습니다.")
                self.news_listbox.itemconfig(tk.END, {'fg': 'red'})

        def open_article(event):
            selected_indices = self.news_listbox.curselection()
            if selected_indices:
                actual_index = selected_indices[0]
                if 0 <= actual_index < len(self.news_items_cache):
                    item = self.news_items_cache[actual_index]
                    url = item.get('link')
                    if url and not ("❌" in item['title'] or "✅" in item['title']):
                        webbrowser.open(url)
                    elif not url:
                        messagebox.showinfo("뉴스 정보", "이 항목에는 연결된 링크가 없습니다.")
        self.news_listbox.bind("<Double-Button-1>", open_article)

        for i, category in enumerate(news_fetcher.CATEGORY_RSS.keys()):
            btn = ttk.Button(category_buttons_frame, text=category,
                             command=lambda c=category: load_news_for_category(c))
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
            if i == 0:
                load_news_for_category(category)

    def show_calendar_view_new(self):
        print("--- show_calendar_view_new 함수 호출됨 ---")
        self.clear_content_frame()
        
        calendar_ui_container = tk.Frame(self.current_view_frame)
        calendar_ui_container.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        left_frame = tk.Frame(calendar_ui_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        right_frame = tk.Frame(calendar_ui_container, width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        right_frame.pack_propagate(False)

        today = date.today()
        # self.cal을 여기서 생성하고 저장합니다.
        self.cal = Calendar(
            left_frame, selectmode='day', year=today.year, month=today.month, day=today.day,
            date_pattern='yyyy-mm-dd', locale='ko_KR', showweeknumbers=False,
        )
        self.cal.pack(expand=True, fill=tk.BOTH, pady=(0,10))
        
        tk.Label(right_frame, text="선택한 날짜의 일정:", font=("Arial", 11, "bold")).pack(anchor="w", padx=5, pady=(0,5))
        self.event_details_listbox = tk.Listbox(right_frame, height=15, font=("Arial", 10), activestyle="none")
        event_details_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.event_details_listbox.yview)
        self.event_details_listbox.config(yscrollcommand=event_details_scrollbar.set)
        event_details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.event_details_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0))

        # 이벤트 바인딩 전에 on_date_or_month_changed 메소드가 정의되어 있어야 합니다.
        self.cal.bind("<<CalendarSelected>>", self.on_date_or_month_changed)
        self.cal.bind("<<CalendarMonthChanged>>", self.on_date_or_month_changed)

        print(">>> 이제 self.load_events_for_displayed_month()를 호출합니다. <<<")
        self.load_events_for_displayed_month()
        print(">>> self.load_events_for_displayed_month() 호출 완료. <<<")

    # ★★★ 누락되었던 on_date_or_month_changed 메소드 정의 ★★★
    def on_date_or_month_changed(self, event=None):
        print(f"--- on_date_or_month_changed 함수 호출됨 --- (이벤트 정보: {event})")
        self.load_events_for_displayed_month()
        self.update_event_details_for_selected_date()

    def load_events_for_displayed_month(self):
        print("--- load_events_for_displayed_month 함수 시작 ---")

        if not hasattr(self, 'cal') or self.cal is None:
            print("XXX 오류: self.cal (달력 위젯)이 초기화되지 않았습니다. load_events_for_displayed_month 함수를 종료합니다.")
            return

        try:
            print(">>> self.cal.tag_delete('event_marker') 호출 시도...")
            self.cal.tag_delete('event_marker')
            print("<<< self.cal.tag_delete('event_marker') 호출 성공 (또는 태그가 이미 없었음).")
        except ValueError as e_tag_delete:
            if 'does not exists' in str(e_tag_delete).lower(): # 오류 메시지 소문자로 비교
                print(f"정보: 'event_marker' 태그가 존재하지 않아 삭제할 수 없습니다. (정상적인 상황일 수 있음): {e_tag_delete}")
            else:
                print(f"경고: self.cal.tag_delete('event_marker') 실행 중 예상치 못한 ValueError 발생: {e_tag_delete}")
                traceback.print_exc()
        except Exception as e_generic_tag_delete:
            print(f"XXX 오류: self.cal.tag_delete('event_marker') 실행 중 문제 발생: {e_generic_tag_delete}")
            traceback.print_exc()

        # 테스트용 print문은 이제 핵심 로그 확인 후 주석 처리하거나 삭제해도 됩니다.
        # print("testteststsetsgjdfkgjsrhjlgksngjhsngkjlsgnsjghskdjgndlgkjsdgfhslfjksejfiusnfvsuogvnhfsuijgvhrgjkhi --- 이 로그가 보여야 합니다!")

        year = None
        month = None
        try:
            print(">>> 현재 달력의 연도와 월 가져오기 시도...")
            displayed_month_year = self.cal.get_displayed_month()
            year = displayed_month_year[1]
            month = displayed_month_year[0]
            print(f"<<< get_displayed_month() 사용 성공. 연도={year}, 월={month}")
        except AttributeError:
            try:
                current_cal_date_str = self.cal.get_date()
                current_cal_date_obj = date.fromisoformat(current_cal_date_str)
                year = current_cal_date_obj.year
                month = current_cal_date_obj.month
                print(f"<<< get_displayed_month() 실패, get_date() 사용 성공. 연도={year}, 월={month}")
            except Exception as e_get_date:
                print(f"XXX 오류: get_date()로 날짜 가져오기 실패: {e_get_date}")
                messagebox.showerror("달력 오류", f"날짜 정보를 가져오는 데 실패했습니다: {e_get_date}")
                return
        except Exception as e_get_month_year:
            print(f"XXX 오류: 달력에서 연도/월 정보 가져오기 중 예외 발생: {e_get_month_year}")
            messagebox.showerror("달력 오류", f"달력 정보를 가져오는 데 실패했습니다: {e_get_month_year}")
            return

        if year is None or month is None:
            print("XXX 연도 또는 월 정보를 가져오지 못했습니다. 함수를 종료합니다.")
            messagebox.showerror("달력 오류", "달력의 연도와 월 정보를 가져올 수 없습니다.")
            return

        print(f"로딩 중: {year}년 {month}월 이벤트...")
        self.monthly_events_cache = calendar_manager.get_events_for_month(year, month)
        print(f"=== 데이터 수신 확인 ===\n{year}년 {month}월 이벤트 데이터: {self.monthly_events_cache}\n=======================")
        if "error" in self.monthly_events_cache:
            messagebox.showerror("캘린더 오류", self.monthly_events_cache["error"])
            return

        marked_event_count = 0
        if self.monthly_events_cache:
            for event_date_obj, summaries in self.monthly_events_cache.items():
                if summaries: # summaries 리스트가 비어있지 않은 경우에만 마킹
                    try:
                        self.cal.calevent_create(event_date_obj, text='이벤트', tags=('event_marker',))
                        marked_event_count += 1
                    except Exception as e_create_event: # calevent_create 에서도 오류 발생 가능
                        print(f"XXX 오류: self.cal.calevent_create 실행 중 문제 발생 (날짜: {event_date_obj}): {e_create_event}")
                        traceback.print_exc()

            print(f"=== 마킹 시도 확인 ===\n총 {marked_event_count}개의 날짜에 이벤트 마커 생성 시도함\n=======================")
        else:
            print(f"=== 마킹 시도 확인 ===\n표시할 이벤트 데이터가 없음 (monthly_events_cache가 비어있거나 오류 없음)\n=======================")

        try:
            self.cal.tag_config('event_marker', background='red', foreground='white')
        except Exception as e_tag_config:
            print(f"XXX 오류: self.cal.tag_config 실행 중 문제 발생: {e_tag_config}")
            traceback.print_exc()

        self.update_event_details_for_selected_date()
        print("--- load_events_for_displayed_month 함수 종료 (정상적일 경우) ---")

    def update_event_details_for_selected_date(self):
        print("--- update_event_details_for_selected_date 함수 시작 ---")
        if not hasattr(self, 'event_details_listbox') or not self.event_details_listbox.winfo_exists():
             print("정보: event_details_listbox가 없거나 파괴되었습니다.")
             return
        if not hasattr(self, 'cal') or self.cal is None:
            print("정보: self.cal이 초기화되지 않아 선택된 날짜를 가져올 수 없습니다.")
            self.event_details_listbox.delete(0, tk.END)
            self.event_details_listbox.insert(tk.END, "달력을 먼저 로드하세요.")
            return

        self.event_details_listbox.delete(0, tk.END)
        
        try:
            selected_date_obj = self.cal.selection_get()
            if not selected_date_obj:
                self.event_details_listbox.insert(tk.END, "날짜를 선택하세요.")
                return
        except Exception as e_selection_get:
            print(f"정보: 날짜 선택 정보를 가져오는 중 오류 (무시 가능): {e_selection_get}")
            self.event_details_listbox.insert(tk.END, "날짜를 선택하세요.")
            return

        print(f"선택된 날짜: {selected_date_obj}")
        if selected_date_obj in self.monthly_events_cache:
            events_today = self.monthly_events_cache[selected_date_obj]
            if events_today:
                for summary in events_today:
                    self.event_details_listbox.insert(tk.END, f"- {summary}")
            else:
                self.event_details_listbox.insert(tk.END, "선택한 날짜에 일정이 없습니다.")
        else:
            self.event_details_listbox.insert(tk.END, "선택한 날짜에 일정이 없습니다. (캐시 미포함)")
        print("--- update_event_details_for_selected_date 함수 종료 ---")

def launch_gui():
    root = tk.Tk()
    app = PlanManApp(root)
    root.mainloop()

if __name__ == '__main__':
    launch_gui()