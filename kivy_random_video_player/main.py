import kivy

kivy.require('1.11.1')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.videoplayer import VideoPlayer
from kivy.properties import StringProperty, ObjectProperty
from kivy.storage.jsonstore import JsonStore

from pathlib import Path
from random import choice
from datetime import date


class MenuScreen(Screen):
    """"the screen with the main menu"""
    # current month of year
    monthofyear = date.today().month
    day = date.today().day
    # all the paths with the regular videos
    video_paths = sorted(Path('data', 'resources').glob('*.mp4'))
    # all the paths with the bonus material
    bonus_paths = sorted(Path('data', 'bonus').glob('*.mp4'))
    # the current video path
    video_name = StringProperty()
    # the dumped log of previously played videos
    played_videos = ObjectProperty()

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.played_videos = JsonStore('data.json')

    def select_video(self):
        """"wrapper function for selecting a main video considering previously played videos of the month"""
        video_name = self.get_video_name()
        self.video_name = video_name
        self.add_to_previous_videos(video_name)

    def get_video_name(self):
        """"
        get today's video name, get from storage if already chosen previously today,
        else select from remaining videos that have not been played this month
        """
        removals = []
        # json storage is built as follows:
        # {self.monthofyear: {'removals': ['path_to_video_1', 'path_to_video_2', ...],
        #                     'today': self.day}}
        # check if we have entries for this month
        if self.played_videos.exists(self.monthofyear):
            # get removals and today
            entries = self.played_videos.get(self.monthofyear)
            removals = entries['removals']
            if self.day == entries['today']:
                # if day is today, then return the last item from list
                return removals[-1]
        # we need to randomly select a new video, first remove previously played ones from candidates
        for removal in removals:
            if removal in self.video_paths:
                self.video_paths.remove(removal)
        # return a random video
        return str(choice(self.video_paths))

    def add_to_previous_videos(self, video_name):
        """"add a video name to the storage"""
        # check if we already have entries for this month
        if self.played_videos.exists(self.monthofyear):
            # get the current entries
            entries = self.played_videos.get(self.monthofyear)
            # if not yet added...
            if self.day != entries['today']:
                # add new entry
                removals = entries['removals']
                removals.append(video_name)
                # and dump to storage
                self.dump_store(removals)
        else:
            # remove the whole storage - fresh month!
            self.played_videos.clear()
            self.dump_store([video_name])

    def dump_store(self, removals):
        """"write removals to storage"""
        self.played_videos.put(
            self.monthofyear,
            removals=removals,
            today=self.day,
        )

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
