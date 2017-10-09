import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read user-modify-playback-state'

if len(sys.argv) > 2:
    username = sys.argv[1]
    track_id = sys.argv[2]
else:
    print "Usage: %s username track_id" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    
    results = sp.track(track_id)
    print results['name'] + '-' + results['artists'][0]['name']
else:
    print "Can't get token for", username
