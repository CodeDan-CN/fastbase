# hraisearch


## 快速启动
> （默认已安装Conda并切换国内镜像）

**第一步：创建conda环境并且切换环境**
```text
> conda create -n hraisearch python=3.10
> conda activate hraisearch
```

**第二步：使用pycharm打开项目并选择hraisearch环境后安装依赖**
```text
> pip install -r requirements.txt
```

**第三步：修改项目环境配置**
```python
# Milvus连接配置（修改为你本地或者对应环境配置即可）
MILVUS_DB_CONFIG = {
    "host": "localhost",  
    "port": "19530",
    "username": "",
    "password": "",
    "db_name": "default",
}

# TORTOISE连接pgsql配置（修改为你本地或者对应环境配置即可）
TORTOISE_ORM_PGSQL = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            'credentials': {
                'database': 'odoo',
                'host': 'localhost',  
                'password': 'root',
                'port': '5432',
                'user': 'root',
            }
        }
    },
    'apps': {
        'models': {
            "models": ["models.pgsql_model"]
        }
    },
    'timezone': 'Asia/Shanghai'
}

# 临时文件存储路径（修改为你本地或者对应环境配置即可）
FILE_CONFIG = {
    "path": "/Users/codedan/local/project/pycharmProjects/digital_portrait/file/" #换成服务器地址或者你本地地址
}

# 日志文件配置
LOG_CONFIG = {
    "url" : "/Users/codedan/local/project/pycharmProjects/digital_portrait/log", # 换成服务器地址或者你本地地址
    "name": "digital_portrait",
    "time_format": "%Y-%m-%d"  # 修改时间格式以包含分钟
}
```
**第四步：启动项目**
```text
使用hraisearch环境到项目最外层app.py文件中对main方法进行run或者debug即可
```




## 如何debug fastAPI项目
> 在pycharm中不能直接使用debug按钮进行fastAPI项目的debug，需要修改一些配置pycharm配置

方法：在pycharm中双击shift搜索registry—找到 python.debug.asyncio.repl-取消勾选一保存



## 介绍项目基础结构
```text
project

   |

    --config

    --core

    --exception

    --models

    --utils

    --web

    app.py

    init_database_sql.sql

    update_database_sql.sql
```
+ config目录：存储外部中间件的连接配置，日志文件地址，服务文件存储地址等配置信息


+ core目录：业务逻辑以及数据操作层，等同于service层结合mapper层，进行业务逻辑和数据库的使用


+ exception：目录：存储全局异常定义以及自定义异常定义类


+ models目录：tortoise-orm映射数据实体类目录，在tortoise-orm连接配置中指定了此目录为读取的实体类目录


+ utils目录：工具类


+ web目录：定义多种不同业务的对外暴露接口，接收外部请求的调用以及数据的获取，相当于controller层。


+ app.py: fastAPI定义类也是启动类，在这里定义了fastAPI实体，路由，生命周期，启动等等。




## 重点：关于项目SQL的问题！！！！
> 项目最外层有两个sql文件，分别是`init_database_sql.sql`和`update_database_sql.sql`。
+ `init_database_sql.sql`：是项目最初上线之前截止记录的SQL的SQL文件
+ `update_database_sql.sql`：是项目上线之后，记录每次功能迭代涉及到的数据库表或者表字段新增，修改等操作的SQL操作的SQL文件
所以第一次正式上线之前开发的SQL均可记录在init_database_sql.sql文件中，当正式上线之后的迭代修改均记录在update_database_sql.sql中


# 项目部署
> 部署篇幅分为两篇，分别是`前置环境准备篇章`以及`已有环境下直接部署篇章`
### 前置环境篇
**第一步：安装conda安装脚本并给予执行权限（清华源）,执行过程会询问你要不要安装默认路径，可自定义安装路径，推荐：/opt/software/miniconda3**
```text
> wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
> chmod +x Miniconda3-latest-Linux-x86_64.sh
> ./Miniconda3-latest-Linux-x86_64.sh
```
注意：执行过程中选择不要自动初始化，不然每次与服务器建立连接都会自动启动conda，这样在命令行会有conda base作为输入基础，有些别的服务是不需要conda的，所以选择no。


**第二步：手动初始化或者启动conda(来到conda安装路径),并安装项目所需虚拟环境，并且进行pip换源**
```text
> source /opt/software/miniconda3/bin/activate
> conda create -n hraisearch python=3.10
> conda activate hraisearch
> pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```


**第三步：创建/opt/software/hraisearch目录**
```text
> mkdir -p /opt/software/hraisearch
> cd /opt/software/hraisearch
```

**第四步：编写服务启动脚本**
```text
> mkdir config
> vim start_config.py
### 内容

import os

# 设置守护进程
daemon = True
# 监听内网端口8000
bind = '0.0.0.0:8000'
# 设置进程文件目录
pidfile = './gunicorn.pid'
chdir = './digital_portrait'  # 设置为项目目录
# 工作模式
worker_class = 'uvicorn.workers.UvicornWorker'
# 并行工作进程数 核心数*2+1个
workers = 3  # multiprocessing.cpu_count() * 2 + 1
# 指定每个工作者的线程数
threads = 2
# 设置最大并发量
worker_connections = 2000

###

> cd ../
> vim start.sh
### 内容

#!/bin/bash

source /opt/software/miniconda3/bin/activate

conda activate hraisearch

# 启动 Gunicorn，并使用 start_config.py 配置文件
gunicorn -c ./config/start_config.py app:app

###

```

