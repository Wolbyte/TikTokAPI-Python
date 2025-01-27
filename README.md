
# Unofficial TikTok API Wrapper in Python

This is an unofficial TikTok Api python wrapper. I have an App using this API, and thus will constantly keep updating this wrapper  
This implementation is inspired by [TikTokApi](https://github.com/davidteather/TikTok-Api/), but runs faster.  


## Table of Contents
- [Getting Started](#getting-started)
    - [Installing](#installing)
- [Quick Start Guide](#quick-start-guide)
- [Detailed Documentation](#detailed-documentation)
    - [Methods](#methods)
        - [TikTok Class](#tiktok-class)
        - [Get Trending Videos](#get-trending-videos)
        - [Get User](#get-user)
        - [Get Videos By UserName](#get-videos-by-username)
        - [Get Likes By UserName](#get-likes-by-username)
        - [Get HashTag](#get-hashtag)
        - [Get Videos By HashTag](#get-videos-by-hashtag)
        - [Get Music](#get-music)
        - [Get Videos By Music](#get-videos-by-music)
        - [Get Video By Id](#get-video-by-id)
        - [Download Video](#download-video)
        - [Download Video no Watermark](#download-video-no-watermark)
- [Built With](#built-with)
- [Authors](#authors)
- [License](#license)

## Getting Started

To get started using this API, follow the instructions below.

### Installing
Pip
```
pip install PyTikTokAPI
```

Install from source
```
git clone https://github.com/avilash/TikTokAPI-Python.git
python setup.py install
```

## Quick Start Guide
Import
```
from TikTokAPI import TikTokAPI
```
Get your keys from Cookie. You can get them from the Applications tab in Chrome developer console.  
By default it used hardcoded values which may not work after some time.  
The keys to extract are `s_v_web_id` and `sid_ucp_v1`
```
cookie = {
  "s_v_web_id": "<your_key>",
  "sid_ucp_v1": "<your_key>"
}
```
Get the most trending Videos on TikTok
```
api = TikTokAPI(cookie=cookie)
retval = api.getTrending(count=5)
```
Get a user by name
```
api = TikTokAPI(cookie=cookie)
user_obj = api.getUserByName("fcbarcelona")
```
Get videos of a user
```
api = TikTokAPI(cookie=cookie)
user_videos = api.getVideosByUserName("fcbarcelona")
```
Get likes of a user
```
api = TikTokAPI(cookie=cookie)
user_videos = api.getLikesByUserName("fcbarcelona")
```

## Detailed Documentation
This section contains details about the parameters of each function and what it returns

### Methods

#### Tiktok Class
Inputs
* language - Self explanatory
* region - Self explanatory
* cookie - The TikTok Cookie containing the parameter <em>s_v_web_id</em>. If not provided, the parameter will be generated.

```buildoutcfg
__init__(self, language='en', region='IN', cookie=None)
```

#### Get Trending Videos
Inputs
* count - Number of videos to fetch  

```buildoutcfg
getTrending(self, count=30)
```

#### Get User
Inputs
* user_name - Username, eg - <em>fcbarcelona</em>

```buildoutcfg
getUserByName(self, user_name)
```

#### Get Videos By Username
Inputs
* user_name - Username, eg - <em>fcbarcelona</em>
* count - Number of videos to fetch

```buildoutcfg
getVideosByUserName(self, user_name, count=30)
```

#### Get Likes By Username
Inputs
* user_name - Username, eg - <em>fcbarcelona</em>
* count - Number of videos to fetch

```buildoutcfg
getLikesByUserName(self, user_name, count=30)
```

#### Get Hashtag
Inputs
* hashTag - HashTag, eg - <em>#fcbarcelona</em>

```buildoutcfg
getHashTag(self, hashTag)
```

#### Get Videos By Hashtag
Inputs
* hashTag - HashTag, eg - <em>#fcbarcelona</em>
* count - Number of videos to fetch

```buildoutcfg
getVideosByHashTag(self, hashTag, count=30)
```

#### Get Music
Inputs
* music_id - Music Id, eg - <em>6704854531001289474</em>

```buildoutcfg
getMusic(self, music_id)
```

#### Get Videos By Music
Inputs
* music_id - Music Id, eg - <em>6704854531001289474</em>
* count - Number of videos to fetch

```buildoutcfg
getVideosByMusic(self, music_id, count=30)
```

#### Get Video By Id
Inputs
* video_id - Video Id, eg - <em>6843481669886954757</em>

```buildoutcfg
getVideoById(self, video_id)
```

#### Download Video
Inputs
* video_id - Video Id, eg - <em>6843481669886954757</em>
* save_path - Path where the downloaded video should be saved

```buildoutcfg
downloadVideoById(self, video_id, save_path)
```

#### Download Video No Watermark
Inputs
* video_id - Video Id, eg - <em>6843481669886954757</em>
* save_path - Path where the downloaded video should be saved

```buildoutcfg
downloadVideoByIdNoWatermark(self, video_id, save_path)
```

## Built With

* [Python 3.7](https://www.python.org/)

## Authors

* **Avilash Kumar** - [avilash](https://github.com/avilash)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

[![Run on Repl.it](https://repl.it/badge/github/avilash/TikTokAPI-Python)](https://repl.it/github/avilash/TikTokAPI-Python)
