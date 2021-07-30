from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.voxel import Voxel

class Hand(Entity):
    now_texture = 'brick'
    def __init__(self,texture = now_texture,**kwargs):
        super().__init__(
            parent = camera.ui,
            model = 'cube',
            texture = texture,
            color = color.clear,
            scale = (.15,.15,.99),
            rotation = Vec3(160, -15, 180),
            position = Vec3(.7,-.6,0)
        )
        self.voxel = Entity(
            parent = self,
            model = 'cube',
            texture = Hand.now_texture,
            scale = (1.5,1.5,.3),
            #color = color.red,
            position = Vec3(.13,.13,-.7) 
        )
        self.finger = Entity(
             parent = self,
             model = 'sphere',
             texture = 'brick',
             scale = (1.2,1.2,.2),
             color = color.yellow,
             position = Vec3(0,0,-.57) 
        )                                 
        self.hand = Entity(
            parent = self,
            model = 'cube',
            texture = 'brick',
            scale = 1,
            color = color.green,
            position = Vec3(0, 0, 0) 
        )   

    def change_block(self, texture) :
        self.voxel.texture = texture
    
    def input(self,key) :
        if key == 'left mouse down' or key == 'right mouse down' :
            self.position = (.6,-.5,0)
        else :
            self.position = (.7,-.6,0)

if __name__ == '__main__':
    app = Ursina()
    player = FirstPersonController()

    for z in range(-5,5) :
        for x in range(-5,5) :
            voxel = Voxel(position=(x,0,z))

    hand = Hand()
    app.run()