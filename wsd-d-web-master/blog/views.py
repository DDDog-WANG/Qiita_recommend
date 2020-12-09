from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Post
from .models import RawFromApi
from .models import ArticleSimilarArticles
from urllib import request as ureq
from bs4 import BeautifulSoup
import json
import datetime




# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def read_vec60(request):
    user_likes_url=""
    if request.method == 'GET':
        return render(request,'blog/show_vec60.html',
     {'request':request,'url_list':[],'user_likes_url':'',
    'recommend_articles':[]})
    try:
        p_dist = int(request.POST['p_dist']) if (int(request.POST['p_dist']) != 0) else 1 
        p_like = int(request.POST['p_like']) if (int(request.POST['p_like']) != 0) else 1 
        p_date = int(request.POST['p_date']) if (int(request.POST['p_date']) != 0) else 1 
    
        user_likes_url = str(request.POST['url'])
        #get html
        html = ureq.urlopen(user_likes_url)
    
        #set BueatifulSoup
        soup = BeautifulSoup(html, "html.parser")
        atags=soup.find_all("a", attrs={"class", "u-link-no-underline"})
        url_title_id_list = list()
        user_article_ids = list()
        for atag in atags:
            url='https://qiita.com'+str(atag.get('href'))
            splited_url=url.split('/')
            article_id = splited_url[-1]
            url_title_id_list.append([url,atag.string,article_id])
            user_article_ids.append(article_id)

        records=RawFromApi.objects.using('mysql').filter(article_id__in=user_article_ids)
        row_length=len(records)
        dict_similar_articles = dict()
    

        for record in records: 

            origin_article_url=record.url
            origin_article_title=record.title
            origin_article_id=record.article_id


            if record == None:
                continue
           
            if record.similar_articles_vec60 != None:
                tmp_articles = json.loads(record.similar_articles_vec60)
            else :
                if record.similar_articles != None:
                    tmp_articles = json.loads(record.similar_articles)
                else:
                    continue
            
            #辞書の追加（既存のキーはアップデートされる）
            for key,val_dic in tmp_articles.items():
                val_dic['origin_title'] = origin_article_title
                val_dic['origin_url'] = origin_article_url
                if 'topic_id' not in val_dic:
                    sa=RawFromApi.objects.using('mysql').filter(article_id=str(key)).first()
                    # print(sa.topic_id)
                    if sa.topic_id is not None:
                        val_dic['topic_id'] = sa.topic_id
                    else:
                        val_dic['topic_id']=60
                    pass

                tmp_articles[key]=val_dic 
                
            #dict_similar_articles.update(json.loads(record.similar_articles)) 
            dict_similar_articles.update(tmp_articles) 
           
     
        #推薦リストからいいね履歴を削除
        dict_similar_articles=drop_key(user_article_ids,dict_similar_articles)
    
        #推薦記事をソートして、article_idのリストを返す(templateにdict_similar_articlesとrecommend_article_idsを渡す)
        all_recommend_articles = sort_articles(dict_similar_articles,p_dist,p_like,p_date)
        paginator = Paginator(all_recommend_articles, 20) # 1ページに20件表示
        p = request.POST['button'] # URLのパラメータから現在のページ番号を取得
      
        recommend_articles = paginator.get_page(p) # 指定のページのArticleを取得
       
        return render(request,'blog/show_result_vec60.html',
        {'request':request,'url_list':url_title_id_list,'user_likes_url':user_likes_url,
        'recommend_articles':recommend_articles,'p_dist':p_dist,'p_like':p_like,'p_date':p_date})
    except :
        return render(request,'blog/show_vec60.html',
     {'request':request,'url_list':[],'user_likes_url':'',
    'recommend_articles':[]})
    
