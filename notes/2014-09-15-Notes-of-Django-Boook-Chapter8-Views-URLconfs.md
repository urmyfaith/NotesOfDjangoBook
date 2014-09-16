#Chapter8-Views-URLconfs


## urls.py 导入包的优化:

URLconfs的patterns里url的第二个参数接收的是代表一个视图的函数,如下:

```python

# urls.py

from django.conf.urls import patterns, include, url
from mysite.views import hello, \ 
    current_datetime, hours_ahead, \
    show_request, \ 
    search_form,show_search_result
from mysite.sendMailViewByForms import contact,contact_thanks
urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$',hello),
    url(r'^time/$',current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^request-info/$',show_request),
    url(r'^search-form/$',search_form),
    url(r'^search/$',show_search_result),
    url(r'^contact/$',contact),
    url(r'^contact/thanks/$',contact_thanks),                  
)
```

### 导入视图函数-->导入视图所在包,通过包访问函数.

**通过导入视图所在包,来访问视图函数.**

 ```python
from mysite import views
urlpatterns = patterns('',
    ...
    #url(r'^hello/$',hello),
    url(r'^hello/$',views.hello),
    ...
```
![import_package_instead_of_func.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/import_package_instead_of_func.png)


### 导入视图函数-->直接通过app.package.func访问函数:
```python
from django.conf.urls import *
urlpatterns = patterns('',
...
    url(r'^contact/$','mysite.sendMailViewByForms.contact'),
    url(r'^contact/thanks/$','mysite.sendMailViewByFormscontact_thanks'), 
...                 
)
```
> 注意:这里有些改变:
1) 导入包从"from django.conf.urls import patterns, include, url"改为了"from django.conf.urls import *"

2) 没有导入sendMailViewByForms包,而是直接使用了**带引号的**mysite.sendMailViewByForms.contact来访问函数.

*(ps.如果不带引号,就会找不到包,也就找不到函数.)*

### patterns() 对象相加

```python
#urls.py
from django.conf.urls import *
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact/$','mysite.sendMailViewByForms.contact'),
    url(r'^contact/thanks/$','mysite.sendMailViewByForms.contact_thanks'),                  
)
urlpatterns += patterns('mysite.views',
    url(r'^hello/$','hello'),
    url(r'^time/$','current_datetime'),
    url(r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
    url(r'^search/$','show_search_result'),
    url(r'^request-info/$','show_request'),
    url(r'^search-form/$','search_form'),
)
```
> 注意:

1) 这里的两个patterns()相加了
2) 后面的将会查找的是'mysite.views.hello'等,

他们有一个公共的前缀,这里提取出来了.

3) 不导入包的话,**后面的实际视图函数名称,使用了单引号.**

### patterns() 对象相加更进一步的优化:

利用上面的,可以更进一步优化URLconfs
```python
#urls.py
from django.conf.urls import *
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('mysite.sendMailViewByForms',
    url(r'^contact/$','contact'),
    url(r'^contact/thanks/$','contact_thanks'),                  
)
urlpatterns += patterns('mysite.views',
    url(r'^hello/$','hello'),
    url(r'^time/$','current_datetime'),
    url(r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
    url(r'^search/$','show_search_result'),
    url(r'^request-info/$','show_request'),
    url(r'^search-form/$','search_form'),
)
```
> 小结:**一个view文件里的视图函数可以提取出前缀,相加后返回.**

---

## 命名组(Named Groups)(?P\<name>pattern) 
如果不使用命名组,是这样的:
URLconf可能是:
```python
#urls.py
urlpatterns += patterns('mysite.articlesViews',
    (r'^articles/(\d{4})/$', 'year_archive'),
    (r'^articles/(\d{4})/(\d{2})/$','month_archive'),
)
```
view可能是:
```python
#articlesViews.py
from django.http import HttpResponse

def year_archive(request,year):
    rawHtml='<html><head></head><body>year_archive:%s</body></html>'% year
    return HttpResponse(rawHtml)
def month_archive(request,year,month):
    rawHtml='<html><head></head><body>year_archive:%s-%s</body></html>'% (year,month)
    return HttpResponse(rawHtml)
```
> 这样的话,在URL里的参数,传递到视图中去的时候,是按**顺序传递**:
articles/(\d{4})/(\d{2})/    -->    articles/year/month/

如果我们使用命名组的话,它的形式是这样的:**(?P\<name>pattern)**

```python
#urls.py
urlpatterns += patterns('mysite.articlesViews',
    (r'^articles/(?P<year>\d{4})/$', 'year_archive'),
    (r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$','month_archive'),
)
```
相应的,视图中,我们可以这样写:
```python
#articlesViews.py
from django.http import HttpResponse
def year_archive(request,year):
    rawHtml='<html><head></head><body>year_archive:%s</body></html>'% year
    return HttpResponse(rawHtml)
def month_archive(request,month,year):
    rawHtml='<html><head></head><body>year_archive:%s-%s</body></html>'% (year,month)
    return HttpResponse(rawHtml)
```
> 注意:

1) 在URLconf中,使用了命名组的方式,即第一个位置命名为year,第二个位置命名为month

2) 在view文件,month_archive视图中的参数,我们故意颠倒了位置.


**小结:** 使用命名组,可以很好的说明参数位置所代表的意义,也可以防止顺序颠倒带来的错误.

![named_groups_month_year.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/named_groups_month_year.png)

----
## 传递额外的参数到视图函数中

从上面的命名组中可以看到,URLconf可以传递参数到View中.
那么怎么传递额外的参数到视图中?

假设,有两个url,分别匹配到两个视图,但是**它们使用不同的模版来渲染.**
```python
#urls.py
urlpatterns += patterns('mysite.foobar_view',
    (r'^chapter8_url_view/pass_extra_options_to_view/foo/$','foo_view'),
    (r'^chapter8_url_view/pass_extra_options_to_view/bar/$','bar_view'),
)

#foobar_view.py
from django.shortcuts import render
from books.models import Book
def foo_view(request):
    books = Book.objects.filter(title__icontains='world')  
    return render(request,'foobar/foo.html',{'books':books})
def bar_view(request):
    books = Book.objects.filter(title__icontains='the')
    return render(request,'foobar/bar.html',{'books':books})

```
这样村的问题:功能机会相同,只是渲染的模版不一样.

我们可以使用传递额外的参数到view中去,动态的指定渲染模版:

```python
#urls.py
urlpatterns += patterns('mysite.foobar_view',
    (r'^chapter8_url_view/pass_extra_options_to_view/foo/$', \
     'foo_bar_view',{'template_name':'foobar/foo.html','search_str':'world'}),
    (r'^chapter8_url_view/pass_extra_options_to_view/bar/$', \
     'foo_bar_view',{'template_name':'foobar/bar.html','search_str':'the'}),
)
#foobar_view.py
def foo_bar_view(request,template_name,search_str):
    books=Book.objects.filter(title__icontains=search_str)
    return render(request,template_name,{'books':books})
```
1) 在urls.py的patterns里,使用的第三个参数:传入了一个字典.

这个字典会从URLconf传入到视图中.

2) 在视图里,将两个视图函数合并为一个,使用字典参数,这样就是多个不同的视图.

![foo_bar_view.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/foo_bar_view.png)
---



