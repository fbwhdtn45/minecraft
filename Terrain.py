from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor, abs
from perlin_noise import PerlinNoise
import math, time
from ursina.prefabs.loading import Loading

class Terrain(Entity) :
    ground = 'brick'
    def __init__(self) :
        super().__init__()
        self.terrain = Entity(model=None,collider=None)

        # Terrain 생성할 가로/세로 칸
        self.terrainWidth = 100
        self.subWidth = self.terrainWidth
        
        # subset / subset current index
        self.subsets = []
        self.subCubes = []
        self.sci = 0
        self.currentSubset = 0
        
        self.shellies = []
        self.shellWidth = 5
        
        # 펄린 노이즈 매개변수 설정
        self.noise = PerlinNoise(octaves=1,seed=2021)
        self.amp = random.randint(0,100)
        self.freq = random.randint(0,100)

        # Terrain 그리기 종료 여부
        self.finishedTerrain = False

        # self.loading = Loading()

        # empty
        for i in range(self.subWidth) :
            bud = Entity(model = 'cube')
            self.subCubes.append(bud)

        # empty
        for i in range(int((self.terrainWidth*self.terrainWidth)/self.subWidth)) :
            bud = Entity(model=None)
            bud.parent = self.terrain
            self.subsets.append(bud)

        # shell
        for i in range(self.shellWidth*self.shellWidth):
            bud = Entity(model='cube',collider='box')
            bud.visible=False
            self.shellies.append(bud)

        self.subject = FirstPersonController()
        self.subject.gravity = 0

        self.generateShell()

    def update(self):
        if not self.finishedTerrain :
            self.generateSubset()
            self.generateShell()

    def input(self,key) :
        if key =='g' :
            self.subject.gravity = 1

    def generateSubset(self) :
        if self.currentSubset >= len(self.subsets) :
            self.finishTerrain()
            return
        for i in range(self.subWidth) :
            x = self.subCubes[i].x = floor((i + self.sci) / self.terrainWidth)
            z = self.subCubes[i].z = floor((i + self.sci) % self.terrainWidth)
            y = self.subCubes[i].y = floor((self.noise([x/self.freq,z/self.freq]))*self.amp)
            self.subCubes[i].parent = self.subsets[self.currentSubset]
            self.subCubes[i].color = color.white
            self.subCubes[i].visible = False

        self.subsets[self.currentSubset].combine(auto_destroy = False)
        self.subsets[self.currentSubset].texture = 'brick'
        self.sci += self.subWidth
        self.currentSubset += 1
    
    # Terrain 다 그렸으면,
    def finishTerrain(self) :
        if not self.finishedTerrain :
            self.terrain.combine()
            #destroy(self.loading_bar)
            #destroy(self.loading_panel)
            self.finishedTerrain = True
            self.terrain.texture = 'brick'
        else :
            return
    
    def generateShell(self):
        for i in range(len(self.shellies)):
            x = self.shellies[i].x = floor((i/self.shellWidth) + 
                                self.subject.x - 0.5*self.shellWidth)
            z = self.shellies[i].z = floor((i%self.shellWidth) + 
                                self.subject.z - 0.5*self.shellWidth)
            self.shellies[i].y = floor((self.noise([x/self.freq,z/self.freq]))*self.amp)

if __name__ == "__main__" : 
    app = Ursina()

    terrain = Terrain()

    app.run()