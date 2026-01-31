# 打包与分发 (Packaging and Distribution)

相关源文件

-   [.bumpversion.cfg](https://github.com/celery/celery/blob/4d068b56/.bumpversion.cfg)
-   [Changelog.rst](https://github.com/celery/celery/blob/4d068b56/Changelog.rst)
-   [LICENSE](https://github.com/celery/celery/blob/4d068b56/LICENSE)
-   [MANIFEST.in](https://github.com/celery/celery/blob/4d068b56/MANIFEST.in)
-   [README.rst](https://github.com/celery/celery/blob/4d068b56/README.rst)
-   [celery/\_\_init\_\_.py](https://github.com/celery/celery/blob/4d068b56/celery/__init__.py)
-   [requirements/default.txt](https://github.com/celery/celery/blob/4d068b56/requirements/default.txt)
-   [requirements/pkgutils.txt](https://github.com/celery/celery/blob/4d068b56/requirements/pkgutils.txt)
-   [requirements/test-ci-default.txt](https://github.com/celery/celery/blob/4d068b56/requirements/test-ci-default.txt)
-   [requirements/test.txt](https://github.com/celery/celery/blob/4d068b56/requirements/test.txt)
-   [setup.cfg](https://github.com/celery/celery/blob/4d068b56/setup.cfg)
-   [setup.py](https://github.com/celery/celery/blob/4d068b56/setup.py)

## 目的与范围

本文档描述了 Celery 的打包、依赖管理和发布流程。它涵盖了项目的元数据配置、依赖定义（包括用于各种代理和后端的可选 extras）、版本控制机制以及分发流程。

有关开发和测试基础设施的信息，请参阅[开发与测试](/celery/celery/10-development-and-testing)。

---

## 概述

Celery 使用标准的 Python 打包工具，并结合了自定义的依赖管理系统。该项目支持广泛的可选功能，这些功能通过 `setup.py` 中定义的 extras 进行管理。

**核心组件：**

-   **`setup.py`**：项目定义和依赖配置的主入口点。
-   **`requirements/` 目录**：包含按功能类别组织的详细依赖列表。
-   **`.bumpversion.cfg`**：用于自动化版本号自增和发布的配置。
-   **`celery/__init__.py`**：定义了版本号和项目元数据的单一事实来源。

---

## 打包元数据

Celery 的包元数据在 `setup.py` 中定义，并从 `celery/__init__.py` 中提取动态信息。

### 项目定义

| 属性 | 描述 | 来源 |
| --- | --- | --- |
| **名称 (Name)** | `celery` | `setup.py` |
| **版本 (Version)** | 语义化版本 (例如 `5.6.2`) | `celery/__init__.py` |
| **作者 (Author)** | Ask Solem | `setup.py` |
| **维护者 (Maintainer)** | Celery 团队 | `setup.py` |
| **许可证 (License)** | BSD 3-Clause | `LICENSE` |
| **主页 (Home Page)** | [https://docs.celeryq.dev/](https://docs.celeryq.dev/) | `setup.py` |

---

## 依赖管理

Celery 维护着一个复杂的依赖树，由核心运行时的必选依赖和针对特定功能的广泛可选依赖（extras）组成。

### 核心依赖

核心依赖通过 `requirements/default.txt` 定义，并集成到 `setup.py` 的 `install_requires` 中。

**主要依赖项：**

| 包名 | 用途 |
| --- | --- |
| `kombu` | 消息传递和代理通信 |
| `billiard` | 针对 Celery 优化的多进程支持 |
| `vine` | 异步 Promise 库 |
| `click` | 命令行界面框架 |
| `python-dateutil` | 日期和时间解析 |

**来源：** [requirements/default.txt](https://github.com/celery/celery/blob/4d068b56/requirements/default.txt)

### 可选依赖 (Extras)

由于 Celery 支持多种代理和后端，它大量使用了 `extras_require`。这允许用户仅安装其特定架构所需的库。

**Extras 分类：**

1.  **消息代理 (Brokers)**：`librabbitmq`, `redis`, `sqs`, `gcpubsub` 等。
2.  **结果后端 (Backends)**：`sqlalchemy`, `memcache`, `mongodb`, `cassandra`, `dynamodb`, `azureblockblob` 等。
3.  **序列化 (Serialization)**：`msgpack`, `yaml`, `auth`。
4.  **并发模型 (Concurrency)**：`eventlet`, `gevent`。
5.  **监控与开发 (Monitoring & Dev)**：`pytest`, `sphinx`。

有关 extras 的完整列表及其用途，请参阅[依赖与 Extras](/celery/celery/11.2-dependencies-and-extras)。

**来源：** [setup.py12-46](https://github.com/celery/celery/blob/4d068b56/setup.py#L12-L46)

---

## 版本管理

Celery 使用 `bumpversion` 工具来协调多个文件之间的版本号更新。

### 版本定义

版本号在 `celery/__init__.py` 中定义：

```python
__version__ = '5.6.2'
```
### 自动化流程

`.bumpversion.cfg` 确保当执行版本自增时，以下文件会同步更新：

-   `celery/__init__.py`
-   `README.rst`
-   `docs/includes/introduction.txt`

该流程还会自动创建 Git 提交和标签（Tags）。

有关详细的版本策略和发布说明，请参阅[版本管理与发布](/celery/celery/11.3-version-management-and-release)。

**来源：** [.bumpversion.cfg](https://github.com/celery/celery/blob/4d068b56/.bumpversion.cfg)

---

## 包结构与入口点

### 目录布局

```text
celery/
├── app/            # 核心应用逻辑
├── worker/         # 工作者实现
├── beat/           # 调度器实现
├── bin/            # 命令行入口点 (Click 命令)
├── backends/       # 结果后端实现
├── contrib/        # 框架集成和插件
└── utils/          # 内部工具集
```
### 命令行入口点

Celery 通过 `setup.py` 中的 `entry_points` 导出其 CLI 脚本：

```python
entry_points={
    'console_scripts': [
        'celery = celery.__main__:main',
    ],
}
```
这使得 `celery` 命令在安装后在系统路径中可用。

**来源：** [setup.py154-158](https://github.com/celery/celery/blob/4d068b56/setup.py#L154-L158) [celery/\_\_main\_\_.py](https://github.com/celery/celery/blob/4d068b56/celery/__main__.py)

---

## 发布流程

### 构建分发包

Celery 使用 `Makefile` 提供的命令来构建分发包：

```bash
# 构建源码包和 Wheel 包
make build
```
该命令执行 `python setup.py sdist bdist_wheel`。

### 质量检查 (Pre-release Checks)

在发布之前，必须通过所有质量门禁：

```bash
# 运行单元测试、集成测试和 Lint 检查
make distcheck
```
### 分发到 PyPI

分发包上传到 PyPI (The Python Package Index)，通常使用 `twine` 完成。

---

## 后续步骤

-   **包结构**：请参阅[包结构](/celery/celery/11.1-package-structure)获取内部模块布局的详细视图。
-   **Extras 详情**：请参阅[依赖与 Extras](/celery/celery/11.2-dependencies-and-extras)获取所有可选包的参考。
-   **发布日志**：请参阅[版本管理与发布](/celery/celery/11.3-version-management-and-release)获取历史记录和发布程序。
