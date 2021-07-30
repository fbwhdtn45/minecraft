from ursina import *
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.first_person_controller import FirstPersonController
from minecraft_login import Login
from ursina.application import *
from ursina.prefabs.quick_slot import QuickSlot
from ursina.prefabs.cursor import Cursor
from ursina.prefabs.voxel import Voxel
from ursina.prefabs.clock import Clock
from ursina.prefabs.background import Background
import math
from ursina.prefabs.hand import Hand

class Minecraft(Entity) :
    app = Ursina()
    window.fps_counter.enabled = False
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

    def __init__(self):
        # 초기화
        super().__init__()
        # 1인칭 플레이어 생성
        self.player = FirstPersonController()
        # 배경 생성  
        self.sky = Background(texture = load_texture('assets/background/sky.jpg'))

        # 손 생성
        self.hand = Hand()

        # 체력 바 생성
        self.health = HealthBar(position = (-.4, -.35))

        # 체력 이미지 생성
        self.heart = Button(icon='./assets/heart.png', scale = .05, color = color.clear, position = (-.4,-.365,-.1)) 

        # 탭 패널 생성
        self.tab_panel = Button(color=color.black33, scale = .2, position = (-.4 * window.aspect_ratio, .0))

        # 죽었는 지 변수
        self.is_died = False

        # 퀵슬롯 창 생성
        self.quickSlot = QuickSlot()

        # 초기 퀵슬롯 설정 --------------- 인벤토리랑 엮어서 수정하기
        for i in range(9):                                                  
            self.quickSlot.append(Minecraft.blocks[i])

        # 초기 지형 생성 ---------------- 수정하기
        for z in range(-5,5) :
            for x in range(-5,5) :
                self.voxel = Voxel(position=(x,0,z))


        # 오른쪽 위 시간패널 생성
        self.clock = Clock()

        # 실행
        Minecraft.app.run()
    
    # 키보드 입력받기
    def input(self,key) :
        # 자유모드
        if key == 'f6' :
            self.player.gravity = 0
            return

        # 중력모드
        elif key == 'f7' :
            self.player.gravity = 1
            return

        # 블록 바꾸기(1~10)
        if key.isdigit() :
            if int(key) <= 9 :
                Minecraft.block_id = 9 * Minecraft.block_section + (int(key) - 1)
        # 블록 바꾸기(f1~f3)
        elif len(key) == 2 and key[0] == 'f':
            if int(key[1]) <= 3 :
                Minecraft.block_section = int(key[1:]) - 1
                Minecraft.block_id = 9 * Minecraft.block_section
                # 인벤토리 삭제 후
                self.quickSlot.delete()
                # 다시 인벤토리 채워넣기
                for i in range(Minecraft.block_id,Minecraft.block_id+9):                                                  
                    self.quickSlot.append(Minecraft.blocks[i])

        # 손에 있는 블록 교체
        self.voxel.change_block(Minecraft.blocks[Minecraft.block_id])
        self.hand.change_block(Minecraft.blocks[Minecraft.block_id])
        return

    # 자동 호출되는 함수 
    def update(self) :
        # Y : -50 이하로 내려가면 player 죽음
        if not self.player :
            return

        if self.player.position.y < - 50 :
            self.player.position = (0,0,0)
            self.health.value = 0
            return

        # 낙사 데미지
        if self.player.fall_time >= 0.2:
            if self.player.fall_time >= 0.25 :
                self.health.value -= 20
            elif self.player.fall_time >= 0.3 :
                self.health.value -= 30
            else :
                self.health.value -= 10 
            self.player.fall_time = 0
            return

        # 체력이 0 이면 죽음.
        if self.health.value == 0 :
            # 죽지 않은 상태이면,
            if not self.is_died :
                # 죽은 상태로 전환
                self.is_died = True
                # 1인칭 사용해제
                self.player.on_disable()
                destroy(self.player.cursor)
                # 죽었을 때 패널 생성
                die_panel = Button(scale = (3,1), color = color.black66, position = (0,0,-.99), text = 'You Died!!',disabled = True)
                # restart 버튼
                restart_btn = Button(parent = die_panel,scale = (.1,.05),color = color.black,text_color = color.white,text = 'Restart : [ R ]',position = (-.1,-.15,-.1), _on_click = self.restart)
                # quit 버튼
                quit_btn = Button(parent = die_panel,scale = (.1,.05),color = color.black,text_color = color.white,text = 'Quit : [ Q ]',position = (.1,-.15,-.1), _on_click = self.restart)
            else :
                return

        # CTRL 눌러진 상태라면, 플레이어 속도 제어
        if held_keys['control'] :
            self.player.speed = 2.5
        elif held_keys['shift'] :
            self.player.speed = 10
        else :
            self.player.speed = 5

        # 탭 누르는 동안 tab_panel 보여주기
        if held_keys['tab'] : 
            # 탭 패널 생성
            self.tab_panel.text = "My Position" + "\n"
            self.tab_panel.text += "X : " + str(round(self.player.position.x,1)) + "\n"
            self.tab_panel.text += "Y : " + str(round(self.player.position.y,1)) + "\n"
            self.tab_panel.text += "Z : " + str(round(self.player.position.z,1))
            self.tab_panel.visible = True
        else : 
            self.tab_panel.visible = False

    def restart(self) :
        print('다시하기')
        return


if __name__ == "__main__" :
    # login = Login()
    # if login.success :
    #     minecraft = Minecraft()

    minecraft = Minecraft()