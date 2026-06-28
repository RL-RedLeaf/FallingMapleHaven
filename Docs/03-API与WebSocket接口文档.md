# API 与 WebSocket 接口文档 — FallingMapleHaven

> 版本: v1.0  
> 面向读者: 全栈开发  
> 基础路径: `/api/v1`

---

## 1. 通用规范

### 1.1 响应格式

**成功响应:**
```json
{
    "code": 0,
    "message": "success",
    "data": { ... }
}
```

**错误响应:**
```json
{
    "code": 40001,
    "message": "用户名已存在",
    "data": null
}
```

### 1.2 错误码定义

| 错误码 | 含义 |
|--------|------|
| 0 | 成功 |
| 40001 | 参数错误 |
| 40002 | 用户不存在 |
| 40003 | 登录凭证无效 |
| 40004 | 无权限 |
| 40005 | 资源不存在 |
| 40006 | 操作冲突（如重复申请） |
| 50000 | 服务器内部错误 |

### 1.3 认证方式

- 使用 Django Session 认证（后端渲染 Session）
- 前端通过 `credentials: 'include'` 发送请求
- 或使用 Token 认证（DRF 的 TokenAuthentication）

---

## 2. 用户系统 API

### 2.1 注册

```
POST /api/v1/auth/register/
```

**请求体:**
```json
{
    "username": "testuser",
    "password": "Password123!",
    "nickname": "测试用户",
    "email": ""          // 选填
}
```

**响应:**
```json
{
    "code": 0,
    "message": "success",
    "data": {
        "user_id": 1,
        "username": "testuser",
        "nickname": "测试用户"
    }
}
```

### 2.2 登录

```
POST /api/v1/auth/login/
```

**请求体:**
```json
{
    "username": "testuser",
    "password": "Password123!"
}
```

**响应:**
```json
{
    "code": 0,
    "message": "success",
    "data": {
        "user_id": 1,
        "username": "testuser",
        "nickname": "测试用户",
        "avatar": "/media/avatars/default.png"
    }
}
```

### 2.3 退出登录

```
POST /api/v1/auth/logout/
```

**响应:** 标准成功响应

### 2.4 获取当前用户信息

```
GET /api/v1/auth/me/
```

**响应:**
```json
{
    "code": 0,
    "data": {
        "user_id": 1,
        "username": "testuser",
        "nickname": "测试用户",
        "avatar": "/media/avatars/default.png",
        "cover_image": null,
        "bio": "你好世界",
        "email": "",
        "real_name": "张三",
        "show_real_name": false,
        "is_admin": false
    }
}
```

### 2.5 更新个人信息

```
PATCH /api/v1/auth/me/
```

**请求体:** (所有字段可选)
```json
{
    "nickname": "新昵称",
    "bio": "新签名",
    "email": "user@example.com",
    "real_name": "张三",
    "show_real_name": true
}
```

### 2.6 修改密码

```
POST /api/v1/auth/change-password/
```

**请求体:**
```json
{
    "old_password": "OldPass123!",
    "new_password": "NewPass456!"
}
```

### 2.7 上传头像

```
POST /api/v1/auth/avatar/
```

**请求体:** multipart/form-data, 字段名 `avatar`

### 2.8 上传封面

```
POST /api/v1/auth/cover/
```

**请求体:** multipart/form-data, 字段名 `cover_image`

---

## 3. 用户主页 API

### 3.1 获取用户主页信息

```
GET /api/v1/profiles/{user_id}/
```

**响应:**
```json
{
    "code": 0,
    "data": {
        "user": {
            "user_id": 1,
            "nickname": "测试用户",
            "avatar": "/media/avatars/1.jpg",
            "cover_image": "/media/covers/1.jpg",
            "bio": "签名文字",
            "real_name": "张三",
            "show_real_name": true
        },
        "friend_status": "self",          // self/pending_sent/pending_received/accepted/none
        "visitor_count": 42,
        "plugins": [
            {"type": "quiz", "name": "默契问答", "is_active": true},
            {"type": "question_box", "name": "匿名提问箱", "is_active": true}
        ]
    }
}
```

### 3.2 获取用户的动态列表

```
GET /api/v1/profiles/{user_id}/posts/
```

**参数:** `?page=1&page_size=10`

**响应:** 分页的动态列表

### 3.3 获取访客足迹

```
GET /api/v1/profiles/{user_id}/visitors/
```

**参数:** `?page=1&page_size=20`

**响应:**
```json
{
    "code": 0,
    "data": {
        "count": 42,
        "results": [
            {
                "visitor_id": 2,
                "nickname": "访客A",
                "avatar": "/media/avatars/2.jpg",
                "visited_at": "2026-06-22T14:30:00Z"
            }
        ]
    }
}
```