def read_vec50(request):
    user_likes_url=""
    if request.method == 'GET':
        return render(request,'blog/show_vec50.html',
     {'request':request,'url_list':[],'user_likes_url':'',
    'recommend_articles':[]})

    try:
        p_dist = int(request.POST['p_dist']) if (int(request.POST['p_dist']) != 0) else 1 
        p_like = int(request.POST['p_like']) if (int(request.POST['p_like']) != 0) else 1 
        p_date = int(request.POST['p_date']) if (int(request.POST['p_date']) != 0) else 1 
    
        user_likes_url = str(request.POST['url'])
        #get html
        html = ureq.urlopen(user_likes_url)
    
        #set BueatifulSoup
        soup = BeautifulSoup(html, "html.parser")
        atags=soup.find_all("a", attrs={"class", "u-link-no-underline"})
        url_title_id_list = list()
        user_article_ids = list()
        for atag in atags:
            url='https://qiita.com'+str(atag.get('href'))
            splited_url=url.split('/')
            article_id = splited_url[-1]
            url_title_id_list.append([url,atag.string,article_id])
            user_article_ids.append(article_id)
        
        
        dict_similar_articles = dict()

        loop=0
        for url_title_id in url_title_id_list:
            origin_article_url=url_title_id[0]
            origin_article_title=url_title_id[1]
            origin_article_id=url_title_id[2]

            record=RawFromApi.objects.using('mysql').filter(article_id=str(origin_article_id)).first()
            
            if record == None:
                loop+=1
                continue
            
            tmp_articles = dict()
            if record.similar_articles != None:
                tmp_articles = json.loads(record.similar_articles)
            else :
                if record.similar_articles_vec60 != None:
                    tmp_articles = json.loads(record.similar_articles_vec60)
                else:
                    loop+=1
                    continue

            #辞書の追加（既存のキーはアップデートされる）
            for key,val_dic in tmp_articles.items():
                val_dic['origin_title'] = origin_article_title
                val_dic['origin_url'] = origin_article_url
                # # print(key)
                if 'topic_id' not in val_dic:
                    sa=RawFromApi.objects.using('mysql').filter(article_id=str(key)).first()
                    # print(sa.topic_id)
                    if sa.topic_id is not None:
                        val_dic['topic_id'] = sa.topic_id
                    else:
                        #60は適当な画像
                        val_dic['topic_id']=60
                    pass
                
                tmp_articles[key]=val_dic 
               
                
            #dict_similar_articles.update(json.loads(record.similar_articles)) 
            dict_similar_articles.update(tmp_articles) 
            loop+=1
        
     
        #推薦リストからいいね履歴を削除
        dict_similar_articles=drop_key(user_article_ids,dict_similar_articles)
    
        #推薦記事をソートして、article_idのリストを返す(templateにdict_similar_articlesとrecommend_article_idsを渡す)
        all_recommend_articles = sort_articles(dict_similar_articles,p_dist,p_like,p_date)
        paginator = Paginator(all_recommend_articles, 20) # 1ページに20件表示
        p = request.POST['button'] # URLのパラメータから現在のページ番号を取得
      
        recommend_articles = paginator.get_page(p) # 指定のページのArticleを取得
       
        return render(request,'blog/show_result_vec50.html',
        {'request':request,'url_list':url_title_id_list,'user_likes_url':user_likes_url,
        'recommend_articles':recommend_articles,'p_dist':p_dist,'p_like':p_like,'p_date':p_date})
    # except Exception as e:
    #     print('=== エラー内容 ===')
    #     print('type:' + str(type(e)))
    #     print('args:' + str(e.args))
    #     print('e自身:' + str(e))
    except :
        return render(request,'blog/show_vec50.html',
     {'request':request,'url_list':[],'user_likes_url':'',
    'recommend_articles':[]})
   
def mysql_seach(request):
    rows = RawFromApi.objects.using('mysql').get(id=3)
    return render(request,'blog/show_rows.html',{'rows':rows})

def drop_key(key_list,dic):
    for key in key_list:
        value=dic.pop(key,None)
    return dic

def sort_articles(dic,p_dist,p_like,p_date):
    #辞書からidと類似度のリストのリストを作りsortしたリストを返す
    
    articleId_scores = []
    for key,value in dic.items():
        today=datetime.datetime.today()
        created_at = datetime.datetime.strptime(value['created_at'], '%Y-%m-%d %H:%M:%S')
        td = abs(today -created_at)
        score =  p_dist*(1-float(value['distance'])) + float(value['likes_count'])/p_like - td.days/p_date
        articleId_scores.append([key,score])

    articleId_scores.sort(key=lambda x: x[1],reverse=True)

    recommend_articles=list()
    for articleId_score in articleId_scores:
        recommend_articles.append(dic[articleId_score[0]])

    return  recommend_articles


    # article_ids = list(dic.keys())
    # print(article_ids)
    # return article_ids
