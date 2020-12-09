FROM continuumio/anaconda3

RUN apt update \
    && apt install -y build-essential python-dev default-libmysqlclient-dev \
        mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file sudo \
    && /opt/conda/bin/pip install sqlalchemy mysqlclient lxml mecab-python3 cssselect gensim

RUN /opt/conda/bin/conda install faiss-cpu -c pytorch -y

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && ./mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y \
        --ignore_noun_ortho --ignore_noun_sahen_conn_ortho

RUN mkdir /usr/local/lib/mecab \
    && mkdir /usr/local/lib/mecab/dic \
    && ln -s /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd/ /usr/local/lib/mecab/dic/mecab-ipadic-neologd

WORKDIR /root/faiss-knn

ENTRYPOINT /opt/conda/bin/python3 main.py 0.0.0.0 9000
