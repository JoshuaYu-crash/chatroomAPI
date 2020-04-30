# 接口

## 全局状态码

| 错误码 | 错误描述       |
| ------ | -------------- |
| 1001   | 关键信息错误   |
| 1002   | 数据库处理出错 |
| 1003   | 查不到信息     |
| 1004   | 信息重复       |
| 0      | 正常           |

## 接口示例

### 首页注册

**请求URL：**

- <http://127.0.0.1:5000/apiv1/user/register>

**请求方式：**

- POST

**参数：**

| 参数名     | 必选 | 类型   | 说明     |
| ---------- | ---- | ------ | -------- |
| username   | 是   | String | 用户名   |
| userdetail | 否   | Text   | 自我介绍 |
| phone      | 否   | String | 手机号   |
| location   | 否   | String | 地址     |

**请求示例:**

```json
{
    "username":"testuser",
    "userdetail":"哈哈",
    "phone":"13800000000"
}
```

**返回示例：**

```json
{
    "status": 0,
    "message": "",
    "data":{
        "username":"testuser",
        "userdetail":"哈哈",
        "phone":"13800000000"
	}
}
```

**备注：**

- 无

---

### 房间创建

**请求URL：**

- <http://127.0.0.1:5000/apiv1/user/roomcreate>

**请求方式：**

- POST

**参数：**

| 参数名     | 必选 | 类型   | 说明     |
| ---------- | ---- | ------ | -------- |
| roomowner  | 是   | String | 房主     |
| roomname   | 是   | String | 房间名   |
| roomdetail | 是   | Text   | 房间介绍 |

**请求示例:**

```json
{
    "roomowner": "testuser",
    "roomname":"testroom",
    "roomdetail":"哈哈哈",
}
```

**返回示例：**

```json
{
    "status": 0,
    "message": "",
    "data":{
        "roomname": "testroom",
        "roomdetail": "哈哈哈",
    	"roomurl": "http://127.0.0.1/apiv1/joinroom/testroom",
    	"roomowner": "testuser"
	}
}
```

**备注：**

- 无

---

### 个人头像

**请求URL：**

- <http://127.0.0.1:5000/apiv1/user/avatar/username>

**请求方式：**

- POST

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| username | 是   | String | 用户名 |

**请求示例:**

<http://127.0.0.1:5000/apiv1/user/avatar/testuser>

**返回示例：**

```json
{
    "status": 0,
    "message": ""
}
```

**备注：**

- 无

---

### 房间头像

**请求URL：**

- <http://127.0.0.1:5000/apiv1/room/avatar/upload/roomname>

**请求方式：**

- POST

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| roomname | 是   | String | 房间名 |

**请求示例:**

<http://127.0.0.1:5000/apiv1/room/avatar/upload/testroom>

**返回示例：**

```json
{
    "status": 0,
    "message": ""
}
```

**备注：**

- 无

---

### 个人信息

**请求URL：**

- <http://127.0.0.1:5000/apiv1/user/query>

**请求方式：**

- POST

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| roomname | 是   | String | 房间名 |

**请求示例:**

```json
{
    "username":"testuser",
}
```

**返回示例：**

```json
{
    "status": 0,
    "message": "",
    "data":{
        "username": "testuser",
        "userdetail": "哈哈",
    	"phone": "13800000000",
    	"useravatar": "/apiv1/user/avatar/download/testuser"
	}
}
```

**备注：**

- 无

---

### 房间信息

**请求URL：**

- <http://127.0.0.1:5000/apiv1/room/query>

**请求方式：**

- POST

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| roomname | 是   | String | 房间名 |

**请求示例:**

```json
{
    "roomname":"testroom",
}
```

**返回示例：**

```json
{
    "status": 0,
    "message": "",
    "data":{
        "roomname": "testuser",
        "onlineusers": 1,
        "roomdetail": "哈哈哈",
    	"roomavatar": "/apiv1/user/avatar/download/testroom",
    	"roomowner": "testuser",
    	"roomurl": "/apiv1/joinroom/testroom"
	}
}
```

**备注：**

- 无

---

### 获取用户头像

**请求URL：**

- <http://127.0.0.1/apiv1/user/avatar/download/username>

**请求方式：**

- GET

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| username | 是   | String | 用户名 |

**请求示例:**

<http://127.0.0.1/apiv1/user/avatar/download/testuser>

**返回示例：**

- 一张图片

**备注：**

- 无

---

### 获取房间头像

**请求URL：**

- <http://127.0.0.1:5000/apiv1/room/avatar/download/roomname>

**请求方式：**

- GET

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| roomname | 是   | String | 房间名 |

**请求示例:**

<http://127.0.0.1:5000/apiv1/room/avatar/download/testroom>

**返回示例：**

- 一张图片

**备注：**

- 无

---

### 房间之前的消息

**请求URL：**

- <http://127.0.0.1:5000/apiv1/room/message/roomname>

**请求方式：**

- GET

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| roomname | 是   | String | 房间名 |

**请求示例:**

