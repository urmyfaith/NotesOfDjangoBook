# Chapter 14 session_user

* Chapter 14 session_user
* 存、取cookie
* 打开Sessions功能
* 在View(视图)中使用Session
* 设置session值
* 读取session值
* 删除某个session值
* 判断是否存在某个session值
*  简单（但不很安全）的、防止多次评论方法
* 设置测试是否允许Cookies
* 在视图(View)外使用Session

---

* Users and Authentication
* 打开认证支持
* 判断用户是否登录
*  使用User对象
* 设置用户组
* 给用户添加组
* 把用户从组里移除
* 把用户从所有组里移除
* 用户的权限相关
* 登录和退出--自己编写login,logout的视图
*登录和退出--使用系统视图
* 在某一个页面中,判断用户是否已经认证登录--->login_required
* 对已经登录用户,进一步限制访问---->user_passes_test
* 限制用户访问的三个修饰符:login_required,user_passes_test,permission_required
* 限制通用视图的访问-->重新包装视图函数

---

* 管理 Users, Permissions 和 Groups
* 创建用户-->User.objects.create_user()
* 修改密码-->user.set_password('xx')
* 用户注册-->
* 在模版中使用认证数据.
* 权限,组和消息--->messages.add_message()





##存、取cookie

取出cookie:
> request.COOKIES["favorite_color"]

```python
# mysite/cookie_view.py
def show_color(request):
    if "favorite_color" in request.COOKIES:
        return HttpResponse("Your favourite color is %s" % \
                            request.COOKIES["favorite_color"])
    else:
        return HttpResponse("You don't have a favorite color.")
```

存cookie:
>  response.set_cookie("favourtie_color",cookie_value)

```python
# mysite/cookie_view.py
def set_color(request):
    if "favourite_color" in request.GET:
        response = HttpResonse("Your favourite color is now %s" % \
                              request.GET["favourite_color"]
                              )
        response.set_cookie("favourtie_color",request.GET["favourite_color"])
        return response
    else:
        return HttpResponse("You don't have a favorite color.")
```

![cookie_view.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/cookie_view.png)

----


## 打开Sessions功能

> 1. 编辑 MIDDLEWARE_CLASSES 配置，确保 MIDDLEWARE_CLASSES 中包含 'django.contrib.sessions.middleware.SessionMiddleware'。

> 2. 确认 INSTALLED_APPS 中有 'django.contrib.sessions' 

> 3. (如果你是刚打开这个应用，别忘了运行 manage.py syncdb )

```python
# mysite/settings.py

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mysite',
    'books',
    'blog'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
)
```

---
## 在View(视图)中使用Session
> SessionMiddleware 激活后，每个传给视图(view)函数的第一个参数``HttpRequest`` 对象都有一个 session 属性，这是一个字典型的对象。

```python

#设置session值
request.seesion["fav_color"]="blue"

#读取session值
fav_color=request.session["fav_color"]

#删除某个session值
del request.session["fav_color"]

#判断是否存在某个session值
if "fav_color" in request.session:
    ...
```
注意:

1> 不要使用下划线开头的变量作为key

2> 不要将新对象替换 request.session对象.

### 简单（但不很安全）的、防止多次评论方法
```python
#mysite/urls.py
urlpatterns += patterns('mysite.session_view',
    url(r'^chapter14/post_comment/$','post_comment'),
)
#mysite/session_view.py
def post_comment(request):
    errors=[]
    if request.method == 'POST':
        if not request.POST.get('subject',''):
            errors.append('Enter a subject.')
        if not request.POST.get('message',''):
            errors.append('Enter a meeage.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if request.session.get('has_commented', False):
           return HttpResponse("You've already commented.")
        if not errors:
            #do something here, eg: save it to database
            request.session['has_commented'] = True
            return HttpResponse('Thanks for your comment!')
    return render_to_response('post_comment.html',\
                              {'errors':errors,}, \
                              context_instance=RequestContext(request))

#mysite/templates/post_comment.html
<html>
<head>
    <title>post comment</title>
</head>
<body>
    <h1>post comment</h1>
    {% if errors %}
        <ul>
            {% for error in errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
    {% endif %}
	<form action="" method="post">
		{% csrf_token %}
		<p> Subject:<input type="text" name= "subject" value="{{ subject }}"></p>
		<p>Your e-mail(optional):<input type="text" name="email" value="{{ email }}">
		<p>message:<textarea name ="message" rows="10" cols="50">{{ message }}</textarea><p>
		<input type="submit" value="Submit">
 	</form>
</body>
</html>

```
上面:

> 1.URLconf

> 2.视图中,判断是否为post方法,

a) post:判断提交参数合法性,判断session值,分别返回.

b) get:显示form

> 3.模版,显示一个form和错误处理.

