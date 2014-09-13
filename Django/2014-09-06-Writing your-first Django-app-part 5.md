# Writing your-first Django-app-part 5 -test

*   确认bug
*   写test测试暴露bug
*   修复bug
*   更多测试例子
*   测试一个view
*  * The Django test client测试客户端.
*  * 提升DemoAppPoll/views.py
*  * 测试我们的view.index
*  * 测试DemoAppPoll/views.py/DetailView
*  测试的技巧:
*  完整的测试文件

## 确认bug
如果传入一个未来的时间,那么was_published_recently()会返回什么?

```python
D:\desktop\todoList\Django\mDjango\demoSite>python manage.py shell
Python 2.7.6 (default, Nov 10 2013, 19:24:18) [MSC v.1500 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> import datetime
>>> from django.utils import timezone
>>> from DemoAppPoll.models import Question
>>> future_question = Question(pub_date=timezone.now()+datetime.timedelta(days=30))
>>> future_question.was_published_recently()
True

```
##写test测试暴露bug
将上述的过程,写成test如下:

***DemoAppPoll/tests.py***

```python
import datetime

from django.test import TestCase
from django.utils import timezone

from DemoAppPoll.models import Question

class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now()+datetime.timedelta(days=30)
        furture_question = Question(pub_date=time)
        self.assertEqual(furture_question.was_published_recently(),False)
```

运行测试:

```python
python manage.py test DemoAppPoll
```

> 1> "python manage.py test DemoAppPoll "从DemoAppPoll(APP)下找tests.

> 2>"**django.test.TestCase**",测试示例,DemoAppPoll作为TestCase参数传入:
```python
class QuestionMethodTests(TestCase):
```

> 3>创建了一个为了测试的特殊的数据库

> 4>assertEqual() 最后来判断.



## 修复bug

***DemoAppPoll/models.py***

```python
def was_published_recently(self):
        now = timezone.now()
        return now-datetime.timedelta(days=1) <=self.pub_date<=now
        #return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```

> 由原来的单边不等式,改为现在的双边不等式即可.

测试结果:
```python
D:\desktop\todoList\Django\mDjango\demoSite>python manage.py test DemoAppPoll
Creating test database for alias 'default'...
.
----------------------------------------------------------------------
Ran 1 test in 0.318s
OK
Destroying test database for alias 'default'...
```

## 更多测试例子

如果是以前的问题?如果是最近的问题?

***DemoAppPoll/tests.py***
```python
    def test_was_published_rencently_with_old_question(self):
        time = timezone.now()-datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(),False)
    def test_was_published_rencently_with_recent_question(self):
        time = timezone.now()-datetime.timedelta(hours=1)
        recent_question=Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(),True)
       
```
----

## 测试一个view


### The Django test client测试客户端.


```python
D:\Documents\mandroid\demoSite>python manage.py shell
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
>>> from django.test import Client
>>> client =Client()
>>> response=client.get('/')
>>> response.status_code
404
>>> from django.core.urlresolvers import reverse
>>> response=client.get(reverse('DemoAppPoll:index'))
>>> response.status_code
200
>>> response.content
'\r\n    <ul>\r\n    \r\n     \r\n\t\t<li><a href="/DemoAppPoll/1/">what&#39;s up </a></li>\r\n    \r\n     \'
>>> from DemoAppPoll.models import Question
>>> from django.utils import timezone
>>> q=Question(question_text="who is your favourite Beatle",pub_date=timezone.now())
>>> q.save()
>>> response=client.get('/DemoAppPoll/')
>>> response.content
'\r\n    <ul>\r\n    \r\n     \r\n\t\t<li><a href="/DemoAppPoll/3/">who is your favourite Beatle</a></li>\r\n
\r\n\t\t<li><a href="/DemoAppPoll/2/">what time is it?</a></li>\r\n    \r\n    </ul>\r\n'
>>> response.context['latest_question_list']
[<Question: who is your favourite Beatle>, <Question: what's up >, <Question: what time is it?>]
>>>

```


### 提升DemoAppPoll/views.py


```python
    def get_queryset(self):
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
```
上面需要
```python
from django.utils import timezone
```

### 测试我们的view.index

```python
def create_question(question_text,days):
    time = timezone.now()+ datetime.timedelta(days=days)
    
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_a_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('DemoAppPoll:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
```
> 还是那几个步骤:

> 1> 导入需要的包:
```python
from django.core.urlresolvers import reverse
```
> 2>编写类,传入TestCase参数

> 3>编写测试方法:a)创建实例,b)模拟请求,c)比较结果



### 测试DemoAppPoll/views.py/DetailView
首先,稍微修改DemoAppPoll/views.py:
```python
class DetailView(generic.DetailView):
    model = Question
    template_name = "DemoAppPoll/detail.html"
    def get_queryset(self):
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now())
   
```
如果有人直接访问DemoAppPoll/xx/,那么,返回空.

下面编写测试:
```python
class QuestionIndexDetailTests(TestCase):#编写类,传入参数TestCase
    #
    def test_detail_view_with_a_future_question(self):
        #编写测试方法
        future_question=create_question(question_text="Future question", days=5)
        #测试场景前提
        response = self.client.get(reverse('DemoAppPoll:detail',args=(future_question.id,)))
        #模拟请求.
        self.assertEqual(response.status_code,404)
        #与预期结果比较.
    def test_detail_view_with_a_past_question(self):
        past_question=create_question(question_text="past question", days=-5)
        response = self.client.get(reverse('DemoAppPoll:detail',args=(past_question.id,)))
        self.assertContains(response,'past question')
```
## 测试的技巧:
    
1. 为每个model/view编写一个单独的测试类方法

2. 为每一种测试条件编写一个单独的测试函数/过程.

3. 测试的函数名称,能够描述这个函数的功能.

-----

## 最后,附上完整的测试文件:

demoSite/DemoAppPoll/tests.py

```python
# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase
from django.utils import timezone
from DemoAppPoll.models import Question
from django.core.urlresolvers import reverse


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        furture_question = Question(pub_date=time)
        self.assertEqual(furture_question.was_published_recently(), False)
    def test_was_published_rencently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)
    def test_was_published_rencently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)

def create_question(question_text,days):
    time = timezone.now()+ datetime.timedelta(days=days)
    
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_question(self):
        response = self.client.get(reverse('DemoAppPoll:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    def test_index_view_with_a_past_question(self):
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse("DemoAppPoll:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], 
                                 ['<Question: Past question>']
                                 )
    def test_index_view_with_a_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('DemoAppPoll:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('DemoAppPoll:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('DemoAppPoll:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
class QuestionIndexDetailTests(TestCase):#编写类,传入参数TestCase
    #
    def test_detail_view_with_a_future_question(self):#编写测试方法
        future_question=create_question(question_text="Future question", days=5)#测试场景前提
        response = self.client.get(reverse('DemoAppPoll:detail',args=(future_question.id,)))#模拟请求.
        self.assertEqual(response.status_code,404)#与预期结果比较.
    def test_detail_view_with_a_past_question(self):
        past_question=create_question(question_text="past question", days=-5)
        response = self.client.get(reverse('DemoAppPoll:detail',args=(past_question.id,)))
        self.assertContains(response,'past question')
    
```

