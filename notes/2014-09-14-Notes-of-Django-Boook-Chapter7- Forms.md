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

3>  

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

## 编写表单提交后显示页面(简单的显示)request.GET['name']

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

## GET和POST的用法:

具体参见:

http://www.w3school.com.cn/tags/html_ref_httpmethods.asp

> 两种 HTTP 请求方法：GET 和 POST
在客户机和服务器之间进行请求-响应时，两种最常被用到的方法是：GET 和 POST。
* GET - 从指定的资源请求数据。(不需要修改服务器数据)
* POST - 向指定的资源提交要被处理的数据(需要修改服务器后台数据)

---

## 编写表单提交后显示页面(查询数据库后输出)

1>在**mysite\views.py**修改方法.

* 得到查询字符串request.GET['q']

* 筛选数据库记录filter(a=b)

* 参数传入模版render_to_response

* 渲染输出显示页面.
 
```python
def show_search_result(request):
    if 'q' in request.GET:
        #message = 'You searched for : %r' % request.GET['q']
        #message = 'You searched for : %s' % request.GET['q']
        search_str = request.GET['q']
        books = Book.objects.filter(title__icontains=search_str)
        return render_to_response('search_results.html',{
            'books':books,
            'search_str':search_str
            })
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
```

2> 编写模版渲染,显示页面:

**mysite\templates\search_results.html**
```python
#search_results.html
{% extends 'base.html' %}

{% block title %}show search results  infomation{% endblock %}
{% block content %}
<p>You searched for: <strong>{{ search_str }}</strong></p>

{% if books %}
    <p>Found {{ books|length }} book{{ books|pluralize }}.</p>
	<table width="600" border="0" bgcolor="blue" bordercolor="black" cellpadding="5" cellspacing="1">
		<tr bgcolor="white"  > 
			<td>#</td>   
			<td> title </td>
			<td>book.publisher </td>
			<td>publication_date </td>
		</tr>
        {% for book in books %}
		<tr bgcolor="white" > 
			<td>{{ forloop.counter }}</td>   
			<td>{{ book.title }}</td>
			<td>{{ book.publisher }}</td>
			<td>{{ book.publication_date }}</td>
		</tr>
        {% endfor %}
	</table>
{% else %}
    <p>No books matched your search criteria.</p>
{% endif %}
	
{% endblock %}

```
![show_search_result_in_db.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/show_search_result_in_db.png)

---


## 表单改进

> 提交之后,如果是因为用户不小心提交了,提交为空字符串,那么就需要返回去重新填写.

> 所以,在提交空搜索字的时候,直接返回到搜索页面即可.

1>**views.py(show_search_result)**里修改显示逻辑:

如果带参数,获得搜索参数.

检查参数是否为空.

如果非空,查询显示.
如果为空,显示搜索页面,并标记搜索出现出错.

```python
def show_search_result(request):
    if 'q' in request.GET:
        #message = 'You searched for : %r' % request.GET['q']
        #message = 'You searched for : %s' % request.GET['q']
        search_str = request.GET['q']
        if search_str!="":
            books = Book.objects.filter(title__icontains=search_str)
            return render_to_response('search_results.html',{
            'books':books,
            'search_str':search_str
            })
        #message = 'You submitted an empty form.'
        #return HttpResponse(message)
        return render_to_response('search_form.html', {'error': True})

```

2>修改模版显示逻辑:

* search_form.html,检查是否有搜索错误标记,如果有,显示出错.

* search_results.html.添加搜索的框,方便再次搜索.

```python
#search_form.html
{% extends 'base.html' %}

{% block title %}show search form {% endblock %}
{% block content %}
    {% if error %}
        <p style="color: red;">Please submit a search term.</p>
    {% endif %}
	<form action="/search/" method="get">
        <input type="text" name="q">
        <input type="submit" value="Search">
    </form>
{% endblock %}
```

```python
#  search_results.html
{% extends 'base.html' %}

{% block title %}show search results  infomation{% endblock %}
{% block content %}
	<form action="/search/" method="get">
        <input type="text" name="q">
        <input type="submit" value="Search">
    </form>

<p>You searched for: <strong>{{ search_str }}</strong></p>
{% if books %}
    <p>Found {{ books|length }} book{{ books|pluralize }}.</p>
	<table width="600" border="0" bgcolor="blue" bordercolor="black" cellpadding="5" cellspacing="1">
		<tr bgcolor="white"  > 
			<td>#</td>   
			<td> title </td>
			<td>book.publisher </td>
			<td>publication_date </td>
		</tr>
        {% for book in books %}
		<tr bgcolor="white" > 
			<td>{{ forloop.counter }}</td>   
			<td>{{ book.title }}</td>
			<td>{{ book.publisher }}</td>
			<td>{{ book.publication_date }}</td>
		</tr>
        {% endfor %}
	</table>
{% else %}
    <p>No books matched your search criteria.</p>
{% endif %}

	
{% endblock %}
```
![show_serach_result.gif](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/show_serach_result.gif)
