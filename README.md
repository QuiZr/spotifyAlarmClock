# Spotify Alarm Clock _and music player_
spotifyAlarmClock is well... An alarm clock! I really wanted some sort of stationary music player, but since I almost exclusively use Spotify for all of my music needs I had my options limited to only a few (quite expensive) speakers, and since I'm already making something that plays music, why don't I just code it to press "play" at a specific time?

Built using Raspberry Pi Zero W, 16x2 hd44780 compatible screen and a couple of buttons.

```play-pause``` executable is my fork of [Spotcontrol](https://github.com/badfortrains/spotcontrol) and it will soon be made public.
### TODO:
- [ ] Tutorial on how to set it up
- [ ] Fix Python 3 compatibility

### Basic functionality:
- [x] Spotify Connect (via [Librespot](https://github.com/plietar/librespot))
- [x] 16x2 display with song title, artist, date and time
- [x] Playing music at specified, hardcoded time
- [x] Play/Pause/Next buttons
- [ ] Auto start on boot
### Additional functionality:
- [ ] Previous button
- [ ] Photoresistor for auto screen brightness
- [ ] Possibility of setting alarms using 16x2 screen
- [ ] Possibility of choosing an alarm album (from a list of user albums) using 16x2 screen
- [ ] Web interface for login and alarm management
