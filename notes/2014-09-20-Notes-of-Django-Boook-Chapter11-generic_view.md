# Chapter11-generic_view

## 通用视图实现的功能:

* 完成简单的任务

* 显示列表/某个特定对象的详细内容页面

* 显示基于日期的数据的年月日归档页面

## 使用通用视图的一个示例:TemplateView

```python
from django.views.generic import TemplateView
urlpatterns += patterns('',
    url(r'^chapter11_generic_view/about/$', \ 
                  TemplateView.as_view(template_name="about.html")),
)
```
> 使用通用视图:

1)在urls.py里导入包

2)将url地址,指向一个带参数的TemplateView视图.

![generic_view_template_view.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/generic_view_template_view.png)

这里,我们只需要2个步骤:

a) 编写urls.py,指定URL匹配.(将参数传递给TemplateView视图)

b) 编写指定的模版文件.

---

## 列表对象的通用视图

1) 把'books/'开始的 URL使用books里的urls.py来设置
```python
# mysite/mysite/urls.py
urlpatterns = patterns('',
    ...
    url(r'^books/', include('books.urls')),
)
```

2) 在books这个APP里增加urls.py,指定URLConf匹配
```python
# mysite/books/urls.py
from django.conf.urls import *
from books.views import PublisherList

urlpatterns = patterns('books.views',
    url(r'publishers/$',PublisherList.as_view()),
)
```
3) 使用通用视图编写views.py
```python
# mysite/books/views.py
from django.views.generic import ListView
from books.models import Publisher

class PublisherList(ListView):
    model = Publisher
```

4) 设置模版,默认的模版是**publisher_list.html**

即为[modelName.lowcase()]_list.html

```python
Django tried loading these templates, in this order:
Using loader django.template.loaders.filesystem.Loader:
Using loader django.template.loaders.app_directories.Loader:
...\site-packages\django-1.7-py2.7.egg\django\contrib\admin\templates\books\publisher_list.html (File does not exist)
...\site-packages\django-1.7-py2.7.egg\django\contrib\auth\templates\books\publisher_list.html (File does not exist)
...\NotesOfDjangoBook\mysite\mysite\templates\books\publisher_list.html (File does not exist)
...\NotesOfDjangoBook\mysite\books\templates\books\publisher_list.html (File does not exist)
```

编写一个简单的模版:
```python
# mysite\books\templates\books\publisher_list.html
{% block content %}
    <h2>Publishers</h2>
    <ul>
        {% for publisher in object_list %}
            <li>{{ publisher.name }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```
![generic_view_list_view.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/generic_view_list_view.png)

---