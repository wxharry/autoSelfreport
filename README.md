# autoSelfreport

上海大学新冠疫情自动填报脚本

## 参考&鸣谢

[rllll/selfreport 上海大学SHU自动每日一报](https://github.com/rllll/selfreport)

## 代码介绍：
`selfreport-win.py`是适用于windows操作系统的脚本，可以看到操作流程。

`selfreport-linux.py`是适用于linux操作系统的服务器脚本，不会打开网页。

## 使用方式：
考虑到使用人信息，存放用户名和密码的`userInfo.json`不会提交上传，使用前请自行创建。格式如下：

```
# userInfo.json
{
    "userList":[{
        "username": "YourUsername",
        "password": "YourPassword"
    }]
}
```
创建并填写正确的账户和密码，运行操作系统对应的脚本即可。

## TODO:
1. 定时填报
2. 代码封装