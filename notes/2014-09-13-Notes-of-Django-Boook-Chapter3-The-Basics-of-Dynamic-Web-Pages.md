
# Chapter3 Views and URLconfs

## Django是怎么处理请求的

1. 进来的请求转入/hello/.

2. Django通过在ROOT_URLCONF配置来决定根URLconf.

3. Django在URLconf中的所有URL模式中，查找第一个匹配/hello/的条目。

4. 如果找到匹配，将调用相应的视图函数

5. 视图函数返回一个HttpResponse

6. Django转换HttpResponse为一个适合的HTTP response， 以Web page显示出来

## 出错信息的使用


1. 点击代码可以查看代码所在的附近的行

2. 可以复制所有的出错信息

3. 可以直接将出错信息生成页面,分享.

##   assert False

代码中添加此句,可以在浏览器访问页面时查看附近行代码和变量

```python
  assert False
```
 