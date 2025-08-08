# 爬虫管理系统

这是一个基于 Django 的简单爬虫管理系统。它提供了一个 Web 界面来管理和监控爬虫，并允许异步执行爬取任务。

## 主要功能

- **爬虫管理**: 通过 Django admin 界面来创建、编辑和删除爬虫。
- **异步爬取**: 使用 Python 内置的 `threading` 模块在后台执行爬取任务，避免阻塞 Web 界面。
- **Web 用户界面**:
    - **爬虫列表**: 显示所有已配置的爬虫，并提供一个表单来启动新的爬取任务。
    - **工作列表**: 显示所有爬取任务的历史记录，包括它们的状态（待处理、运行中、已完成、已失败）。
- **命令行工具**: 提供一个 Django management command (`run_crawler`)，用于从命令行手动触发爬取任务。

## 项目结构

- `crawler_project/`: Django 项目根目录。
- `crawler/`: 核心的爬虫应用。
    - `models.py`: 定义了 `Crawler`, `CrawlJob`, `CrawlResult` 三个核心模型。
    - `views.py`: 处理 Web 请求的视图函数。
    - `crawlers.py`: 包含爬虫的实际执行逻辑。
    - `management/commands/`: 包含了自定义的 Django 命令。
    - `templates/`: 包含了应用的 HTML 模板。

## 如何运行

1.  **安装依赖**:
    ```bash
    pip install django requests beautifulsoup4
    ```

2.  **数据库迁移**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3.  **创建管理员用户**:
    ```bash
    python manage.py createsuperuser
    ```

4.  **运行开发服务器**:
    ```bash
    python manage.py runserver
    ```

5.  **访问系统**:
    - **Web 界面**: 打开浏览器并访问 `http://127.0.0.1:8000/`。
    - **Admin 界面**: 访问 `http://127.0.0.1:8000/admin/` 并使用您创建的管理员账户登录。

## 如何使用

### 1. 创建一个新的爬虫

- 登录 Admin 界面。
- 导航到 "爬虫" (Crawlers) 部分并点击 "添加爬虫" (Add crawler)。
- 填写爬虫的名称、描述和脚本路径。脚本路径是一个指向 `crawlers.py` 文件中函数的 Python 路径 (例如: `crawler.crawlers.simple_crawler`)。

### 2. 从 Web 界面启动一个爬取任务

- 访问主页 (`/crawler/`)。
- 从下拉列表中选择一个爬虫。
- 输入您想要爬取的 URL。
- 点击 "启动爬虫"。
- 您将被重定向到 "工作列表" 页面，在那里您可以看到任务的状态。

### 3. 从命令行启动一个爬取任务

您也可以使用 `run_crawler` 命令来手动启动一个任务：

```bash
python manage.py run_crawler <crawler_id> <url_to_crawl>
```

---
