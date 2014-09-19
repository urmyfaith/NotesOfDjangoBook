#Chapter10-models


* 访问多对多(Many-to-Many Values)
* 添加字段
* Managers
* 修改初始Manager QuerySets
* 模型方法
* 访问数据库:
* 将数据库操作放在自定义models或者manager中...

## book model

![books_model_view.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/books_model_view.png)

```python
>>> from books.models import *
>>> b = Book.objects.get(id=2)
>>> b.title
u'A History of the Classical Greek World'
>>> b.author
<django.db.models.fields.related.ManyRelatedManager object at 0x027541F0>
>>> b.publisher
<Publisher: O'Reilly>
>>> b.publication_date
datetime.date(2014, 9, 14)
```

## 访问外键(Foreign Key)

```python
# books.models.py
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField(blank=True, null=True)
    
    def __unicode(self):
        return self.title
```
可以看到publisher设置了一个外键,是一个Publisher对象.
```python
>>> b = Book.objects.get(id=2)
>>> b.publisher
<Publisher: O'Reilly>
>>> b.publisher.website
u'http://www.oreilly.com/'
```
> 注意到,用b.publisher.website访问了Publisher对象的字段.

从ForeignKey的另外一面访问:
```python
>>> p = Publisher.objects.get(name="O'Reilly")
>>> p.book_set.all()
[<Book: Book object>]
>>> p.book_set.filter(title__icontains='world')
[<Book: Book object>]
```

> **book_set 只是一个 QuerySet**

---
## 访问多对多(Many-to-Many Values)

直接使用 b.author.all()

或者使用filter对结果筛选:

```python
>>> b=Book.objects.get(id=2)
>>> b.author.all()
[<Author: Tom Acer>]
>>> b.author.filter(first_name='Tom')
[<Author: Tom Acer>]
>>> b.author.filter(first_name='cat')
[]
>>>
```
反查询:
```python
>>> a = Author.objects.get(first_name='Tom')
>>> print a
Tom Acer
>>> type(a)
<class 'books.models.Author'>
>>> a.book_set.all()
[<Book: Book object>, <Book: Book object>]
>>>
```
> 这里,就像使用 ForeignKey字段一样，

> 属性名book_set是在数据模型(model)名后追加_set。

![Book_Author_Publisher.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/Book_Author_Publisher.png)


----
## 添加字段

1) 在models.py添加字段:
```python
class Book(models.Model):
    ...
    num_pages = models.IntegerField(blank=True, null=True)
```
2) 执行 python manager.py makemigrations

3) 执行python manager.py migrate

----
## Managers

> 在语句Book.objects.all()中，objects是一个特殊的属性，需要通过它查询数据库。

> 模块manager是一个对象，

>  Django模块通过它进行数据库查询。 

> 每个Django模块至少有一个manager

> 可以创建自定义manager以定制数据库访问

## 增加额外的Manager方法

为什么要增加Manager方法?

*  增加额外的manager方法，
*  修改manager返回的初始QuerySet

```python
# /mysite/books/models.py

class BookManager(models.Manager):
    def title_count(self,keyword):
        return self.filter(title__icontains=keyword).count()
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField(blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    objects=BookManager()    
    
    def __unicode(self):
        return self.title
```
可以看到:

1) 我们定义了一个新的类"BookManager",类的参数是:"**models.Manager**"其中包含一个方法"title_count".

2) 在title_count()方法里,使用了self,这self指的是Manager对象本身.

在方法里,通过数据库筛选,返回了包含关键字的结果集的数量.

3) 在Book类里,我们将上面定义的BookManager类,赋值给了***objects***变量.

这样,我们就可以通过bojects来访问title_count()方法了:

```python
..\NotesOfDjangoBook\mysite>python manage.py shell
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from books.models import *
>>> Book.objects.title_count('the')
1
>>>
```
4 ) 注意,上面两个类的先后顺序:先定义BookManager类,然后是在Book类中使用.

