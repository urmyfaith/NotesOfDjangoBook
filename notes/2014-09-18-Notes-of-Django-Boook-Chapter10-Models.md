#Chapter10-models

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

