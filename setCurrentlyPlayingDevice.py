import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read user-modify-playback-state'

if len(sys.argv) > 2:
    username = sys.argv[1]
    device = sys.argv[2]
else:
    print "Usage: %s username device_id" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    
    sp.transfer_playback(device)
    #print results['name'] + '-' + results['artists'][0]['name']
else:
    print "Can't get token for", username
