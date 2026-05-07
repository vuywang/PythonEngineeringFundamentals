# 1. 先用 Java 思维理解 SQLAlchemy ☕🐍

你之前问过它和 JDBC、MyBatis 的关系。可以这样类比：

| Java 体系             | Python / SQLAlchemy                       |
| ------------------- | ----------------------------------------- |
| JDBC                | DBAPI 驱动，比如 `pymysql`、`sqlite3`、`psycopg` |
| MyBatis             | SQLAlchemy Core 更接近一些                     |
| JPA / Hibernate     | SQLAlchemy ORM 更接近一些                      |
| DataSource / 连接池    | SQLAlchemy Engine                         |
| SqlSession          | SQLAlchemy Session                        |
| Entity              | SQLAlchemy ORM Model                      |
| Mapper XML / 注解 SQL | SQLAlchemy Core 的 SQL 表达式，或者 ORM 查询       |

但是注意：SQLAlchemy 不是简单的“Python 版 MyBatis”。它底层可以写 SQL 表达式，也可以做 ORM。官方文档里也明确说 SQLAlchemy 的 **dialect** 负责和不同数据库、不同 DBAPI 驱动通信，而且所有 dialect 都需要对应的 DBAPI driver。([docs.sqlalchemy.org][2])

---

# 2. SQLAlchemy 有两种主要用法 🧩

SQLAlchemy 主要有两层：

## 2.1 Core：更接近 SQL

Core 更像是：

> 用 Python 代码拼出 SQL，然后执行。

比如：

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///demo.db", echo=True)

with engine.connect() as conn:
    result = conn.execute(text("select 1"))
    print(result.scalar())
```

这种写法更接近 JDBC / MyBatis 的感觉。

---

## 2.2 ORM：更接近对象

ORM 更像是：

> 把数据库表映射成 Python 类，把表里的行映射成 Python 对象。

比如：

```python
user = User(username="admin", age=22)
session.add(user)
session.commit()
```

这就像 Java 里的：

```java
User user = new User();
user.setUsername("admin");
user.setAge(22);
userMapper.insert(user);
```

SQLAlchemy ORM 官方文档说明，如果你想让 SQL 自动构造，并且把 Python 对象持久化到数据库，就应该看 ORM。([docs.sqlalchemy.org][3])

---

# 3. 安装 SQLAlchemy 📦

先在你的虚拟环境里安装：

```bash
python -m pip install sqlalchemy
```

如果你用 SQLite 学习，Python 自带 `sqlite3`，一般不用额外装数据库驱动。

如果你连接 MySQL，通常还需要一个 MySQL 驱动，比如：

```bash
python -m pip install pymysql
```

然后连接地址可以写成：

```python
mysql+pymysql://用户名:密码@主机:端口/数据库名
```

SQLAlchemy 官方的 Engine 配置文档也展示了 MySQL 使用 PyMySQL 时的连接写法：`mysql+pymysql://scott:tiger@localhost/foo`。([docs.sqlalchemy.org][4])

---

# 4. 最小可运行示例：SQLite 版本 🌟

我们先用 SQLite，因为它最适合学习，不需要先装 MySQL。

创建 `main.py`：

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///demo.db", echo=True)

with engine.connect() as conn:
    result = conn.execute(text("select 'hello sqlalchemy'"))
    print(result.scalar())
