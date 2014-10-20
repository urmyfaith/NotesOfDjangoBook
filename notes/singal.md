# signal

全文概览：

* signal的实现
* 一个简单的signal实现
* 类似于在 android开发中的监听器
* 另外的一个比较了类似例子ajax/jquery
* signal的其他内容


-----

**Django的signal相当于某个条件触发之后，执行一个操作。**

可以自定义触发条件和执行的操作，同时Django也提供了很多的默认的触发条件，例如：

* django.db.models.signals.pre_save & django.db.models.signals.post_save

提交或者保存这个条件触发后执行一个操作


* django.db.models.signals.pre_delete & django.db.models.signals.post_delete

* django.db.models.signals.m2m_changed


* django.core.signals.request_started & django.core.signals.request_finished

请求结束这个条件触发后执行的操作。


## signal的实现：

1）自定义触发条件或者django内置的触发条件（上面已经提到了）

2）实现条件触发之后所执行的具体内容。（回调函数）

3）将触发条件与回调函数关联起来。（两种实现方法）


###一个简单的signal实现：
通常signal在model中实现，这里为了简单，直接在view中实现。
一个简单的页面：
```python
#urls.py
from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/',"testsignal.view.hello"),
]

#view.py
from django.http import HttpResponse
def hello(request):	
	return HttpResponse("Hello signal.")
```
上面访问/hello，就可以看到页面中显示“Hello signa”


我们在上面的基础上来实现一个简单的signal：每一个亲请求结束后打印一下请求结束。

1）使用内置的触发条件：

```python
from django.core.signals import request_finished
```

2）实现条件触发之后所执行的具体内容。（回调函数）

```python
def my_callback(sender, **kwargs):
    print("request finished")
```

3)将触发条件与回调函数关联起来
```python
request_finished.connect(my_callback)
```
或者使用receiver（）来实现：

```python
from django.dispatch import receiver
@receiver(request_finished)
```

完整代码（）：
```python
# -*- coding: utf-8-*-
from django.http import HttpResponse
from django.core.signals import request_finished
from django.dispatch import receiver

def hello(request):   
	return HttpResponse("Hello signal.")
	
@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("request finished")

```
或者：
```python
# -*- coding: utf-8-*-
from django.http import HttpResponse
from django.core.signals import request_finished

def hello(request):
        request_finished.connect(my_callback)
	return HttpResponse("Hello signal.")

def my_callback(sender, **kwargs):
    print("request finished")
```

###  类似于在 android开发中的监听器：

```java
protected void onCreate(Bundle savedInstanceState) {
       super.onCreate(savedInstanceState);
       setContentView(R.layout.activity_main);

       button =(Button)findViewById(R.id.button);//生成监听器对象
       ButtonListener buttonListener =new ButtonListener();//为控件绑定监听器对象
       button.setOnClickListener(buttonListener);
       
//定义监听类，实现监听器接口
class ButtonListener implements OnClickListener{
    public void onClick(View arg0) {
        //do something here...
         textView.setText("onclick ok");
}    

```

这是个按钮的监听器，这样每次点击按钮的时候，触发OnClickListener事件，执行里面的内容。

---

###另外的一个比较类似例子：
在ajax中有onreadystatechange函数,

> 当请求被发送到服务器时，我们需要执行一些基于响应的任务。

> 每当 readyState 改变时，就会触发 onreadystatechange 事件。

> [w3chool: ajax_xmlhttprequest_onreadystatechang](http://www.w3school.com.cn/ajax/ajax_xmlhttprequest_onreadystatechange.asp)

---


在jquery中，也有类似的特性：

[w3chool:jquery](http://www.w3school.com.cn/jquery/jquery_ref_events.asp)

事件名称 | 内容
--------------|--------------
mousedown()	 |    触发、或将函数绑定到指定元素的 mouse down 事件
mouseenter() |    触发、或将函数绑定到指定元素的 mouse enter 事件
mouseleave() |    触发、或将函数绑定到指定元素的 mouse leave 事件

## signal的其他的问题

* 自定义signal（自定义触发条件）

```python
import django.dispatch

pizza_done = django.dispatch.Signal(providing_args=["toppings", "size"])
class PizzaStore(object):
    ...

    def send_pizza(self, toppings, size):
        pizza_done.send(sender=self.__class__, toppings=toppings, size=size)
        ...

```

* 断开触发条件与执行动作之间的关系Disconnecting signals

* 触发条件是谁触发的问题

```python
@receiver(pre_save, sender=MyModel)
```


* 防止重复的信号执行

```python
request_finished.connect(my_callback, dispatch_uid="my_unique_identifier")
```