![befor_post_comment.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/befor_post_comment.png)

![after_post.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/after_post.png)

![post_again.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/post_again.png)

![table_django_session.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/table_django_session.png)


---
### 设置测试是否允许Cookies

在访问网页时(get),尝试设置cookie,

在登录的时候(post),判断设置cookie是否正常.然后进行分支处理.

```python
def login(request):
    errors=[]
    if request.method == 'POST':
        if not request.POST.get('username',''):
            errors.append('Enter a username.')
        if not request.POST.get('password',''):
            errors.append('Enter a password.')
        if not errors:
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                return HttpResponse("Logged in.")
            else:
                return HttpResponse('Please enable coookie.')
    request.session.set_test_cookie()
    return render_to_response('login.html',\
                              {'errors':errors,}, \
                              context_instance=RequestContext(request))
```
1)判断是否允许设置cooke:
> request.session.test_cookie_worked()

2)删除测试cookie:
> request.session.delete_test_cookie()

3)请求的时候设置cookie(正常访问网页时判断)
> request.session.set_test_cookie()

![set_test_cookie.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/set_test_cookie.png)

---
## 在视图(View)外使用Session

1)需要导入包: from django.contrib.sessions.models import Session

2) 常见的函数/属性:exprire_data,session_data,get_decoded()

```python
D:\Documents\GitHub\NotesOfDjangoBook\mysite>python manage.py shell
>>> from django.contrib.sessions.models import Session
>>> s= Session.objects.get(pk='vyrd47zvgrj2ot7z7lguekw1d42n0isl')
>>> s.expire_date
datetime.datetime(2014, 10, 5, 5, 49, 6, 915000, tzinfo=<UTC>)
>>> s.session_data
u'ODNiOGJmNmVkN2NjMjA5ODhhN2M1NmViNjU1N2E2ZDlhNGQ4Yzc5Yjp7fQ=='
>>> s.session_key
u'vyrd47zvgrj2ot7z7lguekw1d42n0isl'
>>> s.get_decoded()
{u'has_commented': True, u'testcookie': u'worked'}
>>> cookies=s.get_decoded()
>>> cookies['has_commented']
True
>>>


```
---

## Users and Authentication

Django 认证/授权 系统会包含以下的部分：

>用户 : 在网站注册的人

>权限 : 用于标识用户是否可以执行某种操作的二进制(yes/no)标志

>组 :一种可以将标记和权限应用于多个用户的常用方法

>Messages : 向用户显示队列式的系统消息的常用方法

## 打开认证支持

1> 需要确认用户使用cookie，这样sesson 框架才能正常使用。1

2>将 'django.contrib.auth' 放在你的 INSTALLED_APPS 设置中，然后运行 manage.py syncdb以创建对应的数据库表。

3>确认 SessionMiddleware 后面的 MIDDLEWARE_CLASSES 设置中包含 'django.contrib.auth.middleware.AuthenticationMiddleware' SessionMiddleware

### 判断用户是否登录
```python
if request.user.is_authenticated():
    # Do something for authenticated users.
else:
    # Do something for anonymous users.
```

##  使用User对象

```python
# 设置用户组
myuser.groups = group_list

# 给用户添加组
myuser.groups.add(group1, group2,...)

# 把用户从组里移除
myuser.groups.remove(group1, group2,...)

# 把用户从所有组里移除
myuser.groups.clear()

# 用户的权限相关
myuser.permissions = permission_list
myuser.permissions.add(permission1, permission2, ...)
myuser.permissions.remove(permission1, permission2, ...)
myuser.permissions.clear()
```
-----

## 登录和退出--自己编写login,logout的视图

自己编写login和logout的话:
```python
#mysite/urls.py
urlpatterns += patterns('mysite.user_login_logout_view',
    url(r'^chapter14/user/login/$','login'),
    url(r'^chapter14/user/logout/$','logout'),                  
)
#mysite/user_login_logout_view.py
from django.contrib import auth

def login(request):
    errors=[]
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not request.POST.get('username',''):
            errors.append('Enter a username.')
        if not request.POST.get('password',''):
            errors.append('Enter a password.')
        if not errors:
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponse('You have logged in.')
            else:
                return HttpResponse('usrname or password invalid.')
    return render_to_response('user_login.html',\
                              {'errors':errors,}, \
                              context_instance=RequestContext(request))  
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/chapter14/user/login/")
#mysite/templates/user_login.html
<html>
<head>
    <title>login</title>
</head>
<body>
    <h1>login</h1>
    {% if errors %}
        <ul>
            {% for error in errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
    {% endif %}
	<form action="" method="post">
		{% csrf_token %}
		<p> username<input type="text" name= "username" value="{{ username }}"></p>
		<p>password<input type="password" name="password" value="{{ password }}">
		<input type="submit" value="Submit">
 	</form>
</body>
</html>
```

