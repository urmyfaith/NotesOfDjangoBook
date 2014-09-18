#Chapter8-Views-URLconfs

*   导入视图函数-->导入视图所在包,通过包访问函数.
*    导入视图函数-->直接通过app.package.func访问函数:
*   patterns() 对象相加
*   patterns() 对象相加更进一步的优化:
*     命名组(Named Groups)(?P\<name>pattern) 
*     传递额外的参数到视图函数中
*   伪造捕捉到的URLconf值
*     创建一个通用视图
*     使用默认的视图参数
*     关于URL的匹配的说明:
*     请求方法分支的讨论
*     请求方法分支的讨论 - 带参数的请求分支
*     函数的参数,动态参数,关键字参数
*     每个页面的认证:封装视图函数
*     Include的用法:

-----

## urls.py 导入包的优化:

URLconfs的patterns里url的第二个参数接收的是代表一个视图的函数,如下:

```python

# urls.py

from django.conf.urls import patterns, include, url
from mysite.views import hello, \ 
    current_datetime, hours_ahead, \
    show_request, \ 
    search_form,show_search_result
from mysite.sendMailViewByForms import contact,contact_thanks
urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$',hello),
    url(r'^time/$',current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^request-info/$',show_request),
    url(r'^search-form/$',search_form),
    url(r'^search/$',show_search_result),
    url(r'^contact/$',contact),
    url(r'^contact/thanks/$',contact_thanks),                  
)
```

### 导入视图函数-->导入视图所在包,通过包访问函数.

**通过导入视图所在包,来访问视图函数.**

 ```python
from mysite import views
urlpatterns = patterns('',
    ...
    #url(r'^hello/$',hello),
    url(r'^hello/$',views.hello),
    ...
```
![import_package_instead_of_func.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/import_package_instead_of_func.png)


### 导入视图函数-->直接通过app.package.func访问函数:
```python
from django.conf.urls import *
urlpatterns = patterns('',
...
    url(r'^contact/$','mysite.sendMailViewByForms.contact'),
    url(r'^contact/thanks/$','mysite.sendMailViewByFormscontact_thanks'), 
...                 
)
```
> 注意:这里有些改变:
1) 导入包从"from django.conf.urls import patterns, include, url"改为了"from django.conf.urls import *"

2) 没有导入sendMailViewByForms包,而是直接使用了**带引号的**mysite.sendMailViewByForms.contact来访问函数.

*(ps.如果不带引号,就会找不到包,也就找不到函数.)*

### patterns() 对象相加

```python
#urls.py
from django.conf.urls import *
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact/$','mysite.sendMailViewByForms.contact'),
    url(r'^contact/thanks/$','mysite.sendMailViewByForms.contact_thanks'),                  
)
urlpatterns += patterns('mysite.views',
    url(r'^hello/$','hello'),
    url(r'^time/$','current_datetime'),
    url(r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
    url(r'^search/$','show_search_result'),
    url(r'^request-info/$','show_request'),
    url(r'^search-form/$','search_form'),
)
```
> 注意:

1) 这里的两个patterns()相加了
2) 后面的将会查找的是'mysite.views.hello'等,

他们有一个公共的前缀,这里提取出来了.

3) 不导入包的话,**后面的实际视图函数名称,使用了单引号.**

### patterns() 对象相加更进一步的优化:

利用上面的,可以更进一步优化URLconfs
```python
#urls.py
from django.conf.urls import *
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('mysite.sendMailViewByForms',
    url(r'^contact/$','contact'),
    url(r'^contact/thanks/$','contact_thanks'),                  
)
urlpatterns += patterns('mysite.views',
    url(r'^hello/$','hello'),
    url(r'^time/$','current_datetime'),
    url(r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
    url(r'^search/$','show_search_result'),
    url(r'^request-info/$','show_request'),
    url(r'^search-form/$','search_form'),
)
```
> 小结:**一个view文件里的视图函数可以提取出前缀,相加后返回.**

