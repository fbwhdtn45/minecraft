from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor, abs
from perlin_noise import PerlinNoise
import math, time

from ursina.prefabs.health_bar import HealthBar

app = Ursina()

# Terrain 생성 주기 계산 시간
prevTime = time.time()
# loading... <- "." 개수 제어
loading_cnt = 0
# 안개 설정
# scene.fog_color = color.rgb(0,200,0)
# scene.fog_density = 0.1
# 땅(=grain) 텍스쳐 설정
grain = load_texture('assets/block/stone.png')

# Terrain 엔티티 설정
terrain = Entity(model=None,collider=None)
# Terrain 생성할 가로/세로 칸
terrainWidth = 50

subWidth = terrainWidth
subsets = []
subCubes = []
sci = 0 # SubCube index.
currentSubset = 0

# 펄린 노이즈 매개변수 설정
noise = PerlinNoise(octaves=2,seed=2021)
amp = 32
freq = 100

# 로딩 창
loading_panel = Button(text='loading', scale = (2.5,1), color = color.azure)
# 로딩 progress bar
loading_bar = HealthBar(position = (-.25,-.05),is_health = False,value = .0,bar_color = color.green)
loading_bar.text_entity.color = color.clear

# Terrain 그리기 종료 여부
finishedTerrain = False

shellies = []
shellWidth = 10


def update():
    global prevX, prevZ, prevTime, finishedTerrain
    if abs(player.z - prevZ) > 1 or abs(player.x - prevX) > 1 :
        generateShell()

    if not finishedTerrain :
        if time.time() - prevTime > 0.1 :
            generateSubset()
            loading()
            prevTime = time.time()

def loading() :
    global subsets, currentSubset, loading_cnt, finishedTerrain
    
    # 로딩 중일 때 loading bar 변경
    loading_bar.value = int(currentSubset/len(subsets)*100)

    # 로딩 중일 때 text 변경
    if loading_cnt < 5 and not finishedTerrain:
        loading_panel.text += "."
        loading_cnt += 1
    else :
        if not finishedTerrain :
            loading_panel.text = "loading"
            loading_cnt = 0
        # 로딩 끝나면 text 삭제
        else :
            loading_panel.text = ''

for i in range(subWidth) :
    bud = Entity(model = 'cube')
    subCubes.append(bud)

for i in range(int((terrainWidth*terrainWidth)/subWidth)) :
    bud = Entity(model=None)
    bud.parent = terrain
    subsets.append(bud)

def generateSubset() :
    global subWidth, terrainWidth, currentSubset, sci
    if currentSubset >= len(subsets) :
        finishTerrain()
        return
    for i in range(subWidth) :
        x = subCubes[i].x = floor((i + sci) / terrainWidth)
        z = subCubes[i].z = floor((i + sci) % terrainWidth)
        y = subCubes[i].y = floor((noise([x/freq,z/freq]))*amp)
        subCubes[i].parent = subsets[currentSubset]
        subCubes[i].color = color.green
        subCubes[i].visible = False

    subsets[currentSubset].combine(auto_destroy = False)
    subsets[currentSubset].texture = grain
    sci += subWidth
    currentSubset += 1

# Terrain 다 그렸으면,
def finishTerrain() :
    global finishedTerrain,loading_bar,loading_panel
    if not finishedTerrain :
        destroy(loading_bar)
        destroy(loading_panel)
        player.cursor.visible = True
        finishedTerrain = True



for i in range(shellWidth*shellWidth) :
    bud = Entity(model='cube',collider='box')
    bud.visible = False
    shellies.append(bud)

def generateShell() :
    global shellWidth, amp, freq
    for i in range(len(shellies)) :
        x = shellies[i].x = floor((i/shellWidth) +
                            player.x - 0.5*shellWidth)
        z = shellies[i].z = floor((i%shellWidth) +
                            player.z - 0.5*shellWidth)
        shellies[i].y = floor((noise([x/freq,z/freq]))*amp)
        
player = FirstPersonController()
player.cursor.visible = False
player.gravity = 1
player.x = player.z = 2
player.y = 20
prevZ = player.z
prevX = player.x

generateShell()

app.run()