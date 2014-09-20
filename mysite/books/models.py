# _*_ coding: utf-8 _*_

from django.db import models,connection

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    
    def __unicode__(self):
        return self.name
class  AuthorManager(models.Manager):
    def first_names(self,last_name):
        cursor = connection.cursor()
        cursor.execute('''
                SELECT DISTINCT first_name
                FROM books_author
                WHERE last_name=%s''',[last_name])
        return [row[0] for row in cursor.fetchone()]

class Author(models.Model):
    #salutation = models.CharField(maxlength=10)
    first_name   =    models.CharField(max_length=30)
    last_name   =   models.CharField(max_length=40)
    email =models.EmailField(blank=True,verbose_name='电子邮件')
    last_accessed = models.DateTimeField(blank=True, null=True)
    #headshot = models.ImageField(upload_to='/tmp')
    def __unicode__(self):
        return u'%s %s' % (self.first_name,self.last_name)
    def _get_full_name(self):
        "Returns the Author's full name."
        return u'%s %s' % (self.first_name, self.last_name)
    full_name=property(_get_full_name)
    objects=models.Manager()
    m_objects=AuthorManager()
    
class BookManager(models.Manager):
    def title_count(self,keyword):
        return self.filter(title__icontains=keyword).count()
class OneBookManager(models.Manager):
    def get_query_set(self):
        return super(OneBookManager,self).get_query_set().filter(title__icontains='the')
        #return self.get_query_set().filter(title__icontains='the')
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField(blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    objects=models.Manager()
    oneBook_objects=OneBookManager()
    
    def __unicode(self):
        return self.title
    
    
