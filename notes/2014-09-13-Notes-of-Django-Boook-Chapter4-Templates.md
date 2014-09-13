# Django-Boook-Chapter4-Templates



---
## 模版可以在view中使用,也可以单独使用

单独使用:
```python
from django import template
t=template.Template("my name is {{name}}.")
print t
c=template.Context({'name':'zx'})

print t.render(c)
```

```python
>>>from django.template import Context,Template
>>>t=Template("my name is {{name}}")
>>>c=Context({"name":'zx'})
>>>t.render(c)
u'my name is zx'
```

> t.render(c)返回的值是一个Unicode对象，不是普通的Python字符串。

----

## 使用同一模板源渲染多个context

```python
from django.conf import settings
from django import template

settings.configure()
t=template.Template("hello,{{name}}.")

for name in ('John','Julie','Pat'):
    print t.render(template.Context({'name':name}))

'''
>>> 
hello,John.
hello,Julie.
hello,Pat.
'''
```

----
## 句点查找规则

 当模板系统在变量名中遇到点时，按照以下顺序尝试进行查找：

1. 字典类型查找 （比如 foo["bar"] )

2. 属性查找 (比如 foo.bar )

3. 方法调用 （比如 foo.bar() )

4. 列表类型索引查找 (比如 foo[bar] )

```python
from django.conf import settings
from django import template
settings.configure()

person={'name':'zx','age':'100'}
t=template.Template('{{ person.name.upper }} is {{person.age}} years old.}')
c = template.Context({'person':person})
print t.render(c)
'''
>>>
ZX is 100 years old.
'''
```
---

## python和Django的真值:

在Python和Django模板系统中，以下这些对象相当于布尔值的False

- 空元组(() )

- 空字典({} )

- 空字符串('' )

- 零值(0 )

- 特殊对象None

- 对象False（很明显）

- 提示：你也可以在自定义的对象里定义他们的布尔值属性(这个是python的高级用法)。

---

## Templates里for可以反向迭代

```python
from django.conf import settings
from django import template

settings.configure()
t=template.Template("{% for p in person_list reversed %} <li>{{p}}></li>{% endfor %}")
name_list=['AAA','BBB','CCC']
print t.render(template.Context({'person_list':name_list}))

'''
>>> 
<li>CCC></li> <li>BBB></li> <li>AAA></li>
'''
```
----

##  Templates里for里有empty判断是否为空

```python
from django.conf import settings
from django import template

settings.configure()
t=template.Template('''
{% for p in person_list  %} 
    <li>{{p.name}}></li>
     {% empty %}
     <p>NO Persosn.</p>
{% endfor %}''')

c =template.Context({'person_list': [{'name': 'personA_name'},
                                     {'name': 'personB_name'}]})
print t.render(c)
'''
>>> 
<li>personA_name></li> <li>personB_name></li>
'''
```
> 如果为空,那么输出No Person.

----

## Templates里for里有forloop.count,forloop.first,forloop.last

* forloop.count,循环计数器
* forloop.first,第一次开始循环(布尔值)
* forloop.last,最后一次循环.(布尔值)

```python
from django.conf import settings
from django import template
settings.configure()

t=template.Template('''
{% for link in links %} {{forloop.counter}}-->{{link}} {% if not forloop.last%}|{% endif %}{% endfor %}''')
links=['LinkA','LinkB','LinkC','LinkD']
c =template.Context({'links':links})
print t.render(c)

'''
>>> 
 1-->LinkA | 2-->LinkB | 3-->LinkC | 4-->LinkD 
'''
```

> ```python
{% for link in links %}
    {{link}} 
    {% if not forloop.last%}
        |
    {% endif %}
{% endfor %}
```

##  模版里的注释:
* 单行注释:
    {# This is a comment #}
* 多行注释:

```python

{% comment %}
This is a
multi-line comment.
{% endcomment %}

```

## 模版中变量的过滤器

**过滤器的作用是,在输出变量值前,对变量进行一些预处理**

* 比如字符串的截取

* 比如大小写的转换

* 比如时间格式的的转换.

```python
# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
settings.configure()

t=template.Template('''
{% for link in links %}
    {{ link}}
    {{ link|lower }}{# Upcase,Lowercase#}
    {{ link|first|upper }}
    {{ link|truncatewords:"3" }}
    {{ link|slice:"3" }}
{% endfor %}
''')
links=['linkA is a link .',u'我是中国人,我爱自己的祖国,你呢?是那国人?']
c =template.Context({'links':links})
print t.render(c)

'''
    linkA is a link .
    linka is a link .
    L
    linkA is a ...
    lin

    我是中国人,我爱自己的祖国,你呢?是那国人?
    我是中国人,我爱自己的祖国,你呢?是那国人?
    我
    我是中国人,我爱自己的祖国,你呢?是那国人?
    我是中
'''
```
>```python
    {{ link}}  直接输出变量值
    {{ link|lower }}{# Upcase,Lowercase#}英文字母的大小写转换
    {{ link|first|upper }} 取出第一个字符,大写.
    {{ link|truncatewords:"3" }}取出前三个单词
    {{ link|slice:"3" }}取出前三个字符(字符,中文字符)
```

----

## 使用templates目录

### 使用HttpResponse

修改settings,添加mysite

```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mysite'
)
```


修改**view.py**
```python
from django.http import HttpResponse,Http404
import datetime
from django.template.loader import get_template
from django.template import Context

def current_datetime(request):
    now = datetime.datetime.now()
    t=get_template('current_datetime.html')
    html=t.render(Context({'current_date':now}))
    return HttpResponse(html)
```
### 使用render_to_response简化代码:

使用render_to_response简化代码来代替使用HttpResponse.
```python
from django.shortcuts import render_to_response
def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_date':now})
    #return HttpResponse(html)
```

注意,这里的导入包变化了很多:
不需要

```python
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
```
取而代之的是:
```python
from django.shortcuts import render_to_response
```

## templates目录下,可以再创建目录来分离整理各个文件

**NotesOfDjangoBook\mysite\mysite\templates\current_datetime.html**

```python
return render_to_response('current_datetime.html',{'current_date':now})
```

新建目录date,然后移入文件进入:

**NotesOfDjangoBook\mysite\mysite\templates\date\current_datetime.html**

```python
return render_to_response('date/current_datetime.html',{'current_date':now})

```

## 模版继承

包含的方法:

include的方法:
```python
{% include 'nav.html' %}
{% include "nav.html" %}
{% include 'includes/nav.html' %}
{% include template_name %}   #变量名template_name
```

> **模版继承**是先分块,然后extends(继承),覆盖/重写的方法.

将页面分成多个块的方法:

```python
# base.html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <h1>My helpful timestamp site</h1>
    {% block content %}{% endblock %}
    {% block footer %}
    <hr>
    <p>Thanks for visiting my site.</p>
    {% endblock %}
</body>
</html>
```

> * 标题块
> * 内容块
> * 底部块

使用继承的方法,NotesOfDjangoBook\mysite\mysite\templates\base.html,可以重写为:
```python
{% extends "base.html" %}

{% block title %}The current time{% endblock %}

{% block content %}
<p>It is now {{ current_date }}.</p>
{% endblock %}
```

> **{% extends %} 的参数应该是字符串，但是如果直到运行时方能确定父模板名，这个参数也可以是个变量。这使得你能够实现一些很酷的动态功能。**

