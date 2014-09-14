# Chapter 7: Forms

## 有关request的相关信息

写一个view来显示request相关的信息:

1>在**mysite\urls.py**里配置请求url地址:
```python
    url(r'^request-info/$',show_request)
```

2>在**mysite\views.py**添加方法.
 
```python
def show_request(request):
    request_path = request.path
    request_host = request.get_host()
    request_full_path = request.get_full_path()
    request_is_secure = request.is_secure()
    request_dic={
        'request_path':request_path,
        'request_host':request_host,
        'request_full_path':request_full_path,
        'request_is_secure':request_is_secure,
        }
    request_meat_values = request.META.items()
    request_meat_values.sort()
    return render_to_response('show_request.html',{
        'request_dic':request_dic,
        'request_meat_values':request_meat_values,
        })
```
3> 编写模版渲染,显示页面:
**mysite\templates\show_request.html**
```python
{% extends 'base.html' %}

{% block title %}show request infomation{% endblock %}
{% block content %}
<table width="300" border="0" bgcolor="blue" bordercolor="black" cellpadding="5" cellspacing="1">
	{% for key,value in request_dic.items %} 
	<tr bgcolor="white">              
		<td>{{ forloop.counter }}</td>            
		<td>{{ key }}</td>            
		<td>{{ value }}</td>            
	 </tr>
	{% endfor %}
	{% for k,v in  request_meat_values %}
	<tr  bgcolor="white">
		<td>{{ forloop.counter }}</td> 
		<td>{{ k }}</td>
		<td>{{ v }}</td>
	</tr>
	{% endfor %}
	</table>
{% endblock %}
```
![requst_info.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/requst_info.png)

> **注意:**,这里有个在模版里输出字典的方法.

----

## 在模版里输出字典的方法

```python
    {% for key,value in request_dic.items %} 
	<tr bgcolor="white">              
		<td>{{ forloop.counter }}</td>            
		<td>{{ key }}</td>            
		<td>{{ value }}</td>            
	 </tr>
	{% endfor %}
```
> request_dic标准的字典的遍历和request_meat_values的遍历稍有区别,在于是否使用items方法.

---

## 编写简单的表单页面(不含提交后显示)


1>在**mysite\urls.py**里配置请求url地址:

```python
    url(r'^search-form/$',search_form),
```

2>在**mysite\views.py**添加方法.

```python
def search_form(request):
    return render_to_response('search_form.html',)
```

3> 编写模版渲染,显示页面:

**mysite\templates\show_request.html**

```python
#search_form.html
{% extends 'base.html' %}
{% block title %}show search form {% endblock %}
{% block content %}
	<form action="/search/" method="get">
        <input type="text" name="q">
        <input type="submit" value="Search">
    </form>
{% endblock %}
```

> 应该来说,提交到的页面地址应该是作为参数传入到模版中,而不是硬编码.

![search_form.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/search_form.png)
----

## 编写表单提交后显示页面(简单的显示)

1>在**mysite\urls.py**里配置请求url地址:

```python
     url(r'search/$',show_search_result),
```

2>在**mysite\views.py**添加方法.

```python
def show_search_result(request):
    if 'q' in request.GET:
        #message = 'You searched for : %r' % request.GET['q']
        message = 'You searched for : %s' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
```
![show_search_result.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/show_search_result.png)

----

