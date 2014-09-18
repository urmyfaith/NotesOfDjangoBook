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

