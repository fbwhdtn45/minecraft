from ursina import *
from ursina.application import *
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.first_person_controller import FirstPersonController
from login import Login
from ursina.application import *
from ursina.prefabs.quickslot import Quickslot
from ursina.prefabs.inventory import Inventory
from ursina.prefabs.tempinventory import Tempinventory
from ursina.prefabs.cursor import Cursor
from ursina.prefabs.voxel import Voxel
from ursina.prefabs.clock import Clock
from ursina.prefabs.background import Background
import math
from ursina.prefabs.hand import Hand
from ursina.prefabs.dropitem import Dropitem
import pyautogui
from ursina.prefabs.tabpanel import Tabpanel
from ursina.prefabs.terrain import Terrain

class Minecraft(Entity) :
    acquire = False
    def __init__(self):
        super().__init__()

        # 1인칭 플레이어
        self.player = FirstPersonController()

        # 배경
        self.sky = Background(texture = load_texture('assets/background/sky.jpg'))

        # 손
        self.hand = Hand()

        # 체력 바
        self.health = HealthBar(position = (-.4, -.35))

        # 체력 이미지(하트모양)
        self.heart = Button(icon='./assets/heart.png', scale = .05, color = color.clear, position = (-.4,-.365,-.1)) 

        # 탭 패널
        self.tab_panel = Tabpanel(self.player)

        # 퀵 슬롯
        self.quickslot = Quickslot()
        
        # 인벤토리
        self.inventory = None
        self.is_first = True

        # 임시 인벤토리
        self.temp = Tempinventory()

        # 현재 시간
        self.clock = Clock()
        
        # 죽었을 때 패널
        self.die_panel = None
            # 블록 배열
        self.blocks = [
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

        # 초기 지형 생성
        self.terrain = Terrain()
        self.terrain.generate(5,5,self.player,self.blocks,self.temp)

    # 키보드 입력받기
    def input(self,key) :
        # e 누르면 생성or삭제 // esc 누르면 삭제
        if key == 'e' :
            # 인벤토리 삭제
            if self.inventory :
                self.temp.delete()
                for e in self.inventory.item_slot.children :
                    self.temp.append(e.texture, e.x, e.y)
                destroy(self.inventory)
                # 1인칭 모드
                self.player.on_enable()

            # 인벤토리 생성
            else :
                self.inventory = Inventory()
                # 커서 모드
                self.player.on_disable()

                # 인벤토리 퀵 슬롯 <-> 퀵 슬롯 연동
                for e in self.quickslot.item_parent.children :
                    self.inventory.append(self.inventory.quick_slot, e.texture, position = (e.x,0,-.1))
                # 인벤토리 <-> 임시 인벤토리 연동
                for e in self.temp.item_slot.children :
                    self.inventory.append(self.inventory.item_slot, e.texture, position = (e.x,e.y,-.1))
            return

        # 블록 바꾸기(1~9)
        if key.isdigit() :
            if int(key) > 0 :
                # 손에 있는 블록 교체
                for e in self.quickslot.item_parent.children :
                    if e.x == int(key) - 1 :
                        self.hand.change_block(e.texture)
                        return
                # 텍스처가 없는 칸인 경우
                self.hand.change_block(None)
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

        # CTRL 눌러진 상태라면, 플레이어 속도 제어
        if held_keys['control'] :
            # 자유모드는 속도 하락 x
            if self.player.gravity == 0 :
                return
            self.player.speed = 2.5
        elif held_keys['shift'] :
            self.player.speed = 10
        else :
            self.player.speed = 5

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
            if not self.player.is_died :
                # 죽은 상태로 전환
                self.player.is_died = True
                # 1인칭 사용해제
                self.player.on_disable()
                # 죽었을 때 패널 생성
                self.die_panel = Button(parent = camera.ui,scale = (3,1), color = color.black66, position = (0,0,-.99), text = 'You Died!!',disabled = True)
                # restart 버튼
                restart_btn = Button(parent = self.die_panel,scale = (.1,.05),color = color.black,text_color = color.white,text = 'Restart',position = (-.1,-.15,-.1), _on_click = self.restart)
                # quit 버튼
                quit_btn = Button(parent = self.die_panel,scale = (.1,.05),color = color.black,text_color = color.white,text = 'Quit',position = (.1,-.15,-.1), _on_click = self.quit)
            else :
                return

        # 인벤토리가 있으면, 인벤토리 퀵 슬롯이랑 퀵 슬롯이랑 동기화시키기
        if self.inventory : 
            self.quickslot.delete()
            for e in self.inventory.quick_slot.children :
                self.quickslot.append(e)
        
        if Minecraft.acquire :
            Minecraft.acquire = False
            self.temp.drop_append(Tempinventory.texture)
            return


    def restart(self) :
        destroy(self.terrain)
        self.player.is_died = False
        self.player.on_enable()
        destroy(self.die_panel)
        self.health.value = 100
        return

    # 게임 종료
    def quit(self) :
        application.quit()

if __name__ == "__main__" :

    def start() :
        # login = Login()
        # if login.success :

        app = Ursina()

        window.fps_counter.enabled = False
        
        game = Minecraft()     

        app.run()


    
    start()
    
