# Chapter13_non_html_content

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




