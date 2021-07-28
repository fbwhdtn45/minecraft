from ursina import *
from ursina.models.procedural.quad import Quad
import textwrap

class Voxel(Button) :
    def __init__(self, position=(0,0,0), texture = 'stone') :
        super().__init__(
            parent=scene,
            position=position,
            model='cube', # 기본 블록 모델 (정육면체 )
            origin_y=0.5,
            texture=texture,
            color=color.color(0,0,random.uniform(0.9,1.0)), # 하얀색 블록, 명도 0.9~1.0 랜덤
            scale=1.0 # 블록의 크기
        )
    # 왼쪽/오른쪽 마우스 클릭 매서드
    def input(self, key, texture) : # 
        if self.hovered : #구형에 갖다댄 채
            if key == 'left mouse down' : # 왼쪽마우스 클릭 
                Voxel(position=self.position + mouse.normal, texture = texture) # 박스 생성
            elif key == 'right mouse down' : # 오른쪽마우스 클릭
                destroy(self) # 박스 파괴



if __name__ == '__main__':
    from ursina import *
    app = Ursina()

    for z in range(-5,5) :
        for x in range(-5,5) :
            voxel = Voxel(position=(x,0,z))
    
    app.run()