<http://127.0.0.1:5000/apiv1/room/message/testroom>

**返回示例：**

```json
{
    "status": 0,
    "message": "",
    "data": {
        "onlineusers": 1,
        "msg":[
            {
                "username": "testuser",
                "useravatar": "/apiv1/user/avatar/download/testuser",
                "message": "666",
                "sendtime": "2020-04-06 14:00:28"
            },
            {
                "username": "testuser",
                "useravatar": "/apiv1/user/avatar/download/testuser",
                "message": "666",
                "sendtime": "2020-04-06 14:10:28"
            }
        ]
}
```

**备注：**

- 无

---

### 房间删除

**请求URL：**

- <http://127.0.0.1:5000/apiv1/room/delete/>

**请求方式：**

- POST

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| roomname | 是   | String | 房间名 |

**请求示例:**

```json
{
    "roomowner": "testuser",
    "roomname":"testroom"
}
```

**返回示例：**

```json
{
    "status": 0,
    "message": "",
}
```

**备注：**

- 先检查用户是否为房主，如果是则先删除所有消息，再删除所有用户（直接在数据库中删除），如果不是，则没有权限

---

### 用户退出

**请求URL：**

- <http://127.0.0.1:5000/apiv1/user/delete/>

**请求方式：**

- POST

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| username | 是   | String | 用户名 |

**请求示例:**

```json
{
    "username":"testuser"
}
```

**返回示例：**

```json
{
    "status": 0,
    "message": "",
}
```

**备注：**

- 检查用户是否为房主，如果是则先删除所有消息，再删除所有用户（直接在数据库中删除），如果不是，则删除该用户所有历史消息

### 修改用户信息

**请求URL：**

- <http://127.0.0.1:5000/apiv1/user/modify>

**请求方式：**

- POST

**参数：**

| 参数名     | 必选 | 类型   | 说明     |
| ---------- | ---- | ------ | -------- |
| username   | 是   | String | 用户名   |
| userdetail | 否   | Text   | 自我介绍 |
| phone      | 否   | String | 手机号   |
| location   | 否   | String | 地址     |

**请求示例:**

```json
{
    "username":"testuser",
    "newusername":"testuser1",
    "userdetail":"哈哈",
    "phone":"13800000000",
    "location":"福建省"
}
```

**返回示例：**

```json
{
    "status": 0,
    "message": "",
    "data":{
       "username":"testuser1",
        "userdetail":"哈哈",
        "phone":"13800000000",
        "location":"福建省" 
    }
}
```

**备注：**

- 无

### 修改房间信息

**请求URL：**

- <http://127.0.0.1:5000/apiv1/room/modify>

**请求方式：**

- POST

**参数：**

| 参数名     | 必选 | 类型   | 说明     |
| ---------- | ---- | ------ | -------- |
| roomname   | 是   | String | 房间名   |
| roomdetail | 否   | Text   | 房间介绍 |

**请求示例:**

```json
{
    "roomname":"testroom",
    "roomdetail":"哈哈哈",
}
```

**返回示例：**

```json
{
    "status": 0,
    "message": "",
    "data":{
       "roomname":"testroom",
        "roomdetail":"哈哈哈",
    }
}
```

**备注：**

- 无

## socket接口事件（http://127.0.0.1:5000/）

### join

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| username | 是   | String | 用户名 |
| roomname | 是   | String | 房间名 |

**返回示例：**

- 消息名：message

```json
{
    "status": 0,
    "data":{
          "action":"in",
       	  "onlineusers":1,
          "username":"testuser",
          "useravatar": "/apiv1/user/avatar/download/testuser"
    }
}
```

**备注：**

- json格式

### leave

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| username | 是   | String | 用户名 |
| roomname | 是   | String | 房间名 |

**返回示例：**

- 消息名：message

```json
{
    "status": 0,
    "data":{
        "action":"out",
        "onlineusers":1,
        "username":"testuser",
        "useravatar": "/apiv1/user/avatar/download/testuser"
    }
}
```

**备注：**

- json格式

### new message

**参数：**

| 参数名   | 必选 | 类型   | 说明     |
| -------- | ---- | ------ | -------- |
| username | 是   | String | 用户名   |
| roomname | 是   | String | 房间名   |
| message  | 是   | String | 消息内容 |

**返回示例：**

- 消息名：message

```json
{
    "status": 0,
    "data":{
       "useranme":"testuser",
        "useravatar": "/apiv1/user/avatar/download/testuser",
       "roomname":"testroom",
       "message":"hello",
       "sendttime":"2020-04-06 14:10:28"
    }
}
```

**备注：**

- json格式

### close

**参数：**

| 参数名    | 必选 | 类型   | 说明     |
| --------- | ---- | ------ | -------- |
| roomname  | 是   | String | 房间名   |
| roomowner | 是   | String | 房间主人 |

**返回示例：**

- 消息名：message

```json
{
    "status": 0,
    "data":{
        "action":"close",
        "roomname":"testroom"
    }
}
```

**备注：**

- json格式