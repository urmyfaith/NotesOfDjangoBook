# windows下git使用

* git的安装
从网盘下载安装即可

* 使用git连接github

1）生成本机的密钥
```bat
ssh-keygen -C 'urmyfaith.com' -t rsa
```
2）将生存的密钥添加到github网站中

a)登陆https://github.com/settings/ssh

b）Add an SSH Key

3）测试是否可以登录github使用
```bat
	ssh -T git@github.com
```


4）本地git初始化
```bat
    git init  
```

    
5） 拉取服务器项目
```bat
 git pull  https://github.com/urmyfaith/NotesOfDjangoBook.git 
```

  
6） 修改，添加文件,提交
```bat
git add filname_here

git commit -m "notes_here"
```



7） 提交更改到服务器


```bat
git remote add origin https://github.com/urmyfaith/NotesOfDjangoBook
# also:
# git remote add origin https://github.com/urmyfaith/NotesOfDjangoBook.git

git push -u origin

```



----

参考：

* [http://casparzhang.blog.163.com/blog/static/12662655820140705139542/](git安装和简单使用 "")

* [git总结](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/Git%E7%AE%80%E6%98%8E%E6%89%8B%E5%86%8C.pdf "") 