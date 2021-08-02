from ursina import *
from ursina.models.procedural.quad import Quad
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import load_texture
import math

class Voxel(Button) :
    # Init 값
    now_texture = 'brick'
    now_color = color.white
    def __init__(self, position=(0,0,0), texture=now_texture, **kwargs) :
        super().__init__(
            parent=scene,
            model='cube', # 기본 블록 모델 (정육면체)
            position = position,
            texture = texture,
            origin_y=0.5,
            color = Voxel.now_color,
            scale=1.0 # 블록의 크기
        )
    
    def change_block(self, texture) :
        Voxel.now_texture = texture
        if texture :
            Voxel.now_color = color.white
        else :
            Voxel.now_color = color.clear
    
    # 왼쪽/self.오른쪽 마우스 클릭 매서드
    def input(self, key) : # 
        if self.hovered : #구형에 갖다댄 채
            # distance = ((self.position.x - mouse.normal.x)**2 + (self.position.y - mouse.normal.y)**2 + (self.position.z - mouse.normal.z)**2)**0.5
            # print(distance)
            # if distance <= 6 :
            if key == 'left mouse down' : # 왼쪽마우스 클릭
                # 손에 아무것도 없을 경우,
                if Voxel.now_color == color.clear or Voxel.now_texture == 'brick' :
                    return
                Voxel(position=self.position + mouse.normal,texture=Voxel.now_texture) # 박스 생성
            elif key == 'right mouse down' : # 오른쪽마우스 클릭
                destroy(self) # 박스 파괴



if __name__ == '__main__':
    from ursina import *
    app = Ursina()
    player = FirstPersonController()

    for z in range(-5,5) :
        for x in range(-5,5) :
            voxel = Voxel(position=(x,0,z))

    voxel.change_block('sword')      
    
    app.run()