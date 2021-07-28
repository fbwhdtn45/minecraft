from ursina import *
from ursina.prefabs.button import Button
from ursina.models.procedural.quad import Quad

class Panel(Entity):

    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.model = Quad()
        self.color = color.yellow

        for key, value in kwargs.items():
            setattr(self, key, value)

    # 텍스트 설정
    def __setattr__(self, name, value):
        if name == 'text':
            self.text = value
            return

if __name__ == '__main__':
    app = Ursina()
    p = Panel()
    app.run()
