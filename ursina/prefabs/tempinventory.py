from ursina import *

class Tempinventory(Button):
    def __init__(self):
        # 초기 설정 ( 1 x 9 칸 )
        super().__init__(
            parent = scene,
            model = 'quad',
            origin = (-.5,.5),
            scale = 0,
            # visible = False                              
            )

        # ( 5 x 9 )칸의 각 칸마다 자식 Entity 설정
        self.item_slot = Button(parent=self, modle = 'quad',texture_scale = (9,5))       

    def append(self, item_texture, item_x, item_y):      
        # 아이템 박스                                  
        box = Draggable(                                                         
            parent = self.item_slot,                             
            model = 'quad',                                             
            origin = (-.5,.5),                                          
            #color = color.clear,
            texture = item_texture,
            position = (item_x,item_y,-.1),                         
            z = -.2                                                      
            )

    def delete(self) :
        for e in self.item_slot.children :
            destroy(e)




if __name__ == '__main__':
    app = Ursina()

    temp = Tempinventory()

    index = 0

    for e in temp.children :
        index += 1
        print(index)
        print(e)

    app.run()