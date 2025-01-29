scrapy-fake-useragent 依赖 fake-useragent 生成用户代理，但 fake-useragent==2.0.0 开始对其内部实现做了较大改动，可能导致兼容性问题。
如果 scrapy-fake-useragent 版本是 1.4.4，需要使用fake-useragent==1.1


pip install selenium==4.27.1

pip install scrapy==2.11.2

pip install fake-useragent==1.1.0

pip install scrapy_fake_useragent==1.4.4

pip install pipreqs

pipreqs . --encoding=utf8 --force


动态网页数据爬取+文件下载实践
