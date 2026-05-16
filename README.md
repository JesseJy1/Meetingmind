# MeetingMind 会后清单 Bot

粘贴会议记录，AI自动生成会议概览、关键决策和按角色分配的 Todo。

## 项目结构

```
meetingmind/
├── app.py              # Flask 后端
├── requirements.txt    # Python 依赖
├── Procfile            # Render 部署配置
└── templates/
    └── index.html      # 前端页面
```

## 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置 API Key（替换成你自己的）
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxx"

# 3. 启动服务
python app.py

# 4. 浏览器打开
# http://localhost:5000
```

## 部署到 Render（免费）

1. 把项目 push 到 GitHub
2. 登录 [render.com](https://render.com)，New → Web Service
3. 连接你的 GitHub 仓库
4. 在 Environment Variables 里添加 `ANTHROPIC_API_KEY`
5. 点击 Deploy，等待部署完成
6. 访问 Render 给你的链接，分享给任何人即可

## 获取 API Key

前往 [console.anthropic.com](https://console.anthropic.com) 注册并生成 API Key。
