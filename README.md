# 🍁 FallingMapleHaven

> 秋叶落下的地方，有一片属于朋友们的温暖小天地 ✨

一个面向高中同学及社交圈朋友的轻量社交平台 —— 集个人主页、社交动态、即时聊天、趣味互动插件于一体。

---

## 🌟 特色功能

| 模块 | 说些什么好呢 | 状态 |
|------|-------------|------|
| 👤 **个人主页** | 头像 / 封面 / 签名 / 访客足迹 / 留言板，展示独一无二的你 | ✅ 已完成 |
| 📝 **社交广场** | 发布图文动态、点赞评论、话题标签、可见权限控制 | ✅ 已完成 |
| 🤝 **好友系统** | 搜索、申请、双向确认、一键解除 | ✅ 已完成 |
| 💬 **即时聊天** | 私聊 + 群聊，WebSocket 实时推送，未读计数 | ✅ 已完成 |
| 🔌 **互动插件** | 默契问答 / 匿名提问箱，可插拔架构，即插即用 | ✅ 已完成 |
| 🔔 **通知系统** | 8 种通知类型，已读管理，导航栏角标 | ✅ 已完成 |
| 🏕️ **兴趣小组** | 创建圈子、组内动态隔离、小组聊天室 | ✅ 已完成 |
| ⚙️ **管理后台** | 用户 / 内容 / 插件管理、数据统计、操作日志、匿名追溯 | ✅ 已完成 |

---

## 🛠️ 技术栈

| 层 | 技术 | 用途 |
|---|------|------|
| 🖥️ **前端** | **Vue 3** + Composition API + **Tailwind CSS 3** + **Pinia** + **Vue Router 4** | SPA |
| 🎨 **图标** | **lucide-vue-next** 🇳 | 干净漂亮的图标库 |
| ⚡ **构建** | **Vite 5** | 闪电般的开发体验 |
| 📡 **后端** | **Django 5** + **Django REST Framework 3.15** | RESTful API |
| 🔌 **实时通信** | **Django Channels 4** + **daphne** | WebSocket |
| 🗄️ **数据库** | **PostgreSQL 16** | 可靠的关系存储 |
| 🧩 **缓存** | **Redis 7** | Channel Layer + 缓存 |
| 🐳 **部署** | **Docker Compose** (PG + Redis) | 一键拉起基础设施 |

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose（可选，用于启动 PG + Redis）

### 🏗️ 1. 克隆 & 安装依赖

```bash
# 后端
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

### 🐘 2. 启动基础设施（PostgreSQL + Redis）

```bash
cd docker
docker compose up -d
```

### ⚙️ 3. 配置后端

```bash
cd backend
cp .env.example .env
# 编辑 .env 中的数据库配置（默认值即可用于本地开发）
python manage.py migrate
python manage.py runserver
```

### 🎨 4. 启动前端

```bash
cd frontend
npm run dev
```

浏览器打开 `http://localhost:5173` 🎉

---

## 📁 项目结构

```
FallingMapleHaven/
├── backend/                          # 🐍 Django 后端
│   ├── config/                       #   项目配置
│   │   ├── settings/                 #     base.py / dev.py / prod.py
│   │   ├── urls.py                   #     根路由
│   │   └── asgi.py                   #     Channels ASGI 入口
│   ├── apps/                         #   Django Apps
│   │   ├── accounts/                 #     用户系统
│   │   ├── profiles/                 #     个人主页
│   │   ├── friends/                  #     好友系统
│   │   ├── feed/                     #     动态 & 广场
│   │   ├── chat/                     #     聊天 & WebSocket
│   │   ├── groups/                   #     兴趣小组
│   │   ├── plugins/                  #     插件系统（含默契问答 / 匿名提问箱）
│   │   ├── notifications/            #     通知系统
│   │   └── admin_dashboard/          #     管理后台
│   ├── media/                        #   用户上传文件
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                         # 🎨 Vue 3 前端
│   └── src/
│       ├── api/                      #   API 请求（9 个模块）
│       ├── stores/                   #   Pinia 状态管理
│       ├── router/                   #   路由配置
│       ├── views/                    #   16 个页面
│       ├── components/               #   19 个公共组件
│       ├── plugins/                  #   前端插件注册
│       ├── composables/              #   组合式函数
│       └── utils/                    #   工具函数
│
├── docker/                           # 🐳 docker-compose.yml
├── Docs/                             # 📚 16 份设计文档
└── Plans/                            # 📋 迭代路线图、协作规范等
```