---

## 命名组(Named Groups)(?P\<name>pattern) 
如果不使用命名组,是这样的:
URLconf可能是:
```python
#urls.py
urlpatterns += patterns('mysite.articlesViews',
    (r'^articles/(\d{4})/$', 'year_archive'),
    (r'^articles/(\d{4})/(\d{2})/$','month_archive'),
)
```
view可能是:
```python
#articlesViews.py
from django.http import HttpResponse

def year_archive(request,year):
    rawHtml='<html><head></head><body>year_archive:%s</body></html>'% year
    return HttpResponse(rawHtml)
def month_archive(request,year,month):
    rawHtml='<html><head></head><body>year_archive:%s-%s</body></html>'% (year,month)
    return HttpResponse(rawHtml)
```
> 这样的话,在URL里的参数,传递到视图中去的时候,是按**顺序传递**:
articles/(\d{4})/(\d{2})/    -->    articles/year/month/

如果我们使用命名组的话,它的形式是这样的:**(?P\<name>pattern)**

```python
#urls.py
urlpatterns += patterns('mysite.articlesViews',
    (r'^articles/(?P<year>\d{4})/$', 'year_archive'),
    (r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$','month_archive'),
)
```
相应的,视图中,我们可以这样写:
```python
#articlesViews.py
from django.http import HttpResponse
def year_archive(request,year):
    rawHtml='<html><head></head><body>year_archive:%s</body></html>'% year
    return HttpResponse(rawHtml)
def month_archive(request,month,year):
    rawHtml='<html><head></head><body>year_archive:%s-%s</body></html>'% (year,month)
    return HttpResponse(rawHtml)
```
> 注意:

1) 在URLconf中,使用了命名组的方式,即第一个位置命名为year,第二个位置命名为month

2) 在view文件,month_archive视图中的参数,我们故意颠倒了位置.


**小结:** 使用命名组,可以很好的说明参数位置所代表的意义,也可以防止顺序颠倒带来的错误.

![named_groups_month_year.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/named_groups_month_year.png)

----
## 传递额外的参数到视图函数中

从上面的命名组中可以看到,URLconf可以传递参数到View中.
那么怎么传递额外的参数到视图中?

假设,有两个url,分别匹配到两个视图,但是**它们使用不同的模版来渲染.**
```python
#urls.py
urlpatterns += patterns('mysite.foobar_view',
    (r'^chapter8_url_view/pass_extra_options_to_view/foo/$','foo_view'),
    (r'^chapter8_url_view/pass_extra_options_to_view/bar/$','bar_view'),
)

#foobar_view.py
from django.shortcuts import render
from books.models import Book
def foo_view(request):
    books = Book.objects.filter(title__icontains='world')  
    return render(request,'foobar/foo.html',{'books':books})
def bar_view(request):
    books = Book.objects.filter(title__icontains='the')
    return render(request,'foobar/bar.html',{'books':books})

```
这样村的问题:功能机会相同,只是渲染的模版不一样.

我们可以使用传递额外的参数到view中去,动态的指定渲染模版:

```python
#urls.py
urlpatterns += patterns('mysite.foobar_view',
    (r'^chapter8_url_view/pass_extra_options_to_view/foo/$', \
     'foo_bar_view',{'template_name':'foobar/foo.html','search_str':'world'}),
    (r'^chapter8_url_view/pass_extra_options_to_view/bar/$', \
     'foo_bar_view',{'template_name':'foobar/bar.html','search_str':'the'}),
)
#foobar_view.py
def foo_bar_view(request,template_name,search_str):
    books=Book.objects.filter(title__icontains=search_str)
    return render(request,template_name,{'books':books})
```
1) 在urls.py的patterns里,使用的第三个参数:传入了一个字典.

这个字典会从URLconf传入到视图中.