---
## 修改初始Manager QuerySets

> 我们可以通过覆盖Manager.get_query_set()方法来重写manager的基本QuerySet。 

```python
# /mysite/books/models.py
class BookManager(models.Manager):
    def title_count(self,keyword):
        return self.filter(title__icontains=keyword).count()
class OneBookManager(models.Manager):
    def get_query_set(self):
        return super(OneBookManager,self).get_query_set().filter(title__icontains='the')
        #return self.get_query_set().filter(title__icontains='the')
class Book(models.Model):
    ...
    objects=models.Manager()
    oneBook_objects=OneBookManager()
    ...
```
可以看到,上面有两个Manager类,其中一个赋值给了默认的objects,另外一个赋值给了oneBook_objects.

那么在使用的时候,就有两个Manager对象(objects,oneBook_objects)可用:
```python
>>> from books.models import *
>>> Book.oneBook_objects.all()
[<Book: Book object>]
>>> Book.oneBook_objects.filter(title__contains='the')
[<Book: Book object>]
>>> Book.oneBook_objects.count()
1
>>> Book.objects.all()
[<Book: Book object>, <Book: Book object>]
>>>
```

-----
## 模型方法

> 可以给model添加一些方法,例如:

```python
# /mysite/books/models.py
class Author(models.Model):
    first_name   =    models.CharField(max_length=30)
    last_name   =   models.CharField(max_length=40)
    email =models.EmailField(blank=True,verbose_name='e-mail')
    def _get_full_name(self):
        "Returns the Author's full name."
        return u'%s %s' % (self.first_name, self.last_name)
    full_name=property(_get_full_name)
 
>>> from books.models import *
>>> a = Author.objects.get(email="autumn528@gmail.com")
>>> a.full_name
u'Tom Acer'
>>>
```
---
## 访问数据库:

1)导入 djangod.db.connection

2)从连接获取游标

3) 执行sql语句,得到结果集.

4) 处理结果集(得到一行,打印输出.)
```python
>>> from django.db import connection
>>> c = connection.cursor()
>>> c.execute('''
... select distinct first_name
... from books_author
... where last_name=%s''',['Acer'])
<django.db.backends.sqlite3.base.SQLiteCursorWrapper object at 0x029246B8>
>>> row = c.fetchone()
>>> print row
(u'Tom',)
>>>
```


### 将数据库操作放在自定义models或者manager中...

```python
# /mysite/books/models.py
class  AuthorManager(models.Manager):
    def first_names(self,last_name):
        cursor = connection.cursor()
        cursor.execute('''
                SELECT DISTINCT first_name
                FROM books_author
                WHERE last_name=%s''',[last_name])
        return [row[0] for row in cursor.fetchone()]

class Author(models.Model):
    first_name   =    models.CharField(max_length=30)
    last_name   =   models.CharField(max_length=40)
    email =models.EmailField(blank=True,verbose_name='email')
    def __unicode__(self):
        return u'%s %s' % (self.first_name,self.last_name)
    def _get_full_name(self):
        "Returns the Author's full name."
        return u'%s %s' % (self.first_name, self.last_name)
    full_name=property(_get_full_name)
    objects=models.Manager()
    m_objects=AuthorManager()
```
> 让我们看看上面的代码:

1) 又定义了一个新的Manager类,在里面包含了一个方法first_names(),

用于根据last_name查询数据库,返回一个first_name.

2) 注意:在查询语句里,我们使用的是参数,而不是直接把last_name包含进去.这里会有一个转义.

3) 在Author类里面,有两个Manager.

一个是默认的,我们给予了明确的指定:" objects=models.Manager()"

第二个是新建的,命名为m_objects.

4) 下面是如何使用的示例:

```python
 (InteractiveConsole)
>>> from books.models import *
>>> Author.m_objects.first_names('Acer')
[u'T']
       
```


