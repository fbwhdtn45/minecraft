import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Canvas, N, E, W, S
from tkinter import messagebox
from tkinter.constants import ANCHOR, CENTER
from PIL import ImageTk, Image
import time
from queryProcess import queryProcess

class Forget(tk.Toplevel) :
    def __init__(self):
        super().__init__()
        # tkinter 창 가로/세로 설정
        self.width = int(self.winfo_screenwidth() / 5)
        self.height = int(self.winfo_screenheight() / 4)

        # 배경 투명 설정
        self.wm_attributes('-transparentcolor',self['bg'])
        
        # 로그인 창 이미지 설정
        self.image = ImageTk.PhotoImage(Image.open('assets/forget.jpg').resize((self.width,self.height), Image.ANTIALIAS))
        
        # 해상도 및 위치 설정
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, int((self.winfo_screenwidth()-self.width)/2),int((self.winfo_screenheight()-self.height)/2)))
        
        # tk 설정
        self.resizable(0,0)
        self.title("아이디 / 비밀번호 찾기")

        # 배경 설정
        self.bg_label = tk.Label(self,image=self.image) 
        self.bg_label.place(x=0,y=0, relwidth = 1, relheight = 1)

        # -----------아이디 찾기------------
        self.id_search_label = tk.Label(self,text='아이디', bg='snow2')
        self.id_search_label.grid(row = 1, column = 1, columnspan = 6, sticky = 'ew')
        # 이름
        self.id_name_label = tk.Label(self,text="이름", bg='snow2')
        self.id_name_label.grid(row = 2, column = 1)
        # 이름 TEXT
        self.id_name_textfield = tk.Entry(self, bg = 'linen')
        self.id_name_textfield.grid(row = 2, column = 2,columnspan=5)

        # 연락처
        self.id_phone_label = tk.Label(self,text="연락처", bg='snow2')
        self.id_phone_label.grid(row = 3, column = 1)
        # 연락처 TEXT1
        self.id_phone1_textfield = tk.Entry(self, bg = 'linen', width = 4)
        self.id_phone1_textfield.grid(row = 3, column = 2, sticky= 'e')
        # -
        self.id_phone1_label = tk.Label(self,text="-", bg='snow2')
        self.id_phone1_label.grid(row = 3, column = 3)
        # 연락처 TEXT2
        self.id_phone2_textfield = tk.Entry(self, bg = 'linen', width = 5)
        self.id_phone2_textfield.grid(row = 3, column = 4,sticky = 'ew')
        # -
        self.id_phone2_label = tk.Label(self,text="-", bg='snow2')
        self.id_phone2_label.grid(row = 3, column = 5)
        # 연락처 TEXT3
        self.id_phone3_textfield = tk.Entry(self, bg = 'linen', width = 6)
        self.id_phone3_textfield.grid(row = 3, column = 6, sticky= 'w')
        # 엔터키 이벤트 설정
        self.id_phone3_textfield.bind('<Return>', self.id_enter)

        # 찾기 버튼
        self.register_btn = tk.Button(self,text="찾기", command = self.id_search, borderwidth=0, bg='salmon2',activebackground="salmon3")
        self.register_btn.grid(row=4,column=2, sticky = 'ew', columnspan=4)

        # --------비밀번호 찾기------------
        self.pw_search_label = tk.Label(self,text='비밀번호', bg='snow2')
        self.pw_search_label.grid(row = 5, column = 1, columnspan = 6, sticky = 'ew')
        # ID
        self.pw_id_label = tk.Label(self,text="ID", bg='snow2')
        self.pw_id_label.grid(row = 6, column = 1)
        # ID TEXT
        self.pw_id_textfield = tk.Entry(self, bg = 'linen')
        self.pw_id_textfield.grid(row = 6, column = 2,columnspan=5)

        # 이름
        self.pw_name_label = tk.Label(self,text="이름", bg='snow2')
        self.pw_name_label.grid(row = 7, column = 1)
        # 이름 TEXT
        self.pw_name_textfield = tk.Entry(self, bg = 'linen')
        self.pw_name_textfield.grid(row = 7, column = 2,columnspan=5)

        # 연락처
        self.pw_phone_label = tk.Label(self,text="연락처", bg='snow2')
        self.pw_phone_label.grid(row = 8, column = 1)
        # 연락처 TEXT1
        self.pw_phone1_textfield = tk.Entry(self, bg = 'linen', width = 4)
        self.pw_phone1_textfield.grid(row = 8, column = 2, sticky= 'e')
        # -
        self.pw_phone1_label = tk.Label(self,text="-", bg='snow2')
        self.pw_phone1_label.grid(row = 8, column = 3)
        # 연락처 TEXT2
        self.pw_phone2_textfield = tk.Entry(self, bg = 'linen', width = 5)
        self.pw_phone2_textfield.grid(row = 8, column = 4,sticky = 'ew')
        # -
        self.pw_phone2_label = tk.Label(self,text="-", bg='snow2')
        self.pw_phone2_label.grid(row = 8, column = 5)
        # 연락처 TEXT3
        self.pw_phone3_textfield = tk.Entry(self, bg = 'linen', width = 6)
        self.pw_phone3_textfield.grid(row = 8, column = 6, sticky= 'w')
        # 엔터키 이벤트 설정
        self.pw_phone3_textfield.bind('<Return>', self.pw_enter)

        # 찾기 버튼
        self.pw_search_btn = tk.Button(self,text="찾기", command = self.pw_search, borderwidth=0, bg='salmon2',activebackground="salmon3")
        self.pw_search_btn.grid(row=9,column=2, sticky = 'ew', columnspan=4)

        # 종료 버튼
        self.quit_btn = tk.Button(self,text="종료", command = self.quit, borderwidth=0, bg='slategray1',activebackground="blue")
        self.quit_btn.grid(row=10,column=0, sticky = 'nesw', columnspan=8)

        # 각 컴포넌트 정렬
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=2)
        self.grid_rowconfigure(4, weight=2)
        self.grid_rowconfigure(5, weight=2)
        self.grid_rowconfigure(6, weight=2)
        self.grid_rowconfigure(7, weight=2)
        self.grid_rowconfigure(8, weight=2)
        self.grid_rowconfigure(9, weight=2)
        self.grid_rowconfigure(10, weight=2)
        self.grid_columnconfigure(0, weight=20)
        self.grid_columnconfigure(1, weight=10)
        self.grid_columnconfigure(2, weight=10)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=10)
        self.grid_columnconfigure(7, weight=20)

        self.mainloop()

    def id_search_validation(self) :
        if self.id_name_textfield.get() :
            if self.id_phone1_textfield.get() :
                if self.id_phone2_textfield.get() :
                    if self.id_phone3_textfield.get() :
                        return True
        else :
            tk.messagebox.showerror('오류','아이디 찾기 정보 오류')
            return False

    def pw_search_validation(self) :
        if self.pw_id_textfield.get() :
            if self.pw_name_textfield.get() :
                if self.pw_id_textfield.get() :
                    if self.pw_phone1_textfield.get() :
                        if self.pw_phone2_textfield.get() :
                            if self.pw_phone3_textfield.get() :
                                return True
        else :
            tk.messagebox.showerror('오류','비밀번호 찾기 정보 오류')
            return False
    def id_enter(self,event) :
        if self.id_search_validation() :
            self.id_search() 

    def pw_enter(self,event) :
        if self.pw_search_validation() :
            self.pw_search()
            return  

    def id_search(self) :
        if self.id_search_validation() :
            name = self.id_name_textfield.get()
            phone = self.id_phone1_textfield.get() + self.id_phone2_textfield.get() + self.id_phone3_textfield.get() 
            ####  DB  ###### 수정하기 ~~~
            qp = queryProcess()
            try :
                result = qp.select_id(name,phone)
                id = result[0]
                tk.messagebox.showinfo('아이디 찾기',name + "님의 ID는 " + id + "입니다.")
            except :
                tk.messagebox.showinfo('실패',"정보를 못 찾았습니다.")
            return
        else :
            return
            ###############
    def pw_search(self) :
        if self.pw_search_validation() :
            id = self.pw_id_textfield.get()
            name = self.pw_name_textfield.get()
            phone = self.pw_phone1_textfield.get() + self.pw_phone2_textfield.get() + self.pw_phone3_textfield.get() 
            #####  DB  ###### 수정하기 ~~~~
            print('<비밀번호 찾기 정보>')
            print('id : ' + id)
            print('name : ' + name)
            print('phone : ' + phone)
            #################
            return

    def quit(self) :
        self.destroy()
        return


if __name__ == "__main__" :
    forget = Forget()