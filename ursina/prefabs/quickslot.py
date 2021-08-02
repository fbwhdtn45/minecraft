from ursina import *

class Quickslot(Button):
    def __init__(self):
        # 초기 설정 ( 1 x 9 칸 )
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            scale = (.9, .1),                                           
            origin = (-.5, .5),                                         
            position = (-.5,-.4,-.1),                                        
            texture = 'white_cube',                                     
            texture_scale = (9,1),                                      
            color = color.black33,
            disabled = True      
            )

        # ( 1 x 9 )칸의 각 칸마다 자식 Entity 설정
        self.item_parent = Entity(parent=self, scale=(1/9,1))

        # quick index 배경
        self.quick_index_background = Button(parent=self, model = 'quad',scale = (1,.2),origin = (-.5,.5),position = (0,0,-.6), color = color.clear)

        # quick index 컴포넌트
        self.quick_index_slot = Button(parent = self.quick_index_background, model = 'quad', scale = (1/9,1), color = color.clear,texture_scale = (1,9))

        # 퀵 슬롯 인덱스 추가
        self.putIndex(self.quick_index_slot)


    def append(self, item):      
        # 아이템 박스                                  
        box = Button(                                                         
            parent = self.item_parent,                             
            model = 'quad',                                             
            origin = (-.5,.5),                                          
            color = color.clear,
            texture = item.texture,
            icon = item.texture,
            position = (round(item.x,0),0,-.1),                         
            z = -.2                                                      
            )

    # f1 ~ f3 눌렀을 때, 각 박스 삭제하고 다시 생성하기 위한 delete 
    def delete(self) :
        for e in self.item_parent.children :
            destroy(e)

    # 퀵슬롯 1 ~ 9 인덱스 추가
    def putIndex(self,parent) :
        for i in range(9) :
            # 각 박스 인덱스 설정
            Button(                                                         
                parent = parent,                             
                model = 'quad',
                scale = (1/5,1),    
                origin = (-.5,.5),                                    
                color = color.black33,
                text = str(i+1),
                position = (i,0,-.1),                      
                z = -.3                                                     
                )        






if __name__ == '__main__':
    app = Ursina()

    quickslot = Quickslot()
    for i in range(9):    
        print(1)     
        # 테스트 할 때는 item으로 넣기                                         
        
    app.run()