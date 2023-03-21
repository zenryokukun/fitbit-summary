# [Fitbit-Summary]Fitbitを使った健康報告バッチ

毎晩23時にFitbit APIを使って健康情報をTwitterに投稿する。プログラムの実行は、サーバのcronで登録する。

## Fitbit Web API

[https://dev.fitbit.com/build/reference/web-api/](https://dev.fitbit.com/build/reference/web-api/)

## エントリーポイント

```bash
# linux
python3 ./main.py
# windows
python ./main.py
```

## スクリプトについて

- *main.py* エントリーポイント
- *api.py* Fitbit Web APIの実行
- *graph.py* 心拍数やSpO2データをグラフ化し画像にする
- *tweet.py* テキストと画像（任意）を投稿

## 必要なファイル

- *conf.json* fitbit conf file
- *twitter_conf.json* twitter conf file

## 出力されるファイル

- **heart-spo.png** tweetする画像

## cron（備忘）

### 登録スクリプト

ログインスクリプトが流れないのでコマンドもフルパスで登録
```bash
/usr/bin/python3 /home/crypto/fitbit/main.py
```

### スケジュール

| 分 | 時 | 日 | 月 | 曜日 |
|----|----|----|----|----|
| 0-59 | 0-23 | 1-31 | 1-12 | 0-7 |

- 曜日は0,7が日曜日。
- ```*```は全ての値を設定したことになる。分を*にすると毎分になる。
- ex: 0 2 * * * 毎日2時00分に実行
- ex: * 2 * * * 毎日2時の**毎分**実行

