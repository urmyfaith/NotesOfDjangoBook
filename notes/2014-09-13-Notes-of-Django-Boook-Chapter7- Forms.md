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
**mysite\templatesshow_request.html**
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
