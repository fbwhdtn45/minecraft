from ursina import *

class Inventory(Button):
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
            color = color.black33                                     
            )

        # ( 1 x 9 )칸의 각 칸마다 자식 Entity 설정
        self.item_parent = Entity(parent=self, scale=(1/9,1))       

        # 각 칸의 index 변수                             
        self.index = 0

    def append(self, item):      
        # 아이템 박스                                  
        box = Button(                                                         
            parent = self.item_parent,                             
            model = 'quad',                                             
            origin = (-.5,.5),                                          
            color = color.clear,
            texture = item,
            icon = item,
            position = self.find_free_spot(),                              
            z = -.2                                                     
            )

        # 인덱스 제어
        self.index += 1
        if self.index % 10 == 0 :
            self.index = 1

        # 각 박스 인덱스 설정
        index = Button(                                                         
            parent = box,                             
            model = 'quad',
            scale = (1/5,1/5),                                         
            origin = (-.5,.5),                                          
            color = color.black50,
            text = str(self.index),                            
            z = -.1                                                     
            )

    # f1 ~ f3 눌렀을 때, 각 박스 삭제하고 다시 생성하기 위한 delete 
    def delete(self) :
        for e in self.item_parent.children :
            destroy(e)

    # ( 1 x 9 ) 박스의 빈 칸 찾는 매서드
    def find_free_spot(self):                                                      
        taken_spots = [(int(e.x), int(e.y)) for e in self.item_parent.children]    
        for y in range(1):                                                         
            for x in range(9):                                                     
                if not (x,-y) in taken_spots:                                      
                    return (x,-y)





if __name__ == '__main__':
    app = Ursina()
    inventory = Inventory()
    for i in range(9):                                                  
        inventory.append('sword')  

    app.run()