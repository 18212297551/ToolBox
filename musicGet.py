import re

import requests, json
a= """type
含义
ng
单曲
ly
歌词
comments评论
detail
歌曲详情
artist
歌手
album
专辑
playlist
歌单
my
MV
dj
radio
主播电台
dj
主播电台单曲id
detail_di主播电台歌曲详情
search
搜索"""

GTYPE = {
    "单曲":'ng',
    '歌词':'ly', '评论': 'comments', '歌曲详情': 'detail', '歌手': 'artist', '专辑': 'album', '歌单': 'playlist',
    "MV": 'mv', '主播电台': 'radio', '主播电台单曲id': 'dj', '主播电台歌曲详情': 'detail_di', '搜索': 'search'

}

def get_music_info(bk, bv):
    """获取音乐信息"""
    __url = 'https://api.imjad.cn/cloudmusic/?type={}&id={}'.format(GTYPE.get(bk), bv)
    __result = requests.get(__url)
    __content = __result.content
    return json.loads(__content)

def get_musicId_from_playlist(plist):
    mids = plist['playlist']["tracks"]
    print(len(mids))
    for mid in mids:
        _id = mid.get('id')
        name = mid.get('name')
        music = get_music_info('单曲', _id)
        __url = music['data'][0].get('url')
        if __url:
            music_download_by_url(__url, name)
        # print(music)

def music_download_by_url(_url, name=None):
    name = re.sub('[,|，|\s|\"|\'|:|：|；|;]', '', name)
    print('正在下载->{0}'.format(name))
    result = requests.get(_url)
    with open("./Temp/{}.mp3".format(name), 'wb') as f:
        f.write(result.content)

def test():
    _url = 'http://api.lostg.com/music/163/3779629'
    res = requests.get(_url)
    print(res)
    print(json.loads(res.content))

test()
# infos = get_music_info('歌单',3779629)
# get_musicId_from_playlist(infos)
# print(infos['playlist']["tracks"])