2) 在视图里,将两个视图函数合并为一个,使用字典参数,这样就是多个不同的视图.

3)达到:动态指定模版,动态指定一些变量的值(几个值之间选择).

![foo_bar_view.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/foo_bar_view.png)
---

### 伪造捕捉到的URLconf值

> **你有匹配某个模式的一堆视图，以及一个并不匹配这个模式但视图逻辑是一样的URL**

怎么解决这个问题?

使用 命名组(Named Groups) + 传递额外的参数到视图函数中 上面的两种方法结合来做.

```python

#urls.py
urlpatterns += patterns('mysite.articlesViews',
    url(r'^chapter8_url_view/fake_captured_URLconf_values/articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$','day_archive'),
    url(r'^chapter8_url_view/fake_captured_URLconf_values/articles/birthday/$','day_archive',{'year':'2014','month':'09','day':'16'}),
)

#articlesViews.py
def day_archive(request,month,year,day):
    rawHtml='<html><head></head><body>day_archive:%s-%s-%s</body></html>'% (year,month,day)
    return HttpResponse(rawHtml
```
这样,第一个URL匹配模式,匹配一系列的日期

第二个URL虽然结构不同,但是它匹配到了同一个视图中去.

![fake_captured_URLconf_values.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/fake_captured_URLconf_values.png)

---

## 创建一个通用视图

需求:比如这个视图显示一系列blog对象,那个视图显示一系列book对象:
如:
```python
#urls.py
urlpatterns += patterns('mysite.objectView',
    url(r'^chapter8_url_view/make_a_view_generic/blog/$','blog_list'),
    url(r'^chapter8_url_view/make_a_view_generic/book/$','book_list'),
)

#objectView.py
from django.shortcuts import render_to_response
from books.models import Book
from blog.models import blog
def blog_list(request):
    blog_list=blog.objects.all()
    return render_to_response('make_a_view_generic/blog_list.html',{'blogs':blog_list})
def book_list(request):
    book_list=Book.objects.all()
    return render_to_response('make_a_view_generic/book_list.html',{'books':book_list})

#make_a_view_generic/book_list.html
<table width="600" border="0" bgcolor="blue" bordercolor="black" cellpadding="5" cellspacing="1">
		<tr bgcolor="white"  > 
			<td>#</td>   
			<td> subject </td>
			<td>author </td>
			<td>content </td>
			<td>post_time </td>
		</tr>
        {% for blog in blogs %}
		<tr bgcolor="white" > 
			<td>{{ forloop.counter }}</td>   
			<td>{{ blog.subject }}</td>
			<td>{{ blog.author }}</td>
			<td>{{ blog.content }}</td>
			<td>{{ blog.post_time }}</td>
		</tr>
        {% endfor %}
	</table>
```

可以看到,我们在objectView.py里定义了两个视图,那么怎么样才能只是用一个视图呢?

```python
#urls.py
from books.models import Book
from blog.models import blog
urlpatterns += patterns('mysite.objectView',
    url(r'^chapter8_url_view/make_a_view_generic/blog/$','object_list',{'model':blog}),
    url(r'^chapter8_url_view/make_a_view_generic/book/$','object_list',{'model':Book}),
)

#objectView.py
def object_list(request,model):
    obj_list=model.objects.all()
    key_name=model.__name__.lower()
    template_name='make_a_view_generic/%s_list.html' % key_name
    key_name=key_name+'s'
    return render_to_response(template_name,{key_name:obj_list})
```

> 如上:

1) 在URLconf里使用了同一个视图函数object_list

2) 使用了额外的参数,从URLconf传递到视图函数,(见上面的*传递额外的参数到视图函数中*)

3) 如果模版不同

a) 可以像上面使用类的名字
b) 可以使用额外参数指定

4) 像上面的,完全可以使用同一个模版来渲染.

-----

## 使用默认的视图参数

