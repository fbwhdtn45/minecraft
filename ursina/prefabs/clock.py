from ursina import *
import datetime, time

class Clock(Button):
    def __init__(self):
        # 초기 설정 ( 1 x 9 칸 )
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            scale = (.25, .05),                                           
            origin = (-.5, .5),                                                                                 
            position = (.58,.5,-.1),                                                                          
            texture_scale = (9,1),                                      
            color = color.clear,
            )

    def update(self) :
        self.text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.text_entity.color = color.black


if __name__ == '__main__':
    app = Ursina()
    clock = Clock()
    app.run()