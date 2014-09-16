# _*_ coding: utf-8 _*_

from django.db import models

class blog(models.Model):
    subject = models.CharField(max_length=30)
    author = models.CharField(max_length=20)
    content = models.CharField(max_length=1000)
    post_time=models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return self.subject

    
    
