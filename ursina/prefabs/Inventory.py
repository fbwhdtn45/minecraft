from ursina import *
from ursina.prefabs.button import Button

class Inventory(Button):
    def __init__(self):
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

        self.item_parent = Entity(parent=self, scale=(1/9,1))                                     
        self.index = 0

    def append(self, item):                                             
        icon1 = Button(                                                         
            parent = self.item_parent,                             
            model = 'quad',                                             
            origin = (-.5,.5),                                          
            color = color.clear,
            texture = item,
            icon = item,
            position = self.find_free_spot(),                              
            z = -.2                                                     
            )

        icon = Button(
            parent = icon1,
            model = 'quad',
            origin = (-.5,.5),
            scale= (1/5,1/5),
            color = color.black33,
            value = self.index,                             
            z = -.3
        )

    def delete(self) :
        for e in self.item_parent.children :
            destroy(e)

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