---

## 🎨 秋叶主题色

| 色名 | 色值 | 用途 |
|------|------|------|
| 🍁 枫叶红 | `#C73B1D` | 导航栏、按钮、重要元素 |
| 🧡 橙黄 | `#F5A623` | 强调、悬停、标签 |
| 🌾 米白 | `#FFF8F0` | 页面主背景 |
| 📄 纯白 | `#FFFFFF` | 卡片、内容区域 |
| ✒️ 文字主色 | `#2D2D2D` | 正文 |
| 🌫️ 文字辅色 | `#8C8C8C` | 次级文字 |
| 🖼️ 边框 | `#E8DDD4` | 分割线、边框 |

Tailwind 中通过 `maple-50` ~ `maple-900` 使用，详见 `frontend/tailwind.config.js`。

---

## 📜 可用的脚本

### 后端

```bash
python manage.py migrate          # 数据库迁移
python manage.py createsuperuser  # 创建管理员
python manage.py runserver        # 启动开发服务器 (http://localhost:8000)
python manage.py makemigrations   # 生成迁移文件
```

### 前端

```bash
npm run dev       # 启动开发服务器 (http://localhost:5173)
npm run build     # 构建生产版本
npm run preview   # 预览构建产物
```

---

## 🏗️ 设计文档

所有设计文档位于 `Docs/` 目录下：

| 文档 | 内容 |
|------|------|
| `01-PRD-需求规格说明书.md` | 完整功能定义、用户故事、优先级矩阵 |
| `02-技术架构与数据库设计.md` | 架构图、技术选型、所有表结构 |
| `03-API与WebSocket接口文档.md` | 全部 REST API + WebSocket 协议 |
| `04-前端设计规范.md` | 主题色、路由、组件树、Pinia Store 规范 |
| `05-插件系统设计.md` | 后端 BasePlugin + 前端 PluginRegistry |
| `06-开发任务书与验收标准.md` | 分阶段开发任务 + 验收 checklist |
| `07-访客公开浏览功能设计方案.md` | 未登录访客权限矩阵设计 |
| `08-管理后台插件扩展系统设计.md` | 管理后台插件自动发现机制 |

---

## 📸 页面一览（这样说吧）

| 页面 | 路由 | 说明 |
|------|------|------|
| 🏠 首页广场 | `/` | 动态流 + 话题筛选 + 发布入口 |
| 🔑 登录 | `/login` | 用户名密码登录 |
| 📝 注册 | `/register` | 一键加入大家庭 |
| 👤 个人主页 | `/profile/:id` | 资料卡 + 动态时间线 + 插件入口 |
| 💬 聊天 | `/chat` & `/chat/:roomId` | 私聊 / 群聊 |
| 🤝 好友 | `/friends` | 好友列表 + 申请管理 |
| 🔔 通知 | `/notifications` | 所有通知汇总 |
| 🏕️ 小组 | `/groups` & `/groups/:id` | 兴趣圈子 |
| ⚙️ 设置 | `/settings` | 个人资料编辑 |
| 🔌 默契问答 | `/profile/:id/plugins/quiz` | 出题答题 |
| 📬 匿名提问箱 | `/profile/:id/plugins/question-box` | 匿名 Q&A |
| 🛡️ 管理后台 | `/admin/*` | 7 个管理子页面 |

---

## 🤝 如何贡献

1. 本项目的开发分支为 `UIUX`
2. 提交前请确保 `npm run build` 通过
3. 代码风格请遵循项目中既有的约定（Vue 3 Composition API、Tailwind 设计系统类等）

更详细的内容请看 `Plans/03-开发协作规范.md` ✨

---

## 📄 许可证

[MIT](./LICENSE) © 2026 RL-RedLeaf

---

<p align="center">
  用 🍁 秋叶的温暖，连接每一份友谊 ✨
</p>