---

## 4. 好友系统 API

### 4.1 发送好友申请

```
POST /api/v1/friends/request/
```

**请求体:**
```json
{
    "to_user_id": 2
}
```

### 4.2 处理好友申请

```
POST /api/v1/friends/handle/
```

**请求体:**
```json
{
    "request_id": 1,
    "action": "accept"        // accept / reject
}
```

### 4.3 解除好友

```
POST /api/v1/friends/unfriend/
```

**请求体:**
```json
{
    "friend_id": 2
}
```

### 4.4 获取好友列表

```
GET /api/v1/friends/
```

### 4.5 获取收到的申请

```
GET /api/v1/friends/requests/
```

### 4.6 搜索用户

```
GET /api/v1/friends/search/?q=关键词
```

---

## 5. 动态/广场 API

### 5.1 发布动态

```
POST /api/v1/posts/
```

**请求体:** multipart/form-data
```
content: "今天的夕阳好美"
visibility: "public"
topic_tag: "分享"
images: [File, File, ...]   // 最多9张
files: [File, File, ...]    // 可选
```

### 5.2 获取广场动态

```
GET /api/v1/posts/
```

**参数:** `?page=1&page_size=20&topic=话题&visibility=public`

### 5.3 获取单个动态

```
GET /api/v1/posts/{post_id}/
```

### 5.4 删除动态

```
DELETE /api/v1/posts/{post_id}/
```

### 5.5 点赞/取消点赞

```
POST /api/v1/posts/{post_id}/like/
```

**响应:**
```json
{
    "code": 0,
    "data": {
        "is_liked": true,
        "like_count": 10
    }
}
```

### 5.6 获取评论列表

```
GET /api/v1/posts/{post_id}/comments/
```

### 5.7 发表评论

```
POST /api/v1/posts/{post_id}/comments/
```

**请求体:**
```json
{
    "content": "好漂亮！"
}
```

### 5.8 删除评论

```
DELETE /api/v1/comments/{comment_id}/
```

---

## 6. 聊天系统 API

### 6.1 获取聊天列表

```
GET /api/v1/chat/rooms/
```

**响应:**
```json
{
    "code": 0,
    "data": [
        {
            "room_id": 1,
            "name": "张三",
            "type": "private",
            "last_message": "好的明天见",
            "last_message_at": "2026-06-22T14:30:00Z",
            "unread_count": 2
        }
    ]
}
```

### 6.2 获取房间消息历史

```
GET /api/v1/chat/rooms/{room_id}/messages/
```

**参数:** `?page=1&page_size=50`

### 6.3 创建私聊房间

```
POST /api/v1/chat/rooms/
```

**请求体:**
```json
{
    "type": "private",
    "member_ids": [2]
}
```

**响应:** 返回 room_id，如房间已存在则返回现有房间

### 6.4 创建群聊

```
POST /api/v1/chat/rooms/
```

**请求体:**
```json
{
    "type": "group",
    "name": "高中同学群",
    "member_ids": [2, 3, 4]
}
```

### 6.5 发送消息 (REST 后备)

```
POST /api/v1/chat/rooms/{room_id}/messages/
```

**请求体:**
```json
{
    "content": "你好！",
    "msg_type": "text"
}
```

> 注: 正常情况下通过 WebSocket 发送消息，此接口作为后备/历史同步

---

## 7. WebSocket 聊天协议

### 7.1 连接

```
WebSocket URL: ws://host/ws/chat/?token=xxx
```

认证方式：URL 参数携带 Session Token 或 JWT

### 7.2 消息格式

所有 WebSocket 消息使用 JSON 格式:

**客户端 → 服务器:**
```json
{
    "type": "send_message",
    "room_id": 1,
    "content": "你好！",
    "msg_type": "text"
}
```

**服务器 → 客户端 (广播):**
```json
{
    "type": "new_message",
    "data": {
        "message_id": 100,
        "room_id": 1,
        "sender_id": 1,
        "sender_nickname": "测试用户",
        "sender_avatar": "/media/avatars/1.jpg",
        "content": "你好！",
        "msg_type": "text",
        "created_at": "2026-06-22T14:30:00Z"
    }
}
```

### 7.3 事件列表

| type (客户端→服务端) | 说明 |
|---------------------|------|
| send_message | 发送消息 |
| typing | 正在输入 |
| mark_read | 标记已读(二期) |
| join_room | 加入房间（自动） |
| leave_room | 离开房间 |

