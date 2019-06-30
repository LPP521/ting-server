# ting-server

目前针对http方式，以www.ting89.com为例做了第一个server模板。

主要提供以下接口：
1、获得支持的模板，目前只支持ting89模板
2、根据提供的url获得指定播放列表
3、根据提供的url+index获得指定的播放url

python3 -m aiohttp.web -P 18004 -H 0.0.0.0 server:app

添加了对百度网盘的支持，但是目前版本的百度网盘开发接口貌似不好用了，找了一个python2的项目，这也是目前找到唯一能用的代码https://github.com/PeterDing/iScript
取了其中百度网盘部分脚本放在baidu2.py中

百度部分需要登录才能使用，特意注册了一个百度网盘，u03013112密码是a131的那个
目前只支持cookies登录，cookies文件一并上传，如果过期太过频繁，再想办法，测测看吧

登录方式https://github.com/PeterDing/iScript#cookie_login