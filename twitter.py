"""
Twitterに投稿するスクリプト。tweet(msg:str,*img_paths)。
"""

from requests_oauthlib import OAuth1Session as session
import json
from pathlib import Path


# ツイート用URL
URL = "https://api.twitter.com/1.1/statuses/update.json"
# 画像アップロードURL
URL_IMAGE = "https://upload.twitter.com/1.1/media/upload.json"
# Confidentialファイルパス
CONF_FILEPATH = Path(__file__).parent / "twitter_conf.json"
# Confを読み取り、reqを設定。reqはリクエストを投げるオブジェクト
with open(CONF_FILEPATH, "r", encoding="utf-8") as f:
    cf = json.load(f)
    req = session(cf["API_KEY"], cf["API_SECRET"],
                  cf["ACCESS_TOKEN"], cf["ACCESS_SECRET"])
# ツイートにつけるtag
TAGS = "#Fitbit #Fitbit_Web_API #Fitbitはサードパーティアプリを解放しろ"


def tweet_image(*img_paths):
    """画像をアップロードし、media_idを返す。アップロードのみでツイートはされないので注意。
    ツイートに添付するには、media_idを付けてURLのエンドポイントにPOSTする必要がある。

    Args:
        img_paths (List(str|pathlib.Path)) : 画像のパス（文字列かpathlib.Pathオブジェクト）

    Returns:
        str: media_ids。複数ある場合はカンマで区切られた文字列
    """
    media_ids = []
    for img in img_paths:
        params = {"media": open(img, "rb")}
        data = {"media_category": "tweet_image"}
        res = req.post(URL_IMAGE, files=params, data=data)

        if res.status_code != 200:
            print(f"error at {img}:{res.json()}")
            continue

        res_data = res.json()
        media_ids.append(res_data["media_id"])

    media_ids_str = ",".join([str(m) for m in media_ids])
    return media_ids_str


def tweet(msg: str, *img_paths):
    """tweetする。img_pathsで指定した画像を添付してmsgをツイートする

    Args:
        msg (str): ツイートする文字列
        img_paths (List(str|pathlib.Path)) : 画像のパス（文字列かpathlib.Pathオブジェクト）
    """
    media_ids = tweet_image(*img_paths)
    txt = msg + "\n" + TAGS

    params = {"status": txt}

    if len(media_ids) > 0:
        params["media_ids"] = media_ids

    res = req.post(URL, params=params)

    if res.status_code != 200:
        print("tweet func went something wrong!")
        print(res.json())