> 如果访问 'www.abc.com/blog/',那么我们希望默认显示的是第一个页博客,如果访问'www.abc.com/blog/page3',那么我们显示第三页博客.

> 然而,第一页和第三页博客的显示方法应该一样的,也就是使用同一个view视图函数来实现,那么怎么实现这个呢?

我们使用默认的视图函数参数来实现:
```python
#urls.py
urlpatterns += patterns('mysite.blogPageView',
    url(r'^chapter8_url_view/use_default_view_arguments/blog/$','show_blog_page'),
    url(r'^chapter8_url_view/use_default_view_arguments/blog/page(?P<num>\d+)/$','show_blog_page')
from django.http import HttpResponse

#blogPageView.py
def show_blog_page(request,num='1'):
    rawHtml='<html><head></head><body>you are at page:%s.</body></html>'% num
    return HttpResponse(rawHtml)
```
可以看到,

1) 在URLconfs里,使用了同一个视图函数:'mysite.blogPageView.show_blog_page'

2) 在视图里,我们使用了一个参数num,但是它被赋予了一个默认的值1.

3) 这样,在访问第一个URL的时候,将使用默认参数.在访问第二个URL的时候,num的值将是从URL里提取出来的.
 

>4) **但是**,如果使用额外的参数,从URLcongs里传递到视图,num的值

> 以字典里的为准,而不是从URL里捕捉到.

例如:
```python
urlpatterns = patterns('',
    (r'^mydata/(?P<id>\d+)/$', views.my_view, {'id': 3}),
)
```

**在视图里,id的值将会永远是3,而不管URL里捕捉到的值.**

![use_default_view_arguments.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/use_default_view_arguments.png)

----

## 关于URL的匹配的说明:

URL匹配的时候,

1) 不会区分get,post,head,等方法,

2) 不会去匹配post参数:

例如,对于"www.example.com/myapp/?page=3 ",只会去匹配到'myapp/'

3) 匹配到patterns里的一行后,不再往下匹配. (**短路逻辑**)
```python
urlpatterns = patterns('',
    # ...
    ('^auth/user/add/$', views.user_add_stage),
    ('^([^/]+)/([^/]+)/add/$', views.add_stage),
    # ...
)
```
即上面的patterns,'auth/user/add/'将会匹配到第一行,而不是第二行.

4) 从URL里使用命名组的参数的值都是字符串

例如:
```python
    url(r'^chapter8_url_view/fake_captured_URLconf_values/articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$','day_archive'),
```
year,month,day将都是字符串,而不是整数!

---

## 请求方法分支的讨论

在上面一章里,有个通过填写表单发送邮件的例子:

```python

# mysite\mysite\sendMailViewByForms.py
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email','urmyfaith@qq.com'),
                ['1278908611@qq.com','904312072@qq.com'],
                )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        #GET Method ---default visite site method.
        form = ContactForm(initial={'subject': 'I love your site!'})
    return render_to_response('contact_formByForms.html',{'form': form},context_instance=RequestContext(request))

```
访问"[ip]:/contact/"url的时候,通过contact()方法来处理.

* 如果是POST请求方法访问,那么取出表单数据,发送邮件,页面重定向

* 如果是GET方法访问,那么初始化表单,渲染页面后输出.

将上面的代码概括一下:
```python
def some_page(request):
    if request.method == 'POST':
        do_something_for_post()
        return HttpResponseRedirect('/someurl/')
    elif request.method == 'GET':
        do_something_for_get()
        return render_to_response('page.html')
    else:
        raise Http404()
```

在上面的例子中,这两种请求方法被写在了一起,如果对每一种请求方法都很复杂,

那么,将两种请求放在一个view函数里写就不适合了,考虑分开两个视图来编写.

现在问题是,怎么样实现使用两个视图来编写?

