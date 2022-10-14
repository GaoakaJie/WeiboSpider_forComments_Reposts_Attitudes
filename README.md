## 功能
本程序可以根据**微博的mid**爬取**对应微博的点赞、转发与评论**的几乎全部信息，并将**结果写入csv文件**中。

## 代码结构
|文件名|函数名|功能|
|----|-----|----|
|parseAttitude|init|定义cookie、weibo_id、headers等参数|
||SpiderAttitude|构造点赞的url并解析点赞页的数据，包括点赞页翻页等功能|
||CsvPipeLineAttitude|创建csv文件并将解析好的result_lines列表写入文件|
|parseRepost|init|定义cookie、weibo_id、headers等参数|
||SpiderTransmit|构造转发页url并爬取所有转发人信息，包括转发页翻页等功能|
||CsvPipeLineTransmit|创建csv文件并将解析好的result_lines列表写入文件|
|parseComments|init|定义cookie、weibo_id、headers等参数|
||main|构造一级评论的url，提取翻页所用的相关参数，调用parse_response_data函数解析一级评论，包括一级评论翻页等内容|
||parse_response_data|解析一级评论的所有信息，并判断是否有二级评论，若有二级评论，则构造二级评论url，提取相关翻页参数，调用parse_secondary_comments函数解析二级评论，包括二级评论翻页等内容|
||parse_secondary_comments|解析二级评论的所有信息|
||CsvPipeLineComment|创建csv文件并将解析好的result_lines列表写入文件|
|start||输入weibo_id和cookie，运行整个程序|

## 输入和输出
### **输入**
- weibo_id = '详细博文的mid'<br>
- cookie = 'your cookie 值'

### **输出**
会分别输出三个文件：<br>
*attitudes.csv:*<br>

- mid:初始微博的mid，为一串数字形式
- attitude_id:初始微博的每一条点赞的id
- attitude_user_id:点赞用户的id
- attitude_user_screen_name:点赞用户的昵称

*reposts.csv:*<br>

- mid:初始微博的mid，为一串数字形式
- transmit_mid:初始微博的每一条转发的id
- transmit_user_id:转发用户的id
- transmit_user_screen_name:转发用户的昵称
- 该条转发显示的文本内容（eg.“转发微博”字样）

*comments.csv:*<br> 

- mid:初始微博的mid，为一串数字形式
- comment_mid:初始微博的每一条**一级评论**的id 
- comment_user_id:**一级评论**用户的id
- comment_user_screen_name:**一级评论**用户的昵称
- comment_content:**一级评论**的文本内容
- comment_pic_urls:**一级评论**中包含的图片url
- has_comments:bool值，是否有二级评论
- secondary_comments_num:**二级评论**的数量
- secondary_comment_mid:**二级评论**的id
- secondary_comment_user_id:**二级评论**用户的id
- secondary_user_screen_names:**二级评论**用户的名称
- secondary_comment_content:**二级评论**的文本内容
- secondary_comment_pic_urls:**二级评论**中包含的图片url

## 运行程序
输入weibo_id与cookie后直接运行start.py即可<br>

## tips:

**如何获取cookie**<br>
1. 用Chrome打开[https://weibo.com/](https://weibo.com/)<br>
2. 点击“立即登录”，完成私信验证或手机验证码验证，进入新版微博
3. 按F12打开开发者工具，在开发者工具的Network->Name->weibo.cn->Headers->Request Headers，找到“cookie:"后的值，这就是我们需要的cookie值，复制即可,如图所示。<br>
![](/pics/pic1.png)

**如何获取初始微博的mid，即weibo-id**<br>
方式一：<br>
通过其他微博爬虫，如关键字爬取微博内容等获取相应微博的mid<br>
方式二：（手动获取）<br>
1. 点击某条微博右上角向下箭头符号，复制微博链接
2. 打开新链接，注意链接中最后一串字符串，F12打开开发者工具，在开发者工具的Network->Name中找到'show?id=刚才链接中的字符串'
3. 点击后找到preview->“id:”,其中id后的值就是我们需要的微博mid，复制即可，如图所示。<br>
![](/pics/pic2.png)

*second commit*<br>
*新增了异常捕获，补充了请求头的信息，注意容易被封ip和账号，要记得更新cookie*
