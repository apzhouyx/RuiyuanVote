<<<<<<< HEAD
# 小区投票统计系统

基于 FastAPI 和 Vue.js 的小区投票统计系统，支持实时数据同步和可视化展示。

## 功能特点

- 17栋楼动态投票进度展示
- 实时数据同步更新
- 住户自助投票功能
- 防重复投票机制
- 详细的楼栋户型管理

## 技术栈

### 后端
- Python 3.8+
- FastAPI
- MySQL
- Redis
- WebSocket

### 前端
- Vue 3
- Element Plus
- ECharts
- Vue Router
- Pinia

## 安装说明

1. 克隆项目
```bash
git clone [项目地址]
```

2. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

3. 安装前端依赖
```bash
cd frontend
npm install
```

4. 配置环境变量
复制 `.env.example` 到 `.env` 并填写相应配置

5. 启动服务
```bash
# 后端
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 前端
cd frontend
npm run dev
```

## 项目结构
```
vote/
├── backend/           # 后端代码
│   ├── app/          # 应用代码
│   ├── tests/        # 测试文件
│   └── requirements.txt
├── frontend/         # 前端代码
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
``` 
=======
# RuiyuanVote
瑞园业主投票统计系统
>>>>>>> 76f58862c372975eebea7532b40548bb27063683
