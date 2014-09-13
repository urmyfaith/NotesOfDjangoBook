# Writing your-first Django-app-part 4-simple-form


*   简单的表单
*   处理表单提交-跳转/错误信息
*   处理表单提交--结果显示
*   通用view (generic view) 设计:越少代码越好?
*  * 1.修改DemoAppPoll/urls.py
*  * 2.修改DemoAppPoll/views.py


## 简单的表单

DemoAppPoll/templates/details.html

```python
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'DemoAppPoll:vote' question.id %}" method="post">
    {% csrf_token %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
    {% endfor %}
    <input type="submit" value="Vote" />
</form>
```
转换成源码文件是:

```html

<h1>what time is it?</h1>

<form action="/DemoAppPoll/2/vote/" method="post">
<input type='hidden' name='csrfmiddlewaretoken' value='nEUM2klSzxP2tZFq9oFnVai2MqqUt2z2' />

    <input type="radio" name="choice" id="choice1" value="4" />
    <label for="choice1">q2 win</label><br />

    <input type="radio" name="choice" id="choice2" value="5" />
    <label for="choice2">who win</label><br />

<input type="submit" value="Vote" />
</form>
```
这里有几个要关注的地方:

> 1> 表单的提交地址,我们写的是{% url 'DemoAppPoll:vote' question.id %},在DemoAppPoll/urls.py里,我们使用

```python
 url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'

```
名称为vote来处理这个url匹配,全称需要加上命名空间,就成了DemoAppPoll:vote(http://localhost:8080/DemoAppPoll/2/vote/)

> 2>**forloop.counter**,用来显示循环的次数.

> 3>跨域保护CSRF, {% csrf_token %},自动生成一个隐藏的input.作为校验,保护.

---

## 处理表单提交-跳转/错误信息

上面的表单提交后,并没有做有效的处理.

DemoAppPoll/views.py

```python
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from DemoAppPoll.models import Question,Choice

def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." % question_id)
    q = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=q.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request,'DemoAppPoll/detail.html',{
            'question':q,
            'error_message':"You didn't select choice.",
            })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        print "question.id=",q.id
        print "question_text=",q.question_text
        print "selected_choice.id=",selected_choice.id
        print "selected_choice.votes=",selected_choice.votes
        print "url-redirect=",reverse('DemoAppPoll:results',args=(q.id,))   
        return HttpResponseRedirect(reverse('DemoAppPoll:results',args=(q.id,)))
    
```

> 首先,根据问题ID,查找问题,确认为有效问题.

> 然后,根据post信息,判断是哪个选项.

> **投票的票数增加1之后,网页跳转.**

有几个要点:

> 1>**reqest.POST**,类字典型数据(key-value).value总是Strngs

> 2>同理**reqest.GET**可以从GET方法中获取数据.

> 3>**HttpResponseRedirect(url-to-redirect)**,网页跳转,仅带一个参数,那就是要跳转到的网页.
这里

> 4>需要跳转的url,使用了reverse()方法,返回:
```python
"/DemoAppPoll/2/results/" 
```
----


## 处理表单提交--结果显示

提交表单后,跳转到"/DemoAppPoll/2/results/",这个页面还没有显示什么实际的内容.

首先需要确认问题,然后指定模版来处理url:

DemoAppPoll/views.py/[fun]results

```python
def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'DemoAppPoll/results.html', {'question': question})
```
下面就需要编写结果显示的界面:

DemoAppPoll/templates/results.html

```python
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
	"choice.votes|pluralize"={{ choice.votes|pluralize }}
{% endfor %}
</ul>

<a href="{% url 'DemoAppPoll:detail' question.id %}">Vote again?</a>
```

> "choice.votes|pluralize"=s ,单词加复数的方法.
![forms-show-results](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/Django/images/forms-show-results.gif)

---
## 通用viw设计:越少代码越好?

detail(),results(),index(),这三个views里方法,都代表了一个通用的网页开发过程:

* 根据URL参数,从数据库得到数据

* 加载模版,返回渲染后数据.

更为便捷的方法是,使用"generic views":

1. 转换URLconf
2. 删除冗余代码
3. 使用"generic views."

### 1.修改DemoAppPoll/urls.py
```python
from django.conf.urls import patterns,url

from DemoAppPoll import views

urlpatterns = patterns('',
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^(?P<pk>\d+)/$',views.DetailView.as_view(),name='detail'),
    url(r'^(?P<pk>\d+)/results/$',views.ResultsView.as_view(),name='results'),
    url(r'^(?P<question_id>\d+)/vote/$',views.vote,name='vote'),                       
)
```
和之前比较一下:
> 
```python
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
```
使用\<pk>代替了\<question_id>

### 2.修改DemoAppPoll/views.py

```python
from django.views import generic

class IndexView(generic.ListView):
    template_name='DemoAppPoll/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name="DemoAppPoll/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name="DemoAppPoll/results.html"   
```
新导入了包,传入参数也有了变化.
之前是:

```python
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'DemoAppPoll/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'DemoAppPoll/detail.html', {'question': question})

def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'DemoAppPoll/results.html', {'question': question})
```


这里我们使用了2个view:

* ListView
* DetailView

> 1>每一个"geneic view"需要知道所作用的model.

> 2>DetailView需要一个 primary key,(pk,关键字).

> 3>ListView的默认模版是:"app name>/<model name>_list.html"

> 4>DetailView的默认模版是"app name>/<model name>_detail.html."

为了指定模版而不是默认的模版,给变量template_name赋值.

> 5>传递变量: quesiton对象,由于使用了modle:Question,需要另外再次传递.

>  但是,默认提供的的 question_list,我们需要使用的是latest_question_list变量,所以通过
```python
    context_object_name='latest_question_list'
```
这段代码,达到我们的目的.




