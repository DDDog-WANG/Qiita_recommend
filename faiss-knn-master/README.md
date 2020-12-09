# faiss-knn

`GET /knn?id=<article_id_1>,<article_id_2>,...,<article_id_n>&count=<k>` でn個の各記事に対するk個の近傍の記事idを取得

`id`: Qiitaの記事id

`count`: 近傍探索の個数

### setup
`$ unzip data/vec.csv.zip -d data`

`$ docker-compose up`
### query test
`$ curl 'localhost:9000/knn?id=<article_id_1>,<article_id_2>,...,<article_id_n>&count=<k>' | jq .`
