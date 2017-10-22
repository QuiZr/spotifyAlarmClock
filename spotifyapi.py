import sys
import spotipy
import spotipy.util as util
import unicodedata
#import traceback

class SpotifyApi:
    def __init__(self, username):
        self.username = username
        self.token = None
        self.sp = spotipy.Spotify(auth=self.token)

    def renew_token(self):
        scope = 'user-library-read user-modify-playback-state'
        self.token = util.prompt_for_user_token(self.username, scope)
        self.sp = spotipy.Spotify(auth=self.token)

    def escape_unicode(self, text):
        return unicodedata.normalize('NFKD', unicode(text)).encode('ascii', 'ignore')

    def get_song_name(self, track_id):
        try:
            results = self.sp.track(track_id)
            name = self.escape_unicode(results['name'])
            artist = self.escape_unicode(results['artists'][0]['name'])
            return name + " - " + artist        
        except:
            #traceback.print_exc()
            self.renew_token()
            return self.get_song_name(track_id)

    def transfer_playback(self, device_id):
        try:
            self.sp.transfer_playback(device_id)
        except:
            #traceback.print_exc()
            self.renew_token()
            self.transfer_playback(device_id)

    def start_playback(self, device_id, album):
        try:
            self.sp.start_playback(device_id, album)
        except:
            #traceback.print_exc()
            self.renew_token()
            self.start_playback(device_id, album)

    def set_volume(self, volume_percent, device_id):
        try:
            self.sp.volume(volume_percent, device_id)
        except:
            #traceback.print_exc()
            self.renew_token()
            self.set_volume(volume_percent, device_id)

