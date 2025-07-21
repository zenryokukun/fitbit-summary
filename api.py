"""
Fitbit Web APIを実行してくれるスクリプト
URL: https://dev.fitbit.com/build/reference/web-api/
"""

from pprint import pprint
from pathlib import Path
import json
from typing import Dict, List, TypedDict, Union
from requests import Session


class Conf(TypedDict):
    """conf.jsonの型"""
    client_id: str
    client_secret: str
    access_token: str
    refresh_token: str
    user_id: str
    scope: str
    redirect_url: str


# トークン等の重要ファイル
CONF_FILEPATH = Path(__file__).parent / "conf.json"

# 重要ファイルから読み取る
conf: Union[Conf, None] = None
with open(CONF_FILEPATH, "r", encoding="utf-8") as f:
    _conf: Conf = json.load(f)
    conf = _conf

# セッション
session = Session()


def bearer_header():
    """Bearer認証用ヘッダ
    Returns:
        dict: {"Authorization":str}
    """
    return {"Authorization": "Bearer " + conf["access_token"]}


def is_expired(resObj: Dict[str, List[Dict[str, str]]]) -> bool:
    """
    Responseから、accesss-tokenが失効しているかチェックする。
    失効ならTrue、失効していなければFalse。Fitbit APIでは8時間が寿命。
    Args:
        reqObj (_type_): response.json()したもの

    Returns:
        boolean: 失効ならTrue、失効していなければFalse。Fitbit APIでは8時間が寿命。
    """

    errors = resObj.get("errors")

    # エラーなし。
    if errors is None:
        return False

    # エラーあり
    for err in errors:
        etype = err.get("errorType")
        if (etype is None):
            continue
        if etype == "expired_token":
            print("TOKEN_EXPIRED!!!")
            return True

    # 失効していないのでFalse。エラーありだが、ここでは制御しない。
    return False


def refresh() -> None:
    """access_tokenを再取得し、conf.jsonを更新する。refresh_tokenはaccess_tokenの再取得に必要なので重要。
    is_expiredがTrueの時のみ呼ぶ。False時に呼んでも、一式更新される。実害はない。
    """
    if conf is None:
        return

    url = "https://api.fitbit.com/oauth2/token"

    # client typeのようなので、Basic認証は不要
    headers = {
        # "Authorization": "Basic " + str(basic),
        "Accept": "application/json",
    }

    # client typeのようなのでclient_idが必要
    params = {
        "grant_type": "refresh_token",
        "refresh_token": conf["refresh_token"],
        "client_id": conf["client_id"],
    }

    # POST Body部はapplication/x-www-form-urlencoded。requestsならContent-Type不要。
    res = session.post(url, headers=headers, data=params)
    res_data = res.json()

    # errorあり
    if res_data.get("errors") is not None:
        emsg = res_data["errors"][0]
        pprint(emsg)
        return

    pprint(res_data)
    # errorなし
    # confを更新し、ファイルを更新
    if conf["access_token"] == res_data["access_token"]:
        print("access token was not updated! -> ", conf["access_token"])
        return

    conf["access_token"] = res_data["access_token"]
    conf["refresh_token"] = res_data["refresh_token"]
    conf["scope"] = res_data["scope"]
    conf["user_id"] = res_data["user_id"]

    with open(CONF_FILEPATH, "w", encoding="utf-8") as f:
        json.dump(conf, f, indent=2)


def request(method, url, **kw):
    """sessionを通してリクエストを実行する関数。アクセストークンが8Hで失効するため、
    失効時は再取得し、リクエストを再実行する。レスポンスはパースしないので、呼ぶ側で.json()なり
    .text()なりすること。

    Args:
        method (_type_): session.get,session.post...等
        url (_type_): エンドポイント
        **kw: headers={},params={}を想定

    Returns:
        session.Response: レスポンス
    """
    res = method(url, **kw)
    res_data = res.json()
    if is_expired(res_data):
        # トークンを更新する
        refresh()
        # headersに設定されているトークンも古いので書き換える。
        kw["headers"] = bearer_header()
        res = method(url, **kw)
    # parseしていないほうを返す
    return res


# def heartbeat(date: str = "today", period: str = "1d"):
#     """心拍数を取得しレスポンスを返す。パースはしない。

#     Args:
#         date (str, optional): 取得する日付。yyyy-mm-ddで指定も可能。Defaults to "today".
#         period (str, optional): 取得する範囲。1d,7d,30d,1w,1m。 Defaults to "1d".

#     Returns:
#         session.Response: レスポンス
#     """
#     url = "https://api.fitbit.com/1/user/-/activities/heart/date/"\
#         f"{date}/{period}.json"

#     headers = bearer_header()
#     res = request(session.get, url, headers=headers)
#     return res


def breath_rate(date: str = "today"):
    """呼吸レート。まだデータ溜まってない模様。

    Args:
        date (str, optional): 取得する日付。yyyy-mm-ddで指定も可能。Defaults to "today".

    Returns:
        session.Response: レスポンス
    """
    url = f"https://api.fitbit.com/1/user/-/br/date/{date}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res


def sleep_log(date: str = "today"):
    """睡眠情報

    Args:
        date (str, optional): 取得する日付。yyyy-mm-ddで指定も可能。Defaults to "today".

    Returns:
        session.Response: レスポンス
    """
    url = f"https://api.fitbit.com/1.2/user/-/sleep/date/{date}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res


def spo2_summary(date: str = "today"):
    """血中酸素濃度のサマリ

    Args:
        date (str, optional): 取得する日付。yyyy-mm-ddで指定も可能。Defaults to "today".

    Returns:
        session.Response: レスポンス
    """
    url = f"https://api.fitbit.com/1/user/-/spo2/date/{date}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res


def spo2_intraday(date: str = "today"):
    """血中酸素濃度の詳細版

    Args:
        date (str, optional): 取得する日付。yyyy-mm-ddで指定も可能。Defaults to "today".

    Returns:
        session.Response: レスポンス
    """
    url = f"https://api.fitbit.com/1/user/-/spo2/date/{date}/all.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res


def skin_temperature(date: str = "today"):
    """皮膚温度

    Args:
        date (str, optional): 取得する日付。yyyy-mm-ddで指定も可能。Defaults to "today".

    Returns:
        session.Response: レスポンス
    """
    url = f"https://api.fitbit.com/1/user/-/temp/skin/date/{date}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res


def core_temperature(date: str = "today"):
    """コア温度

    Args:
        date (str, optional): 取得する日付。yyyy-mm-ddで指定も可能。Defaults to "today".

    Returns:
        session.Response: レスポンス
    """
    url = f"https://api.fitbit.com/1/user/-/temp/core/date/{date}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res


def activity_summary(date: str = "today"):
    """Activityのサマリ

    Args:
        date (str, optional): 取得する日付。yyyy-mm-ddで指定も可能。Defaults to "today".

    Returns:
        session.Response: レスポンス
    """
    url = f"https://api.fitbit.com/1/user/-/activities/date/{date}.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res


def heart_intraday(date:str = "today"):
    """_心拍数をグラフ化するために必要
    参考
    https://dev.fitbit.com/build/reference/web-api/intraday/get-heartrate-intraday-by-date/
    Args:
        date (str, optional): _description_. Defaults to "today".

    Returns:
        _type_: _description_
    """
    url = f"https://api.fitbit.com/1/user/-/activities/heart/date/{date}/1d/1min.json"
    headers = bearer_header()
    res = request(session.get, url, headers=headers)
    return res