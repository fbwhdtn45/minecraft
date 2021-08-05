from ursina import *
from ursina.prefabs.health_bar import HealthBar

class Loading(Entity):
    def __init__(self):
        super().__init__()

        # loading... <- "." 개수 제어 // 10프로부터 시작함 , 왜냐하면 10프로 미만인 경우 로딩 바 테두리가 안둥글해짐
        self.loading_cnt = 0
        
        # 로딩 창
        self.loading_panel = Button(text='loading', scale = (2.5,1), color = color.azure)
        
        # 로딩 progress bar
        self.loading_bar = HealthBar(position = (-.25,-.05),is_health = False,bar_color = color.green)
        self.loading_bar.text_entity.color = color.clear

        self.finished = False

    def loading(self,a, b) :
        # 로딩 중일 때 loading bar 변경   // a : currentSubset, b : len(subsets)
        self.loading_bar.value = int(a/b*100)

        # 로딩 중일 때 text 변경
        if self.loading_cnt < 5 and not self.finished:
            self.loading_panel.text += "."
            self.loading_cnt += 1
        else :
            if not self.finished :
                self.loading_panel.text = "loading"
                self.loading_cnt = 0
            # 로딩 끝나면 text 삭제
            else :
                self.loading_panel.text = ''

if __name__ == '__main__':
    app = Ursina()
    
    loading = Loading()

    loading.loading(2,100)
    
    app.run()