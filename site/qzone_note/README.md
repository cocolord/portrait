# 留言

## config.ini

新建配置文件，内容如下

```
{
  "qq": 100001,
  "dump_dir": "data/test",
  "base_url": "https://mobile.qzone.qq.com/get_feeds",
  "cookie": ""
}
```

- qq：需要抓取的qq号，必须有权限进入其空间
- dump_dir：存储数据的路径
- base_url：数据接口，无需调整
- cookie：使用chrome登录空间，自行复制粘贴


## 未登录

```
{
    "code":-3000,
    "subcode":-3000,
    "message":"请先登录",
    "notice":0,
    "time":1479383674,
    "tips":"0000-366"
}
```

## 服务器繁忙
```
{
    "code":-5008,
    "subcode":-5008,
    "message":"服务器繁忙，请稍候再试。",
    "notice":0,
    "time":1479372314,
    "tips":"0000-366"
}
```

## 接口分析
```
{
    "code":0,
    "subcode":0,
    "message":"",
    "default":0,
    "data":{
        "attach_info":"att=offset%3D10%26&tl=1472132755",
        "auto_load":0,
        "has_more":1,
        "remain_count":2536,
        "vFeeds":Array[10]
    }
}
```

```
"vFeeds":[
    {
        "cell_template":{
            "id":""
        },
        "comm":{
            "actiontype":0,
            "actionurl":"",
            "appid":334,
            "curlikekey":"",
            "feedskey":"2000060539",
            "feedstype":0,
            "operatemask":2195456,
            "orglikekey":"",
            "originaltype":0,
            "refer":"",
            "subid":0,
            "time":1478842732
        },
        "id":{
            "cellid":"2000060539",
            "subid":""
        },
        "operation":{
            "busi_param":{
                "14":"1126180429",
                "16":"3"
            },
            "share_info":{
                "photo":null,
                "summary":"",
                "title":""
            }
        },
        "summary":{
            "summary":"么么么么哒[em]e400846[/em]"
        },
        "userinfo":{
            "user":{
                "from":1,
                "is_owner":0,
                "level":1,
                "logo":"",
                "nickname":"", //昵称
                "stuStarInfo":{
                    "iStarLevel":0,
                    "iStarStatus":0,
                    "isAnnualVip":0
                },
                "uin":"", //qq号
                "vip":0
            }
        }
    }
]
```