| type (服务端→客户端) | 说明 |
|---------------------|------|
| new_message | 新消息 |
| typing | 对方正在输入提示 |
| user_joined | 用户加入群聊 |
| user_left | 用户离开群聊 |
| error | 错误信息 |

---

## 8. 兴趣小组 API

### 8.1 创建小组

```
POST /api/v1/groups/
```

**请求体:**
```json
{
    "name": "篮球爱好者",
    "description": "喜欢打篮球的一起约球",
    "is_public": true
}
```

### 8.2 获取小组列表

```
GET /api/v1/groups/
```

### 8.3 获取小组详情

```
GET /api/v1/groups/{group_id}/
```

### 8.4 加入小组

```
POST /api/v1/groups/{group_id}/join/
```

### 8.5 退出小组

```
POST /api/v1/groups/{group_id}/leave/
```

### 8.6 管理成员 (组长)

```
POST /api/v1/groups/{group_id}/members/{user_id}/
```

**请求体:**
```json
{
    "action": "remove"    // remove / promote_admin
}
```

### 8.7 更新小组信息 (组长)

```
PATCH /api/v1/groups/{group_id}/
```

### 8.8 获取小组动态

```
GET /api/v1/groups/{group_id}/posts/
```

---

## 9. 互动插件 API

### 9.1 默契问答

**给好友出题:**
```
POST /api/v1/plugins/quiz/questions/
```
```json
{
    "target_user_id": 2,
    "question": "我最喜欢的颜色是？",
    "correct_answer": "蓝色"
}
```

**获取我收到的题目:**
```
GET /api/v1/plugins/quiz/questions/received/
```

**答题:**
```
POST /api/v1/plugins/quiz/questions/{question_id}/answer/
```
```json
{
    "answer": "红色"
}
```

**获取我与某好友的匹配度:**
```
GET /api/v1/plugins/quiz/result/{friend_user_id}/
```

### 9.2 匿名提问箱

**向某人提问:**
```
POST /api/v1/plugins/questions/
```
```json
{
    "recipient_id": 1,
    "content": "你最近在看什么书？"
}
```

**获取我的提问箱(他人向我提问):**
```
GET /api/v1/plugins/questions/inbox/
```

**回答提问:**
```
POST /api/v1/plugins/questions/{question_id}/answer/
```
```json
{
    "answer": "最近在看《百年孤独》"
}
```

**删除提问:**
```
DELETE /api/v1/plugins/questions/{question_id}/
```

---

## 10. 通知系统 API

### 10.1 获取通知列表

```
GET /api/v1/notifications/
```

**参数:** `?page=1&page_size=20&unread_only=true`

### 10.2 标记已读

```
POST /api/v1/notifications/{id}/read/
```

### 10.3 全部标记已读

```
POST /api/v1/notifications/read-all/
```

### 10.4 获取未读通知数

```
GET /api/v1/notifications/unread-count/
```

---

## 11. 管理后台 API

### 11.1 用户管理

```
GET /api/v1/admin/users/                      # 用户列表
PATCH /api/v1/admin/users/{user_id}/           # 修改用户状态
DELETE /api/v1/admin/users/{user_id}/          # 删除用户
```

### 11.2 内容管理

```
GET /api/v1/admin/posts/                      # 动态列表(含匿名者)
DELETE /api/v1/admin/posts/{post_id}/          # 删除动态
GET /api/v1/admin/comments/                   # 评论列表
DELETE /api/v1/admin/comments/{comment_id}/    # 删除评论
```

> 匿名提问: 管理员 GET 接口返回的数据中包含 `real_sender` 字段

### 11.3 站点设置

```
GET /api/v1/admin/settings/                   # 获取所有设置
PATCH /api/v1/admin/settings/                  # 更新设置
```

### 11.4 插件管理

```
GET /api/v1/admin/plugins/                    # 插件列表
PATCH /api/v1/admin/plugins/{plugin_id}/       # 启停插件
```

### 11.5 统计数据

```
GET /api/v1/admin/stats/                      # 概览数据
```

### 11.6 操作日志

```
GET /api/v1/admin/logs/                       # 日志列表
```

---

## 12. 文件上传通用接口

### 12.1 上传文件

```
POST /api/v1/upload/
```

**请求体:** multipart/form-data

**响应:**
```json
{
    "code": 0,
    "data": {
        "url": "/media/uploads/2026/06/22/file.pdf",
        "size": 1024000,
        "original_name": "文档.pdf"
    }
}
```

### 12.2 上传图片

```
POST /api/v1/upload/image/
```

**限制:** 仅接受 jpg/png/gif/webp, 单文件最大 10MB
