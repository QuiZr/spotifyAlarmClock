import sys
import spotipy
import spotipy.util as util
import unicodedata
#import traceback

class getTrackNameAndArtist:
    global scope
    scope = 'user-library-read user-modify-playback-state'

    def __init__(self, username):
        self.username = username
        self.token = None
        self.sp = spotipy.Spotify(auth=self.token)

    def renewToken(self):
        self.token = util.prompt_for_user_token(self.username, scope)
        self.sp = spotipy.Spotify(auth=self.token)

    def escapeUnicode(self, text):
        return unicodedata.normalize('NFKD', unicode(text)).encode('ascii', 'ignore')

    def getSongName(self, track_id):
        try:
            results = self.sp.track(track_id)
            name = self.escapeUnicode(results['name'])
            artist = self.escapeUnicode(results['artists'][0]['name'])
            return name + " - " + artist        
        except:
            #traceback.print_exc()
            self.renewToken()
            return self.getSongName(track_id)
