## 介绍
项目使用`djangorestframework`实现前后端分离

## 环境
python3.6+

mysql5.7+

## 环境搭建
1. 下载源码
    ```
    git clone git@gitee.com:qDonl/Online-Imooc.git
    ```

2. 文件修改
    ```
    cd Online-Imooc
    mkdir media  # gitignore忽略
    ```
   
3. 安装环境
    ```
    # path/to/Online-Imooc
    pip install pipenv
    pipenv install
    ```

4. 运行环境
    ```.env
    python manage.py runserver
    ```
