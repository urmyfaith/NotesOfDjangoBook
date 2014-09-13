# Writing your first Django app--part 3 about view

*   添加更多的view
*   写actually有用的view
*   使用模版来设计view
*   使用模版设计view的捷径:render()
*   抛出异常404
*   抛出异常404-快捷方法: get_object_or_404()
*   修改URL硬编码
*   URL命名空间

> view : Django应用(作为一个特殊的功能或者有一个特定的模版)里的一种网页.

在DemoAppPoll里,我们下面的view:

* Question index  page  -->展示最新的问题

* Question detail page -->展示一个问题和一个投票表格

* Question result page --> 展示特定问题的投票结果

* Vote action --> 处理特定问题的投票.

    在Django里,每一个view都代表一个python 函数/方法.

    请求一个url的时候,Django就会使用一个view来处理这个page.

    从URL传递到view,Django使用URLconfs

## 第一个view

1.修改DemoAppPoll/views.py:
```python
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello,urmyfatih.")

```

2.创建DemoAppPoll/urls.py

```python
from django.conf.urls import patterns,url
from DemoAppPoll imoprt views

urlpatterns =patterns(
    '',
    url(r'^$',views.index,name='index')
    )

```
3.在工程demoSite/urls.py中添加应用DemoAppPoll的urls.py
```python
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demoSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^DemoAppPoll/', include('DemoAppPoll.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)
```
>   url(r'^DemoAppPoll/', include('DemoAppPoll.urls')),就是我们新增的.

>    表示,我们使用DemoAppPoll.urls来处理http://localhost:8080/DemoAppPoll/的请求.

>    在DemoAppPoll.urls里,我们绑定了views.index来处理请求.

![成功处理请求](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/Django/images/DemoAppPoll-first-app.png)

-----

1. url()参数:regex
python将url请求在工程里urls.py中的pattterns列表中一一匹配.
并且这种匹配不会匹配请求的参数.即http://www.example.com/myapp/?name=zx仅会匹配myapp/

2. url()参数:view
匹配到正则表达式之后,调用特定的view函数.

3. url()参数:kwargs
   任意的关键字参数,可以通过字典传递给特定的view.

4. url()参数:name 
    给url命名,这样就可以全局使用.

----

## 添加更多的view

**DemoAppPoll/urls.py**
```python
from django.conf.urls import patterns,url

from DemoAppPoll import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)

```

指定类/方法/函数来处理匹配到url:

> views.index -->处理/DemoAppPoll/

> views.detail-->处理/DemoAppPoll/[number]/

> view.results-->处理/DemoAppPoll/[number]/results/

> views.vote -->处理/DemoAppPoll/[number]/vote/


下面的是类/方法/函数具体如何响应请求的:

**DemoAppPoll/views.py:**

```python
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello,urmyfatih.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

```
![路径匹配](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/Django/images/DemoAppPoll-url-view.png)

---

当请求http://localhost:8080/DemoAppPoll/33/的时候,

第一步:Django加载项目下的urls.py模块,即(**demoSite.urls**),从demoSite/urls.py中找到代表匹配列表的变量:urlpatterns,从列表中匹配.
```python
 url(r'^DemoAppPoll/', include('DemoAppPoll.urls')),
```

此时,匹配到DemoAppPoll/,

当Django遇到include()的时候,截掉已经匹配到的(DemoAppPoll/),将剩余的(33/)传递到URLconf继续处理.


第二步:Django截掉前面的之后,剩下的(33/),使用**DemoAppPoll.urls**模块(DemoAppPoll/urls.py)来处理.

```python
url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
```
此时,匹配到view.detail,

第三步:由view.detail(DemoAppPoll/views.py中detail函数)响应请求.

![include()](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/Django/images/request-url.png)

------

## 写actually有用的view

> 每一个view做2件事情:

1. 返回HttpResponse(它包含了真实的html内容.)
2. 抛出一个异常,例如Http404

其他的事情就是自己安排了,例如,利用Django的数据库API,显示最新的5条问题:


```python
#in DemoAppPoll/views.py/[fun]index

from DemoAppPoll.models import Question

def index(request):
    # IMPORTANT: read db , order , limit
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # format question for output.
    output=','.join([p.question_text for p in latest_question_list])
   
    return HttpResponse(output)
```
![hard-coded-view](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/Django/images/hard-coded-view.png)

有个问题是,这个**页面看起来是如此的简陋**,这时候,可以使**用template**来设计.

另外一个问题是,**template的位置放在哪里?**

> Django的TEMPLATE_LOADER设置包含了从哪里获得模版.
它的默认值有两个.
```python
TEMPLATE_LOADERS
Default:
('django.template.loaders.filesystem.Loader',
 'django.template.loaders.app_directories.Loader')
```
> 其中一个是app的,它在INSTALLED_APP的目录下查找templates目录.

##  使用模版来设计view

1th. 在App(DemoAppPoll)目录下,创建templates目录.

2th. 在templates目录下创建App名称(DemoAppPoll)的目录.

3th. 在DemoAppPoll目录下,创建index.html.

