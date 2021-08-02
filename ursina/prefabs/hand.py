from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.voxel import Voxel

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'cube',
            texture = texture,
            color = color.clear,
            scale = (.15,.15,.99),
            rotation = Vec3(160, -15, 180),
            position = Vec3(.7,-.6,0)
        )
        # 큐브
        self.voxel = Entity(
            parent = self,
            model = 'cube',
            # 초기 선언
            texture = None,
            color = color.clear,
            
            scale = (1.5,1.5,.3),
            position = Vec3(.13,.13,-.7) 
        )
        # 손
        self.finger = Entity(
             parent = self,
             model = 'sphere',
             texture = 'brick',
             scale = (1.2,1.2,.2),
             color = color.yellow,
             position = Vec3(0,0,-.57) 
        )   
        # 팔                              
        self.hand = Entity(
            parent = self,
            model = 'cube',
            texture = 'brick',
            scale = 1,
            color = color.green,
            position = Vec3(0, 0, 0) 
        )   

    def change_block(self, texture) :
        # 텍스처 바꾸기
        self.voxel.texture = texture
        # 텍스처가 있는 경우,
        if texture :
            # color.clear -> color.white 바꾸기
            self.voxel.color = color.white
        else :
            self.voxel.color = color.clear
    
    def input(self,key) :
        # 왼쪽 / 오른쪽 마우스 클릭 시, 손 움직이게
        if key == 'left mouse down' or key == 'right mouse down' :
            # 손에 voxel이 없으면, 안 움직이게
            if self.voxel.color == color.clear and key == 'left mouse down': 
                return
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