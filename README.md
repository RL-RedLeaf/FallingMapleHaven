# FallingMapleHaven

面向高中同学及社交圈朋友的轻量社交平台，集个人主页展示、社交互动、即时聊天、趣味工具于一体。

---

## 功能模块

| 模块 | 说明 | 状态 |
|------|------|------|
| 个人主页 | 头像 / 封面 / 签名 / 访客足迹 / 留言板 | 已完成 |
| 社交广场 | 发布图文动态、点赞评论、话题标签、可见性控制 | 已完成 |
| 好友系统 | 用户搜索、好友申请 / 确认 / 解除 | 已完成 |
| 即时聊天 | 私聊 + 群聊，WebSocket 实时推送，未读计数 | 已完成 |
| 互动插件 | 默契问答、匿名提问箱，可插拔架构 | 已完成 |
| 通知系统 | 8 种通知类型，已读管理，角标计数 | 已完成 |
| 兴趣小组 | 创建圈子、组内动态、小组聊天室 | 已完成 |
| 管理后台 | 用户 / 内容 / 插件管理、数据统计、操作日志 | 已完成 |

---

## 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| 前端框架 | Vue 3 + Composition API | SPA 页面 |
| 状态管理 | Pinia 2 | 全局状态 |
| 路由 | Vue Router 4 | 前端路由 |
| UI 样式 | Tailwind CSS 3 | 原子化样式（秋叶主题色板） |
| 图标 | lucide-vue-next | SVG 图标库 |
| 构建工具 | Vite 5 | 开发服务器与打包 |
| 后端框架 | Django 5 | 业务逻辑与 ORM |
| API | Django REST Framework 3.15+ | RESTful 接口 |
| 实时通信 | Django Channels 4 + daphne | WebSocket |
| 数据库 | PostgreSQL 16 | 关系数据存储 |
| 缓存 / 消息 | Redis 7 | Channel Layer |
| 部署 | Docker Compose | 基础设施容器化 |

---

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose（用于启动 PostgreSQL 和 Redis）

### 安装

**1. 克隆项目**

```bash
git clone <repo-url>
cd FallingMapleHaven
```

**2. 启动基础设施**

```bash
cd docker
docker compose up -d
```

这将启动 PostgreSQL 16（端口 5432）和 Redis 7（端口 6379）。

**3. 后端设置**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

后端将运行于 `http://localhost:8000`。

**4. 前端设置**

```bash
cd frontend
npm install
npm run dev
```

前端将运行于 `http://localhost:5173`，开发模式下自动代理 API 请求到后端。

---

## 项目目录结构

