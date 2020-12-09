# scraping
# blog_scraping

はてなブックマークの人気エントリを250件くらいurlとタイトルとテキストデータを取ってくる

# 初期設定
MongoDBの設定

MongoDB Compassがあると便利

https://garafu.blogspot.com/2019/02/install-mongod-on-macos.html

https://qiita.com/____easy/items/4dcda6cc4f5e7de13d36

# requirement

`scrapy, request, readability-lxml` をpipかcondaかで入れるのだ...

# 現在のmongoDBの状態
|名前| 意味|
|---|---|
| url | URL |
| title | ブログタイトル |
| html | htmlそのまま |
| content | 文章|

# 使い方
ルートディレクトリ で

`scrapy crawl broad`



# 参考

参考にしたページとかをそれぞれがまとめておくと、つまづかなくて済むかも？？（自由に追記、編集して...）

[スクレイピングのまとめ](https://vaaaaaanquish.hatenablog.com/entry/2017/06/25/202924)

[はてなapiで文書とブックマーク数を取得](https://note.nkmk.me/python-scrapy-hatena-bookmark-api/)

[自然言語処理における前処理](https://qiita.com/Hironsan/items/2466fe0f344115aff177)

[scrapy入門](https://sutaba-mac.site/scrapy-s2-settings-and-items/)