import requests

from scraping.hatena_project.hatena_project.database.basic_mongo import Mongo


class AddMongo(Mongo):
    """
    いろいろな説明変数をデータベースに追加する
    """
    hateb_api = "http://api.b.st-hatena.com/entry.counts"

    def hateb(self):
        """
        はてなブックマークを調べてhatebカラムに追加する
        """
        find = list(self.collection.find({'hateb': {"$exists": False}}).limit(50))
        urls = [dic['url'] for dic in find]

        while(len(urls)!=0):
            response = requests.get(self.hateb_api, params={'url': urls})
            j = response.json()

            print(len(urls))

            for item in j:
                title = item
                self.collection.update_one({"url": title}, {"$set": {"hateb": j[item]}})

            find = list(self.collection.find({'hateb': {"$exists": False}}).limit(50))
            urls = [dic['url'] for dic in find]


def main():
    AddMongo().hateb()


if __name__ == '__main__':
    main()