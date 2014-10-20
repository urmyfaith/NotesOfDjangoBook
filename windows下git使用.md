# windows下git使用

* git的安装
从网盘下载安装即可

* 使用git连接github

1）生成本机的密钥
ssh-keygen -C 'urmyfaith.com' -t rsa

2）将生存的密钥添加到github网站中

a)登陆https://github.com/settings/ssh

b）Add an SSH Key

3）测试是否可以登录github使用

	ssh -T git@github.com

4）本地git初始化

    git init  
    
5） 拉取服务器项目

  git pull  https://github.com/urmyfaith/NotesOfDjangoBook.git
  
6） 修改，添加文件后push

