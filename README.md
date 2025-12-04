# 舆情分析系统

舆情分析系统 - 一个用于分析和管理舆情信息的Web应用程序

## 项目结构

```
├── app/                 # 应用程序主目录
├── templates/           # HTML模板文件
├── static/              # 静态资源文件（CSS、JavaScript、图片等）
├── migrations/          # 数据库迁移文件
├── tests/               # 测试文件
├── requirements.txt     # 项目依赖项
├── run.py               # 应用程序入口文件
└── README.md            # 项目说明文档
```

## 安装步骤

1. 克隆或下载项目到本地
2. 安装项目依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 运行项目

```bash
python run.py
```

应用程序将在 http://localhost:5000 启动

## 依赖项

- Flask: Web框架
- Flask-SQLAlchemy: 数据库ORM
- Flask-Migrate: 数据库迁移管理
- Flask-WTF: 表单处理
- python-dotenv: 环境变量管理

## 使用说明

1. 启动应用程序后，在浏览器中访问 http://localhost:5000
2. 根据页面提示进行操作

## 开发说明

- 开发环境下，Debug模式已启用
- 数据库默认使用SQLite
- 可以通过修改app目录下的配置文件来更改数据库连接

## 测试

```bash
python -m pytest tests/
```
