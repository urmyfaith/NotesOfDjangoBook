# Chapter11-generic_view

## 通用视图实现的功能:

* 完成简单的任务

* 显示列表/某个特定对象的详细内容页面

* 显示基于日期的数据的年月日归档页面

## 使用通用视图的一个示例:TemplateView

```python
from django.views.generic import TemplateView
urlpatterns += patterns('',
    url(r'^chapter11_generic_view/about/$', \ 
                  TemplateView.as_view(template_name="about.html")),
)
```
> 使用通用视图:

1)在urls.py里导入包

2)将url地址,指向一个带参数的TemplateView视图.

![generic_view_template_view.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/generic_view_template_view.png)

这里,我们只需要2个步骤:

a) 编写urls.py,指定URL匹配.(将参数传递给TemplateView视图)

b) 编写指定的模版文件.

---
