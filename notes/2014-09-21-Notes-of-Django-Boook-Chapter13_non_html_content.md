# Chapter13_non_html_content

* 输出一张图片
* 输出生成 CSV 文件-part1
* 输出生成 CSV 文件-part2
* zip,list方法
* 输出生成 CSV 文件-part3
* 输出生成 XLS文件
* 关于生成xls的资料
* 输出生成 PDF文件
* 安装reportlab
* 输出PDF文件-使用StringIO()
* 输出其他类型的文件的讨论 ,zip,图片,图表


## 输出一张图片

**需求:**通过输入图片的文件名称,显示一张图片

1) 设置URLconf

```python
# mysite/urls.py
urlpatterns += patterns('mysite.show_non_html_content',
    url(r'^chapter13/show_images/(?P<filename>[\w-]+).png/$','show_images'),
)
```
这里,patterns匹配的时候,使用命名组参数,传入文件名称.

2) 编写视图,显示图片.
```python
# mysite/show_non_html_content.py
from django.http import HttpResponse
def show_images(request,filename):
    image_data=open("D:\\Documents\\GitHub\\NotesOfDjangoBook\\notes\\images\\%s.png" % filename,"rb")
    return HttpResponse(image_data,content_type="image/png")
```
这里,只需要打开本地图片,返回HttpResponse即可.

需要注意的是,这里必须设置**content_type**,通知浏览器这是一张图片.

![show_images.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/show_images.png)
-----
## 输出生成 CSV 文件-part1

输出csv文件的时候,也是要通知浏览器,这是一个csv文件

```python
# myste/urls.py
urlpatterns += patterns('mysite.show_non_html_content',
   ...
    url(r'^chapter13/show_csv/$','show_csv'),
)

# mysite/show_non_html_content.py 
import csv
def show_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="show_csv.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', "hello"])
    writer.writerow(['Second row', 'A',"Testing"', "Here's a quote"])
    return response
```
需要注意的是在show_csv()视图里的:

1) 通浏览器返回是csv文件,同时生成HttpResponse对象

2) 向对象里写入csv文件的内容.

3) 返回对象.

![show_csv.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/show_csv.png)

![show_csv_content.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/show_csv_content.png)

---

## 输出生成 CSV 文件-part2

这里,输出的csv文件,每一行都有相同的列数:
```python
# myste/urls.py
url(r'^chapter13/show_csv2/$','show_csv2'),

# mysite/show_non_html_content.py 
UNRULY_PASSENGERS = [146,184,235,200,226,251,299,273,281,304,203]
def show_csv2(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=show_csv.csv'
    writer = csv.writer(response)
    writer.writerow(['Year', 'Unruly Airline Passengers'])
   #for (year, num) in zip(range(1995, 2006), UNRULY_PASSENGERS):
        #writer.writerow([year, num])
        #print [year,num]
    for row in zip(range(1995, 2006), UNRULY_PASSENGERS):
        #(1995,146)==>[1995,146]
       writer.writerow(list(row))
    return response
```
这里,写入的是一个list,[year,num],即[(1995, 146), (1996, 184),...]
也可以使用list(row)方法,将(1995, 146)格式变换为==>[1995, 146]

### zip,list方法

tuple和list的转换

```python
# zip_list_method.py
x=[1,2,3]
print "type(x)=",type(x)    #type(x)= <type 'list'>
y=[4,5,6]

zipped=zip(x,y)
print "zippped=",zipped     #zippped= [(1, 4), (2, 5), (3, 6)]
print "type(zipped)=",type(zipped)  #type(zipped)= <type 'list'>

x2,y2=zip(*zipped)
print "x2=",x2,"\ty2=",     #x2= (1, 2, 3) 	y2= (4, 5, 6)
print "type(x2)=",type(x2)  #type(x2)= <type 'tuple'>

x2_list=list(x2)
print "x2_list=",x2_list    #x2_list= [1, 2, 3]
print "type(x2_list)=",type(x2_list)    #type(x2_list)= <type 'list'>
```
---
## 输出生成 CSV 文件-part3

如果要输出的csv文件很大,可以使用**StreamingHttpResponse**来代替HttpResponse

```python
# mysite/urls.py
url(r'^chapter13/show_csv3/$','some_streaming_csv_view'),

# mysite/show_non_html_content.py 
class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

from django.utils.six.moves import range
from django.http import StreamingHttpResponse
def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = (["Row {0}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response
```

在视图中,使用StreamingHttpResponse的方法:

1) 准备数据
> rows = (["Row {0}".format(idx), str(idx)] for idx in range(65536))

2) csv的writer对象,重写write方法,直接返回值,而不是存储在缓冲里.
> pseudo_buffer = Echo()

> writer = csv.writer(pseudo_buffer)

3) 使用上面的数据作为参数,生成StreamingHttpResponse对象实例
>response = StreamingHttpResponse((writer.writerow(row) for row in rows),content_type="text/csv")

4) 通知浏览器,文件保存的名称
> response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

5) 返回StreamingHttpResponse对象.

----


## 输出生成 XLS文件

在 https://docs.djangoproject.com/en/1.7/howto/outputting-csv/ 里有这样的一段话:
>Notice that there isn’t very much specific to CSV here – just the specific output format. You can use either of these techniques to output any text-based format you can dream of. You can also use a similar technique to generate arbitrary binary data;

