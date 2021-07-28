from ursina import *
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.first_person_controller import FirstPersonController
import math
from minecraft_login import Login
from ursina.application import *
from ursina.prefabs.Inventory import Inventory
from ursina import ursinastuff
from ursina.prefabs.cursor import Cursor

if __name__ == "__main__" :
    # login = Login()
    # login.mainloop()
    # if login.login_success :
    app = Ursina()
    window.fps_counter.enabled = False

    # 1인칭 플레이어 생성
    player = FirstPersonController()

    # 땅 블록 선언
    grain = load_texture('assets/block/stone.png')

    # 블록 배열
    blocks = [
        load_texture('assets/block/stone.png'), # 0
        load_texture('assets/block/brick.png'), # 1
        load_texture('assets/block/glass.png'), # 2
        load_texture('assets/block/quartz.png'), # 3
        load_texture('assets/block/gold.png'), # 4
        load_texture('assets/block/diamond.png'), # 5
        load_texture('assets/block/emerald.png'), # 6
        load_texture('assets/block/amethyst.png'), # 7
        load_texture('assets/block/honey.png'), # 8
        load_texture('assets/block/slime.png'), # 9
        load_texture('assets/block/redsand.png'), # 10
        load_texture('assets/block/redstone.png'), # 11
        load_texture('assets/block/bluestone.png'), # 12
        load_texture('assets/concrete/white.png'), # 13
        load_texture('assets/concrete/red.png'), # 14
        load_texture('assets/concrete/purple.png'), # 15
        load_texture('assets/concrete/pink.png'), # 16
        load_texture('assets/concrete/orange.png'), # 17
        load_texture('assets/concrete/lime.png'), # 18
        load_texture('assets/concrete/lightblue.png'), # 19
        load_texture('assets/concrete/green.png'), # 20
        load_texture('assets/concrete/gray.png'), # 21
        load_texture('assets/concrete/cyan.png'), # 22
        load_texture('assets/concrete/blue.png'), # 23
        load_texture('assets/concrete/black.png'), # 24
        load_texture('assets/concrete/brown.png'), # 25
        load_texture('assets/concrete/magenta.png'), # 26
        load_texture('assets/concrete/lightgray.png'), # 27
        load_texture('assets/concrete/yellow.png') # 28
    ]

    # 블록 순서
    block_section = 0
    block_id = 0

    # 블록 클래스 선언
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
        def input(self, key) : # 
            if self.hovered : #구형에 갖다댄 채
                if key == 'left mouse down' : # 왼쪽마우스 클릭 
                    Voxel(position=self.position + mouse.normal,texture = blocks[block_id]) # 박스 생성
                elif key == 'right mouse down' : # 오른쪽마우스 클릭
                    destroy(self) # 박스 파괴 

    # 배경 생성  
    sky = Sky(texture=load_texture('assets/background/sky.jpg'),scale = 500, model = 'sphere', double_sided = True)

    # 손 생성
    hand = Entity(
        parent = camera.ui,
        model = 'cube',
        texture = blocks[block_id],
        scale = 0.3,
        rotation = Vec3(-10, -10, 10),
        position = Vec2(0.6, - 0.5)
    )

    # 체력 바 생성
    health = HealthBar(position = (-.4, -.35))

    # 체력 이미지 생성
    heart = Button(icon='./assets/heart.png', scale = .05, color = color.clear, position = (-.4,-.365,-.1)) 

    # 탭 패널 생성
    tab_panel = Button(color=color.black33, scale = .2, position = (-.4 * window.aspect_ratio, .0))

    # 죽었는 지 변수
    is_died = False

    # 인벤토리 창 생성
    inventory = Inventory()

    # 초기 인벤토리 설정
    for i in range(9):                                                  
        inventory.append(blocks[i]) 

    # 키보드 입력받기
    def input(key) :
        global block_id, player, block_section,blocks, is_died
        # 자유모드
        if key == 'f6' :
            player.gravity = 0
            return

        # 중력모드
        elif key == 'f7' :
            player.gravity = 1
            return

        # 블록 바꾸기(1~10)
        if key.isdigit() :
            if int(key) <= 9 :
                block_id = 9 * block_section + (int(key) - 1)
                # 손에 있는 블록 교체
                hand.texture = blocks[block_id]
                return
        # 블록 바꾸기(f1~f3)
        elif len(key) == 2 and key[0] == 'f':
            if int(key[1]) <= 3 :
                block_section = int(key[1:]) - 1
                block_id = 9 * block_section
                # 인벤토리 삭제 후
                inventory.delete()
                # 다시 인벤토리 채워넣기
                for i in range(block_id,block_id+9):                                                  
                    inventory.append(blocks[i])
                # 손에 있는 블록 교체
                hand.texture = blocks[block_id]
                return

    # 자동 호출되는 함수 
    def update() :
        global player, is_died, application
        # Y : -50 이하로 내려가면 player 죽음
        if not player :
            return

        if player.position.y < - 50 :
            player.position = (0,0,0)
            health.value = 0
            return

        # 낙사 데미지
        if player.fall_time >= 0.2:
            if player.fall_time >= 0.25 :
                health.value -= 20
            elif player.fall_time >= 0.3 :
                health.value -= 30
            else :
                health.value -= 10 
            player.fall_time = 0
            return

        # 체력이 0 이면 죽음.
        if health.value == 0 :
            # 죽지 않은 상태이면,
            if not is_died :
                # 죽은 상태로 전환
                is_died = True
                # 1인칭 사용해제
                player.on_disable()
                destroy(player.cursor)
                # 죽었을 때 패널 생성
                die_panel = Button(scale = (3,1), color = color.black66, position = (0,0,-.99), text = 'You Died!!',disabled = True)
                # restart 버튼
                restart_btn = Button(parent = die_panel,scale = (.1,.05),color = color.black,text_color = color.white,text = 'Restart : [ R ]',position = (-.1,-.15,-.1), _on_click = restart)
                # quit 버튼
                quit_btn = Button(parent = die_panel,scale = (.1,.05),color = color.black,text_color = color.white,text = 'Quit : [ Q ]',position = (.1,-.15,-.1), _on_click = application.quit)
            else :
                return
        
        # CTRL 눌러진 상태라면, 플레이어 속도 제어
        if held_keys['control'] :
            player.speed = 2.5
        elif held_keys['shift'] :
            player.speed = 10
        else :
            player.speed = 5

        # 탭 누르는 동안 tab_panel 보여주기
        if held_keys['tab'] : 
            # 탭 패널 생성
            tab_panel.text = "My Position" + "\n"
            tab_panel.text += "X : " + str(round(player.position.x,1)) + "\n"
            tab_panel.text += "Y : " + str(round(player.position.y,1)) + "\n"
            tab_panel.text += "Z : " + str(round(player.position.z,1))
            tab_panel.visible = True
        else : 
            tab_panel.visible = False

    # 초기 지형 생성
    for z in range(-5,5) :
        for x in range(-5,5) :
            voxel = Voxel(position=(x,0,z),texture=grain)
    
    def restart() :
        print('다시하기')

    # 실행
    app.run()