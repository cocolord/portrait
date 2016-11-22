# 说说

## config.ini

新建配置文件，内容如下

```
{
  "qq": 100001,
  "dump_dir": "talk/data/",
  "base_url": "https://mobile.qzone.qq.com/get_feeds",
  "cookie": ""
}
```

- qq：需要抓取的qq号，必须有权限进入其空间
- dump_dir：存储数据的路径
- base_url：数据接口，无需调整
- cookie：使用chrome登录空间，自行复制粘贴


## response 分析

使用spider得到的数据并非json格式

- [说说](#说说)
- [评论](#评论)
- [点赞](#点赞)
- [图片](#图片)

### 例子

```
_Callback({
  "code": 0,
  "subcode": 0,
  "message": "",
  "default": 0,
  "data" {
    "attachinfo": "att=back%5Fserver%5Finfo%3Doffset%253D10%2526",
    "hasmore": 1,
    "newcnt": 0,
    "undeal_info": {
      "active_cnt": 3,
      "gamebar_cnt": 1,
      "gift_cnt": 0,
      "passive_cnt": 0,
      "visitor_cnt": 0
    },
    "vFeeds": [
      {
        "cell_template": {},
        "comm": {},
        "comment": {},        // 评论
        "id": {},
        "lbs": {},
        "like": {},           // 点赞
        "operation": {},
        "pic": {},            // 图片
        "summary": {},        // 说说
        "userinfo": {},       // 说说主人的信息，昵称、qq
        "visitor": {
          "view_count":41,    // 多少人看了
          "visitor_count":0,
          "visitors":null
        }
      },
      {},
      {}
    ]
  }
);
```

### 未登录

```
{
  "code":-3000,
  "subcode":-3000,
  "message":"请先登录",
  "notice":0,
  "time":1479383674,
  "tips":"0000-403"
}
```


### 请求繁忙

```
{
  "code":-10000,
  "subcode":-19000,
  "message":"服务器繁忙，请稍候再试。",
  "notice":0,
  "time":1479116441,
  "tips":"0000-692"
}
```


### 说说

```
"summary": {
  "summary": "说说正文"
}
```


### 评论

这里只把必要的字段展示出来

```
"comment": {
  "cntnum": 5,
  "comments": [
    "content": "评论内容，吧啦吧啦[em]e400824[/em]",
    "date": 1454249315,
    "replys": [
      {
        "content": "回复1",
        "date": 1454250816,
        "target": {
          "nickname": "昵称",
          "uin": "qq号"
        },
        "user": {
          "nickname": "昵称",
          "uin": "qq号"
        }
      }
    ]
  ],
  "main_comment": null,
  "num": 5
}
```


### 点赞

```
"like": {
  "isliked": 0,           // 自己是否点赞
  "likemans": [{},{}],    // 点赞的个别好友，有昵称和qq
  "num": 6                // 点赞人数
}
```


### 图片

URL经过处理，可以下载图片

https://h5.qzone.qq.com/tx_tls_gate=m.qpic.cn/psb?V1PE&rfdc_b-0-0

```
"pic": {
  "picdata": {
    "pic": [
      {
        "photourl": {
          "0": {
            "height": 1080,
            "url": "",
            "width": 1442
          },
          "1": {
            "height":1080,
            "url":"http://m.qpic.cn/psb?/V10V1neG0jBXPE/",
            "width":1442
          },
          "11":{
            "height":200,
            "url":"http://m.qpic.cn/psb?/V10V1neG0jBXPE/*vHF5iY1",
            "width":267
          }
        }
      }
    ]
  }
}
```

0和1对应的都是大图，虽然url有非常细微的差别，这里我们还把他们归为一类，即大图。11对应的是小图。

大图1080 * 1442，小图200 * 267。这两个的区别在于：

- 大图对应 `b`，小图对应 `m`
- sce对应的值不同。大图34-0-0，小图34-11-3

```
http://m.qpic.cn/psb?/V10V1neG0jBXPE/**5Ob3ggxuvBqBRys!/b/&ek=1&kp=1&pt=0&bo=!&su=#sce=34-0-0&rf=.4.-0-0

http://m.qpic.cn/psb?/V10V1neG0jBXPE/**5Ob3ggxuvBqBRys!/m/&ek=1&kp=1&pt=0&bo=!&su=#sce=34-11-3&rf=.4.-0-00
```


