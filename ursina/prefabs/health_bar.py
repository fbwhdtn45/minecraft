from ursina import *


class HealthBar(Button):
    def __init__(self, max_value=100, **kwargs):
        super().__init__(
            position = (-.45 * window.aspect_ratio, .45),
            origin = (-.5, .5),
            scale = (Text.size*20, Text.size*1.3),
            color = color.black,
            highlight_color = color.black,
            text = 'hp / max hp',
            )

        self.bar = Entity(parent=self, model='quad', origin=self.origin, z=-.01, color=color.black, ignore=True)
        # 애니메이션 시간
        self.animation_duration = .2
        self.lines = Entity(parent=self.bar, origin=self.origin, z=-0.1, color=color.clear, ignore=True)
        # 체력 바 텍스트 굵기
        self.text_entity.scale *= .85
        # 체력 바 모서리 둥글게
        self.roundness = .5
        # 텍스트 하얀색
        self.text_entity.color = color.white
        # 체력 최대값 설정
        self.max_value = max_value
        # 죽었는 지 여부
        self.died = False

        self.clamp = True
        self.scale_x = self.scale_x # update rounded corners

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.scale_y = self.scale_y # update background's rounded corners
        self.value = self.max_value

    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, n):
        if self.clamp:
            n = clamp(n, 0, self.max_value)

        self._value = n

        self.bar.animate_scale_x(n/self.max_value, duration=self.animation_duration, curve=curve.in_out_bounce)
        invoke(setattr, self.lines, 'enabled', True, delay=.1)

        # HP : 100 / 100
        self.text_entity.text = f'HP: {n} / {self.max_value}'

        if self.lines.enabled:
            self.lines.model = Grid(n, 1)

        if n / self.max_value >= self.scale_y / self.scale_x:
            aspect_ratio = n/self.max_value*self.scale_x / self.scale_y
            self.bar.model = Quad(radius=self.roundness, aspect=aspect_ratio)
        else:
            self.bar.model = 'quad'
        self.bar.origin = self.bar.origin

    def update(self) :
        # 체력 바 관리 
        # 3분의 2 넘으면 초록색
        if self.value >= self.max_value / 3 * 2:
            self.bar_color = color.green
        # 3분의 1 넘으면 주황색
        elif self.value >= self.max_value / 3 * 1 :
            self.bar_color = color.gold
        # 체력 0 이면 죽음
        elif self.value == 0 :
            self.died = True
        # 그 이외는 빨간색
        else :
            self.bar_color = color.red

    # 속성 설정
    def __setattr__(self, name, value):
        if name == 'show_lines':
            self.lines.enabled = value
            return

        if name == 'text_color' :
            self.text_entity.color = value
            return

        if name == 'bar_color':
            self.bar.color = value
            return


        super().__setattr__(name, value)

        if 'scale' in name and hasattr(self, 'roundness'):  # update rounded corners of background when scaling
            orginal_text_position = self.text_entity.position
            self.model = Quad(radius=self.roundness, aspect=self.world_scale_x / self.world_scale_y)
            self.origin = self.origin
            self.text_entity.position = orginal_text_position

        if 'scale' in name and hasattr(self, 'text_entity'):  # make sure the text doesn't scale awkwardly
            self.text_entity.world_scale_x = self.text_entity.world_scale_y


# 메인 일 때 실행
if __name__ == '__main__':
    app = Ursina()

    health_bar_1 = HealthBar(bar_color=color.green, roundness=.5, max_value=50)

    def input(key):
        if key == '+' or key == '+ hold':
            health_bar_1.value += 10
        if key == '-' or key == '- hold':
            health_bar_1.value -= 10

    app.run()