```

运行：

```bash
python main.py
```

你会看到控制台输出 SQL。这里：

```python
echo=True
```

表示把 SQLAlchemy 实际执行的 SQL 打印出来，适合学习阶段观察。

---

# 5. Engine 是什么？🚗

你可以把 `Engine` 理解成：

> **数据库连接入口 + 连接池管理器。**

代码：

```python
engine = create_engine("sqlite:///demo.db", echo=True)
```

这句话并不是立刻查数据库，而是创建一个数据库访问入口。

Java 类比：

```text
SQLAlchemy Engine ≈ DataSource / 连接池入口
```

SQLAlchemy 官方资料里也把 Engine 描述为 SQLAlchemy 应用的起点，它负责数据库连接来源，并持有连接池。([DEV Community][5])

---

# 6. Session 是什么？🧠

如果用 ORM，`Session` 非常重要。

你可以把它理解成：

> **一次数据库操作上下文 / 工作单元。**

它负责：

* 管理对象状态
* 新增对象
* 查询对象
* 修改对象
* 删除对象
* 提交事务
* 回滚事务

Java 类比：

```text
SQLAlchemy Session ≈ MyBatis SqlSession + JPA EntityManager 的混合感觉
```

SQLAlchemy 文档也说，使用 Session 时，可以把 ORM 映射对象看成数据库行的代理对象，这些对象存在于 Session 当前事务之中。([docs.sqlalchemy.org][6])

---

# 7. ORM 模型：把表写成类 🧱

现在我们正式写 ORM。

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "sys_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    age: Mapped[int | None] = mapped_column(nullable=True)


engine = create_engine("sqlite:///demo.db", echo=True)

Base.metadata.create_all(engine)
```

这段代码会创建一张表：

```sql
CREATE TABLE sys_user (
    id INTEGER NOT NULL,
    username VARCHAR NOT NULL,
    age INTEGER,
    PRIMARY KEY (id),
    UNIQUE (username)
)
```

SQLAlchemy 2.x 风格里，Declarative 映射经常使用 `DeclarativeBase`、`Mapped[]`、`mapped_column()` 这些写法；官方表配置文档也说明，`mapped_column()` 可以接收 `Column` 的参数，并且通常会用类属性名作为数据库列名。([docs.sqlalchemy.org][7])

---

# 8. 这段模型代码怎么理解？🔍

## 8.1 Base

```python
class Base(DeclarativeBase):
    pass
```

这个 `Base` 是所有 ORM 模型类的父类。

你可以理解成：

> 所有数据库实体类都继承它。

---

## 8.2 表名

```python
__tablename__ = "sys_user"
```

表示这个类对应数据库中的：

```text
sys_user
```

表。

---

## 8.3 主键

```python
id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
```

表示：

* 字段名：`id`
* 类型：整数
* 主键
* 自增

---

## 8.4 非空 + 唯一

```python
username: Mapped[str] = mapped_column(nullable=False, unique=True)
```

表示：

* 字段名：`username`
* 字符串
* 不能为空
* 不能重复

---

## 8.5 可为空字段

```python
age: Mapped[int | None] = mapped_column(nullable=True)
```

表示：

* `age` 是整数
* 也可以是 `None`
* 数据库里允许为空

---

# 9. 新增数据：insert 🆕

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "sys_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    age: Mapped[int | None] = mapped_column(nullable=True)


engine = create_engine("sqlite:///demo.db", echo=True)

Base.metadata.create_all(engine)

with Session(engine) as session:
    user = User(username="admin", age=22)

    session.add(user)
    session.commit()

    print("新增后的用户 id：", user.id)
```

这里重点是：

```python
session.add(user)
```

表示把对象加入 Session。

```python
session.commit()
```

表示提交事务，真正写入数据库。

SQLAlchemy 的事务文档说明，`Session` 和 `Connection` 都有 `commit()`、`rollback()` 方法；Session 默认会自动开始事务，提交时影响当前最外层事务。([docs.sqlalchemy.org][8])

---

# 10. 查询数据：select 🔎

SQLAlchemy 2.x 推荐使用 `select()` 风格：

```python
from sqlalchemy import select

with Session(engine) as session:
    stmt = select(User).where(User.username == "admin")

    user = session.scalar(stmt)

    if user:
        print(user.id, user.username, user.age)
```

这里：

```python
select(User)
```

表示查询 `User` 对应的表。

```python
.where(User.username == "admin")
```

表示查询条件。

```python
session.scalar(stmt)
```

表示取一条结果中的第一个 ORM 对象。

SQLAlchemy Unified Tutorial 也说明，SQLAlchemy 2.0 风格下，ORM 查询使用 Core 风格的 `select()` 构造。([docs.sqlalchemy.org][9])

---

# 11. 查询多条数据 📋

```python
from sqlalchemy import select

