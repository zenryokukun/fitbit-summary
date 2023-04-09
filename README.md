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

## Dependencies

### *requests*

```python
pip install requests
```

### pytweet（githubからクローン）

プロジェクトの直下にクローン。

```bash
git clone https://github.com/zenryokukun/pytweet.git
```

モジュール更新時はgit pullすること。メディア・アップロードは追加され次第対応予定なので、
近いうちに更新する予定。

```bash
cd pytweet
git pull
```


## スクリプトについて

- *main.py* エントリーポイント
- *api.py* Fitbit Web APIの実行
- *graph.py* 心拍数やSpO2データをグラフ化し画像にする
- *pytweet/* Twitter API V2対応の外部パッケージ。(https://github.com/zenryokukun/pytweet.git)

## 必要なファイル

### ■ *conf.json* fitbit conf file

```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "access_token": "your-access-token",
  "refresh_token": "your-refresh-token",
  "redirect_uri": "your-redirect-url",
  "user_id": "your-user-id",
  "scope": "your-scope"
}
```

*client_id*,*access_token*,*refresh_token*の3点あれば動きます。

### ■ *twitter_conf.json* twitter conf file

```json
{
  "API_KEY": "MY-API-KEY",
  "API_SECRET": "MY-API-SECRET",
  "BEARER": "MY-BEARER",
  "ACCESS_TOKEN": "MY-ACCESS-TOKEN",
  "ACCESS_SECRET": "MY-ACCESS-SECRET"
}
```

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

