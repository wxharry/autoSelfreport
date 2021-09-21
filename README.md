[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/wxharry/autoSelfreport)



# autoSelfreport

上海大学新冠疫情自动填报脚本(个人精简版)



## 参考&鸣谢

[rllll/selfreport 上海大学SHU自动每日一报](https://github.com/rllll/selfreport)



## 文件介绍

```selfreport.py``` 兼容win32和linux的自动填报脚本

`Timing.py` 计时器，每小时检查一次(此版本不用，~~因为看不懂，~~ 使用schedule外部库代替)

`log.txt` 日志文件，记录成功填报的用户名和时间




## 使用方式

### Linux下载google-chrome

新建文件 配置yum源

```
vim /ect/yum.repos.d/google-chrome.repo
```

写入以下内容
```
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
```

安装

```
yum install -y google-chrome-stable

yum install -y google-chrome-stable --nogpgcheck # 国内如果无法使用添加参数安装
```


### 查看google-chrome版本

#### windows

在chrome浏览器中输入

`chrome://version`

回车即可查看。



#### Linux

`google-chrome --version`



### 下载chromedriver
根据当前操作系统的类型和google-chrome版本选择对应的驱动下载，解压，放在当前文件夹即可。
> chromedriver下载地址：  
>
> http://chromedriver.storage.googleapis.com/index.html  
>
> https://npm.taobao.org/mirrors/chromedriver/



### 安装依赖
`pip install -r requirements.txt`



### 新建登陆信息表

为保护个人信息安全，存放用户名和密码的`userInfo.json`不会提交上传，使用前必须先自行创建。格式如下：

```
# userInfo.json
{
    "username": "YourUsername",
    "password": "YourPassword"
}
```



###  运行程序

在终端运行`python main.py`即可启动自动填报系统。