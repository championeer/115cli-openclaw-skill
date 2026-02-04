# 115网盘 Cookie 获取方法

## 步骤

1. 在浏览器中登录 [115.com](https://115.com)
2. 打开开发者工具 (F12)
3. 切换到 Network 标签
4. 刷新页面
5. 点击任意请求，找到 Request Headers 中的 `Cookie`
6. 复制完整的 Cookie 字符串

## 关键字段

必需的cookie字段：
- `CID` - 客户端ID
- `UID` - 用户ID
- `SEID` - 会话ID
- `KID` - 密钥ID

## 示例

```
CID=xxx; KID=xxx; SEID=xxx; UID=xxx_A1_xxx; USERSESSIONID=xxx
```

## 有效期

Cookie通常在以下情况失效：
- 手动退出登录
- 长时间未使用（约30天）
- 在其他设备登录

失效后需重新获取cookie并执行 `115cli login`。
