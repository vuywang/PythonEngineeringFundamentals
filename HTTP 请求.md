# 1. HTTP 请求是什么？🤔

HTTP 请求大概就是这个流程：

```text
Python 程序
   ↓ 发送请求
服务器 / API
   ↓ 返回响应
Python 程序拿到结果
```

比如你访问一个天气接口：

```text
请求：我要上海今天的天气
响应：温度、湿度、风速、天气状态
```

HTTP 里常见的方法有 `GET`、`POST`、`PUT`、`DELETE`、`PATCH` 等；其中 `GET` 通常用于获取资源，`POST` 通常用于向服务器提交数据并可能改变服务器状态。([MDN Web Docs][1])

---

# 2. Python 里用什么发 HTTP 请求？📦

Python 标准库里有 `urllib.request`，可以打开 URL、处理 HTTP、认证、重定向、Cookie 等；但 Python 官方文档也直接提示：如果想要更高层的 HTTP 客户端接口，推荐用 Requests。([Python documentation][2])

所以学习阶段建议你先学：

```text
requests
```

它不是 Python 标准库，需要安装：

```bash
python -m pip install requests
```

以后如果你学异步请求，再学：

```text
httpx
aiohttp
```

其中 HTTPX 支持同步和异步 API，也支持 HTTP/1.1 和 HTTP/2。([HTTPX][3])

---

# 3. 第一个 GET 请求 🚀

先写一个最简单的请求：

```python
import requests

response = requests.get("https://api.github.com/events")

print(response.status_code)
print(response.text)
```

这里：

```python
requests.get(...)
```

表示发送一个 GET 请求。

```python
response
```

是服务器返回的响应对象。

Requests 官方文档里的入门示例也是先 `import requests`，然后用 `requests.get(...)` 发起请求，返回的 `r` 是一个 `Response` 对象。([Requests][4])

---

# 4. Response 响应对象里有什么？🧩

一次 HTTP 请求回来之后，你最常用这些东西：

```python
response.status_code   # 状态码
response.text          # 文本内容
response.json()        # JSON 转 Python 对象
response.headers       # 响应头
response.content       # 二进制内容
response.url           # 最终请求 URL
```

比如：

```python
import requests

response = requests.get("https://api.github.com/events")

print("状态码：", response.status_code)
print("响应头：", response.headers)
print("最终 URL：", response.url)
print("响应文本：", response.text[:200])
```

你可以把 `response` 理解成：

> **服务器回给你的完整包裹** 📦

里面有状态码、响应头、响应体。

---

# 5. 状态码是什么？📶

状态码表示这次请求的结果。

常见分类：

| 状态码范围     | 含义    | 常见例子                    |
| --------- | ----- | ----------------------- |
| `100-199` | 信息响应  | 较少手动处理                  |
| `200-299` | 成功    | `200 OK`、`201 Created`  |
| `300-399` | 重定向   | `301`、`302`             |
| `400-499` | 客户端错误 | `400`、`401`、`403`、`404` |
| `500-599` | 服务端错误 | `500`、`502`、`503`       |

MDN 对 HTTP 状态码的分类也是这 5 类：信息响应、成功响应、重定向、客户端错误、服务端错误。([MDN Web Docs][5])

---

# 6. 常见状态码要认识 👀

## `200 OK` ✅

请求成功。

```python
if response.status_code == 200:
    print("请求成功")
```

## `201 Created` 🆕

资源创建成功，常见于 POST 创建数据。

## `204 No Content` 📭

请求成功，但响应体没有内容。

## `400 Bad Request` ⚠️

请求参数不对。

## `401 Unauthorized` 🔐

没有登录或 token 无效。

## `403 Forbidden` 🚫

服务器知道你是谁，但你没权限。

## `404 Not Found` 🔍

资源不存在。

## `500 Internal Server Error` 💥

服务器内部错误。

---

# 7. GET 请求传参数：`params` 🔎

比如你要请求：

```text
https://example.com/search?keyword=python&page=1
```

不要手动拼字符串，推荐用 `params`：

```python
import requests

params = {
    "keyword": "python",
    "page": 1
}

response = requests.get(
    "https://httpbin.org/get",
    params=params,
    timeout=10
)

print(response.url)
print(response.text)
```

Requests 文档说明，查询字符串参数可以通过 `params` 字典传入，Requests 会把它们正确编码到 URL 里。([Requests][4])

你可以理解成：

```python
params = {
    "keyword": "python",
    "page": 1
}
```

会变成：

