import tkinter as tk
from tkinter import Canvas, N, E, W, S
from tkinter import messagebox
from tkinter.constants import ANCHOR, CENTER
from PIL import ImageTk, Image
from minecraft_register import Register
from minecraft_forget import Forget
from queryProcess import queryProcess

class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        # tkinter 창 가로/세로 설정
        self.width = int(self.winfo_screenwidth() / 5)
        self.height = int(self.winfo_screenheight() / 4)

        self.wm_attributes('-transparentcolor',self['bg'])
        # 배경 이미지 설정
        # 로그인 창 이미지 설정
        self.image = ImageTk.PhotoImage(Image.open('assets/login.jpg').resize((self.width,self.height), Image.ANTIALIAS))
        
        # 해상도 및 위치 설정
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, int((self.winfo_screenwidth()-self.width)/2),int((self.winfo_screenheight()-self.height)/2)))
        
        # tk 설정
        self.resizable(0,0)
        self.title("Welcome to MineCraft!")

        #intoduce label
        self.bg_label = tk.Label(self,image=self.image) 
        self.bg_label.place(x=0,y=0, relwidth = 1, relheight = 1)

        # id label
        self.id_label = tk.Label(self,text="ID", bg='snow2')
        self.id_label.grid(row = 1, column = 1, sticky='w')

        # id field
        self.id_textfield = tk.Entry(self, bg = 'linen')
        self.id_textfield.grid(row = 1, column = 1)

        # pw 틀린 횟수
        self.pw_not_corrected = 0
        # pw label
        self.pw_label = tk.Label(self,text="PW", bg='snow2')
        self.pw_label.grid(row = 2, column = 1,sticky='w')

        # pw field
        self.pw_textfield = tk.Entry(self, show='*', bg = 'linen')
        self.pw_textfield.grid(row = 2, column = 1)

        # ID필드와 PW필드에 엔터키 바인딩
        self.id_textfield.bind('<Return>', self.enter)
        self.pw_textfield.bind('<Return>', self.enter)

        # 각 컴포넌트 정렬
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # login 버튼
        self.login_btn = tk.Button(self,text="로그인", command = self.login, borderwidth=0, bg='slategray1',activebackground="blue")
        self.login_btn.grid(row=3,column=1)

        # forget 버튼
        self.forget_btn = tk.Button(self,text="아이디/비밀번호 찾기", command = self.forget, borderwidth=0, bg='slategray1',activebackground="blue")
        self.forget_btn.grid(row=4,column=1)

        # regitser 버튼
        self.register_btn = tk.Button(self,text="회원가입", command = self.register, borderwidth=0, bg='slategray1',activebackground="blue")
        self.register_btn.grid(row=5,column=1)

        self.login_success = False # 로그인 성공 여부
        self.closed = True # 창 닫기 버튼

        # id필드에 포커스
        self.id_textfield.focus_set()
        
        tk.mainloop()

    # 로그인 함수
    def login(self) :
        # id / pw 입력 됬는 지 확인
        if self.id_textfield.get() :
            if self.pw_textfield.get() :
                # id / pw 저장
                id = self.id_textfield.get()
                pw = self.pw_textfield.get()
                #######  DB  ############
                qp = queryProcess()
                # db에 저장된 pw 가져오기
                result = qp.select_from_userid(id)
                db_pw = result[4]
                # pw 같으면
                if pw == db_pw :
                    # pw_error = 0 초기화
                    qp.update_pw_error_cnt(id,'success')
                    tk.messagebox.showinfo('로그인 성공',result[1] + "님 환영합니다!!")
                    self.destroy()
                    return
                # pw 틀림
                else :
                    # pw_error += 1
                    qp.update_pw_error_cnt(id,'fail')
                    # 연속 5회 실패 -> 계정 자금
                    if result[6] == 4 :
                        tk.messagebox.showerror('잠금','로그인 연속 5회 실패하여 계정이 잠겼습니다.' + "\n" + '관리자에게 문의해 주세요.')
                        return
                    # 이미 잠김 -> 잠겼다고 표시
                    elif result[6] > 4 :
                        tk.messagebox.showerror('잠금','잠긴 계정입니다.' + "\n" + '관리자에게 문의해 주세요.')
                        return

                    tk.messagebox.showerror('로그인 실패','아이디/비밀번호가 다릅니다.' + "\n" + '로그인 틀린 횟수 : ' + str(result[6] + 1) + '번' + "\n" + "(5회 실패 시, 계정 잠금)")
                    return
                    
        tk.messagebox.showerror('오류','아이디/비밀번호 입력 오류')
        return

    def register(self) :
        register = Register()

    def forget(self) :
        forget = Forget()

    # 엔터키 입력 시 로그인 진행
    def enter(self,event) :
        self.login()

if __name__ == "__main__" :
    login = Login()