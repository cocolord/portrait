# 知乎

最新改版的个人主页，采用了json的数据格式，对抓取数据更加友好。之前和首页一样返回的是html字符串，解析相对繁琐些。

## config.ini
```
{
	"id": "用户id",
	"authorization": "",
	"dump_dir": "data",
    "ua": "../../config/user-agent.json",
	"base_url": "https://www.zhihu.com/api/v4/members/"
}
```

需要修改 `id` 和 `authorization` 两个字段