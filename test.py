from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor, abs
from perlin_noise import PerlinNoise
import math

app = Ursina()

def input(key) :
    if key =='q' :
        quit()
    if key == 'g' : generateSubset()

def update():
    global prevX, prevZ
    if abs(player.z - prevZ) > 1 or \
        abs(player.x - prevX) > 1 :
        generateShell()

# scene.fog_color = color.rgb(0,200,0)
# scene.fog_density = 0.1

grain = load_texture('assets/block/stone.png')

terrain = Entity(model=None,collider=None)
terrainWidth = 100
subWidth = terrainWidth
subsets = []
subCubes = []
sci = 0 # SubCube index.
currentSubset = 0

for i in range(subWidth) :
    bud = Entity(model = 'cube')
    subCubes.append(bud)

for i in range(int((terrainWidth*terrainWidth)/subWidth)) :
    bud = Entity(model=None)
    subsets.append(bud)

def generateSubset() :
    global subWidth, terrainWidth, currentSubset, sci
    if currentSubset >= len(subsets) :
        return
    for i in range(subWidth) :
        x = subCubes[i].x = floor((i + sci) / terrainWidth)
        z = subCubes[i].z = floor((i + sci) % terrainWidth)
        y = subCubes[i].y = floor((noise([x/freq,z/freq]))*amp)

        subCubes[i].parent = subsets[currentSubset]
        subCubes[i].color = color.green
        subCubes[i].visible = False

    subsets[currentSubset].combine(auto_destroy)
    subsets[currentSubset].texture = grain
    sci += subWidth
    currentSubset += 1

noise = PerlinNoise(octaves=2,seed=2021)
amp = 6
freq = 24


# for i in range(terrainWidth * terrainWidth) :
#     bud = Entity(model='cube',color=color.green,texture=grain)
#     bud.x = floor(i/terrainWidth)
#     bud.z = floor(i%terrainWidth)
#     bud.y = floor((noise([bud.x/freq,bud.z/freq]))*amp)
#     bud.parent = terrain

# terrain.combine()
# terrain.collider = 'mesh'
# terrain.texture = grain

shellies = []
shellWidth = 6
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
player.gravitiy = 0.5
player.x = player.z = 5
player.y = 20
prevZ = player.z
prevX = player.x

generateShell()

app.run()