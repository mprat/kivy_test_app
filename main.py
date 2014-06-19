from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from settings_local import APPLICATION_ID, REST_API_KEY
from parse_rest.datatypes import Object
import threading

__version__ = '1.8.0'

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


    def on_touch_down(self, touch):
        if super(PongBall, self).on_touch_down(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False

        def save_to_parse():
            new_click = Object(x=touch.x, y=touch.y)
            new_click.save()

        t = threading.Thread(target=save_to_parse)
        t.start()

        print('you touched me!')
        return True

class PongGame(Widget):
    ball = ObjectProperty(None)

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(2, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()

        #bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        #bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    from parse_rest.connection import register
    register(APPLICATION_ID, REST_API_KEY)
    PongApp().run()