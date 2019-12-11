import kivy
kivy.require('1.11.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
from kivy.uix.videoplayer import VideoPlayer


class MenuScreen(Screen):
    pass

class VideoScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

main_kivy = Builder.load_file('video_player.kv')

class MyApp(App):

    def build(self):
        return main_kivy


if __name__ == '__main__':
    MyApp().run()