```text
?keyword=python&page=1
```

---

# 8. 读取 JSON 响应 🧾

很多接口返回的是 JSON。

比如：

```python
import requests

response = requests.get("https://api.github.com/events", timeout=10)

data = response.json()

print(type(data))
print(data[0])
```

这里：

```python
response.json()
```

会把 JSON 字符串转换成 Python 对象。

常见转换关系：

| JSON         | Python       |
| ------------ | ------------ |
| object `{}`  | dict         |
| array `[]`   | list         |
| string       | str          |
| number       | int / float  |
| true / false | True / False |
| null         | None         |

Requests 官方高级用法示例里也展示了检查状态码后，通过 `r.json()` 把 GitHub 返回的 JSON 解析成 Python 对象。([Requests][6])

---

# 9. GET 请求完整模板 ✅

你以后调普通查询接口，可以先套这个：

```python
import requests


def get_users(page: int, size: int) -> dict:
    url = "https://example.com/api/users"

    params = {
        "page": page,
        "size": size
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(f"请求失败，状态码：{response.status_code}")

    return response.json()
```

重点是：

```python
params=params
timeout=10
response.json()
status_code
```

---

# 10. POST 请求是什么？📮

`GET` 通常是获取数据。

`POST` 通常是提交数据，比如：

* 登录
* 注册
* 新增用户
* 提交表单
* 创建订单
* 上传数据

Requests 官方文档展示了 `requests.post(...)` 的用法，也说明 `PUT`、`DELETE`、`HEAD`、`OPTIONS` 等方法也可以用类似方式发起。([Requests][4])

---

# 11. POST 提交 JSON：`json=` ⭐

这是现在调接口最常见的方式。

```python
import requests

url = "https://httpbin.org/post"

body = {
    "username": "admin",
    "password": "123456"
}

response = requests.post(url, json=body, timeout=10)

print(response.status_code)
print(response.json())
```

这里：

```python
json=body
```

表示把 Python 字典作为 JSON 请求体发出去。

这个非常常见，尤其你调用后端接口时。

---

# 12. POST 提交表单：`data=` 🧾

有些接口不是 JSON，而是表单格式。

```python
import requests

url = "https://httpbin.org/post"

form_data = {
    "username": "admin",
    "password": "123456"
}

response = requests.post(url, data=form_data, timeout=10)

print(response.status_code)
print(response.text)
```

区别：

```python
json=body
```

发送 JSON。

```python
data=form_data
```

发送表单。

HTTPX 文档里也说明，`POST` 和 `PUT` 这类请求可以携带请求体，常见方式之一就是 form-encoded data。([HTTPX][7])

---

# 13. `json=` 和 `data=` 怎么选？🧠

你可以这样记：

| 场景                                       | 写法          |
| ---------------------------------------- | ----------- |
| 后端接口要求 `application/json`                | `json=字典`   |
| 表单提交 `application/x-www-form-urlencoded` | `data=字典`   |
| 文件上传 `multipart/form-data`               | `files=...` |

实际项目里，大部分现代接口更常见：

```python
json=body
```

比如 Java Spring Boot 后端如果接口参数是：

```java
@RequestBody UserDTO userDTO
```

Python 这边通常就用：

```python
requests.post(url, json=body)
```

如果后端是：

```java
@RequestParam String username
```

那可能更接近：

```python
params=...
```

或者：

```python
data=...
```

具体看接口设计。

---

# 14. 请求头 headers 🧢

请求头常用来放：

* token
* User-Agent
* Content-Type
* Accept
* trace id
* 业务标识

例子：

```python
import requests

url = "https://example.com/api/user"

headers = {
    "Authorization": "Bearer your_token_here",
    "Accept": "application/json",
    "User-Agent": "python-demo/1.0"
}

response = requests.get(url, headers=headers, timeout=10)

print(response.status_code)
print(response.text)
```

HTTPX 文档也展示了可以通过 `headers` 参数给请求添加自定义请求头。([HTTPX][7])

---

# 15. Bearer Token 怎么写？🔐

很多接口要求 token。

```python
import requests

token = "abc123"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(
    "https://example.com/api/profile",
    headers=headers,
    timeout=10
)
```

注意：

> token、密码、密钥不要写死在代码里，更不要提交到 Git。🔒

可以放到环境变量或者配置文件中。

---

# 16. 超时 timeout 很重要 ⏰

HTTP 请求一定要设置超时。

不要这样：

```python
requests.get(url)
```

更推荐：

```python
requests.get(url, timeout=10)
```

