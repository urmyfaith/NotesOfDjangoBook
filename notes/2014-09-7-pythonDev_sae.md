# pythondev on sae.

##创建一个Hello, world!程序

1) sae上创建python应用

2) 创建一个版本

3) 本地SVN检出仓库

包含了两个文件.
```python
└─1
        config.yaml
        index.wsgi
```

其中config.yaml:
```python
#config.yaml
name: pythondev
version: 1
```
4) 修改index.wsgi如下:
```python
#index.wsgi
import sae
def app(environ, start_response):
    status = '200 OK'
    response_headers = [('content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello, world!']
application = sae.create_wsgi_app(app)
```

5) 访问应用地址:"http://pythondev.sinaapp.com/"即可输出"Hello, world!"

## 使用web开发框架-->Django

安装示例,

本地检出一个版本,然后将Django工程复制过来:

修改congfig.yaml,修改index.wsgi就可以..

事实上,这里有很多的问题:

1) SAE内置的Django版本为1.4,而本地使用的是1.7

2) 生成工程的settings文件不一样..

3) 在settings里的数据库配置不同...

4) 其他中间件,插件的配置也有区别.

5) 本地数据库的同步-->云数据库上

直接执行db.sql???这样数据库早就建立了.

