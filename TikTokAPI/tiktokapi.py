import string
import random
import urllib.parse
from .utils import random_key, build_get_url, get_req_json, get_req_content, get_req_text
from .tiktok_browser import TikTokBrowser

class VideoException(Exception):
    pass

class TikTokAPI(object):

    def __init__(self, cookie=None, language='en', browser_lang="en-US", timezone="Asia/Kolkata", region='IN'):
        self.base_url = "https://t.tiktok.com/api"
        self.user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"

        if cookie is None:
            cookie = {}
        self.verifyFp = cookie.get("s_v_web_id", "verify_kjf974fd_y7bupmR0_3uRm_43kF_Awde_8K95qt0GcpBk")
        self.ttwid = cookie.get("ttwid", "1%7CfvPor4KL6zARY23Vxpqt88YEVxh5mate7Sv36qwlJxo%7C1660564559%7C2991d1723358a295ff7511761a9fc114086e1de75cafa2ae60211fe7e6e4a0e8")
        self.sessionid = cookie.get("sessionid", "7e6e4b74e3e3ccfb64718964775aa9f6")

        self.headers = {
            'Host': 't.tiktok.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Referer': 'https://www.tiktok.com/',
            'Cookie': 'ttwid={}; sessionid={}; s_v_web_id={}'.format(self.ttwid, self.sessionid, self.verifyFp),
        }
        self.language = language
        self.browser_lang = browser_lang
        self.timezone = timezone
        self.region = region

        self.default_params = {
            "aid": "1988",
            "app_name": "tiktok_web",
            "device_platform": "web",
            "referer": "",
            "user_agent": urllib.parse.quote_plus(self.user_agent),
            "cookie_enabled": "true",
            "screen_width": "1920",
            "screen_height": "1080",
            "browser_language": self.browser_lang,
            "browser_platform": "Linux+x86_64",
            "browser_name": "Mozilla",
            "browser_version": "5.0+(X11)",
            "browser_online": "true",
            "timezone_name": self.timezone,
            # "page_referer": "https://www.tiktok.com/foryou?lang=en",
            "priority_region": self.region,

            "appId": "1180",
            "region": self.region,
            "appType": "t",

            "isAndroid": "false",
            "isMobile": "false",
            "isIOS": "false",
            "OS": "linux",
            "tt-web-region": self.region,

            "language": self.language,
            "verifyFp": self.verifyFp
        }
        self.signature_key = "_signature"
        self.did_key = "did"
        self.tiktok_browser = TikTokBrowser(self.user_agent)

    def send_get_request(self, url, params, extra_headers=None):
        url = build_get_url(url, params)
        did = ''.join(random.choice(string.digits) for num in range(19))
        url = build_get_url(url, {self.did_key: did}, append=True)
        signature = self.tiktok_browser.fetch_auth_params(url, language=self.language)
        url = build_get_url(url, {self.signature_key: signature}, append=True)
        if extra_headers is None:
            headers = self.headers
        else:
            headers = {}
            for key, val in extra_headers.items():
                headers[key] = val
            for key, val in self.headers.items():
                headers[key] = val
        data = get_req_json(url, params=None, headers=self.headers)
        return data

    def getTrending(self, count=30, cursor=0):
        url = self.base_url + "/recommend/item_list/"
        req_default_params = {
            "id": "1",
            "type": "5",
            "secUid": "",
            "sourceType": "12",
            "cursor": str(cursor)
        }
        params = {
            "count": str(count)
        }
        for key, val in req_default_params.items():
            params[key] = val
        for key, val in self.default_params.items():
            params[key] = val
        return self.send_get_request(url, params)

    def getUserByName(self, user_name):
        url = "https://t.tiktok.com/node/share/user/@" + user_name
        params = {
            "uniqueId": user_name,
            "validUniqueId": user_name,
        }
        for key, val in self.default_params.items():
            params[key] = val
        return self.send_get_request(url, params)

    def getVideosByUserName(self, user_name, count=30, cursor=0):
        user_data = self.getUserByName(user_name)
        user_obj = user_data["userInfo"]["user"]
        user_id = user_obj["id"]
        secUid = user_obj["secUid"]

        url = self.base_url + "/post/item_list/"
        req_default_params = {
            "type": "1",
            "sourceType": "8",
            "cursor": str(cursor)
        }
        params = {
            "id": user_id,
            "secUid": secUid,
            "count": str(count)
        }
        for key, val in req_default_params.items():
            params[key] = val
        for key, val in self.default_params.items():
            params[key] = val
        return self.send_get_request(url, params)

    def getLikesByUserName(self, user_name, count=30, cursor=0):
        user_data = self.getUserByName(user_name)
        user_obj = user_data["userInfo"]["user"]
        user_id = user_obj["id"]
        secUid = user_obj["secUid"]

        url = self.base_url + "/favorite/item_list/"
        req_default_params = {
            "type": "2",
            "sourceType": "9",
            "cursor": str(cursor)
        }
        params = {
            "id": user_id,
            "secUid": secUid,
            "count": str(count)
        }
        for key, val in req_default_params.items():
            params[key] = val
        for key, val in self.default_params.items():
            params[key] = val
        return self.send_get_request(url, params)

    def getHashTag(self, hashTag):
        url = self.base_url + "/challenge/detail/"
        params = {
            "challengeName": hashTag.replace("#", "")
        }
        for key, val in self.default_params.items():
            params[key] = val
        return self.send_get_request(url, params)

    def searchHashtags(self, query: str, count: int):
        url = "https://api2.musical.ly/aweme/v1/search/sug/"
        params = {
            "keyword": query.replace("#", ""),
            "count": str(count),
        }
        for key, val in self.default_params.items():
            params[key] = val
        return self.send_get_request(url, params)

    def getVideosByHashtags(self, hashtags: list[str], cursor: int):
        url = self.base_url + "/search/general/full/"
        req_default_params = {
            "secUid": "",
            "type": "3",
            "minCursor": "0",
            "maxCursor": "0",
            "shareUid": "",
            "recType": ""
        }
        params = {
            "keyword": "%20".join(list("%23" + tag.replace(" ", "%20") for tag in hashtags)),
            "cursor": str(cursor)
        }
        for key, val in req_default_params.items():
            params[key] = val
        for key, val in self.default_params.items():
            params[key] = val

        return self.send_get_request(url, params)

    def getVideosByHashTag(self, hashTag, count=30):
        hashTag = hashTag.replace("#", "")
        hashTag_obj = self.getHashTag(hashTag)
        hashTag_id = hashTag_obj["challengeInfo"]["challenge"]["id"]
        url = self.base_url + "/challenge/item_list/"
        req_default_params = {
            "secUid": "",
            "type": "3",
            "minCursor": "0",
            "maxCursor": "0",
            "shareUid": "",
            "recType": ""
        }
        params = {
            "challengeID": str(hashTag_id),
            "count": str(count),
            "cursor": "0",
        }
        for key, val in req_default_params.items():
            params[key] = val
        for key, val in self.default_params.items():
            params[key] = val
        extra_headers = {"Referer": "https://www.tiktok.com/tag/" + str(hashTag)}
        return self.send_get_request(url, params, extra_headers=extra_headers)

    def getMusic(self, music_id):
        url = self.base_url + "/music/detail/"
        params = {
            "musicId": music_id
        }
        for key, val in self.default_params.items():
            params[key] = val
        return self.send_get_request(url, params)

    def getVideosByMusic(self, music_id, count=30):
        url = self.base_url + "/music/item_list/"
        req_default_params = {
            "secUid": "",
            "type": "4",
            "minCursor": "0",
            "maxCursor": "0",
            "shareUid": "",
            "recType": ""
        }
        params = {
            "musicID": str(music_id),
            "count": str(count),
            "cursor": "0",
        }
        for key, val in req_default_params.items():
            params[key] = val
        for key, val in self.default_params.items():
            params[key] = val
        extra_headers = {"Referer": "https://www.tiktok.com/music/original-sound-" + str(music_id)}
        return self.send_get_request(url, params, extra_headers=extra_headers)

    def getVideoById(self, video_id):
        url = self.base_url + "/item/detail/"
        params = {
            "itemId": str(video_id)
        }
        for key, val in self.default_params.items():
            params[key] = val
        return self.send_get_request(url, params)

    def downloadVideoById(self, video_id, save=True, save_path=None):
        video_info = self.getVideoById(video_id)
        video_url = video_info["itemInfo"]["itemStruct"]["video"]["playAddr"]
        video_data = get_req_content(video_url, params=None, headers=self.headers)
        
        if (save and save_path is not None):
            with open(save_path, 'wb') as f:
                f.write(video_data)
        else:
            return video_data
    
    def downloadVideoByUrl(self, video_url, save=True, save_path=None):
        video_data = get_req_content(video_url, params=None, headers=self.headers)
        
        if (save and save_path is not None):
            with open(save_path, 'wb') as f:
                f.write(video_data)
        else:
            return video_data
    
    def downloadImageByUrl(self, url, save=True, save_path=None):
        image_data = get_req_content(url, params=None, headers=self.headers)
        
        if (save and save_path is not None):
            with open(save_path, 'wb') as f:
                f.write(image_data)
        else:
            return image_data

    def downloadVideoByIdNoWatermark(self, video_id, save_path):
        video_info = self.getVideoById(video_id)
        video_url = video_info["itemInfo"]["itemStruct"]["video"]["downloadAddr"]
        video_data = get_req_text(video_url, params=None, headers=self.headers)
        pos = video_data.find("vid:")
        if pos == -1:
            raise VideoException("Video without watermark not available in new videos")
        video_url_no_wm = "https://api2-16-h2.musical.ly/aweme/v1/play/?video_id={" \
                          "}&vr_type=0&is_play_url=1&source=PackSourceEnum_PUBLISH&media_type=4" \
            .format(video_data[pos + 4:pos + 36])

        video_data_no_wm = get_req_content(video_url_no_wm, params=None, headers=self.headers)
        with open(save_path, 'wb') as f:
            f.write(video_data_no_wm)