上面自己实现的过程中:
1> 在URLconf里设置了2个url

2> 在视图里编写了两个函数来处理登录和登出

登录分以下几个步骤:

a) 获取用户名和密码
>username = request.POST.get('username', '')

b) 进行授权验证
>auth.authenticate(username=username,password=password)

c) 授权成功,则通过session保存用户状态等信息
> auth.login(request,user)

d) 处理登录后才能做的事项.

3> 在模版里 ,简单的写了一个表单.

![user_login_logout.gif ](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/user_login_logout.gif)

---
##登录和退出--使用系统视图
```python
#mysite/urls.py
from django.contrib.auth.views import login,logout
urlpatterns += patterns('',
    url(r'^chapter14/accounts/login/$',login,{'extra_context': {'next': '/hello'}}),
    url(r'^chapter14/accounts/logout/$',logout),                  
)
#mysite/templates/registration/login.html
<html>
<head>
    <title>login</title>
</head>
<body>
    <h1>login</h1>
{% block content %}

  {% if form.errors %}
    <p class="error">Sorry, that is not a valid username or password</p>
  {% endif %}

  <form action="" method="post">
	{% csrf_token %}
    <label for="username">User name:</label>
    <input type="text" name="username" value="" id="username">
    <label for="password">Password:</label>
    <input type="password" name="password" value="" id="password">

    <input type="submit" value="login" />
    <input type="hidden" name="next" value="{{ next|escape }}" />
  </form>

{% endblock %}
</body>
</html>

```
1)在上面,我们并没有自己编写login,logout视图,而是

通过导入包的形式,使用系统自带的视图.

注意:
> 这里我们给login添加了额外的内容

> {'extra_context': {'next': '/hello'}}

> 与表单的中的next数据对应.(表单中next从这里获得.)

2) 表单的路径是"mysite/templates/registration/login.html",需要自己编写login的模版

a)模版中需要使用{% csrf_token %}

b)有个hidden的next字段

3)默认的登陆后跳转是"/accounts/profile ",使用next字段重写.这里,我们跳转到hello

![user_import_login_logout.gif ](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/user_import_login_logout.gif)

---

## 在某一个页面中,判断用户是否已经认证登录--->login_required

第一种方法是,使用 request.user.is_authenticated().

```python
def login(request):
    ...
            if user is not None and user.is_active:
                auth.login(request,user)
                #return HttpResponse('You have logged in.')
                return HttpResponseRedirect('/chapter14/limited_acess_vote/')
            else:
                return HttpResponse('usrname or password invalid.')
    return render_to_response('user_login.html',\
                              {'errors':errors,}, \
                              context_instance=RequestContext(request))

def vote_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("not authenticated.")
    else:
        return HttpResponse("yes authenticated.")
```
在登录后,跳转到vote_view视图,

如果用户已经认证,或者用户没有认证.

第二种方法是,使用auth包里的"login_required"修饰符.
```python
from django.contrib.auth.decorators import login_required
@login_required(login_url="/chapter14/user/login/")
#function under login_required, will be authenticate.
# if authentication failed,will return to login_url.
def poll_view(request):
    return HttpResponse("you are in poll_view")
```

定义的类poll_view在
>@login_required(login_url="/chapter14/user/login/")
之后,这样,在这句之后的所有视图都会使用login_required来认证.

login_required中,如果认证失败,默认跳转到登录页面,

可以通过login_url参数指定.

---

## 对已经登录用户,进一步限制访问---->user_passes_test

可以通过检查用户是否具有某个权限,进一步限制用户访问:
```python
#urls.py
urlpatterns += patterns('mysite.user_login_logout_view',
    ...
    url(r'^chapter14/limited_acess_vote2/$','vote_view2'),
)
#user_login_logout_view.py
from django.contrib.auth.decorators import user_passes_test
def user_can_vote(user):
    #return user.is_authenticated() and user.has_perm("poll.can_vote")
    return user.is_authenticated()
@user_passes_test(user_can_vote,login_url="/chapter14/user/login/")
def vote_view2(request):
    return HttpResponse("vote_view2 under user_passes_test.")
```
访问"chapter14/limited_acess_vote2/"的时候,使用视图"vote_view2"

但是,在视图上面,我们使用了修饰符@user_passes_test()

这个函数需要一个回调函数,可选的登录url.

这样以后,如果访问视图的时候,用户没有通过测试(这里我们测试是user_can_vote(),里面判断用户是否登录,当然,可以判断用户是否具有某某权限,是否在某个组里,等等.),那么跳转到登录界面.

![user_passes_test.gif ](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/user_passes_test.gif)

----

### 限制用户访问的三个修饰符:login_required,user_passes_test,permission_required