with Session(engine) as session:
    stmt = select(User).order_by(User.id.desc())

    users = session.scalars(stmt).all()

    for user in users:
        print(user.id, user.username, user.age)
```

这里：

```python
session.scalars(stmt).all()
```

表示拿到多个 `User` 对象。

你可以把它理解成：

```sql
select * from sys_user order by id desc;
```

---

# 12. 修改数据：update ✏️

ORM 最自然的修改方式是：

```python
from sqlalchemy import select

with Session(engine) as session:
    user = session.scalar(
        select(User).where(User.username == "admin")
    )

    if user:
        user.age = 23
        session.commit()
```

注意：

你不需要手写：

```sql
update sys_user set age = 23 where username = 'admin';
```

你只要改对象属性：

```python
user.age = 23
```

然后：

```python
session.commit()
```

SQLAlchemy 会帮你生成对应的 update SQL。

---

# 13. 删除数据：delete 🗑️

```python
from sqlalchemy import select

with Session(engine) as session:
    user = session.scalar(
        select(User).where(User.username == "admin")
    )

    if user:
        session.delete(user)
        session.commit()
```

这里：

```python
session.delete(user)
```

表示删除这个 ORM 对象对应的数据库行。

---

# 14. 完整 CRUD 示例 ✅

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "sys_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    age: Mapped[int | None] = mapped_column(nullable=True)


engine = create_engine("sqlite:///demo.db", echo=True)
Base.metadata.create_all(engine)


def create_user(username: str, age: int | None) -> User:
    with Session(engine) as session:
        user = User(username=username, age=age)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user_by_username(username: str) -> User | None:
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        return session.scalar(stmt)


def list_users() -> list[User]:
    with Session(engine) as session:
        stmt = select(User).order_by(User.id.desc())
        return list(session.scalars(stmt).all())


def update_user_age(username: str, age: int) -> bool:
    with Session(engine) as session:
        user = session.scalar(select(User).where(User.username == username))

        if user is None:
            return False

        user.age = age
        session.commit()
        return True


def delete_user(username: str) -> bool:
    with Session(engine) as session:
        user = session.scalar(select(User).where(User.username == username))

        if user is None:
            return False

        session.delete(user)
        session.commit()
        return True


if __name__ == "__main__":
    create_user("admin", 22)

    user = get_user_by_username("admin")
    print(user.username if user else "没查到")

    update_user_age("admin", 23)

    for item in list_users():
        print(item.id, item.username, item.age)

    delete_user("admin")
```

这个例子已经够你入门 SQLAlchemy ORM 了。

---

# 15. `session.refresh(user)` 是什么？🔄

你新增后经常会看到：

```python
session.refresh(user)
```

它的作用是：

> 从数据库重新刷新这个对象的数据。

比如数据库自动生成了 `id`、默认时间、触发器字段等，`refresh()` 可以把数据库里的最新值刷回对象。

---

# 16. 事务怎么写更稳？🛡️

你可以手动：

```python
with Session(engine) as session:
    try:
        session.add(user)
        session.commit()
    except Exception:
        session.rollback()
        raise
```

也可以用更推荐的上下文管理方式：

```python
with Session(engine) as session:
    with session.begin():
        session.add(User(username="admin", age=22))
        session.add(User(username="test", age=20))
```

`Session.begin()` 可以作为上下文管理器使用，用来框出 begin / commit / rollback 代码块；如果没有异常则提交，有异常则回滚。([docs.sqlalchemy.org][6])

---

# 17. Session 要不要关闭？🚪

要。

所以推荐使用：

```python
with Session(engine) as session:
    ...
```

这样代码块结束后会自动关闭 Session。

SQLAlchemy Session API 文档也说明，Session 可以通过上下文管理器使用；如果不用上下文管理器，也应该显式调用 `Session.close()`，通常配合 `try/finally` 确保关闭。([docs.sqlalchemy.org][10])

