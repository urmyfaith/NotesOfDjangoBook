

## Django是怎么处理请求的

1. 进来的请求转入/hello/.

2. Django通过在ROOT_URLCONF配置来决定根URLconf.

3. Django在URLconf中的所有URL模式中，查找第一个匹配/hello/的条目。

4. 如果找到匹配，将调用相应的视图函数

5. 视图函数返回一个HttpResponse

6. Django转换HttpResponse为一个适合的HTTP response， 以Web page显示出来