在源码文件
```python
C:\Python27\Lib\site-packages\Django-1.7-py2.7.egg\django\contrib\auth\decorators.py
```
中,可以看到这三个修饰符的具体实现.

总结下功能:

* login_required, 只是用户判断用户是否已经登录.

* user_passes_test,可以对用户进行各种判断:
 * 是否登录认证(**注意:user_passes_test不会自动检查 User是否认证**)
 * 是否具有某个权限
 * 是否在某个组...
 * 等等

* permission_required,可以用来对判断用户是否具有某个权限,例如:


```python
from django.contrib.auth.decorators import permission_required

@permission_required('polls.can_vote', login_url="/login/")
def vote(request):
    # do vote here.
```
上面的代码,判断用户是否具体有权限"'polls.can_vote".

----


## 限制通用视图的访问-->重新包装视图函数

如何限制通用视图的访问呢?
可以使用上面的login_required,**重新包装视图函数**:

```python
from django.contrib.auth.decorators import login_required
from django.views.generic.date_based import object_detail
@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)
```
----

## 管理 Users, Permissions 和 Groups

### 创建用户-->User.objects.create_user()

```python
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user(username="faith",email='apple@qq.com',password='faith')
>>> user.is_staff = True
>>> user.save()
>>>
```
### 修改密码-->user.set_password('xx')
```python
>>> user = User.objects.get(username='faith')
>>> user.set_password('faith')
>>> user.save()
>>>
```
---

### 用户注册-->
```python
#urls.py

urlpatterns += patterns('mysite.user_login_logout_view',
    ...
    url(r'^chapter14/user/register$','register'),
)

#mysite/user_login_logout_view.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/chapter14/user/login/')
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", \
                              {'form':form}, \
                              context_instance=RequestContext(request))
#mysite/templates/registration/register.html
{% block content %}
  <h1>Create an account</h1>

  <form action="" method="post">
	{% csrf_token %}
      {{ form.as_p }}
      <input type="submit" value="Create the account">
  </form>
{% endblock %}

```
1) 在urls.py里,指定URLconf

2) 在view里register():

 * GET:显示表单
 * POST:根据提交值检查表单,如果有效,创建用户,返回登录界面.

注意:还是需要使用"RequestContext"

3) 编写模版,显示表单

注意:表单里,需要{% csrf_token %}.
![register ](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/register.gif)
----

## 在模版中使用认证数据.

> 当前登入的用户以及他（她）的权限可以通过 RequestContext 在模板的context中使用

```python
#urls.py
    url(r'^chapter14/user/user_data$','user_data_in_templates'),

#user_login_logout_view.py
def user_data_in_templates(request):
    return render_to_response("use_data_in_templates.html", \ 
context_instance=RequestContext(request))
 
#mysite/templates/use_data_in_templates.html
{% if user.is_authenticated %}
  <p>Welcome, <b>{{ user.username }}</b>.Thanks for logging in.</p>
{% else %}
  <p>Welcome, new user. Please log in.</p>
{% endif %}
```
注意:

1) 在view中,需要使用RequestContext

2) 在模版中,可以使用user对象,以及对象的各种方法/属性等.

![use_data_in_templates.gif ](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/use_data_in_templates.gif)

---
## 权限,组和消息--->messages.add_message()

> 消息系统会为给定的用户接收消息。 每个消息都和一个 User 相关联。

接收和显示消息的方法:

> 要创建一条新的消息，使用 user.message_set.create(message='message_text') 

> 要获得/删除消息，使用 user.get_and_delete_messages() ，

> 这会返回一个 Message 对象的列表，并且从队列中删除返回的项。

```python
#urls.py
urlpatterns += patterns('mysite.user_message_view',
    url(r'^chapter14/message/playlist/(?P<songs>[\w-]+)/$','create_palylist'),
)
#user_message_view.py
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
def create_palylist(request,songs):
    # creat playlist here.
    #request.user.message_set.create(message="Your playlist was added successfully.")
    messages.add_message(request, messages.INFO, 'Your playlist was added successfully') 
    return render_to_response("user_message.html", \
                              {"songs":songs}, \
                              context_instance=RequestContext(request))
#mysite/tempaltes/user_message.html
{% if messages %}
<ul class="messages">
    {% for message in messages %}
		<li>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}

<p>Your palylist : <strong>{{ songs }}</strong> has been created.
```

1) URLcof里接收参数songs

2) 视图里,使用messages.add_message()方法来创建一条消息.

需要导入包from django.contrib import messages


3) 在模版里

 * 使用RequestContext
 * 传递songs参数供模版使用,**但是不显式提供messages给模版!**
 * 模版里使用for循环来遍历

4) **使用messages框架,不需要用户登录.**

5) request.user.message_set.creat()方法已经过时.

![show_user_message.gif ](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/show_user_message.gif)

---

