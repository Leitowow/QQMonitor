# QQMonitor（AllianceAuth 插件）

`QQMonitor` 是一个 AllianceAuth 插件项目的起始骨架。

当前已实现：

- 在 AllianceAuth 侧边栏注册菜单入口
- 提供一个基础插件页面
- 为后续 QQ 监控逻辑预留清晰结构

## 环境要求

- AllianceAuth v5.x
- Python 3.11+

## 安装方式（开发环境）

1. 克隆本仓库。
2. 在 AllianceAuth 的虚拟环境中安装本插件（可编辑模式）：

```bash
pip install -e /path/to/QQMonitor
```

3. 在 AllianceAuth 的本地配置中加入应用：

```python
INSTALLED_APPS += [
    "qqmonitor.apps.QqmonitorConfig",
]
```

4. 执行数据库迁移：

```bash
python manage.py migrate
```

5. 重启 AllianceAuth。

重启后，你应当可以在侧边栏看到 `QQ Monitor` 菜单项。

