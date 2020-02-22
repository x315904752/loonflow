FROM registry.fit2cloud.com/public/python:v3
MAINTAINER Loonflow Team <tuffy@cenret.com>

WORKDIR /opt/loonflow
RUN useradd loonflow

COPY ./requirements /tmp/requirements

RUN yum -y install epel-release && \
      echo -e "[mysql]\nname=mysql\nbaseurl=https://mirrors.tuna.tsinghua.edu.cn/mysql/yum/mysql57-community-el6/\ngpgcheck=0\nenabled=1" > /etc/yum.repos.d/mysql.repo
RUN yum -y install mariadb-devel mysql-devel

RUN cd /tmp/requirements && pip install --upgrade pip setuptools && pip install wheel && \
    pip install -i https://mirrors.aliyun.com/pypi/simple/ -r pro.txt || pip install -r requirements.txt

COPY . /opt/loonflow

ENV LANG=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8

EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]