```python

#urls.py
from mysite import sendMailViewByForms
##urlpatterns += patterns('mysite.sendMailViewByForms',
##    url(r'^contact/$','contact'),
##    url(r'^contact/thanks/$','contact_thanks'),                  
##)

urlpatterns += patterns('',
    url(r'^contact/$',sendMailViewByForms.method_splitter, \
        {'GET_method':sendMailViewByForms.get_contact, \
         'POST_method':sendMailViewByForms.post_contact}),
    url(r'^contact/thanks/$',sendMailViewByForms.contact_thanks),                  
)
#sendMailViewByForms.py
def method_splitter(request,GET_method=None,POST_method=None):
    if request.method =='POST' and POST_method is not None:
        return POST_method(request)
    elif request.method == 'GET' and  GET_method is not None:
        return GET_method(request)
    raise Http404

def get_contact(request):
    assert request.method == 'GET'
    form = ContactForm(initial={'subject': 'amazing site!'})
    return render_to_response('contact_formByForms.html',{'form': form},context_instance=RequestContext(request))

def post_contact(request):
    assert request.method == 'POST'
    form = ContactForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        send_mail(
            cd['subject'],
            cd['message'],
            cd.get('email','urmyfaith@qq.com'),
            ['1278908611@qq.com','urmyfaith@qq.com'],         
            )
        print 'send_mail_sucess'
        return HttpResponseRedirect('/contact/thanks/')
    return HttpResponseRedirect('/contact/')

```

> 让我们来看看怎么实现的:

1) 在patterns里,我们把'contact/',匹配了视图函数method_splitter(),但是,传入了两个参数.

2) 这两个参数值不是普通的字符串对象,而是一个view对象.

也就是说,我们把view对象,当作了一个参数的值.

3) 在method_splitter()方法里,设置了两个默认参数,进行if判断.

4) 通过参数名(代表一个view对象:sendMailViewByForms.py里的一个函数),调用相应的get/post视图函数

5) 在两个独立的视图函数里分别编写post和get请求时,具体要做的内容.

(PS,虽然显示了thanks界面,但是没有收到邮件,还以为是哪里出错了,看来一集看是回来,收到了好几封邮件.冏.)

----
## 请求方法分支的讨论 - 带参数的请求分支

上面的分支请求,没有处理请求带额外参数的情况,那么如果带参数,该怎么处理呢?

```python
#sendMailViewByForms.py

##def method_splitter(request,GET_method=None,POST_method=None):
##    if request.method =='POST' and POST_method is not None:
##        return POST_method(request)
##    elif request.method == 'GET' and  GET_method is not None:
##        return GET_method(request)
##    raise Http404

def method_splitter(request,*args,**kargs):
    get_method_view = kargs.pop('GET_method',None)
    post_method_view = kargs.pop('POST_method',None)
    if request.method == 'GET' and get_method_view is not None:
        return get_method_view(request,*args,**kargs)
    elif request.method =='POST' and post_method_view  is not None:
        return post_method_view(request,*args,**kargs)
    raise Http404
```
1) 这里,我们重写了method_splitter()方法,

这个方法不再是带位置参数和带默认值的关键字参数,

而是,位置参数 + 代表一元组参数 + 代表关键字参数.

>  如果你在函数定义时,

> 只在参数前面加一个*号,所有传递给函数的参数将会保存为一个元组. 

> 如果你在函数定义时,在参数前面加两个*号,所有传递给函数的关键字参数,将会保存为一个字典

2) 这里,使用pop()方法从字典里取出值(代表一个view对象).更为关键的是,返回对象的同时,从字典里删除了这组key-value.

3) 使用得到的视图对象,传入参数,进行分支.

----
## 函数的参数,动态参数,关键字参数

