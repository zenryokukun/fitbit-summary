"""
Tweet用の画像を出力するスクリプト

graph_heartbeat() -> 心拍数をグラフ化 heart.png
graph_heart_spo() -> 心拍数とSpO2をsubplotでグラフ化 heart-spo.png
"""

import matplotlib.pyplot as plt
import json
import datetime

plt.rcParams["text.color"] = "white"
plt.rcParams['axes.labelcolor'] = "white"
plt.rcParams['xtick.color'] = "white"
plt.rcParams['ytick.color'] = "white"


def full_date(ymd: str, hms: str) -> datetime.datetime:
    dstr = ymd + " " + hms
    dobj = datetime.datetime.strptime(dstr, "%Y-%m-%d %H:%M:%S")
    return dobj


def graph_heartbeat(data):
    """Web API `Heart Rate Time Series by Date`の
    パース済レスポンスをグラフ化。

    Args:
        data (dict): パース済レスポンス
    """
    # YYYY-MM-DD
    ymd = data["activities-heart"][0]["dateTime"]
    # [{"time":"HH:MM:SS","value":int}]
    beats = data["activities-heart-intraday"]["dataset"]

    # X軸とY軸データを抽出。Ｘ軸はdatetimeオブジェクトだと
    # ラベルを間引いて表示してくれるため、文字列→datetimeに変換
    X = [full_date(ymd, d["time"]) for d in beats]
    Y = [d["value"] for d in beats]

    fig = plt.figure(facecolor=((0.2, 0.2, 0.2)))
    ax = fig.add_subplot(111)
    ax.set_facecolor((0.1, 0.1, 0.1))
    ax.set_title("Z-HEART-BEAT")
    ax.set_xlabel("TIME")
    ax.set_ylabel("Beat-Per-Second")
    ax.plot(X, Y, color="red")

    ax.ticklabel_format(style="plain", axis="y")
    plt.grid(color="white")  # グリッドを表示
    plt.gcf().autofmt_xdate()  # 日付を縦表記にする
    plt.tight_layout()  # ラベルが見切れるの防止するために必要
    # plt.show()
    plt.savefig("heart.png")


def graph_heart_spo(heart, spo):
    """Web API `Heart Rate Time Series by Date`と
     `Get SpO2 Intraday by Date`のパース済レスポンスをグラフ化
    パース済レスポンスをグラフ化。

    Args:
        heart (dict): HeartRate パース済レスポンス
        spo (dict): SPO2 Intraday パース済レスポンス
    """
    rot = 15
    fig = plt.figure(facecolor=((0.2, 0.2, 0.2)), figsize=(8, 6))

    # YYYY-MM-DD
    ymd = heart["activities-heart"][0]["dateTime"]
    # [{"time":"HH:MM:SS","value":int}]
    beats = heart["activities-heart-intraday"]["dataset"]

    # X軸とY軸データを抽出。Ｘ軸はdatetimeオブジェクトだと
    # ラベルを間引いて表示してくれるため、文字列→datetimeに変換
    X = [full_date(ymd, d["time"]) for d in beats]
    Y = [d["value"] for d in beats]

    ax = fig.add_subplot(211)
    ax.set_facecolor((0.1, 0.1, 0.1))
    ax.set_title("Z-Heart-Beat")
    ax.set_xlabel("TIME")
    ax.set_ylabel("Beat-Per-Minute")
    ax.plot(X, Y, color="red")
    # ax2.ticklabel_format(style="plain", axis="y")
    ax.grid(color="white")  # グリッドを表示
    # plt.gcf().autofmt_xdate()  # 日付を縦表記にする
    plt.xticks(rotation=rot)
    plt.tight_layout()  # ラベルが見切れるの防止するために必要

    minutes = spo["minutes"]
    X2 = [datetime.datetime.strptime(
        d["minute"], "%Y-%m-%dT%H:%M:%S") for d in minutes]
    Y2 = [d["value"] for d in minutes]
    ax2 = fig.add_subplot(212)
    ax2.set_facecolor((0.1, 0.1, 0.1))
    ax2.set_title("Z-SpO2")
    ax2.set_xlabel("TIME")
    ax2.set_ylabel("SpO2")
    ax2.plot(X2, Y2, color="turquoise")
    ax2.ticklabel_format(style="plain", axis="y")
    ax2.grid(color="white")  # グリッドを表示
    plt.xticks(rotation=rot)
    plt.tight_layout()

    plt.savefig("heart-spo.png")


if __name__ == "__main__":
    with open("test_spo.json", "r") as f:
        spo = json.load(f)

    with open("test_heartbeat.json", "r") as f:
        heart = json.load(f)

    graph_heart_spo(heart, spo)
