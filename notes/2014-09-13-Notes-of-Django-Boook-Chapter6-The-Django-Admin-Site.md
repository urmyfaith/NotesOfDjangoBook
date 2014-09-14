# Django-Boook-Chapter6-The-Admin-Site

---

## Admin是如何工作的

* 当服务启动时，Django从`` url.py`` 引导URLconf，

* 然后执行`` admin.autodiscover()`` 语句。

* 这个函数遍历INSTALLED_APPS配置，并且寻找相关的 admin.py文件。 

* 如果在指定的app目录下找到admin.py，它就执行其中的代码。

----

> SQL有指定空值的独特方式，它把空值叫做NULL。NULL可以表示为未知的、非法的、或其它程序指定的含义。

---


## 字段为空的设置

>**如果你想允许一个日期型（DateField、TimeField、DateTimeField）或数字型（IntegerField、DecimalField、FloatField）字段为空，你需要使用null=True  和* blank=True。**

---
## 自定义字段显示标签

**verbose_name='e-mail'**

```python
class Author(models.Model):
    #salutation = models.CharField(maxlength=10)
    first_name   =    models.CharField(max_length=30)
    last_name   =   models.CharField(max_length=40)
    email =models.EmailField(blank=True,verbose_name='e-mail')
```
可以显示为中文标签,只需要文件编码为utf-8
```python
# _*_ coding: utf-8 _*_
class Author(models.Model):
    ...
    email =models.EmailField(blank=True,verbose_name='电子邮件')
```