---

# 18. 一对多关系：User 和 Article 👨‍👧

比如：

```text
一个用户可以有多篇文章
一篇文章属于一个用户
```

表关系：

```text
sys_user.id  ←  article.user_id
```

代码：

```python
from sqlalchemy import ForeignKey, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "sys_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)

    articles: Mapped[list["Article"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )


class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("sys_user.id"))

    author: Mapped[User] = relationship(back_populates="articles")


engine = create_engine("sqlite:///demo.db", echo=True)
Base.metadata.create_all(engine)


with Session(engine) as session:
    user = User(
        username="admin",
        articles=[
            Article(title="第一篇文章"),
            Article(title="第二篇文章"),
        ]
    )

    session.add(user)
    session.commit()
```

这里：

```python
relationship(...)
```

表示 ORM 层的对象关系。

```python
ForeignKey("sys_user.id")
```

表示数据库层的外键。

SQLAlchemy 官方关系文档说明，ORM 关系配置通常通过 declarative base 类上的 `relationship()` 完成；而一对多、多对一、一对一、多对多都有对应的基础关系模式。([docs.sqlalchemy.org][11])

---

# 19. 查询用户和文章 📖

```python
with Session(engine) as session:
    user = session.scalar(
        select(User).where(User.username == "admin")
    )

    if user:
        print(user.username)

        for article in user.articles:
            print(article.title)
```

这个写法很像：

```java
User user = userMapper.selectByUsername("admin");
List<Article> articles = user.getArticles();
```

不过要注意 ORM 查询里的懒加载、预加载问题，后面项目里要专门学。

---

# 20. Core 写法：直接执行 SQL 🧾

有时候 ORM 太绕，你也可以直接执行 SQL。

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///demo.db", echo=True)

with engine.connect() as conn:
    result = conn.execute(
        text("select id, username, age from sys_user where username = :username"),
        {"username": "admin"}
    )

    for row in result:
        print(row.id, row.username, row.age)
```

这里：

```python
:username
```

是绑定参数，不要直接拼接字符串。

不要这样：

```python
sql = f"select * from sys_user where username = '{username}'"
```

这容易 SQL 注入。

---

# 21. 和 MyBatis 最大的差别 🧠

MyBatis 常见思路是：

```text
你自己写 SQL
MyBatis 帮你执行、映射结果
```

SQLAlchemy ORM 常见思路是：

```text
你定义类和关系
SQLAlchemy 帮你生成 SQL
```

SQLAlchemy Core 则介于两者之间：

```text
你用 Python 表达式构造 SQL
SQLAlchemy 负责生成具体数据库 SQL
```

所以你学 SQLAlchemy 时不要只问“SQL 写在哪里”。SQLAlchemy 的核心是：

> **既能写 SQL，又能用对象模型表达数据库操作。**

---

# 22. 连接 MySQL 示例 🐬

安装：

```bash
python -m pip install sqlalchemy pymysql
```

连接：

```python
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:123456@127.0.0.1:3306/test_db?charset=utf8mb4",
    echo=True
)
```

如果你是本地 MySQL：

```text
用户名 root
密码 123456
地址 127.0.0.1
端口 3306
数据库 test_db
```

那连接串就是：

```text
mysql+pymysql://root:123456@127.0.0.1:3306/test_db?charset=utf8mb4
```

SQLAlchemy 官方 MySQL 文档说明 PyMySQL 是 SQLAlchemy 支持的 MySQL / MariaDB DBAPI 驱动之一。([docs.sqlalchemy.org][12])

---

# 23. 日志里看 SQL：echo=True 📝

学习时你可以：

```python
engine = create_engine("sqlite:///demo.db", echo=True)
```

这样能看到 SQLAlchemy 实际执行的 SQL。

但项目上线不一定建议一直开 `echo=True`，更常见的是用 logging 控制 SQL 日志级别。

---

# 24. 异步 SQLAlchemy 简单认识 ⚡

你刚学过异步，所以这里顺便认识一下。

同步版本：

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
```