或者更细：

```python
requests.get(url, timeout=(3, 10))
```

通常可以理解成：

```python
timeout=(连接超时, 读取超时)
```

为什么要设置超时？

因为网络请求可能卡住。如果不设超时，程序可能一直等，非常影响稳定性。

---

# 17. 异常处理：请求失败怎么办？🧯

网络请求可能出很多问题：

* 网络断开
* 域名解析失败
* 连接超时
* 读取超时
* SSL 失败
* 返回状态码 500
* JSON 解析失败

所以正式一点要用异常处理：

```python
import requests


def fetch_json(url: str) -> dict:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.Timeout:
        print("请求超时")
        raise

    except requests.HTTPError as e:
        print("HTTP 状态码异常：", e)
        raise

    except requests.RequestException as e:
        print("请求发生异常：", e)
        raise

    except ValueError as e:
        print("响应不是合法 JSON：", e)
        raise
```

这里最重要的是：

```python
response.raise_for_status()
```

如果状态码是 4xx 或 5xx，它会抛出异常，避免你误以为请求成功。

---

# 18. 更像项目里的写法：加日志 📝

你刚学了日志，这里正好结合起来。

```python
import logging
import requests

logger = logging.getLogger(__name__)


def fetch_user(user_id: int) -> dict:
    url = f"https://example.com/api/users/{user_id}"

    try:
        logger.info("开始请求用户信息 user_id=%s", user_id)

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        logger.info("请求用户信息成功 user_id=%s", user_id)
        return data

    except requests.Timeout:
        logger.exception("请求用户信息超时 user_id=%s", user_id)
        raise

    except requests.RequestException:
        logger.exception("请求用户信息失败 user_id=%s", user_id)
        raise

    except ValueError:
        logger.exception("用户信息响应不是合法 JSON user_id=%s", user_id)
        raise
```

真实项目里，HTTP 请求失败时一定要记日志，不然排查很难 😵‍💫

---

# 19. PUT、PATCH、DELETE 怎么写？🛠️

## PUT：整体更新

```python
import requests

url = "https://example.com/api/users/1"

body = {
    "username": "admin",
    "age": 22
}

response = requests.put(url, json=body, timeout=10)
print(response.status_code)
```

## PATCH：部分更新

```python
import requests

url = "https://example.com/api/users/1"

body = {
    "age": 23
}

response = requests.patch(url, json=body, timeout=10)
print(response.status_code)
```

## DELETE：删除资源

```python
import requests

url = "https://example.com/api/users/1"

response = requests.delete(url, timeout=10)
print(response.status_code)
```

MDN 对方法语义的说明是：`PUT` 替换目标资源的当前表示，`PATCH` 对资源做部分修改，`DELETE` 删除指定资源。([MDN Web Docs][1])

---

# 20. Session：复用连接和 Cookie 🍪

如果你要连续请求同一个网站或接口，可以用 `Session`。

```python
import requests

session = requests.Session()

session.headers.update({
    "User-Agent": "python-demo/1.0"
})

response1 = session.get("https://httpbin.org/cookies", timeout=10)
response2 = session.get("https://httpbin.org/headers", timeout=10)

print(response1.status_code)
print(response2.status_code)
```

`Session` 常用于：

* 自动保持 Cookie
* 复用连接
* 给一组请求统一设置 headers
* 登录后继续访问其他接口

Requests 文档也说明，Requests 支持连接池和 keep-alive 机制，并且这些能力基于 urllib3 自动提供。([Requests][8])

---

# 21. 下载文件 📥

下载图片、Excel、PDF 这类文件，要用二进制写入。

```python
import requests

url = "https://example.com/file.pdf"

response = requests.get(url, timeout=30)
response.raise_for_status()

with open("file.pdf", "wb") as file:
    file.write(response.content)
```

这里：

```python
"wb"
```

表示二进制写入。

```python
response.content
```

表示二进制内容。

---

# 22. 大文件下载：stream=True 🌊

大文件不要一次性读入内存。

```python
import requests

url = "https://example.com/big-file.zip"

with requests.get(url, stream=True, timeout=30) as response:
    response.raise_for_status()

    with open("big-file.zip", "wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file.write(chunk)
```

这样每次写 1MB，比较稳。

---

# 23. 上传文件 📤

```python
import requests

url = "https://httpbin.org/post"

with open("report.xlsx", "rb") as file:
    files = {
        "file": file
    }

    response = requests.post(url, files=files, timeout=30)

print(response.status_code)
print(response.text)
```

