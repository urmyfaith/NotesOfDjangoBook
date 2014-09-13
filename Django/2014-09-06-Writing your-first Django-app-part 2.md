# Writing your first Django app, part 2

## 创建admin用户

```python
D:\desktop\todoList\Django\mDjango\demoSite>python manage.py createsuperuser

```

然后输入密码

## 进入admin网址

```python
    D:\desktop\todoList\Django\mDjango\demoSite>python manage.py runserver 8080
```

## 改变字段顺序

* fileds 改变字段的顺序

* fieldset 给字段分组

* classes  折叠字段

* serch_fields 添加搜索框

* list_display 需要显示的字段


```python
from django.contrib import admin
from DemoAppPoll.models import Choice,Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #fields=['pub_date','question_text']
    fieldsets=[
        (None,              {'fields':['question_text']}),
        ('Date infomation', {'fields':['pub_date'],'classes':['collapse']}),
        ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    
#admin.site.register(Question)
admin.site.register(Question,QuestionAdmin)
#admin.site.register(Choice)

```