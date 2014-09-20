# Chapter11-generic_view

* 通用视图实现的功能:
* 使用通用视图的一个示例:TemplateView
* 列表对象的通用视图
* 动态过滤:
* 获取和保存用户上次访问时间.

---

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

## 动态过滤:

如果我们想知道某个出版社的相关数据,而不是显示所有的出版社.那么该怎么实现?
```python
# books/uls.py
urlpatterns = patterns('books.views',
    url(r'^publishers/([\w-]+)/$',PublisherBookList.as_view()),
)

# books/views.py
from django.shortcuts import get_object_or_404

from django.views.generic import ListView
from books.models import Publisher,Book

class PublisherBookList(ListView):
    template_name="books/books_by_publisher.html"

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher,name=self.args[0])
        return Book.objects.filter(publisher=self.publisher)
    def get_context_data(self,**kwargs):
        print "self.args[0]=",self.args[0]
        context=super(PublisherBookList,self).get_context_data(**kwargs)
        context['publisher']=self.publisher
        return context
```

> 仔细看上面的代码:

1) 在url里,使用的ListView作为通用视图

2) 在views里,

a) 指定了模版名称

b) 重写了get_queryset()方法,通过这个执行书籍按照出版社筛选

c) 重写了get_context_data()方法,通过这个方法,添加额外的数据.

在context中同时增加publisher，这样一来我们就可以在模板中使用它了：

3) 最后,写模版渲染数据:
```python
{% block content %}
    <h2>Publishers({{ publisher.name}}) info:</h2>
	<table width="500" border="0" bgcolor="blue" bordercolor="black" cellpadding="5" cellspacing="1">
	<tr bgcolor="white">
		<td>name</td>
		<td>address</td>
		<td>city</td>
		<td>state_province</td>
		<td>country</td>
		<td>website</td>
	</tr>
	<tr bgcolor="white">
		<td>{{ publisher.name }}	</td>
		<td>{{ publisher.address }}	</td>
		<td>{{ publisher.city }}	</td>
		<td>{{ publisher.state_province }}	</td>
		<td>{{ publisher.country }}</td>
		<td>{{ publisher.website }}</td>
	</tr>
	</table>
	<p>
	<h2>Publishers({{ publisher.name }}) Books are:</h2>
    <table width="500" border="0" bgcolor="blue" bordercolor="black" cellpadding="5" cellspacing="1">
	
	   {% for book in book_list %}
		<tr bgcolor="white">
		<td>  {{ book.title }}</td>
		<td> {{ book.publisher }}</td>
		<td> {{ book.publication_date }}</td>
		<td> {{ book.num_pages }}</td>
		</tr>
	 {% endfor %}
    </table>

{% endblock %}
```

渲染效果如下:
![publisher_books_filter.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/publisher_books_filter.png)

-----
## 获取和保存用户上次访问时间.

1)首先,设计字段

2) 配置url

3) 编写view

4) 编写模版渲染

```python

#books/modles.py
class Author(models.Model):
     ...
    last_accessed = models.DateTimeField(blank=True, null=True)

# books/urls.py
from books.views import PublisherBookList,AuthorDetailView

urlpatterns = patterns('books.views',
    url(r'^publishers/([\w-]+)/$',PublisherBookList.as_view()),
    url(r'^authors/(?P<pk>\d+)/$',AuthorDetailView.as_view()),
)

#books/views.py
from django.utils import timezone
class AuthorDetailView(DetailView):
    queryset=Author.objects.all()
    def get_object(self):      
        mobject = super(AuthorDetailView,self).get_object()
        mobject.last_accessed=timezone.now()
        mobject.save() 
        return mobject 
    def get_context_data(self,*args,**kwargs):
        context=super(AuthorDetailView,self).get_context_data(*args,**kwargs)
        mm_object=get_object_or_404(Author,id=self.kwargs['pk'])
        m_object = super(AuthorDetailView,self).get_object()
        context['author']=m_object
        print context
        return context
```

> 分析下上面的代码:

1) 设计字段,没什么好说的,时间类型

2) URLconf里,使用通用视图,带一个命名组pk参数(关键字参数).

3) 在视图里,

a)重写了get_object方法,得到对象,修改值,保存.

b)重写了get_ontext_data方法,传入模版里需要的参数.

**这里有两个方法得到对象**

第一个:使用get_object()方法
```python
mobject = super(AuthorDetailView,self).get_object()
```
第二个:使用get_object_or_404()方法
```python
 mm_object=get_object_or_404(Author,id=self.kwargs['pk'])
```
可以看到,第一个方法,没有传入筛选条件,而第二个传入了.

最后,是模版文件:
```python
# mysite\books\templates\books\author_detail.html
{% block content %}

	User "<strong>{{ author.full_name }}</strong>" last  accessed time is <em>{{ author.last_accessed }}</em>.

{% endblock %}
```
渲染效果如下:

![generic_view_last_access_time.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/generic_view_last_access_time.png)
-----
