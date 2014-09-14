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
----

##管理界面-表-显示字段的设置:

>1.>继承类

>2.>需要显示字段赋值给list_dispaly

>3.>注册刚才编写的类.

```python
from django.contrib import admin
from books.models import Author,Publisher,Book

class AuthorAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','email')
admin.site.register(Publisher)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Book)

```
---

##管理界面-表-字段可搜索:

上面添加的是list_display,这里添加:search_fields
```python
search_fields = ('first_name', 'last_name')
```
![search_fields.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/search_fields.png)

---
##管理界面-表-按时间筛选:

添加**list_filter**
```python
    list_filter=('publication_date',)
```
![list_filter.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/list_filter.png)

添加**date_hierarchy**
```python
date_hierarchy = 'publication_date'
```
![date_hierarchy.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/date_hierarchy.png)

添加**ordering**
```python
ordering = ('-publication_date',)
``` 
![ordering.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/ordering.png)


## 管理界面-表- 多对多字段

* filter_horizontal 水平筛选
 
* filter_vertical  垂直筛选

* raw_id_fields  原始id字段

> 使用filter_horizontal默认显示所有的记录,这样页面加载很慢,所以配合raw_id_fields,弹窗选择id.


```python
class BookAdmin(admin.ModelAdmin):
    list_display=('title','publisher','publication_date')
    list_filter=('publication_date',)
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    filter_horizontal = ('author',)
    raw_id_fields = ('publisher',)
```
![filter_horizontal.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/filter_horizontal.png)

![raw_id_fields.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/raw_id_fields.png)
