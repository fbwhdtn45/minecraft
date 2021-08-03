from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Tabpanel(Button) :
    def __init__(self, player) :
        super().__init__(
            color=color.black33,
            scale = .2,
            position = (-.4 * window.aspect_ratio, .0)
        )
        self.player = player
        
    def update(self) :
        # 탭 누르는 동안 tab_panel 보여주기
        if held_keys['tab'] : 
            # 탭 패널 생성
            self.text = "My Position" + "\n"
            self.text += "X : " + str(round(self.player.position.x,1)) + "\n"
            self.text += "Y : " + str(round(self.player.position.y,1)) + "\n"
            self.text += "Z : " + str(round(self.player.position.z,1))
            self.visible = True
        else : 
            self.visible = False

if __name__ == "__main__" :
    app = Ursina()
    
    ground = Entity(model='cube',scale = (20,0,20),position=(0,-5,0),texture='brick',collider='box')

    player = FirstPersonController()

    player.gravity = 0
    
    tabpanel = Tabpanel(player)

    app.run()