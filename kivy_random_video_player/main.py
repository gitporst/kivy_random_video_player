import kivy
kivy.require('1.11.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.videoplayer import VideoPlayer


class MenuScreen(Screen):
    pass

class VideoScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class Player(VideoPlayer):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)


main_kivy = Builder.load_file('video_player.kv')

class MyApp(App):

    def build(self):
        return main_kivy


if __name__ == '__main__':
    MyApp().run()