# QQMonitor 使用说明

## 环境要求

- AllianceAuth >=4.0.0
- Python 3.11+

## 安装与启用

1. 安装插件（在 AllianceAuth 虚拟环境中执行）：

```bash
pip install -e /path/to/QQMonitor
```

2. 在 AllianceAuth 本地配置中启用应用：

```python
INSTALLED_APPS += [
    "qqmonitor.apps.QqmonitorConfig",
]
```

3. 执行数据库迁移：

```bash
python manage.py migrate
```

4. 重启 AllianceAuth。

重启后可在侧边栏看到 `QQ Monitor`。

## 页面使用方法

1. 登录 AllianceAuth，进入 `QQ Monitor` 页面。
2. 页面会显示当前账号在 AllianceAuth 的主角色名（只读）。
3. 首次使用时，填写并提交：
   - `QQ号`
   - `昵称`
4. 提交成功后，页面会改为只读展示当前绑定信息。
5. 如需修改，点击 `修改` 按钮进入编辑模式，改完后点 `提交`。
6. 如果不想保存修改，点击 `取消` 返回只读展示。

说明：

- 每个 AllianceAuth 用户仅维护一条绑定记录。
- `QQ号` 必须唯一，若已被其他用户绑定会提示失败。
- 修改 `QQ号` 时，请注意相关群管理策略带来的影响。

## 对外校验 API 使用方法

接口用于根据 QQ 号校验是否存在绑定关系。

- 路径：`/qqmonitor/api/v1/verify-qq/`
- 方法：`POST`
- Body（JSON）：

```json
{
  "qq_number": "123456789"
}
```

### API 配置

在 AllianceAuth 本地配置中增加：

```python
QQMONITOR_API_TOKEN = "your-public-token"
QQMONITOR_API_SECRET = "your-very-strong-secret"
QQMONITOR_API_MAX_SKEW_SECONDS = 300  # 可选，默认 300 秒
```

### 请求头

- `X-QQM-TOKEN`: 与 `QQMONITOR_API_TOKEN` 一致
- `X-QQM-TIMESTAMP`: 当前 Unix 时间戳（秒）
- `X-QQM-SIGNATURE`: `hmac_sha256(secret, f"{token}.{timestamp}.{qq_number}")` 的十六进制小写结果

### 响应字段说明

- `exists`: 是否存在该 QQ 记录
- `in_alliance`: 关联用户当前是否在联盟范围内
- `main_account_id`: 关联用户在 AllianceAuth 的主角色ID
- `main_character_name`: 关联用户在 AllianceAuth 的主角色名
- `nickname`: 绑定昵称

示例响应：

```json
{
  "ok": true,
  "qq_number": "123456789",
  "exists": true,
  "in_alliance": true,
  "main_account_id": 2112345678,
  "main_character_name": "Leito Main",
  "nickname": "Leito",
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

---

# QQMonitor Documentation (English)

## Requirements

- AllianceAuth >=4.0.0
- Python 3.11+

## Installation and Enablement

1. Install the plugin (inside your AllianceAuth virtual environment):

```bash
pip install -e /path/to/QQMonitor
```

2. Enable the app in your AllianceAuth local settings:

```python
INSTALLED_APPS += [
    "qqmonitor.apps.QqmonitorConfig",
]
```

3. Run database migrations:

```bash
python manage.py migrate
```

4. Restart AllianceAuth.

After restart, `QQ Monitor` will appear in the sidebar.

## Page Usage

1. Log in to AllianceAuth and open the `QQ Monitor` page.
2. The page displays your current AllianceAuth main character name (read-only).
3. On first use, fill in and submit:
   - `QQ Number`
   - `Nickname`
4. After a successful submission, the page switches to read-only display of current binding data.
5. To update data, click `Modify`, edit the fields, then click `Submit`.
6. To discard changes, click `Cancel` to return to read-only mode.

Notes:

- Each AllianceAuth user keeps only one binding record.
- `QQ Number` must be unique. Submission fails if it is already bound to another user.
- When changing `QQ Number`, consider any downstream group-management policies.

## External Verification API

This API verifies whether a QQ number has a binding record.

- Path: `/qqmonitor/api/v1/verify-qq/`
- Method: `POST`
- Body (JSON):

```json
{
  "qq_number": "123456789"
}
```

### API Configuration

Add the following to your AllianceAuth local settings:

```python
QQMONITOR_API_TOKEN = "your-public-token"
QQMONITOR_API_SECRET = "your-very-strong-secret"
QQMONITOR_API_MAX_SKEW_SECONDS = 300  # Optional, default is 300 seconds
```

### Request Headers

- `X-QQM-TOKEN`: must match `QQMONITOR_API_TOKEN`
- `X-QQM-TIMESTAMP`: current Unix timestamp (seconds)
- `X-QQM-SIGNATURE`: lowercase hex value of `hmac_sha256(secret, f"{token}.{timestamp}.{qq_number}")`

### Response Fields

- `exists`: whether the QQ record exists
- `in_alliance`: whether the linked user is currently in alliance scope
- `main_account_id`: main character ID in AllianceAuth
- `main_character_name`: main character name in AllianceAuth
- `nickname`: bound nickname

Example response:

```json
{
  "ok": true,
  "qq_number": "123456789",
  "exists": true,
  "in_alliance": true,
  "main_account_id": 2112345678,
  "main_character_name": "Leito Main",
  "nickname": "Leito",
  "submitted_by_user_id": 42,
  "current_alliance_id": 99000001
}
```

### Python Signature Example

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
