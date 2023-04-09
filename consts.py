"""
Twitter認証ファイル、投稿する画像ファイルのフルパス。
cronで実行する（プロジェクトのルートフォルダから実行しない）ため、
絶対パスにする必要がある。
"""

from pathlib import Path


TWEET_IMAGE = Path(__file__).parent / "tweet.png"
TWITTER = Path(__file__).parent / "twitter_conf.json"
