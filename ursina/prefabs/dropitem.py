from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
import datetime, time

class Dropitem(Entity) :
    def __init__(self, player, texture, position) :
        super().__init__()
        
        self.dropped_item = Entity(parent = self,model = 'cube',scale = .3, texture=texture, position = position)

        self.is_focused = False
        
        self.script = None

        self.dropped_time = datetime.datetime.now()

        self.gravity = 1
        self.grounded = False
        self.speed = 5
        self.height = 1
        self.air_time = .0
        
        self.player = player

    def update(self) :
        # 드롭된 아이템이 존재하면,
        if self.dropped_item :
            # 돌고 있음
            self.dropped_item.rotation_y += 2

            now = datetime.datetime.now()

            # 떨어지고 난 뒤 흘러간 시간 (초)
            dropped_remain = (now - self.dropped_time).total_seconds()

            if dropped_remain > 60 :
                destroy(self)
                return

            # 아이템이랑 플레이어 거리 계산
            r = distance(self.dropped_item.position, self.player.position)

            # 거리가 1 미만이면 사라지게함
            if r < 1 :
                destroy(self)
                return
            
            # 거리가 3.5 미만이면 먹고
            elif r < 3.5 :
                self.dropped_item.add_script(SmoothFollow(target=self.player, offset=[0,0,0],speed = 3))
                return

            # 드롭 아이템 중력 ray
            ray = boxcast(self.dropped_item.world_position + (self.dropped_item.up*.5), self.dropped_item.down, ignore=(self.dropped_item,),debug=False,thickness = (.3,.3))

            if ray.distance > self.height + .5:
                self.dropped_item.y -= .1



if __name__ == "__main__" :
    app = Ursina()
    
    ground = Entity(model='cube',scale = (20,0,20),position=(0,-5,0),texture='brick',collider='box')

    player = FirstPersonController()
    player.gravity = 0
    def input(key) :
        if key == 'e' :
            dropitem = Dropitem(player,'brick',(0,5,0))

    app.run()