```
FallingMapleHaven/
├── backend/                        # Django 后端
│   ├── config/                     #   项目配置
│   │   ├── settings/               #     base.py / dev.py / prod.py
│   │   ├── urls.py                 #     根路由
│   │   └── asgi.py                 #     Channels ASGI 入口
│   ├── apps/
│   │   ├── accounts/               #     用户系统（User 扩展 AbstractUser）
│   │   ├── profiles/               #     个人主页（Profile, VisitRecord, Guestbook）
│   │   ├── friends/                #     好友系统（Friendship）
│   │   ├── feed/                   #     动态与广场（Post, Comment, Like）
│   │   ├── chat/                   #     聊天系统（ChatRoom, Message, Consumer）
│   │   ├── groups/                 #     兴趣小组（InterestGroup, GroupMember）
│   │   ├── plugins/                #     插件系统（BasePlugin, 默契问答, 匿名提问箱）
│   │   ├── notifications/          #     通知系统（Notification）
│   │   └── admin_dashboard/        #     管理后台（SiteSettings, SiteLog, 统计）
│   ├── media/                      #   用户上传文件
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                       # Vue 3 前端
│   └── src/
│       ├── api/                    #   API 请求封装（9 个模块）
│       │   ├── client.js           #   axios 实例与拦截器
│       │   ├── auth.js
│       │   ├── posts.js
│       │   ├── profiles.js
│       │   ├── chat.js
│       │   ├── friends.js
│       │   ├── notifications.js
│       │   ├── plugin.js
│       │   └── admin.js
│       ├── stores/                 #   Pinia 状态管理
│       │   ├── auth.js
│       │   ├── feed.js
│       │   ├── chat.js
│       │   └── friend.js
│       ├── router/                 #   路由配置
│       │   ├── index.js            #   主路由 + 守卫
│       │   └── admin.js            #   管理后台子路由
│       ├── views/                  #   16 个页面组件
│       │   ├── HomePage.vue
│       │   ├── LoginPage.vue
│       │   ├── RegisterPage.vue
│       │   ├── ProfilePage.vue
│       │   ├── SettingsPage.vue
│       │   ├── ChatListPage.vue
│       │   ├── ChatRoomPage.vue
│       │   ├── FriendsPage.vue
│       │   ├── NotificationsPage.vue
│       │   ├── GroupListPage.vue
│       │   ├── GroupDetailPage.vue
│       │   ├── QuizPage.vue
│       │   ├── QuestionBoxPage.vue
│       │   ├── GuestbookPage.vue
│       │   ├── NotFoundPage.vue
│       │   └── admin/              #   7 个管理后台子页面
│       ├── components/             #   19 个公共组件
│       │   ├── NavBar.vue
│       │   ├── MobileTabBar.vue
│       │   ├── PostCard.vue
│       │   ├── PostCreateCard.vue
│       │   ├── AvatarImage.vue
│       │   ├── FriendButton.vue
│       │   ├── PluginEntryGrid.vue
│       │   ├── CommentSection.vue
│       │   ├── PostActions.vue
│       │   ├── PostImageGrid.vue
│       │   ├── MessageBubble.vue
│       │   ├── GuestbookBoard.vue
│       │   ├── ConfirmDialog.vue
│       │   ├── ToastContainer.vue
│       │   ├── TabBar.vue
│       │   ├── ToggleSwitch.vue
│       │   ├── BottomSheet.vue
│       │   ├── Icon.vue
│       │   └── SelectField.vue
│       ├── plugins/                #   前端插件注册
│       │   ├── registry.js
│       │   ├── quiz/index.js
│       │   └── questions/index.js
│       ├── composables/            #   组合式函数
│       ├── utils/                  #   工具函数
│       └── assets/                 #   全局样式与资源
│
├── docker/
│   └── docker-compose.yml          # PostgreSQL + Redis
├── Docs/                           # 设计文档（16 份）
├── Plans/                          # 开发规划（5 份）
├── AGENTS.md                       # AI 助手配置
└── README.md
```

---

## 页面路由

| 路径 | 页面 | 权限 |
|------|------|------|
| `/` | 广场动态流 | 登录 / 访客 |
| `/login` | 登录 | 未登录 |
| `/register` | 注册 | 未登录 |
| `/profile/:userId` | 个人主页 | 登录 / 访客 |
| `/profile/:userId/plugins/quiz` | 默契问答 | 登录 |
| `/profile/:userId/plugins/question-box` | 匿名提问箱 | 登录 |
| `/profile/:userId/guestbook` | 留言板 | 登录 |
| `/friends` | 好友管理 | 登录 |
| `/chat` | 聊天列表 | 登录 |
| `/chat/:roomId` | 聊天室 | 登录 |
| `/groups` | 小组列表 | 登录 / 访客 |
| `/groups/:groupId` | 小组详情 | 登录 |
| `/settings` | 个人设置 | 登录 |
| `/notifications` | 通知列表 | 登录 |
| `/admin` | 管理后台首页 | 管理员 |
| `/admin/users` | 用户管理 | 管理员 |
| `/admin/posts` | 内容管理 | 管理员 |
| `/admin/settings` | 站点设置 | 管理员 |
| `/admin/plugins` | 插件管理 | 管理员 |
| `/admin/stats` | 数据统计 | 管理员 |
| `/admin/logs` | 操作日志 | 管理员 |
| `/admin/anonymous-questions` | 匿名提问追溯 | 管理员 |

---

## API 概览

基础路径：`/api/v1`

