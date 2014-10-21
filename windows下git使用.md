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

3）测试是否可以登录github使用，添加用户名和邮箱
```bat
$ ssh -T git@github.com
$ git config --global user.email "urmyfaith@qq.com"

$ git config --global user.name "urmyfaith"

```


4）本地git初始化
```bat
$    git init  
```

    
5） 拉取服务器项目
```bat
$ git pull  https://github.com/urmyfaith/NotesOfDjangoBook.git 
或者
$ git pull git@github.com:urmyfaith/NotesOfDjangoBook.git
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
# git remote add origin git@github.com:urmyfaith/NotesOfDjangoBook.git
git push -u origin

```

* 提交时候密码的问题：

如果不想每次提交都输入密码，可以更改“.git/config"文件中的url值格式为：
```
 url = git@github.com:[user_name]/[project_name].git
```

```bat
[core]
	repositoryformatversion = 0
	filemode = false
	bare = false
	logallrefupdates = true
	symlinks = false
	ignorecase = true
	hideDotFiles = dotGitOnly
[remote "origin"]
	url = git@github.com:urmyfaith/NotesOfDjangoBook.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
	remote = origin
	merge = refs/heads/master
```


## vim编码设置
(显示中文乱码问题，最后一行解决）
vimrc文件位置：
添加如下设置
```
set nocompatible
set number
filetype on
set history=1000
set background=dark
syntax on
set autoindent
set smartindent
set tabstop=4
set shiftwidth=4
set showmatch
set guioptions-=T
set vb t_vb=
set ruler
set nohls
set incsearch
if has("vms")
set nobackup
else
set backup
endif
set fileencodings=utf-8,gbk
```

## git ls显示中文乱码问题
编辑
```
C:\Program Files\Git\etc\git-completion.bash
```
添加：
```
alias ls="ls --show-control-chars"
```


----

参考：

* [http://casparzhang.blog.163.com/blog/static/12662655820140705139542/](git安装和简单使用 "")

* [git总结](https://raw.githubusercontent.com/urmyfaith/NotesOfDjangoBook/master/Git%E7%AE%80%E6%98%8E%E6%89%8B%E5%86%8C.pdf "") 