```python
# func_args_kargs,py

'''
func-->function
args-->arguments
kwargs-->keyword_arguments
'''
def foo(say_hello,age='20',*args,**kwargs):
    print "say_hello=",say_hello
    print "age=",str(age)
    print "Postional arguments arg:"
    print args
    print "Keyword arguments are:"
    print kwargs

print foo(1,2,3)

print foo('world',1, 2, name='Adrian', framework='Django')

print foo(40,4,name='zx', framework='web.py')

'''
>>>
say_hello= 1
age= 2
Postional arguments arg:
(3,)
Keyword arguments are:
{}
None

say_hello= world
age= 1
Postional arguments arg:
(2,)
Keyword arguments are:
{'framework': 'Django', 'name': 'Adrian'}
None

say_hello= 40
age= 4
Postional arguments arg:
()
Keyword arguments are:
{'framework': 'web.py', 'name': 'zx'}
None
'''
```
可以看到,第一个say_hello也是位置参数,但是不在*args里面.

> **位置参数必须放在关键字参数前面**

可以看到,传入的第一个参数被作为了say_hello的值,

传入的第二参数被作为了age的值,(age本生有默认值),

传入的后面没有命名的参数,进入了*args

传入的后面带有关键字的参数,进入了**kwargs

---
## 每个页面的认证:封装视图函数

每个页面都要做认证,那么怎么实现呢?

例如:下面的这两个页面需要认证才能显示:
```python
#urls.py
urlpatterns += patterns('',
    (r'^chapter8_requires_login/articles/(?P<year>\d{4})/$', articlesViews.year_archive),
    (r'^chapter8_requires_login/articles/(?P<year>\d{4})/(?P<month>\d{2})/$',articlesViews.month_archive),

)
# articlesViews.py
from django.http import HttpResponse

def year_archive(request,year):
    rawHtml='<html><head></head><body>year_archive:%s</body></html>'% year
    return HttpResponse(rawHtml)
def month_archive(request,month,year):
    rawHtml='<html><head></head><body>month_archive:%s-%s</body></html>'% (year,month)
    return HttpResponse(rawHtml)
```

那么怎么样才能实现每一个页面都认证呢?

```python
#urls.py
urlpatterns += patterns('',
    (r'^chapter8_requires_login/articles/(?P<year>\d{4})/$',requires_login(articlesViews.year_archive) ),
    (r'^chapter8_requires_login/articles/(?P<year>\d{4})/(?P<month>\d{2})/$',requires_login(articlesViews.month_archive)),
)
#dologin.py
def requires_login(view):
    def logined_view(request,*args,**kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return view(request,*args,**kwargs)
    return loginde_view
```

> 可以看到:

1.具体的认证在requires_login()里实现的.

2) 注意:**requires_login()传入一个视图函数,返回的也是一个视图函数**

一般的视图函数,像上面的year_archive(),month_archive(),传入的是request请求和参数,返回的是一个http响应.

3) 在urls.py里,不是直接调用处理URL的视图函数,而是先把这个视图函数,

传入requires_login()处理,返回一个新的视图函数,用它来最终显示页面.

4) **这个视图函数,传入requires_login()处理,返回一个新的视图函数,**的这个封装,叫做"**包装视图函数**"


----
## Include的用法:
```python
from django.conf.urls.defaults import *
urlpatterns = patterns('',
    (r'^weblog/', include('mysite.blog.urls')),
    (r'^photos/', include('mysite.photos.urls')),
    (r'^about/$', 'mysite.views.about'),
    (r'^(?P<username>\w+)/blog/', include('foo.urls.blog')),
     (r'^blog/', include('inner'), {'blogid': 3}),
)
```

> 1) include用来包含其他APP下urls.py文件.

> 2) include的patterns里,前面没有$

> 3) 如果遇到命名组参数,命名组参数将会传到include的app里urls.py的每一个URL匹配.

> **如果包含的urls.py里的匹配不要此参数,就会报错.**

> 4)  如果遇到额外的字典参数,此参数也会传到includedapp里urls.py的每一个URL匹配.

>  和命名组参数一样.**如果包含的urls.py里的匹配不要此参数,就会报错.**

