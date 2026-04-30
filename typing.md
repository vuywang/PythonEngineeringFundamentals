`typing` 你可以理解成：**Python 里的“类型提示工具包”** 🐍🧩

它不是让 Python 变成 Java 那种强制静态类型语言，而是用来告诉编辑器、PyCharm、mypy、pyright 这些工具：

> 这个变量应该是什么类型
> 这个函数参数应该传什么类型
> 这个函数最后会返回什么类型

Python 官方文档把 `typing` 模块描述为“支持类型提示”的模块；而 Python 的静态类型体系也有专门文档和工具生态，比如 mypy、pyright、PyCharm、VS Code/Pylance 等。([Python documentation][1])

---

# 1. 先看一个最简单的例子 🌟

普通 Python 写法：

```python
def add(a, b):
    return a + b
```

加上类型提示之后：

```python
def add(a: int, b: int) -> int:
    return a + b
```

这句话的意思是：

```python
a: int
```

表示 `a` 建议是 `int` 类型。

```python
b: int
```

表示 `b` 建议是 `int` 类型。

```python
-> int
```

表示这个函数返回值建议是 `int` 类型。

所以这段代码可以翻译成中文：

> add 函数接收两个整数，返回一个整数。

---

# 2. 这是不是 Java 那种强制类型？🤔

不是。

Python 里即使你写了：

```python
def add(a: int, b: int) -> int:
    return a + b

print(add("你好", "Python"))
```

它依然可以运行，输出：

```python
你好Python
```

因为 Python 的类型提示默认主要给**工具检查**，不是运行时强制拦截。比如 mypy 是一个可选的 Python 静态类型检查器，可以在代码运行前检查类型问题；它也强调 Python 代码可以从动态类型逐步迁移到静态类型，二者可以混用。([mypy-lang.org][2])

所以你可以这样记：

> **Java 的类型是程序运行规则的一部分。**
> **Python 的 typing 更多是给人和工具看的说明书。** 📘

---

# 3. 为什么要用 typing？有什么用？🚀

它主要有 4 个作用。

## 3.1 让代码更清楚 👀

不加类型：

```python
def get_user(id):
    ...
```

你不知道：

* `id` 是整数？
* 字符串？
* 返回用户字典？
* 返回用户对象？
* 可能返回 `None`？

加上类型：

```python
def get_user(user_id: int) -> dict:
    ...
```

一下就清楚很多。

---

## 3.2 PyCharm 能更好地提示你 🛠️

比如：

```python
def greet(name: str) -> str:
    return name.upper()
```

PyCharm 看到 `name: str`，就知道 `name` 是字符串，于是会提示：

```python
name.upper()
name.lower()
name.strip()
```

这对写代码非常舒服 😄

Python typing 文档里也列出了开发环境支持，比如 PyCharm 支持类型桩用于类型检查和代码补全，VS Code 也可以通过 mypy、pyright 或 Pylance 做类型检查。([typing.python.org][3])

---

## 3.3 提前发现错误 🧯

比如你写：

```python
def add(a: int, b: int) -> int:
    return a + b

add("10", 20)
```

Python 运行时可能会报错：

```text
TypeError
```

但如果你用了类型检查工具，它可以提前提醒你：

> 这里第一个参数应该是 int，你传了 str。

这就像 Java 编译器能提前发现很多类型错误一样，只不过 Python 这边通常是靠 mypy、pyright、PyCharm 这些工具检查。mypy 官方也说静态类型能更容易发现 bug，类型声明也像“可被机器检查的文档”。([mypy-lang.org][2])

---

## 3.4 函数和类更适合维护 📦

项目一大，函数越来越多。

没有类型：

```python
def save_user(user):
    ...
```

你以后回来看，可能忘了 `user` 到底是什么。

加上类型：

```python
def save_user(user: dict) -> None:
    ...
```

就更明确。

---

# 4. 基础类型怎么写？🧱

常见写法：

```python
name: str = "张三"
age: int = 18
height: float = 1.75
is_student: bool = True
```

对应关系：

| Python 类型 | 类型提示写法  | 含义           |
| --------- | ------- | ------------ |
| 字符串       | `str`   | 文本           |
| 整数        | `int`   | 整数           |
| 小数        | `float` | 浮点数          |
| 布尔值       | `bool`  | True / False |
| 空值        | `None`  | 没有值          |

函数里这样写：

```python
def introduce(name: str, age: int) -> str:
    return f"我叫{name}，今年{age}岁"
```

---

# 5. 返回值没有内容，写 `None` 🚪

如果函数只是打印，不返回值：

