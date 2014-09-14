#Django-Boook-Chapter7- Forms-sendEmail

## 处理提交的表单数据

使用**request.POST.get('subject', '')**既可以从POST请求中取出数据.

这里已经包含了异常处理..

**编写一个表单**:

* 如果提交了错误参数,那么本页显示错误

* 添加了CSRF验证,注意settings.py的相关配置.

* 表单里设置了默认值,在再次输入时,用户只需要修改即可.

```python
# mysite\templates\contact_form.html

<html>
<head>
    <title>Contact us</title>
</head>
<body>
    <h1>Contact us</h1>
    {% if errors %}
        <ul>
            {% for error in errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
    {% endif %}
	<form action="/contact/" method="post">
		{% csrf_token %}
		<p> Subject:<input type="text" name= "subject" value="{{ subject }}"></p>
		<p>Your e-mail(optional):<input type="text" name="email" value="{{ email }}">
		<p>message:<textarea name ="message" rows="10" cols="50">{{ message }}</textarea><p>
		<input type="submit" value="Submit">
 	</form>
</body>
</html>
```

---

## 发送邮件的方法.

* 发送邮件的数据准备

> 1-主题

> 2-发件人

> 3-收件人

> 4-邮件内容 

* 单独创建了sendMailView.py文件来处理发送邮件.

* **整体逻辑如下:**

> 接收提交的数据,对数据的有效性进行分析,从数据中提取有效数据,发送邮件.

>  如果发送成功,页面重定向,防止二次提交.


```python
# mysite\mysite\sendMailView.py

# -*- coding: utf-8-*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.template import RequestContext
import datetime

def contact(request):
    errors=[]
    if request.method == 'POST':
        if not request.POST.get('subject',''):
            errors.append('Enter a subject.')
        if not request.POST.get('message',''):
            errors.append('Enter a meeage.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email','urmyfaith@qq.com'),
                ['1278908611@qq.com','904312072@qq.com'],
                #html_message=html_message_head+html_message_end
                #html_message=html_message_head+send_time+html_message_end
                #html_message="<html><body>It's time : %s </body></html>" % datetime.datetime.now()
                )
            return HttpResponseRedirect('/contact/thanks/')
    return render_to_response('contact_form.html',{'errors':errors,},context_instance=RequestContext(request))
def contact_thanks(request):
    return HttpResponse('<html><body><h1>thanks</h1></body></html>')

```
### **send_mail()方法的使用:**

> 0.>发送邮件不要额外的什么,配置好信息,Django就能发送,相当于Django起到了一个
类似网易闪电邮,Foxmail,MS Exchange等邮件客户端(代理)的作用.

> 1.> 导入相应的包:from django.core.mail import send_mail

> 2.>四个参数:主题,邮件正文,发送人,接收人列表,(其他可选参数.)

```python
send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)

subject:邮件主题
message:邮件正文
from_email: 发件人
recipient_list: 接收人列表(群发,可以看到相互间的邮件地址.) 
fail_silently:如果发送错误,是否抛出异常
auth_user: 登录邮件服务器的用户名
connection: 会话连接
html_message: html格式正文
```
> 3.>发送邮件需要在settings.py配置:

例如,我们在settings.py里配置如下(使用QQ邮箱):
```python
# Send mail:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'smtp.qq.com' 
EMAIL_PORT = 25
EMAIL_HOST_USER = 'urmyfaith@qq.com' 
EMAIL_HOST_PASSWORD = 'password-here'
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```
> 4.>调用send_mail()的from_email必须和EMAIL_HOST_USER相同.

> 5.>**注意不要将settings.py(包含正确用户名和密码的)文件同步到共公开的云存储,比如Github.**

![sending_email.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/sending_email.png)

**另外:**

**注意:**处理带有CRSF验证的表单的时候,使用**RequestContext**,如下.
```python
return render_to_response('contact_form.html'
    {'errors':errors,},
    context_instance=RequestContext(request)
)

```

**url配置:**

```python
#mysite\mysite\urls.py

from django.conf.urls import patterns, include, url
from mysite.sendMailView import contact,contact_thanks

urlpatterns = patterns('',
    url(r'^contact/$',contact),
    url(r'^contact/thanks/$',contact_thanks),   
```

如果做成APP的话,patterns就可以不用硬编码了.

-----