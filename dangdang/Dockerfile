FROM python
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
RUN pip3 install pymysql
CMD scrapy crawl book
