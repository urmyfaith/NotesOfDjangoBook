# Django-Boook-Chapter5-Models


## 数据库设计

* 作者:姓名,邮件地址,头像

* 书:书名,作者,出版人,出版日期

* 出版社:名称,地址,城市,省,国,网址

## 数据库操作

* 选择对象 
```python
Publisher.objects.all()
```

* 数据过滤
```python
 Publisher.objects.filter(country="U.S.A.", state_province="CA")
```
* 数据排序
1. 单字段排序
2. 多字段排序
3. 逆向排序

```python
Publisher.objects.order_by("name")
Publisher.objects.order_by("state_province", "address")
Publisher.objects.order_by("-name")
```

逆向排序的数据库设计 :
```python
class Meta:
        ordering = ['name']
```
* 连锁查询(多条件查询,)
```python
Publisher.objects.filter(country="U.S.A.").order_by("-name")
```

* 限制返回数据条数
```python
Publisher.objects.order_by('name')[0]    #一条记录
Publisher.objects.order_by('name')[0:2]    #三条记录
```

* 更新记录
```python
 Publisher.objects.all().update(country='USA')
```

* 删除记录
```python
 Publisher.objects.filter(country='USA').delete()
 Publisher.objects.all().delete()
```

-----

![db-design.png](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/notes/images/db-design.png "db-design.png")