异步版本大概是：

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
```

SQLAlchemy 官方异步文档说明，`create_async_engine()` 会创建 `AsyncEngine`，提供传统 Engine API 的异步版本；`AsyncEngine.connect()` 和 `AsyncEngine.begin()` 返回的是异步上下文管理器。([docs.sqlalchemy.org][13])

示例：

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    "sqlite+aiosqlite:///demo.db",
    echo=True
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
```

不过你现在刚学 SQLAlchemy，建议先把同步 ORM 学熟，再学异步版本。不然会同时被数据库、ORM、事务、async/await 绕住 😵‍💫

---

# 25. 建表不要长期靠 `create_all()` ⚠️

学习阶段可以：

```python
Base.metadata.create_all(engine)
```

它会根据模型创建表。

但真实项目里，表结构会不断变化，比如：

* 新增字段
* 修改字段类型
* 增加索引
* 新增表
* 修改外键

这时候更常用数据库迁移工具，比如 **Alembic**。Alembic 官方文档说它是一个轻量级数据库迁移工具，专门配合 SQLAlchemy 使用。([alembic.sqlalchemy.org][14])

你现在先记住：

```text
学习/小 demo：create_all()
正式项目：Alembic 管理迁移
```

---

# 26. 项目结构怎么放？📁

一个简单项目可以这样：

```text
sqlalchemy_demo/
├── .venv/
├── main.py
├── database.py
├── models.py
├── crud.py
└── requirements.txt
```

## database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///demo.db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)
```

## models.py

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "sys_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    age: Mapped[int | None] = mapped_column(nullable=True)
```

## crud.py

```python
from sqlalchemy import select

from database import SessionLocal
from models import User


def create_user(username: str, age: int | None) -> User:
    with SessionLocal() as session:
        user = User(username=username, age=age)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user(username: str) -> User | None:
    with SessionLocal() as session:
        return session.scalar(
            select(User).where(User.username == username)
        )
```

## main.py

```python
from database import engine
from models import Base
from crud import create_user, get_user

Base.metadata.create_all(engine)

create_user("admin", 22)

user = get_user("admin")
print(user.username if user else "没查到")
```

这就是一个最小 ORM 项目结构。

---

# 27. 常见坑 🚨

## 坑 1：忘记 commit

```python
session.add(user)
```

只 add 不 commit，数据库里不一定有。

要：

```python
session.commit()
```

---

## 坑 2：Session 用完不关闭

不要长期这样：

```python
session = Session(engine)
```

然后到处传、不关闭。

建议：

```python
with Session(engine) as session:
    ...
```

---

## 坑 3：把 ORM 对象拿出 Session 后还乱用

有些关系字段是懒加载的，如果 Session 已经关闭，再访问关系属性可能出问题。

例如：

```python
with Session(engine) as session:
    user = session.scalar(select(User))

print(user.articles)
```

如果 `articles` 没提前加载，可能会出错。

---

## 坑 4：SQLAlchemy 版本写法混乱

网上很多老教程还是 SQLAlchemy 1.x 写法，比如：

```python
Base = declarative_base()
session.query(User).filter(...)
```

现在学习建议优先学 2.x 风格：

```python
class Base(DeclarativeBase):
    pass

stmt = select(User).where(...)
session.scalar(stmt)
```

SQLAlchemy 官方迁移文档也强调 2.0 风格的写法，并且大量示例都转向 `select()`、`Mapped[]`、`mapped_column()` 等现代风格。([docs.sqlalchemy.org][15])

---

# 28. 你现在学习 SQLAlchemy 的顺序 🪜

建议你按这个顺序来：

```text
1. 先理解 Engine
2. 再理解 Model
3. 再理解 Session
4. 学会 create_all 创建表
5. 学会 add / commit 新增
6. 学会 select 查询
7. 学会修改对象后 commit
8. 学会 session.delete 删除
9. 学会 relationship 一对多
10. 学会事务 rollback
11. 学会 MySQL 连接
12. 最后学 Alembic 和异步 SQLAlchemy
```

