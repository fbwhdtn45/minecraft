import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Canvas, N, E, W, S
from tkinter import messagebox
from tkinter.constants import ANCHOR, CENTER
from PIL import ImageTk, Image
import time
from queryProcess import queryProcess

class Register(tk.Toplevel) :
    def __init__(self):
        super().__init__()
        # tkinter 창 가로/세로 설정
        self.width = int(self.winfo_screenwidth() / 5)
        self.height = int(self.winfo_screenheight() / 3)

        # 배경 투명 설정
        self.wm_attributes('-transparentcolor',self['bg'])
        
        # 로그인 창 이미지 설정
        self.image = ImageTk.PhotoImage(Image.open('assets/register.gif').resize((self.width,self.height), Image.ANTIALIAS))
        
        # 해상도 및 위치 설정
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, int((self.winfo_screenwidth()-self.width)/2),int((self.winfo_screenheight()-self.height)/2)))
        
        # tk 설정
        self.resizable(0,0)
        self.title("회원가입")

        # 배경 설정
        self.bg_label = tk.Label(self,image=self.image) 
        self.bg_label.place(x=0,y=0, relwidth = 1, relheight = 1)

        self.id = ''
        # ID
        self.id_label = tk.Label(self,text="ID", bg='snow2')
        self.id_label.grid(row = 1, column = 1)
        # ID TEXT
        self.id_textfield = tk.Entry(self, bg = 'linen')
        self.id_textfield.grid(row = 1, column = 2,columnspan=5)
        # ID 유효성 검증 함수 바인딩
        self.id_textfield.bind("<FocusOut>",self.id_check)
        # 유효성 검증 여부 변수
        self.id_ischecked = False

        # PW
        self.pw_label = tk.Label(self,text="PW", bg='snow2')
        self.pw_label.grid(row = 2, column = 1)
        # PW TEXT
        self.pw_textfield = tk.Entry(self, bg = 'linen',show="*")
        self.pw_textfield.grid(row = 2, column = 2,columnspan=5)

        # PW확인 유효성 검증 변수
        self.pw_equal = False
        # PW확인
        self.pw_check_label = tk.Label(self,text="PW확인", bg='snow2')
        self.pw_check_label.grid(row = 3, column = 1)
        # PW확인 TEXT
        self.pw_check_textfield = tk.Entry(self, bg = 'linen',show="*")
        self.pw_check_textfield.grid(row = 3, column = 2,columnspan=5)
        
        # 이름
        self.name_label = tk.Label(self,text="이름", bg='snow2')
        self.name_label.grid(row = 4, column = 1)
        # 이름 TEXT
        self.name_textfield = tk.Entry(self, bg = 'linen')
        self.name_textfield.grid(row = 4, column = 2,columnspan=5)

        # 연락처
        self.phone_label = tk.Label(self,text="연락처", bg='snow2')
        self.phone_label.grid(row = 5, column = 1)
        # 연락처 TEXT1
        self.phone1_textfield = tk.Entry(self, bg = 'linen', width = 4)
        self.phone1_textfield.grid(row = 5, column = 2, sticky= 'e')
        # -
        self.phone1_label = tk.Label(self,text="-", bg='snow2')
        self.phone1_label.grid(row = 5, column = 3)
        # 연락처 TEXT2
        self.phone2_textfield = tk.Entry(self, bg = 'linen', width = 5)
        self.phone2_textfield.grid(row = 5, column = 4,sticky = 'ew')
        # -
        self.phone2_label = tk.Label(self,text="-", bg='snow2')
        self.phone2_label.grid(row = 5, column = 5)
        # 연락처 TEXT3
        self.phone3_textfield = tk.Entry(self, bg = 'linen', width = 6)
        self.phone3_textfield.grid(row = 5, column = 6, sticky= 'w')

        # 주소
        self.address_label = tk.Label(self,text="주소", bg='snow2')
        self.address_label.grid(row = 6, column = 1)
        # 주소 TEXT
        self.address_textfield = tk.Entry(self, bg = 'linen', width = 30)
        self.address_textfield.grid(row = 6, column = 2,columnspan=5)

        # 이메일 콤보박스 목록
        self.emails = ['naver.com','daum.net','gmail.com','nate.com','kakao.com','기타']
        # E-MAIL
        self.email_label = tk.Label(self,text="E-MAIL(선택)", bg='snow2')
        self.email_label.grid(row = 7, column = 1)
        # E-MAIL TEXT
        self.email_textfield = tk.Entry(self, bg = 'linen',width = 10)
        self.email_textfield.grid(row = 7, column = 2, columnspan = 2, sticky = 'e')
        # @
        self.email1_label = tk.Label(self,text="@", bg='snow2')
        self.email1_label.grid(row = 7, column = 4)
        # combo박스
        self.combobox = ttk.Combobox(self,width = 10,values=self.emails)
        self.combobox.grid(row=7, column=5, columnspan = 2, sticky = 'w')
        self.combobox.bind("<<ComboboxSelected>>",self.gita)

        # 가입 신청 버튼
        self.register_btn = tk.Button(self,text="가입 신청", command = self.register, borderwidth=0, bg='slategray1',activebackground="blue")
        self.register_btn.grid(row=9,column=0, sticky = 'nesw', columnspan=8)

        # 주소와 email필드에 엔터키 바인딩
        self.address_textfield.bind('<Return>', self.enter)
        self.email_textfield.bind('<Return>', self.enter)

        # 각 컴포넌트 정렬
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=2)
        self.grid_rowconfigure(4, weight=2)
        self.grid_rowconfigure(5, weight=2)
        self.grid_rowconfigure(6, weight=2)
        self.grid_rowconfigure(7, weight=2)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=2)
        self.grid_columnconfigure(0, weight=20)
        self.grid_columnconfigure(1, weight=10)
        self.grid_columnconfigure(2, weight=10)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=10)
        self.grid_columnconfigure(7, weight=5)

        self.login_success = False # 로그인 성공 여부
        self.closed = True # 창 닫기 버튼

        # id필드에 포커스
        self.id_textfield.focus_set()
        
        # DB 커넥션 실행
        self.qp = queryProcess()
        
        # 0.1초마다 update 함수
        self.update()

        self.mainloop()
    
    # 콤보박스 '기타' 클릭 시 빈칸 설정
    def gita(self,event) :
        if self.combobox.get() == '기타' :
            self.combobox.set('')
            
    # 엔터키 입력 시 가입 신청 진행
    def enter(self, event) :
        self.register()
    
    # id 필드 포커싱 아웃 시, 아이디 유효성 검증
    def id_check(self, event) :
        id = self.id_textfield.get()
        # 이미 아이디가 존재하면,
        if self.id_textfield.get() :
            if self.qp.select_from_userid(id) :
                self.id_ischecked = False
                self.id_textfield.configure(bg='orange red')
            else :
                self.id_textfield.configure(bg='limegreen')
                self.id_ischecked = True
        else :
            self.id_textfield.configure(bg='linen')
    
    def phone_check(self) :
        try : 
            int(self.phone1_textfield.get())
            int(self.phone2_textfield.get())
            int(self.phone3_textfield.get())
            return True
        except :
            return False

    # pw 및 필수 칸 유효성 검증
    def validation(self) :
        # ID 필드
        if not self.id_ischecked :
            tk.messagebox.showerror('오류','아이디 확인하세요.')
            return False 
        if not self.id_textfield.get() :
            tk.messagebox.showerror('오류','아이디 입력하세요.')
            return False     
        # PW 및 PW확인
        if self.pw_textfield.get() :
            if not self.pw_equal :
                tk.messagebox.showerror('오류','비밀번호 확인이 일치하지 않습니다.')
                return False
        else :
            tk.messagebox.showerror('오류','비밀번호를 입력하세요.')
            return False
        # name 필드
        if not self.name_textfield.get() :
            tk.messagebox.showerror('오류','이름을 입력하세요.')
            return False
        # 연락처
        if not self.phone1_textfield.get() or not self.phone3_textfield.get() or not self.phone3_textfield.get() :
            tk.messagebox.showerror('오류','연락처를 입력하세요.')
            return False
        if not self.phone_check() :
            tk.messagebox.showerror('오류','연락처는 숫자로 입력하세요.')
            return False
        # 주소
        if not self.address_textfield.get() :
            tk.messagebox.showerror('오류','주소를 입력하세요.')
            return False

        return True

    def register(self) :
        # 유효성 검증 후
        if not self.validation() :
            self.focus_set()
            return 
        
        # 변수에 데이터 담기
        id = self.id_textfield.get()
        pw = self.pw_textfield.get()
        name = self.name_textfield.get()
        phone = self.phone1_textfield.get() + self.phone2_textfield.get() + self.phone3_textfield.get()
        address = self.address_textfield.get()
        email = self.email_textfield.get() + "@" + self.combobox.get()
        #########  DB  ###############
        if self.qp.insert(id, name, phone, address, pw, email, 0) :
            self.destroy()
            tk.messagebox.showinfo('성공!','정상적으로 회원가입이 되었습니다.')
        else :
            self.destroy()
            tk.messagebox.showerror('실패','관리자에게 문의바랍니다.')
        ##########  DB  ##############
        


    def update(self) :
        # PW & PW확인 체크
        pw = self.pw_textfield.get()
        pw_check = self.pw_check_textfield.get()
        if pw != '' :
            if pw_check != '' : 
                if pw != pw_check :
                    self.pw_equal = False
                    self.pw_check_textfield.configure(bg='orange red')
                else  :
                    self.pw_equal = True
                    self.pw_check_textfield.configure(bg='limegreen')
            else : 
                self.pw_check_textfield.configure(bg='linen')
        else :       
            self.pw_check_textfield.configure(bg='linen')
        # update 주기 : 0.1초
        self.after(100,self.update)
    


if __name__ == "__main__" :
    register = Register()