意思是说,可以用类似生成csv文件的方法,来生成其他的文本类型的文件.

所以,这里,生成了xls文件(excle).

1) 配置URLconf

```python
#urls.py

url(r'^chapter13/show_xls/$','show_xls'),
```
2) 设置响应类型,**生成HttpResponse实例对象.**
> response=HttpResponse(content_type='text/xls')

3) 通知浏览器保存的文件名称

> response['Content-Disposition'] = 'attachment; filename="show_xls.xls"'

4) 将xls文件写入HttpResponse实例对象
>  wb.save(response)

5) 返回HttpResponse实例对象.

下面是完整的过程:

```python

# mysite/show_non_html_content.py 

import xlwt
from datetime import datetime
def show_xls(request):
    response=HttpResponse(content_type='text/xls')
    response['Content-Disposition'] = 'attachment; filename="show_xls.xls"'
    
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
            num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    ws.write(0, 0, 1234.56, style0)     #num
    ws.write(1, 0, datetime.now(), style1)  #time
    ws.write(2, 0, 1)
    ws.write(2, 1, 1)
    ws.write(2, 2, xlwt.Formula("$A3+$B3"))   #Formula
    
    wb.save(response)
    
    return response 
```

其中,生成xls文件内容的时候,使用的是python-excel的xlwt模块中自带的例子.

## 关于生成xls的资料

* 读取excle文件的模块: https://pypi.python.org/pypi/xlrd

* 写入excle文件的模块: https://pypi.python.org/pypi/xlwt

* Github主页:    https://github.com/python-excel/

* 教程: python-excel.pdf  http://www.simplistix.co.uk/presentations/python-excel.pdf

* 教程: https://github.com/python-excel/tutorial

----
## 输出生成 PDF文件

输出生成PDF文件的时候,需要使用reportlab库,找了好半天,发现也没有什么好选择的.

### 安装reportlab

* reportlab下载地址:https://bitbucket.org/rptlab/reportlab/downloads

* reportlab安装出现错误:http://my.oschina.net/zhangdapeng89/blog/54407
> 解决“Unable to find vcvarsall.bat”错误

* 安装minGW或者VS2008(+)

下面就是使用reportlab输出PDF文件.
```python
#mysite/urls.py
urlpatterns += patterns('mysite.show_non_html_content',
    ...
    url(r'^chapter13/show_pdf/$','show_pdf'),
)

# mysite/show_non_html_content.py
from reportlab.pdfgen import canvas    
def show_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="show_pdf.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100,100,"output PDF in Django by reportlab")
    p.showPage()
    p.save()
    return response

```
> 上面的代码很少,但是每一句都很有用.

0) 导入包:
```python
from reportlab.pdfgen import canvas
```

1) 生成HttpResponse对象,通知浏览器文件类型,注意是"**application/pdf**"而不是"**text/pdf**"
```python
response = HttpResponse(content_type='application/pdf')
```
2) 通知浏览器保存文件的名称:
```python
response['Content-Disposition'] = 'attachment; filename="show_pdf.pdf"'
```
3) 生成PDF文件,注意,canvas.Canvas(response)传入的参数是response,即为HttpResponse对象.

```python
    p = canvas.Canvas(response)
    p.drawString(100,100,"output PDF in Django by reportlab")
    p.showPage()
    p.save()
```

> 这里我们使用的 MIME 类型是 application/pdf 。这会告诉浏览器这个文档是一个 PDF 文档，而不是 HTML 文档。 如果忽略了这个参数，浏览器可能会把这个文件看成 HTML 文档，这会使浏览器的窗口中出现很奇怪的文字。 If you leave off this information, browsers will probably interpret the response as HTML, which will result in scary gobbledygook in the browser window.

> 使用 ReportLab 的 API 很简单： 只需要将 response 对象作为 canvas.Canvas 的第一个参数传入。

> 所有后续的 PDF 生成方法需要由 PDF 对象调用（在本例中是 p ），而不是 response 对象。

> 最后需要对 PDF 文件调用 showPage() 和 save() 方法（否则你会得到一个损坏的 PDF 文件）。

----

## 输出PDF文件-使用StringIO()

```python
#mysite/urls.py
urlpatterns += patterns('mysite.show_non_html_content',
    ...
    url(r'^chapter13/show_pdf_StringIO/$','show_pdf_StringIO'),
)

# mysite/show_non_html_content.py
from cStringIO import StringIO
def show_pdf_StringIO(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="show_pdf_StringIO.pdf"'

    temp=StringIO()
    print type(temp)

    p=canvas.Canvas(temp)
    p.drawString(250,500,"create pdf by reportelab,StringIO()")
    p.showPage()
    p.save()
    response.write(temp.getvalue())
    return response
```
上面的视图中,生成PDF,不是在生成对象的时候,

而是在最后使用response.write(temp.getvalue())


> **更多**使用reportlab 生成PDF文档的一个例子:

http://blog.sina.com.cn/s/blog_6b1ed4fb0101d86f.html

----


## 输出其他类型的文件的讨论 ,zip,图片,图表

* zip文件 Python 标准库中包含有 zipfile 模块，它可以读和写压缩的 ZIP 文件。

* Python 图片处理库PIL,它可以用于自动为图片生成缩略图

* matplotlib 可以用于生成通常是由 matlab 或者 Mathematica 生成的高质量图表。


