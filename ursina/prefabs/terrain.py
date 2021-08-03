from ursina import *
from ursina.prefabs.voxel import Voxel
from perlin_noise import PerlinNoise
import numpy
from ursina.prefabs.first_person_controller import FirstPersonController

class Terrain(Entity) :
    def __init__(self, x = 0, z = 0, texture = 'brick', **kwargs) :
        super().__init__()

        self.noise = PerlinNoise(octaves=random.randint(1, 2), seed = random.randint(0,5000))
        
        self.freq = random.randint(1,100)
        
        self.amp = random.randint(1,100)

        self.generate(x,z,texture)

        self.player = player

        for key, value in kwargs.items() :
            if 'player' in kwargs.keys() :
                self.player = value

    def generate(self,map_x,map_z,map_texture) :
        for z in range(-map_z,map_z) :
            for x in range(-map_x,map_x) :
                y = floor((self.noise([x/self.freq, z/self.freq])*self.amp))
                voxel = Voxel(position =(x, y, z),texture = map_texture, player = self.player)


if __name__ == "__main__" :
    app = Ursina()
    
    player = FirstPersonController()
    terrain = Terrain(x = 10, z = 10, texture = 'brick', player = player)

    app.run()