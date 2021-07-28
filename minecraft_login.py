import tkinter as tk
from tkinter import Canvas, N, E, W, S
from tkinter import messagebox
from tkinter.constants import ANCHOR, CENTER
from PIL import ImageTk, Image

class Login(tk.Tk):
    def __init__(self):
        super().__init__()

        # tkinter 창 가로/세로 설정
        self.width = int(self.winfo_screenwidth() / 7)
        self.height = int(self.winfo_screenheight() / 4)

        self.wm_attributes('-transparentcolor',self['bg'])
        # 배경 이미지 설정
        # 로그인 창 이미지 설정
        self.image = ImageTk.PhotoImage(Image.open('./assets/login.jpg').resize((self.width,self.height), Image.ANTIALIAS))
        
        # 해상도 및 위치 설정
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, int((self.winfo_screenwidth()-self.width)/2),int((self.winfo_screenheight()-self.height)/2)))
        
        # tk 설정
        self.resizable = False
        self.title("JS Craft")

        #intoduce label
        bg_label = tk.Label(self,image=self.image) 
        bg_label.place(x=0,y=0, relwidth = 1, relheight = 1)

        # id label
        id_label = tk.Label(self,text="ID", bg='gray')
        id_label.grid(row = 1, column = 1, sticky='w')

        # id field
        id_textfield = tk.Entry(self)
        id_textfield.grid(row = 1, column = 1)

        # pw label
        pw_label = tk.Label(self,text="PW", bg='gray')
        pw_label.grid(row = 2, column = 1,sticky='w')

        # pw field
        pw_textfield = tk.Entry(self)
        pw_textfield.grid(row = 2, column = 1)

        # 로그인 함수
        def login() :
            if id_textfield.get() == 'admin' :
                if pw_textfield.get() == '1234' :
                    self.login_success = True
                    self.destroy()
                else :
                    messagebox.showerror('실패','비밀번호가 맞지 않습니다.')
            elif id_textfield.get() == '' :
                messagebox.showerror('실패','아이디를 입력하세요.')
            elif pw_textfield.get() =='' :
                messagebox.showerror('실패','비밀번호를 입력하세요.')
            else : 
                messagebox.showerror('실패','아이디가 존재하지 않습니다.')
        
        def enter(event) :
            login()

        # ID필드와 PW필드에 엔터키 바인딩
        id_textfield.bind('<Return>', enter)
        pw_textfield.bind('<Return>', enter)

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

        # login button
        login_btn = tk.Button(self,text="로그인", command = login, borderwidth=0, bg='gray')
        login_btn.grid(row=3,column=1)
        # forget button
        forget_btn = tk.Button(self,text="아이디/비밀번호 찾기", command = login, borderwidth=0, bg='gray')
        forget_btn.grid(row=4,column=1)

        # regitser button
        register_btn = tk.Button(self,text="회원가입", command = login, borderwidth=0, bg='gray')
        register_btn.grid(row=5,column=1)

        self.login_success = False # 로그인 성공 여부
        self.closed = True # 창 닫기 버튼

        # id필드에 포커스
        id_textfield.focus_set()


if __name__ == "__main__" :
    login = Login()
    login.mainloop()