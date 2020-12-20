# autoSelfreport

上海大学新冠疫情自动填报脚本



## 参考&鸣谢

[rllll/selfreport 上海大学SHU自动每日一报](https://github.com/rllll/selfreport)



## 文件介绍

~~`selfreport_win.py` 适用于windows操作系统的脚本，运行可以在浏览器中看到操作流程。~~

~~`selfreport_linux.py` 适用于linux操作系统的服务器脚本，不会打开网页，便于后台运行。~~

```selfreport.py``` 兼容win32和linux的自动填报脚本

`selfreport.ipynb` ~~便于在服务器进行开发和简单运行的代码文件~~ 用于手动填报

`Timing.py` 计时器，每小时检查一次

`log.txt` 日志文件，记录成功填报的用户名和时间



## 使用方式

### 下载chromedriver
根据当前操作系统的类型和google-chrome版本选择对应的驱动下载，放在当前文件夹即可。
> chromedriver下载地址：  
> http://chromedriver.storage.googleapis.com/index.html  
> https://npm.taobao.org/mirrors/chromedriver/



### 新建登陆信息表

为保护个人信息安全，存放用户名和密码的`userInfo.json`不会提交上传，使用前必须先自行创建。格式如下：

```
# userInfo.json
{
    "userList":[{
        "username": "YourUsername",
        "password": "YourPassword"
    }]
}
```


###  运行程序

在终端运行`python main.py`即可启动自动填报系统。



## 其他
### windows查看google-chrome版本
在chrome浏览器中输入`chrome://version`并回车即可查看。

### Linux查看google-chrome版本
`google-chrome --version`

### Linux下载google-chrome
对于谷歌Chrome32位版本，使用如下链接：

`wget https://dl.google.com/linux/direct/google-chrome-stable_current_i386.deb`

对于64位版本可以使用如下链接下载：

`wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb`

## TODO:
1. 程序报错后发邮件通知管理员