from ursina import *

class Background(Sky) :
    def __init__(self, texture = texture,**kwargs):
        super().__init__(
            model = 'sphere',
            double_sided = True,
            texture = texture
        )

        for key, value in kwargs.items():
            setattr(self, key, value)


if __name__  == '__main__':
    app = Ursina()
    Background()
    app.run()