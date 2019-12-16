import kivy

kivy.require('1.11.1')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.videoplayer import VideoPlayer
from kivy.properties import StringProperty, ObjectProperty

from pathlib import Path


class MenuScreen(Screen):
    """"the screen with the main menu"""

    # all the paths with the regular videos
    video_paths = sorted(Path('data', 'resources').glob('*.mp4'))
    # all the paths with the bonus material
    bonus_paths = sorted(Path('data', 'bonus').glob('*.mp4'))
    # the current video path
    video_name = StringProperty()

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)


class VideoScreen(Screen):
    video_name = StringProperty()
    player = ObjectProperty()

    def __init__(self, **kwargs):
        super(VideoScreen, self).__init__(**kwargs)

    def on_leave(self, *args):
        """stop the video if still running"""
        self.player.state = 'stop'


class Player(VideoPlayer):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)


main_kivy = Builder.load_file('video_player.kv')


class MyApp(App):

    def build(self):
        return main_kivy


if __name__ == '__main__':
    MyApp().run()
