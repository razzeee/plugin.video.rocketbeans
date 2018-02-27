# -*- coding: utf-8 -*-

import routing

from resources.data import config
from resources.lib.guide import show_guide
from resources.lib.youtube import YoutubeStream
from resources.lib.twitch import TwitchStream
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setContent
from xbmcaddon import Addon


plugin = routing.Plugin()
setContent(plugin.handle, 'videos')

livestream_thumbnail = None
livestream_url = None

def get_livestream():
    if Addon().getSetting("stream") == "Twitch":
        t = TwitchStream(config.TWITCH_USER_LOGIN)
        livestream_url, title, livestream_thumbnail = t.url, t.title, t.thumbnail
    else:
        livestream_url, title, livestream_thumbnail = YoutubeStream().get_live_video_info_from_channel_id(config.CHANNEL_ID)
    return livestream_url, livestream_thumbnail, title

@plugin.route('/')
def index():
    livestream_url, livestream_thumbnail, title = get_livestream()
    li = createListItem(
        ('Live | %s' % title),
        livestream_thumbnail,
        True,
        'The live stream.',
        0
    )
    addDirectoryItem(
        plugin.handle,
        livestream_url,
        li
    )

    url = "plugin://plugin.video.youtube/user/%s/" % config.CHANNEL_ID
    addDirectoryItem(
        plugin.handle,
        url,
        ListItem('Mediathek'),
        True
    )

    url = "plugin://plugin.video.youtube/channel/%s/" % config.LETS_PLAY_CHANNEL_ID
    addDirectoryItem(
        plugin.handle, 
        url, 
        ListItem('Gaming Mediathek'),
        True
    )

    addDirectoryItem(
        plugin.handle,
        "plugin://plugin.video.youtube/channel/%s/" % config.GAME_TWO_CHANNEL_ID,
        ListItem("Game-Two-Mediathek"),
        True 
    )

    addDirectoryItem(
        plugin.handle,
        "plugin://plugin.video.twitch/?mode=channel_video_list&broadcast_type=upload&channel_id=%s" %(config.TWITCH_CHANNEL_ID),
        ListItem("Mediathek auf Twitch"),
        True
    )

    addDirectoryItem(
        plugin.handle,
        plugin.url_for(guide),
        ListItem('Sendeplan'),
        True
    )

    endOfDirectory(plugin.handle)


@plugin.route('/guide')
def guide():
    guide_items = show_guide()

    for guide_item in guide_items:
        title, video_id, duration, game, is_live_now = guide_item
        if video_id:
            url = "plugin://plugin.video.youtube/play/?video_id=%s" % video_id
            thumbnail = "https://i.ytimg.com/vi/%s/hqdefault.jpg" % (
                video_id)

            li = createListItem(
                title,
                thumbnail,
                True,
                '[B]Game[/B]: ' + game if game else '',
                duration
            )
            addDirectoryItem(
                plugin.handle,
                url,
                li
            )
        else:
            if is_live_now:
                livestream_url, livestream_thumbnail, _ = get_livestream()
                li = createListItem(
                    title,
                    livestream_thumbnail,
                    True,
                    'The live stream.',
                    0
                )
                addDirectoryItem(
                    plugin.handle,
                    livestream_url,
                    li
                )
            else:
                li = createListItem(
                    title,
                    '',
                    False,
                    '',
                    0
                )
                addDirectoryItem(
                    plugin.handle,
                    '',
                    li
                )
    endOfDirectory(plugin.handle)

def createListItem(label, thumbnailImage, isPlayable, plot, duration):
    li = ListItem(
        label=label,
        thumbnailImage=thumbnailImage
    )
        
    if isPlayable:
        infoLabels = {}
        infoLabels['plot'] = plot

        if duration > 0:
            infoLabels['duration'] = duration

        li.setInfo(type=u'video', infoLabels=infoLabels)
        li.setProperty('isPlayable', 'true')

    return li

def run():
    plugin.run()
