from ursina import *
from ursina.prefabs.voxel import Voxel
from perlin_noise import PerlinNoise
import numpy, math, random
from ursina.prefabs.first_person_controller import FirstPersonController

class Terrain(Entity) :
    def __init__(self) :
        super().__init__()

        self.noise = PerlinNoise(octaves=random.randint(1, 2), seed = random.randint(0,5000))
        
        self.freq = random.randint(1,100)
        
        self.amp = random.randint(1,100)

    def generate(self,map_x,map_z,player1,blocks,tempinventory) :
        for z in range(-map_z,map_z) :
            for x in range(-map_x,map_x) :
                idx = random.randint(0,len(blocks)-1)
                y = floor((self.noise([x/self.freq, z/self.freq])*self.amp))
                voxel = Voxel(position =(x, y, z),texture = blocks[idx], temp = tempinventory, player = player1)
    

if __name__ == "__main__" :
    app = Ursina()
    
    player = FirstPersonController()

    blocks = ['sword','gem','bag']
    terrain = Terrain()
    terrain.generate(10,10,player,blocks)

    app.run()