不要一上来就学异步 ORM、连接池参数、复杂关系、多表联查。先把 CRUD 和 Session 吃透。

---

# 29. 给你一组练习题 ✍️🔥

## 练习 1：创建用户表

创建 `User` 模型：

```text
id
username
age
```

用 SQLite 创建表。

---

## 练习 2：新增用户

新增：

```text
username = admin
age = 22
```

---

## 练习 3：查询用户

根据 `username` 查询用户，并打印：

```text
id username age
```

---

## 练习 4：修改年龄

把 `admin` 的年龄改成：

```text
23
```

---

## 练习 5：删除用户

删除 `admin`。

---

## 练习 6：一对多

创建：

```text
User
Article
```

要求：

```text
一个 User 有多篇 Article
```

然后新增一个用户和两篇文章。

---

# 30. 最后总结 🎯

SQLAlchemy 你现在先抓住这几个核心：

```text
Engine：数据库连接入口
Model：Python 类映射数据库表
Session：一次数据库操作上下文
select：查询
add + commit：新增
修改对象属性 + commit：更新
delete + commit：删除
relationship：对象关系映射
```

最核心模板：

```python
engine = create_engine("sqlite:///demo.db", echo=True)

with Session(engine) as session:
    user = User(username="admin", age=22)
    session.add(user)
    session.commit()
```

一句话记住：

> **SQLAlchemy ORM 就是把“表”变成 Python 类，把“行”变成 Python 对象，用 Session 管理增删改查和事务。** 🐍🗄️

[1]: https://www.sqlalchemy.org/?utm_source=chatgpt.com "SQLAlchemy - The Database Toolkit for Python"
[2]: https://docs.sqlalchemy.org/dialects/?utm_source=chatgpt.com "Dialects — SQLAlchemy 2.0 Documentation"
[3]: https://docs.sqlalchemy.org/orm/?utm_source=chatgpt.com "SQLAlchemy ORM"
[4]: https://docs.sqlalchemy.org/en/latest/core/engines.html?utm_source=chatgpt.com "Engine Configuration — SQLAlchemy 2.1 Documentation"
[5]: https://dev.to/devsnorte/setting-up-a-standalone-sqlalchemy-20-orm-application-298c?utm_source=chatgpt.com "Setting up a standalone SQLAlchemy 2.0 ORM application"
[6]: https://docs.sqlalchemy.org/en/latest/orm/session_basics.html?utm_source=chatgpt.com "Session Basics — SQLAlchemy 2.1 Documentation"
[7]: https://docs.sqlalchemy.org/en/latest/orm/declarative_tables.html?utm_source=chatgpt.com "Table Configuration with Declarative — SQLAlchemy 2.1 ..."
[8]: https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html?utm_source=chatgpt.com "Transactions and Connection Management"
[9]: https://docs.sqlalchemy.org/tutorial/index.html?utm_source=chatgpt.com "SQLAlchemy Unified Tutorial"
[10]: https://docs.sqlalchemy.org/en/latest/orm/session_api.html?utm_source=chatgpt.com "Session API — SQLAlchemy 2.1 Documentation"
[11]: https://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html?utm_source=chatgpt.com "Basic Relationship Patterns"
[12]: https://docs.sqlalchemy.org/en/latest/dialects/mysql.html?utm_source=chatgpt.com "MySQL and MariaDB — SQLAlchemy 2.1 Documentation"
[13]: https://docs.sqlalchemy.org/en/latest/orm/extensions/asyncio.html?utm_source=chatgpt.com "Asynchronous I/O (asyncio) — SQLAlchemy 2.1 ..."
[14]: https://alembic.sqlalchemy.org/?utm_source=chatgpt.com "Alembic's documentation! - SQLAlchemy"
[15]: https://docs.sqlalchemy.org/en/latest/changelog/migration_20.html?utm_source=chatgpt.com "SQLAlchemy 2.0 - Major Migration Guide"
