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