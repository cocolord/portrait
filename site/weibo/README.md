# 微博

微博是一个开放平台，不需要登录即可以查看其它用户的内容

[v1版文档](readme-v1.md)

## config.ini

新建配置文件，内容如下

```
{
    "uid": 10001000,
    "dump_dir": "weibo/data/"
}
```

- uid：需要抓取的微博账号的id
- dump_dir：存储数据的路径

如果抓取大量数据，超过2000条，则需要添加cookie字段

## 接口分析

这里仅展现部分字段

```
{
    "ok":1,
    "count":298,
    "cards":[
        {
            "card_group":[
            {
                "mblog":{
                    "created_at":"2013-03-03 20:58",
                    "text":"微博正文",
                    "source":"iPhone",
                    "pic_ids":[
                        "图片id",
                        "图片id"
                    ],
                    "thumbnail_pic":"http://ww2.sinaimg.cn/thumbnail/图片id.jpg",     // 小图
                    "bmiddle_pic":"http://ww2.sinaimg.cn/bmiddle/图片id.jpg",     // 中图
                    "original_pic":"http://ww2.sinaimg.cn/large/图片id.jpg",      // 原图
                    "reposts_count":2,      // 转发数
                    "comments_count":2,     // 评论数
                    "attitudes_count":58,   // 点赞数
                    "like_count":7,         // 点赞数
                    "created_timestamp":1362315488,
                    "url_struct":[
                        {
                             "url_title":"地点定位"
                        }
                    ],
                    "topic_struct":[ // 话题
                        {
                            "topic_title":"面包游记推荐",
                            "topic_url":"sinaweibo://pageinfo?containerid=&pageid=&extparam="
                        }
                    ],
                    "url_struct":[ // 链接
                        {
                            "short_url":"http://t.cn/RcLnLDo",
                            "ori_url":"http://t.cn/RcLnLDo",
                            "url_title":"网页链接",
                            "url_type_pic":"http://h5.sinaimg.cn/upload/2015/09/25/3/timeline_card_small_web.png",
                            "position":2,
                            "url_type":0,
                            "result":true,
                            "need_save_obj":1
                        }
                    ]
                }
            }
            ]
        }
    ]
}

```


## 没有更多内容
```
{
    "ok": 1,
    "count": 298,
    "cards": [
        {
            "mod_type": "mod/empty",
            "msg": "没有内容"
        }
    ]
}
```
