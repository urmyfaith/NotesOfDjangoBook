# Chapter7- forms_class


## form类的继承:

form类的继承的写法,有点像models的写法.

定义'字段'

下面是定义form表单里的三个元素:

**mysite/forms.py**
```python
# mysite/forms.py

# -*- coding: utf-8-*-
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required = False)
    message = forms.CharField()

```

forms模块也可以单独使用,例如:

```python
>>> from mysite.forms import ContactForm
>>> f = ContactForm()
>>> print f
<tr>
    <th><label for="id_subject">Subject:</label></th>
    <td><input id="id_subject" name="subject" type="text" /></td>
</tr>
<tr>
    <th><label for="id_email">Email:</label></th>
    <td><input id="id_email" name="email" type="email" /></td>
</tr>
<tr>    
    <th><label for="id_message">Message:</label></th>
    <td><input id="id_message" name="message" type="text" /></td>
</tr>
```

### forms,检验数据f.is_bound

如果对每个forms里的字段赋值,那么使用f.is_bound来检验数据.
```python
>>> f = ContactForm({'subject':'hello','email':'zuoxue@qq.com','message':'Nice site!'})
>>> f.is_bound
True
```

### forms,forms里赋值是否有效呢?f.is_valid()

```python
>>> f = ContactForm({'subject':'hello','email':'zuoxue@qq.com','message':'Nice site!'})
>>> f.is_bound
True
>>> f.is_valid()
True
```

###forms,检验错误信息f['key'].errors()

如下,可以获得校验后的出错的信息:

```python
>>> f = ContactForm({'subject':'hello','email':'zuoxue@qq.com','message':''})
>>> f['message'].errors
[u'This field is required.']
>>> f['subject'].errors
[]
>>> f['email'].errors
[]
>>> f.errors
{'message': [u'This field is required.']}
```
###forms,有条件的属性f.cleaned_data

```python
>>> f = ContactForm(
                    {'subject':'hello',
                    'email':'zuoxue@qq.com',
                    'message':'Nice site!'}
                    )
>>> f.cleaned_data
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'ContactForm' object has no attribute 'cleaned_data'
>>> f.is_valid()
True
>>> f.cleaned_data
{'message': u'Nice site!', 'email': u'zuoxue@qq.com', 'subject': u'hello'}

```
**从上面可以看出:只有在执行了判断is_valid,校验数据有效性之后,才有cleaned_data**

(ps.难道是因为is_valid会执行clean,然后才叫cleaned_data?)

----

## 使用forms类来重写sendMailView.

一、我们新建一个view,叫**mysite\sendMailViewByForms.py**

```python
# mysite\sendMailViewByForms.py
from mysite.forms import ContactForm
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
    return render_to_response('contact_formByForms.html',
                                {'form': form},
                                 context_instance=RequestContext(request)
                            )
```
> 注意,这里需要导入我们刚写的继承forms类

1)首先,访问网页是GET方法,进入的else,执行的是

```python
    else:
        #GET Method ---default visite site method.
        form = ContactForm(initial={'subject': 'I love your site!'})
    return render_to_response('contact_formByForms.html',
                                {'form': form},
                                 context_instance=RequestContext(request)
                            )
```
也就是说:表单为空,显示渲染空页面.

2)然后.POST请求,提交表单,执行的是if里的语句:

> a)request.POST作为参数传入类,新建一个form实例.

> b)判断form里参数是否有效

> c)提取参数,发送邮件

> d)网页跳转,避免二次发送.

----
二、模版编写

新建**mysite\templates\contact_formByForms.html**

```python
<body>
    <h1>Contact us</h1>
    {% if form.errors %}
		<p style="color:red;">
			Please correct the error {{ form.errors|pluralize}} below.
		</p>
    {% endif %}
	<form action="/contact/" method="post">
		{% csrf_token %}
		<table>
				{{ form.as_table }}
		</table>
		 <input type="submit" value="Submit">
 	</form>
</body>
```

> 注意,**这里的显示错误,我们并没有for循环form.errors**

![forms_show_error.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/forms_show_error.png)

1) 表单的提交,

a) 需要:模版文件里表单包含{% csrf_token %}

b) 需要:view文件里使用RequestContext

c) 需要:settings.py里设置中间件,启用插件等配置.


2)成功发送邮件:

![forms_sendMail_thanks.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/forms_sendMail_thanks.png)

---

## 使用forms的其他设置:

### 改变字段显示:

**message = forms.CharField(widget=forms.Textarea)**

从文本框-->文本区域

```python
# forms.py
# -*- coding: utf-8-*-
from django import forms
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required = False,label='Your e-mail address')
    message = forms.CharField(widget=forms.Textarea)
```

### 设置最大长度

**subject = forms.CharField(max_length=100)**

### 自定义显示标签

** email = forms.EmailField(required = False,label='Your e-mail address')**

![your_email_address.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/your_email_address.png)


###  设置初始值

注意:**设置初始值,实在实例化对象的时候传入值:**

```python
# sendMailViewByForms.py
...
    else:
        #GET Method ---default visite site method.
        form = ContactForm(initial={'subject': 'I love your site!'})
    return render_to_response('contact_formByForms.html',{'form': form},context_instance=RequestContext(request))
...

```

![forms_default_data.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/forms_default_data.png)


### 自定义校验规则

需要在forms.py里编写**clean_[字段名]**()的函数 ,并且**返回字段**.

```python
# forms.py
# -*- coding: utf-8-*-
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required = False)
    message = forms.CharField(widget=forms.Textarea)
    
    def clean_message(self):
            message = self.cleaned_data['message']
            num_words = len(message.split())
            if num_words < 4:
                raise forms.ValidationError("Not enough words!")
            return message
```
![Not_enough_words.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/Not_enough_words.png)

----
