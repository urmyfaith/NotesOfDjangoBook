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