HTTPX 官方文档也展示了 multipart 文件上传写法：打开文件后把文件对象放到 `files` 参数里，再发起 POST 请求。([HTTPX][7])

---

# 24. 代理 proxies 🌉

有些时候需要代理：

```python
import requests

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

response = requests.get(
    "https://httpbin.org/ip",
    proxies=proxies,
    timeout=10
)

print(response.text)
```

注意，公司环境、内网环境不要乱配代理，容易导致接口访问异常。

---

# 25. SSL 验证不要随便关 ⚠️

你可能会看到这种写法：

```python
requests.get(url, verify=False)
```

它表示不验证 HTTPS 证书。

不推荐随便用 🚫

因为这会降低安全性。除非你非常明确是在本地测试、自签证书测试，否则不要这样写。真实项目里应该正确配置证书。

---

# 26. requests、urllib、httpx 怎么选？🧭

| 工具               | 特点             | 适合场景               |
| ---------------- | -------------- | ------------------ |
| `urllib.request` | 标准库自带，不用安装     | 简单请求、不能装第三方库的环境    |
| `requests`       | 简单好用，学习成本低     | 大多数同步 HTTP 请求      |
| `httpx`          | 支持同步和异步，现代 API | 需要异步请求、并发请求、HTTP/2 |

Python 标准库文档在 `urllib.request` 页面中也提到，Requests 是更高层的 HTTP 客户端接口；HTTPX 官方文档则说明它支持同步和异步 API。([Python documentation][2])

---

# 27. requests 和 Java 后端调用类比 ☕🐍

你可以这样类比：

| Java                              | Python                          |
| --------------------------------- | ------------------------------- |
| RestTemplate / WebClient / OkHttp | requests / httpx                |
| GET 查询                            | requests.get                    |
| POST JSON                         | requests.post(json=body)        |
| Header                            | headers={...}                   |
| Query 参数                          | params={...}                    |
| RequestBody                       | json={...}                      |
| HTTP Status                       | response.status_code            |
| Response Body                     | response.text / response.json() |
| 超时配置                              | timeout=10                      |
| 异常处理                              | try...except                    |

比如 Java 里调接口：

```java
restTemplate.getForObject(url, User.class);
```

Python 里大概就是：

```python
response = requests.get(url, timeout=10)
user = response.json()
```

---

# 28. 一个完整实战：封装一个 API Client 🧱

这种写法更像真实项目。

```python
import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, base_url: str, token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "python-api-client/1.0"
        })

        if token:
            self.session.headers.update({
                "Authorization": f"Bearer {token}"
            })

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"

        try:
            logger.info("发送 GET 请求 url=%s params=%s", url, params)

            response = self.session.get(
                url,
                params=params,
                timeout=10
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException:
            logger.exception("GET 请求失败 url=%s", url)
            raise

        except ValueError:
            logger.exception("响应 JSON 解析失败 url=%s", url)
            raise

    def post(self, path: str, body: dict[str, Any] | None = None) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"

        try:
            logger.info("发送 POST 请求 url=%s", url)

            response = self.session.post(
                url,
                json=body,
                timeout=10
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException:
            logger.exception("POST 请求失败 url=%s", url)
            raise

        except ValueError:
            logger.exception("响应 JSON 解析失败 url=%s", url)
            raise
```

使用：

```python
client = ApiClient(
    base_url="https://example.com/api",
    token="your_token"
)

users = client.get("/users", params={"page": 1, "size": 10})

new_user = client.post("/users", body={
    "username": "admin",
    "age": 22
})
```

这个例子把你前面学过的东西串起来了：

* 类
* `__init__`
* typing
* logging
* 异常
* HTTP 请求
* Session

---

# 29. 一个更贴近你项目的例子：调用天气 API 🌦️

```python
import requests


def get_weather(city: str) -> dict:
    url = "https://example.com/api/weather"

    params = {
        "city": city
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


weather = get_weather("上海")
print(weather)
```

如果接口返回：

```json
{
  "city": "上海",
  "temperature": 25,
  "humidity": 70
}
```

那么：

```python
print(weather["city"])
print(weather["temperature"])
```

---

# 30. 最常见错误和原因 🚨

## 30.1 `ModuleNotFoundError: No module named 'requests'`

原因：没安装 requests，或者 PyCharm 解释器选错。

解决：

```bash
python -m pip install requests
```

并检查 PyCharm 当前项目解释器是不是 `.venv`。

---

## 30.2 `ConnectionError`

可能原因：