```python
def say_hello(name: str) -> None:
    print(f"你好，{name}")
```

这里：

```python
-> None
```

表示这个函数没有正常返回值。

类似 Java 里的：

```java
void sayHello(String name) {
    ...
}
```

所以你可以粗略类比：

```python
-> None
```

≈ Java 的 `void`。

---

# 6. list、dict、tuple 怎么写？📚

现代 Python 里通常可以直接这样写：

```python
names: list[str] = ["张三", "李四", "王五"]
scores: dict[str, int] = {"张三": 95, "李四": 88}
point: tuple[int, int] = (10, 20)
```

含义：

```python
list[str]
```

表示列表里都是字符串。

```python
dict[str, int]
```

表示字典的 key 是字符串，value 是整数。

```python
tuple[int, int]
```

表示元组里第一个是整数，第二个也是整数。

---

# 7. 函数里使用 list 类型 🧮

```python
def average(scores: list[int]) -> float:
    return sum(scores) / len(scores)
```

意思是：

* 参数 `scores` 是一个整数列表
* 返回值是一个浮点数

调用：

```python
result = average([90, 80, 100])
print(result)
```

---

# 8. 函数里使用 dict 类型 🧾

```python
def get_score(student: dict[str, int], name: str) -> int:
    return student[name]
```

调用：

```python
scores = {
    "张三": 95,
    "李四": 88
}

print(get_score(scores, "张三"))
```

---

# 9. 多种类型：`|` 写法 🌈

如果一个参数可能是 `int`，也可能是 `float`：

```python
def double(num: int | float) -> int | float:
    return num * 2
```

这里：

```python
int | float
```

表示：

> 可以是 int，也可以是 float。

这个有点像 Java 里说“这个值可能有几种类型”，但 Python 写起来更直接。

---

# 10. 可能返回 None 怎么写？⚠️

很多函数可能查不到数据。

比如：

```python
def find_user(user_id: int) -> str | None:
    if user_id == 1:
        return "张三"
    return None
```

这里：

```python
str | None
```

表示返回值可能是：

* `str`
* `None`

这非常常用。

比如数据库查询：

```python
def get_user_by_id(user_id: int) -> User | None:
    ...
```

意思就是：

> 查到了返回 User，查不到返回 None。

---

# 11. 和旧写法 `Optional` 的关系 🧩

你可能还会看到这种：

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    ...
```

它和下面这种意思差不多：

```python
def find_user(user_id: int) -> str | None:
    ...
```

现在更推荐你先学 `str | None` 这种写法，简单直观。

---

# 12. 类型别名：给复杂类型起名字 🏷️

如果类型太长，可以起别名。

比如：

```python
User = dict[str, str | int]

def print_user(user: User) -> None:
    print(user)
```

这里：

```python
User = dict[str, str | int]
```

表示 `User` 是一个类型别名。

以后看到：

```python
user: User
```

就知道它大概是用户数据。

---

# 13. 自定义类也能当类型使用 🧑‍🎓

你刚学了类，这里正好接上。

```python
class Student:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


def print_student(student: Student) -> None:
    print(student.name, student.age)
```

这里：

```python
student: Student
```

表示参数应该是一个 `Student` 对象。

这点和 Java 特别像。

Java：

```java
void printStudent(Student student) {
    ...
}
```

Python：

```python
def print_student(student: Student) -> None:
    ...
```

---

# 14. dataclass + typing 很常见 ✨

你刚问过 `@dataclass`，它和 typing 经常一起用：

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    score: float
```

这里：

```python
name: str
age: int
score: float
```

既是字段说明，也能让 `@dataclass` 自动生成 `__init__`。

使用：

```python
s = Student("张三", 18, 95.5)
print(s)
```

---

# 15. `Any`：任何类型都行 🌀

```python
from typing import Any

def print_value(value: Any) -> None:
    print(value)
```

`Any` 的意思是：

> 什么类型都可以。

但不要滥用。

因为你写了太多 `Any`，类型检查就失去意义了 😵

比如：

```python
def handle_data(data: Any) -> Any:
    ...
```

这就和没写类型差不多。

---

# 16. `Literal`：只能是固定几个值 🎯

```python
from typing import Literal

def set_status(status: Literal["todo", "doing", "done"]) -> None:
    print(status)
```

意思是 `status` 只能建议传这三个字符串之一：

```python
"todo"
"doing"
"done"
```

如果你写：

```python
set_status("cancel")
```

类型检查工具就可能提醒你。

这在状态值、枚举值里很好用。

---

# 17. `TypedDict`：给字典规定结构 🧾

普通字典写法：