**第五步：编写服务停止脚本**
```text
> touch stop.sh
> vim stop.sh
### 内容

#!/bin/bash

#查找gunicorn主进程 PID
gunicorn_pid=$(ps aux | grep 'gunicorn' | grep -v 'grep' | awk '{print $2}')

# 如果找到了主进程 PID
if [ -n "$gunicorn_pid" ]; then
  echo "Found gunicorn process: $gunicorn_pid"

  # 给主进程发 SIGINT 信号，请求正常停止进程
  kill -INT $gunicorn_pid

  # 睡眠 5 秒等待主进程结束 
  sleep 5

  # 查找所有 gunicorn 子进程 PID
  gunicorn_child_pids=$(pstree -p $gunicorn_pid | grep -oP '([0-9]+)(?=\))')

  # 如果找到了子进程 PID
  if [ -n "$gunicorn_child_pids" ]; then
    echo "Found gunicorn child processes: $gunicorn_child_pids"

    # 杀死所有子进程
    for pid in $gunicorn_child_pids; do
      kill -9 $pid
    done
  fi

  echo "Stopped gunicorn process and child processes"

else
  echo "No running gunicorn process found"
fi

###

> chmod +x stop.sh
```

### 已有环境下直接部署篇

**第一步：修改项目内部的环境信息,进入项目config目录下，修改setting.py文件**
```python
# Milvus连接配置
MILVUS_DB_CONFIG = {
    # 下述是本地环境配置
    # "host": "localhost",
    # "port": "19530",
    # "username": "",
    # "password": "",
    # "db_name": "default",
    # 下述是开发环境配置
    "host": "10.0.5.63",
    "port": "31201",
    "username": "tai_test06_dup",
    "password": "QRCGH2F8tRd21xFH",
    "db_name": "tai_test06_dup",
}

# TORTOISE连接pgsql配置
TORTOISE_ORM_PGSQL = {
    "connections": {
        # 下述是david本地地址
        # "default": {
        #     "engine": "tortoise.backends.asyncpg",
        #     'credentials': {
        #         'database': 'odoo',
        #         'host': '10.3.74.219',  # david的本地地址
        #         'password': 'root',
        #         'port': '5432',
        #         'user': 'root',
        #         'maxsize': 10,  # 最大连接数
        #         'minsize': 1,  # 最小连接数
        #     }
        # }
        # 下述是odoo uat地址
        "default": {
            "engine": "tortoise.backends.asyncpg",
            'credentials': {
                'database': 'odoo14',
                'host': '10.3.70.157',  # odoo uat的环境地址
                'password': 'odoo14',
                'port': '5432',
                'user': 'odoo14',
                'maxsize': 30,  # 最大连接数
                'minsize': 1,  # 最小连接数
            }
        }

    },
    'apps': {
        'models': {
            "models": ["models.pgsql_model"]
        }
    },
    'timezone': 'Asia/Shanghai'
}

# 临时文件存储路径
FILE_CONFIG = {
    "path": "/opt/software/hraisearch/digital_portrait/file/",  # 开发环境（部署的时候切换）
    "batch": 50  # 文件单次获取批次
}

# 外部接口管理
INTERFACE_MANAGE = {
    "embedding_server": "182.92.82.8:31864",  # 问学embedding服务正式环境
    "master_file_download_server": "10.3.70.157:8069"  # odoo uat环境
}

# 日志文件配置
LOG_CONFIG = {
    "url": "/opt/software/hraisearch/digital_portrait/log", # 开发环境（部署的时候切换）
    "name": "digital_portrait",
    "time_format": "%Y-%m-%d"  # 修改时间格式以包含分钟
}

# 关键方法重试次数
FUNCTION_RETRY_COUNT = {
    "download_file": 5,  # 文件下载重试次数
    "embedding": 5  # 问学embedding重试次数
}
```

**第二步：修改项目启动方式，即位于项目根目录下的app.py文件**
```python
app = create_app() # 正式环境切换

# if __name__ == '__main__':
#     app = create_app()
#     uvicorn.run(app, host=os.environ.get('SERVER_HOST', '0.0.0.0'), port=int(os.environ.get('SERVER_PORT', 8000)))
```

**第三步：如果目前已经有项目在运行，请先执行停止脚本，并将当前运行项目的zip后缀修改为时间记录，删除项目目录即可**
```text
> ./stop.sh
```

**第四步：将项目打包为zip文件，并丢到/opt/software/hraisearch下，解压缩**
```text
> unzip digital_portrait.zip
```

**第五步：执行启动指令**
```text
> ./start.sh
```

**第六步：查看启动情况**
```text
> pstree -ap | grep gunicorn
```

或者到日志指定目录进行日志查询
```text
> cd /opt/software/hraisearch/digital_portrait/log
> tail -1000f digital_portrait
```