```python
D:\desktop\todoList\Django\mDjango\demoSite\DemoAppPoll>tree /f /a
|   admin.py
|   admin.pyc
|   models.py
|   models.pyc
|   tests.py
|   urls.py
|   urls.pyc
|   views.py
|   views.pyc
|   __init__.py
|   __init__.pyc
|
+---migrations
|       0001_initial.py
|       0001_initial.pyc
|       __init__.py
|       __init__.pyc
|
\---templates
    \---DemoAppPoll
            index.html

```

这样,我们就可以是使用DemoAppPoll/index.html来设计view了.

4th. 修改index.html

使用for循环创建无序列表.

> {% if latest_question_list %} 这是代表使用python语句.

> {{ question.id }}代表使用python变量.

```python
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/DemoAppPoll/{{ question.id }}/">{{ question.question_text}}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}

```

5th. 使用模版文件来渲染之后输出.

```python
from django.http import HttpResponse
from django.template import RequestContext, loader

from DemoAppPoll.models import Question

def index(request):
    # IMPORTANT: read db , order , limit
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('DemoAppPoll/index.html')
    context = RequestContext(
        request,
        {
            'latest_question_list':latest_question_list,
        },
        )
    
    return HttpResponse(template.render(context))
```

这里,涉及到如何使用哪个模版,向模版传入变量,最后渲染后输出.
>
 ```python
    template = loader.get_template('DemoAppPoll/index.html')
    context = RequestContext(
        request,
        {
            'latest_question_list':latest_question_list,
        },
        ) 
    return HttpResponse(template.render(context))
```

![templates-view](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/Django/images/templates-view.png)

----
## 使用模版设计view的捷径:render()

>  常见的习惯是:加载模版,填充内容 ,返回HttpResponse.

Django 提供了一个简洁的方法来实现,例如上面的index()方法,
```python
from django.shortcuts import render
#from django.http import HttpResponse
#from django.template import RequestContext, loader

from DemoAppPoll.models import Question

'''
def index(request):
    # IMPORTANT: read db , order , limit
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('DemoAppPoll/index.html')
    context = RequestContext(
        request,
        {
            'latest_question_list':latest_question_list,
        },
        )
    
    return HttpResponse(template.render(context))
'''
# render(请求,模版,参数列表字典{key:value})

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5] @
    context = {'latest_question_list': latest_question_list}
    return render(request, 'DemoAppPoll/index.html', context)


```
> 注意到,"from django.shortcuts import render"之后,就不需要"from django.http import HttpResponse"和"from django.template import RequestContext, loader"


-----
## 抛出异常404

在数据库里,如果只有2条记录,那么访问第3条记录,就应该抛出异常.

在DemoAppPoll/views.py
```python
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404
    return  render(request, 'DemoAppPoll/detail.html', {'question': question})
    #return HttpResponse("You're looking at question %s." % question_id)
```
注意

a.需要导入新包:

> from django.http import Http404

b.需要创建模版文件:detail.html
```python
<div align="center">
<table  cellpadding="0" cellspacing="0"  width="500">
  <tr align="center" >
	<td>question_id</td>
	<td>question_text</td>
  </tr>
  <tr  align="center">
	<td >{{question_id}}</td>
	<td >{{question}}</td>
  </tr>
  </table>
  </div>

```
![templates-except-404](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/Django/images/templates-except-404.png)

## 抛出异常404-快捷方法

在DemoAppPoll/views.py
```python
'''
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404
    return  render(request, 'DemoAppPoll/detail.html', {'question': question,'question_id':question_id})
    #return HttpResponse("You're looking at question %s." % question_id)
'''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'DemoAppPoll/detail.html', {'question': question})

```
这里,导入包的问题也存在,改为:
```python
from django.shortcuts import render,get_object_or_404
```
多了个get_object_or_404.

> question = get_object_or_404(Question, pk=question_id),得到对象

> 也有一个**get_list_or_404()** 函数,得到列表.

---

## 修改URL硬编码

在DemoAppPoll/templates/index.html中,url为硬编码.
> ```python
li><a href="/DemoAppPoll/{{ question.id }}/">{{ question.question_text }}</a></li>
```

在DemoAppPoll/urls.py里,我们给这个url匹配指定过了名称(**name='detail'**)
```python
url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
```
可以使用{%url %}来生成url.
```python
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```
----
## URL命名空间.

当多个app存在的时候,{%url%}指的是哪个?

可以在工程目录(demosite)下的urls.py中指定命名空间:
demoSite/urls.py

```python

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
   # url(r'^DemoAppPoll/', include('DemoAppPoll.urls')),
    url(r'^DemoAppPoll/', include('DemoAppPoll.urls',namespace="DemoAppPoll")),
    url(r'^admin/', include(admin.site.urls)),    
)
```
这样,模版文件中,使用url名称的时候,需要指定命名空间:

DemoAppPoll/templates/DemoAppPoll/index.html

```python
<li><a href="{% url 'DemoAppPoll:detail'  question.id %}">{{ question.question_text }}</a></li>
```
----