```python
user: dict[str, str | int] = {
    "name": "张三",
    "age": 18
}
```

这个不够精确。

因为它只说：

* key 是 str
* value 是 str 或 int

但没说必须有哪些 key。

这时候可以用 `TypedDict`：

```python
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int


def print_user(user: User) -> None:
    print(user["name"], user["age"])
```

这样就能告诉工具：

> User 这个字典应该有 name 和 age 这两个字段。

Python typing 文档里也把 `TypedDict`、`Required`、`NotRequired`、`ReadOnly` 等列为用于描述字典结构的类型构造，其中 `Required`/`NotRequired` 用来标记 TypedDict 字段是否必须存在。([Python documentation][4])

---

# 18. `Callable`：函数也能当类型 📦

你之前学过，函数可以当参数传。

比如：

```python
from collections.abc import Callable

def run_task(task: Callable[[], None]) -> None:
    task()
```

这里：

```python
Callable[[], None]
```

表示：

> task 是一个函数，不接收参数，返回 None。

再比如：

```python
from collections.abc import Callable

def calculate(a: int, b: int, op: Callable[[int, int], int]) -> int:
    return op(a, b)
```

使用：

```python
def add(x: int, y: int) -> int:
    return x + y

print(calculate(3, 5, add))
```

这里：

```python
Callable[[int, int], int]
```

表示：

> 这是一个函数，接收两个 int，返回一个 int。

---

# 19. `Final`：不希望被改的变量 🔒

```python
from typing import Final

MAX_SIZE: Final[int] = 100
```

意思是：

> MAX_SIZE 不应该再被重新赋值。

如果你写：

```python
MAX_SIZE = 200
```

类型检查工具会提醒。Python 官方文档也说明，`Final` 是告诉类型检查器某个名字不能重新赋值；但它没有运行时检查，也就是说 Python 运行时不会强制拦住。([Python documentation][4])

---

# 20. 真实开发里怎么用 typing？🧠

你现在不用一上来学所有高级写法。
先掌握这几个就够了：

```python
str
int
float
bool
None
list[str]
dict[str, int]
tuple[int, int]
str | None
int | float
自定义类
```

比如：

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    age: int | None


def get_username(user: User) -> str:
    return user.username


def find_user(user_id: int) -> User | None:
    if user_id == 1:
        return User(1, "admin", 22)
    return None
```

这已经很实用了。

---

# 21. typing 和 Java 类型最大的区别 ☕🐍

Java：

```java
public int add(int a, int b) {
    return a + b;
}
```

类型是语言强制的。

Python：

```python
def add(a: int, b: int) -> int:
    return a + b
```

类型是提示，主要给工具检查。

所以你不能完全用 Java 的思维看 Python typing。

更准确的理解是：

> **Python typing = 类型说明 + 工具检查 + 代码补全增强。**

---

# 22. 你现在该不该用 typing？✅

应该用，而且建议从函数开始。

尤其你有 Java 背景，写 Python 时加类型会更舒服。

推荐你这样写：

```python
def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
```

比这样更清楚：

```python
def read_file(path):
    ...
```

---

# 23. 新手最推荐的写法模板 📌

## 普通函数

```python
def 函数名(参数名: 参数类型) -> 返回类型:
    ...
```

例如：

```python
def add(a: int, b: int) -> int:
    return a + b
```

---

## 没有返回值

```python
def log(message: str) -> None:
    print(message)
```

---

## 列表参数

```python
def total(nums: list[int]) -> int:
    return sum(nums)
```

---

## 可能返回 None

```python
def find_name(user_id: int) -> str | None:
    if user_id == 1:
        return "张三"
    return None
```

---

## 类对象

```python
class User:
    def __init__(self, username: str):
        self.username = username


def print_user(user: User) -> None:
    print(user.username)
```

---

# 24. 一句话总结 🎯

`typing` 就是 Python 的**类型提示系统**：

> 它不会默认像 Java 那样强制限制运行，但能让代码更清楚、让 PyCharm 更懂你、让类型检查工具提前发现问题。✨

你现在先重点掌握：

```python
name: str
age: int
def add(a: int, b: int) -> int:
list[str]
dict[str, int]
str | None
-> None
```

这些就够你写大部分入门到中级代码了 🐍💪

[1]: https://docs.python.org/3/library/typing.html?utm_source=chatgpt.com "typing — Support for type hints"
[2]: https://mypy-lang.org/ "mypy - Optional Static Typing for Python"
[3]: https://typing.python.org/ "Static Typing with Python — typing  documentation"
[4]: https://docs.python.org/3/library/typing.html "typing — Support for type hints — Python 3.14.4 documentation"
