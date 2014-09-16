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

