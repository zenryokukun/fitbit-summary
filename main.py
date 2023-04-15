"""
Fitbit APIで心拍、アクティビティ、睡眠、SPO2情報を取得。
グラフ化してtwitterに投稿する。
ex: main()
"""
import datetime
from graph import graph_heart_spo
from pytweet import Pytweet
from api import heartbeat, spo2_intraday, activity_summary, sleep_log
from consts import TWEET_IMAGE, TWITTER

TAGS = "#Fitbit #Fitbit_Web_API #Fitbitはサードパーティアプリを解放しろ"


def min_to_hr(t: int) -> str:
    """XX(分)→〇時館△分に変換

    Args:
        t (int): 分

    Returns:
        str: 〇時館△分
    """
    hr = t // 60
    m = t % 60
    if hr == 0:
        return str(m) + "分"
    return str(hr) + "時間" + str(m) + "分"


def today() -> str:
    """本日の日付を返す。

    Returns:
        str: YYYY-MM-DD
    """
    now = datetime.datetime.now()
    return f"{now.year}-{now.month}-{now.day}"


def main():
    """main処理
    Fitbit APIで心拍、アクティビティ、睡眠、SPO2情報を取得。
    グラフ化してtwitterに投稿
    """
    # データ取得
    heart = heartbeat().json()
    spo = spo2_intraday().json()
    sleep = sleep_log().json()
    act = activity_summary().json()

    # データ取得にエラーが無いかチェック
    is_error = heart.get("errors") is not None \
        or spo.get("errors") is not None \
        or sleep.get("errors") is not None \
        or act.get("errors") is not None

    # error時はerrorツイートをして終了
    if is_error:
        msg = "Googleよ！インターネットの世界を牛耳り、世界を自分たちの手中に納めたつもりでいられるのも今のうちだ！"\
            "前世紀の巨人があなたを倒さんと、再び立ち上がったのだ！"\
            "「F I T B I T を 解 放 し ろ !」聞こえるか、MSの咆哮が！\n"
        msg += TAGS
        twitter = Pytweet(TWITTER)
        twitter.tweet(msg)
        return

    # 歩数、フロア数、カロリーをactivityから取得
    act_summary = act["summary"]
    steps = act_summary["steps"]
    floors = act_summary["floors"]
    calories = act_summary["caloriesOut"]

    # 睡眠情報をsleepから取得
    sleep_summary = sleep["summary"]
    bed_time = sleep_summary["totalTimeInBed"]
    deep = sleep_summary["stages"]["deep"]
    light = sleep_summary["stages"]["light"]
    rem = sleep_summary["stages"]["rem"]
    wake = sleep_summary["stages"]["wake"]

    # 上記からメッセージを生成
    msg = "💛全力君・絶望の鼓動(Heart-Beat)💛\n"
    msg += "[" + today() + "]" + "\n"
    msg += "👟運動情報👟\n"
    msg += "歩数: " + str(steps) + "\n"
    msg += "昇ったフロア数: " + str(floors) + "\n"
    msg += "消費cal: " + str(calories) + "\n"
    msg += "💤睡眠情報💤\n"
    msg += "ベッド時間: " + min_to_hr(bed_time) + "\n"
    msg += "深い睡眠: " + min_to_hr(deep) + "\n"
    msg += "浅い睡眠: " + min_to_hr(light) + "\n"
    msg += "レム睡眠: " + min_to_hr(rem) + "\n"
    msg += "覚醒: " + min_to_hr(wake) + "\n"
    msg += TAGS + "\n"
    # グラフ生成(heart-spo.pngが出力される)
    graph_heart_spo(heart, spo, sleep, TWEET_IMAGE)

    # tweetする
    # tweet(msg, TWEET_IMAGE)
    twitter = Pytweet(TWITTER)
    twitter.tweet(msg, TWEET_IMAGE)


main()