* 网络不通
* 域名不对
* 代理有问题
* 服务器挂了

---

## 30.3 `Timeout`

可能原因：

* 网络慢
* 服务器响应慢
* 接口卡住

解决：设置合理超时，并捕获异常。

---

## 30.4 `JSONDecodeError`

可能原因：

* 服务器返回的不是 JSON
* 返回了 HTML 错误页
* 空响应
* Content-Type 和实际内容不一致

解决：

```python
print(response.status_code)
print(response.text)
```

先看服务器到底返回了什么。

---

## 30.5 401 / 403

可能原因：

* token 没传
* token 过期
* 权限不足
* headers 写错

---

# 31. 学 HTTP 请求最重要的习惯 ✅

## 习惯 1：永远设置 timeout

```python
requests.get(url, timeout=10)
```

## 习惯 2：检查状态码

```python
response.raise_for_status()
```

## 习惯 3：JSON 接口用 `json=`

```python
requests.post(url, json=body)
```

## 习惯 4：查询参数用 `params=`

```python
requests.get(url, params=params)
```

## 习惯 5：异常要记录日志

```python
logger.exception("请求失败")
```

## 习惯 6：token 不要写死

```python
headers = {
    "Authorization": f"Bearer {token}"
}
```

---

# 32. 给你一组练习题 ✍️🔥

## 练习 1：发送 GET 请求

请求一个公开接口，打印：

```text
状态码
响应前 200 个字符
```

---

## 练习 2：GET 携带 params

请求：

```python
params = {
    "keyword": "python",
    "page": 1
}
```

打印最终 URL。

---

## 练习 3：POST JSON

发送：

```python
{
    "username": "admin",
    "password": "123456"
}
```

打印响应 JSON。

---

## 练习 4：封装函数

写一个函数：

```python
def fetch_json(url: str) -> dict:
    ...
```

要求：

* 设置 timeout
* 调用 `raise_for_status()`
* 返回 `response.json()`
* 捕获 `requests.RequestException`

---

## 练习 5：封装类

写一个 `ApiClient`，支持：

```python
client.get(path, params=None)
client.post(path, body=None)
```

---

# 33. 练习参考答案 ✅

## 练习 1

```python
import requests

response = requests.get("https://api.github.com/events", timeout=10)

print("状态码：", response.status_code)
print("响应内容：", response.text[:200])
```

---

## 练习 2

```python
import requests

params = {
    "keyword": "python",
    "page": 1
}

response = requests.get(
    "https://httpbin.org/get",
    params=params,
    timeout=10
)

print(response.url)
```

---

## 练习 3

```python
import requests

body = {
    "username": "admin",
    "password": "123456"
}

response = requests.post(
    "https://httpbin.org/post",
    json=body,
    timeout=10
)

print(response.json())
```

---

## 练习 4

```python
import requests


def fetch_json(url: str) -> dict:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("请求失败：", e)
        raise
    except ValueError as e:
        print("JSON 解析失败：", e)
        raise
```

---

# 34. 最后总结 🎯

Python HTTP 请求你现在先掌握这几个核心：

```python
requests.get(url, params=params, headers=headers, timeout=10)
```

```python
requests.post(url, json=body, headers=headers, timeout=10)
```

```python
response.status_code
response.text
response.json()
response.headers
response.raise_for_status()
```

最推荐的基础模板：

```python
import requests

response = requests.get("https://example.com/api", timeout=10)
response.raise_for_status()
data = response.json()
```

一句话记住：

> **GET 用来拿数据，POST 常用来提交数据；params 放查询参数，json 放请求体，headers 放 token，timeout 一定要写。** 🐍🌐

[1]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods "HTTP request methods - HTTP | MDN"
[2]: https://docs.python.org/3/library/urllib.request.html "urllib.request — Extensible library for opening URLs — Python 3.14.5rc1 documentation"
[3]: https://www.python-httpx.org/?utm_source=chatgpt.com "HTTPX"
[4]: https://requests.readthedocs.io/en/latest/user/quickstart/ "Quickstart — Requests 2.34.0.dev1 documentation"
[5]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status "HTTP response status codes - HTTP | MDN"
[6]: https://requests.readthedocs.io/en/master/user/advanced/ "Advanced Usage — Requests 2.34.0.dev1 documentation"
[7]: https://www.python-httpx.org/quickstart/ "QuickStart - HTTPX"
[8]: https://requests.readthedocs.io/?utm_source=chatgpt.com "Requests: HTTP for Humans - Read the Docs"
