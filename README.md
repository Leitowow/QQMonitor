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

## 对外 API（Token + Signature）

插件提供一个对外可访问的校验接口（无需登录）：

- 路径：`/qqmonitor/api/v1/verify-qq/`
- 方法：`POST`
- Body（JSON）：

```json
{
  "qq_number": "123456789"
}
```

### 本地配置

在 AllianceAuth 的本地配置中增加：

```python
QQMONITOR_API_TOKEN = "your-public-token"
QQMONITOR_API_SECRET = "your-very-strong-secret"
QQMONITOR_API_MAX_SKEW_SECONDS = 300  # 可选，默认 300 秒
```

### 请求头要求

- `X-QQM-TOKEN`: 与 `QQMONITOR_API_TOKEN` 一致
- `X-QQM-TIMESTAMP`: 当前 Unix 时间戳（秒）
- `X-QQM-SIGNATURE`: `hmac_sha256(secret, f"{token}.{timestamp}.{qq_number}")` 的十六进制小写结果

### 返回说明

- `exists=false`：数据库没有该 QQ 记录
- `exists=true` 且 `in_alliance=true`：有记录，且关联用户当前仍在 AA 的联盟范围内
- `exists=true` 且 `in_alliance=false`：有记录，但关联用户已不在当前联盟范围（或无有效用户关联）
- 固定返回 `main_account_id`（此 QQ 关联的主账户ID）与 `nickname`（此 QQ 的昵称），未命中时为 `null`

示例返回：

```json
{
  "ok": true,
  "qq_number": "123456789",
  "exists": true,
  "in_alliance": true,
  "main_account_id": 2112345678,
  "nickname": "Leito",
  "main_character_id": 2112345678,
  "submitted_by_user_id": 42,
  "current_alliance_id": 99000001
}
```

### Python 签名示例

```python
import hashlib
import hmac
import time

token = "your-public-token"
secret = "your-very-strong-secret"
qq_number = "123456789"
timestamp = str(int(time.time()))
message = f"{token}.{timestamp}.{qq_number}".encode("utf-8")
signature = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()
print(timestamp, signature)
```
