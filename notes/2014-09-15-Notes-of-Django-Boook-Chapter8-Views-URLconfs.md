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
    url(r'^contact/thanks/$','mysite.sendMailViewByFormscontact_thanks'),                  
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

