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