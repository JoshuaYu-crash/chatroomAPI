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
| userdetail | 是   | Text   | 自我介绍 |
| phone      | 否   | String | 手机号   |

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

- <http://127.0.0.1:5000/apiv1/user/avatar/upload/username>

**请求方式：**

- POST

**参数：**

| 参数名   | 必选 | 类型   | 说明   |
| -------- | ---- | ------ | ------ |
| username | 是   | String | 用户名 |

**请求示例:**

<http://127.0.0.1:5000/apiv1/user/avatar/upload/testuser>

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
    	"useravatar": "http://127.0.0.1/apiv1/user/avatar/download/testuser"
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
        "roomdetail": "哈哈哈",
    	"roomavatar": "",
    	"roomowner": "testuser",
    	"roomurl": "http://127.0.0.1/apiv1/joinroom/testroom"
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
    "data": [
        {
            "username": "testuser",
            "message": "666",
            "sendtime": "2020-04-06 14:00:28"
        },
        {
            "username": "testuser",
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



