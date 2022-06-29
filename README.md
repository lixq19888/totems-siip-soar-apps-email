## 安博通 www.abtnetworks.com
## 概述

电子邮件是—种用电子手段提供信息交换的通信方式，是互联网应用最广的服务，目前仅提供文本内容的发送。

## 使用说明

Email 在平台上能正常执行的前置条件如下：

1、配置实例，将常用的邮箱服务host、发件人等基础信息填写完成，作为预设，便于后续发邮件时，直接使用；

2、配置动作参数，填写收件人、邮件内容即可发送邮件。


## 配置实例

| **参数** |  **参数别名** | **描述** | **必填** | **示例** |
| --- | --- | --- |  --- | --- |
| host | SMTP 服务器 |不同类型邮箱，支持的smtp不同 |  是 | smtp.exmail.qq.com |
| port | 端口 |  发件人邮箱服务端口 | 否 |465 |
| fromAddress | 发件人 | 发件人邮箱地址 |  否|zhangsan@abt.com |
| fromAddressAlias | 发件人别名 |发件人别名 |  否 |张三 | 
| password | 发件人邮箱密码 | 发件人邮箱密码 | 否 | 123456 |
| debug | 是否打开调试 |  打开调试时，会将运行过程中的日志打印出来，默认关闭 | 否 |false |

#### smtp 服务器说明

| **邮箱类型** | **smtp** |
| --- | --- | 
| QQ邮箱 | smtp.qq.com | 
| 163邮箱 | smtp.163.com |
| 126邮箱 | smtp.126.com |
| 安博通邮箱 | smtp.exmail.qq.com | 

#### 发件人邮箱密码说明
发件人邮箱密码，这里有的是填写密码，部分邮箱填写的是授权码，请注意，目前已知QQ邮箱密码填写的是授权码。


## 配置动作

### 1、文本邮件发送

纯文本内容邮件发送。

#### 参数
| **参数** | **参数别名** | **描述** | **必填** | **示例** |
| --- | --- | --- | --- |  --- |
| toAddress | 收件人 | 收件人，支持多个，用逗号隔开 |  是 |zhangsan@abt.com,lisi@abt.com |
| subject | 主题 |  邮件主题 |是 | 网络安全 |
| content | 邮件内容 | 邮件内容 | 是 | 这是个好工具 |

#### 返回

```
send success
```


#### 返回json字段说明

```json
{
    "message":"success",
    "data":"邮件发送状态",
    "schema":{
        "type":"STRING"
    },
    "debugOutput":"调试信息",
    "status":"Success"
}
```

#### 返回示例
```json
{
    "message":"success",
    "data":"send success",
    "schema":{
        "type":"STRING"
    },
    "debugOutput":"subject:测试邮件发送, to_address:123456@qq.com\nmail_host:smtp.exmail.qq.com\n",
    "status":"Success"
}
```