| 模块 | 端点 | 说明 |
|------|------|------|
| 认证 | `POST /auth/register/` | 注册 |
| 认证 | `POST /auth/login/` | 登录 |
| 认证 | `GET/PATCH /auth/me/` | 获取 / 更新个人信息 |
| 认证 | `POST /auth/avatar/` | 上传头像 |
| 认证 | `POST /auth/cover/` | 上传封面 |
| 主页 | `GET /profiles/:id/` | 获取用户主页信息 |
| 主页 | `GET /profiles/:id/posts/` | 获取用户动态列表 |
| 主页 | `GET /profiles/:id/visitors/` | 获取访客足迹 |
| 主页 | `GET/POST /profiles/:id/guestbook/` | 留言板 |
| 好友 | `GET /friends/` | 好友列表 |
| 好友 | `POST /friends/request/` | 发送好友申请 |
| 好友 | `POST /friends/handle/` | 处理好友申请 |
| 动态 | `GET /posts/` | 广场动态流 |
| 动态 | `POST /posts/create/` | 发布动态 |
| 动态 | `POST /posts/:id/like/` | 点赞 / 取消 |
| 动态 | `GET/POST /posts/:id/comments/` | 评论列表 / 发表评论 |
| 聊天 | `GET /chat/rooms/` | 聊天列表 |
| 聊天 | `GET /chat/rooms/:id/messages/` | 消息历史 |
| 小组 | `GET/POST /groups/` | 小组列表 / 创建 |
| 小组 | `POST /groups/:id/join/` | 加入小组 |
| 插件 | `POST /plugins/quiz/questions/` | 默契问答出题 |
| 插件 | `GET /plugins/quiz/questions/received/` | 收到的题目 |
| 插件 | `POST /plugins/question-box/` | 匿名提问 |
| 插件 | `GET /plugins/question-box/inbox/` | 收到的提问 |
| 通知 | `GET /notifications/` | 通知列表 |
| 管理 | `GET/PATCH /admin/users/` | 用户管理 |
| 管理 | `GET/PATCH /admin/settings/` | 站点设置 |

详细 API 文档见 `Docs/03-API与WebSocket接口文档.md`。

---

## 主题色板

秋叶主题色通过 Tailwind CSS 扩展色板实现：

| 色值 | CSS 类 | 用途 |
|------|--------|------|
| `#C73B1D` | `maple-600` | 导航栏、按钮、重要元素 |
| `#F5A623` | `maple-400` | 强调、悬停、标签 |
| `#FFF8F0` | `maple-50` | 页面主背景 |
| `#FFFFFF` | `white` | 卡片、内容区域 |
| `#2D2D2D` | `text-primary` | 正文 |
| `#8C8C8C` | `text-secondary` | 辅助文字 |
| `#E8DDD4` | `border` | 分割线、边框 |

配置见 `frontend/tailwind.config.js`。

---

## 设计文档

项目文档位于 `Docs/` 目录下：

| 文件 | 内容 |
|------|------|
| `01-PRD-需求规格说明书.md` | 产品需求定义、用户故事、功能优先级矩阵 |
| `02-技术架构与数据库设计.md` | 架构图、技术选型、全部 27 张表结构定义 |
| `03-API与WebSocket接口文档.md` | 全部 REST API 端点与 WebSocket 消息协议 |
| `04-前端设计规范.md` | 主题色规范、路由表、组件树、Pinia Store 设计 |
| `05-插件系统设计.md` | 后端插件基类 + 注册器、前端 PluginRegistry |
| `06-开发任务书与验收标准.md` | 分阶段开发任务分配与验收清单 |
| `07-访客公开浏览功能设计方案.md` | 未登录访客页面级 / API 级权限矩阵 |
| `08-管理后台插件扩展系统设计.md` | 管理后台插件自声明与自动发现机制 |

开发规划见 `Plans/` 目录。

---

## 可用脚本

### 后端

```bash
python manage.py migrate              # 执行数据库迁移
python manage.py makemigrations       # 生成迁移文件
python manage.py createsuperuser      # 创建管理员账号
python manage.py runserver            # 启动开发服务器
```

### 前端

```bash
npm run dev          # 开发模式（热更新）
npm run build        # 生产构建
npm run preview      # 预览构建结果
```

---

## 开发约定

- 分支策略：`UIUX`（基于 `master`），所有功能开发在 `UIUX` 上进行
- 后端：Django 5 + DRF，使用 Session 认证，统一响应格式 `{code, message, data}`
- 前端：Vue 3 Composition API + Tailwind CSS，使用 `@/` 路径别名
- 组件设计：全局组件位于 `src/components/`，设计系统类使用 `card-base`、`btn-primary` 等预定义样式
- 确认弹窗：统一使用 `useConfirm()` composable + `<ConfirmDialog />`
- ToggleSwitch：使用 `<ToggleSwitch v-model="..." />` 组件

详细规范见 `AGENTS.md` 与 `Docs/04-前端设计规范.md`。

---

## 许可证

[MIT](./LICENSE) (c) 2026 RL-RedLeaf
