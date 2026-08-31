# 🐔 Streamlit Cloud 部署指南

本指南将帮助你把"兽医康康 - 禽病问诊AI助手"部署到 Streamlit Cloud。

## 📋 前期准备

### 必需工具

- ✅ GitHub 账号
- ✅ 本地已安装 Git
- ✅ Python 3.11+

### 检查项目文件

确保你的项目包含以下文件：

```
poultry-agent/
├── app.py                  # ✅ Streamlit 主应用
├── requirements.txt        # ✅ 依赖文件
├── .streamlit/
│   └── config.toml        # ✅ Streamlit 配置
├── README.md               # ✅ 项目说明
├── .gitignore              # ✅ Git 忽略文件
└── 其他支持文件...
```

---

## 🚀 部署步骤

### 第一步：创建 GitHub 仓库

1. **登录 GitHub**
   - 打开 [github.com](https://github.com)
   - 登录你的账号

2. **创建新仓库**
   - 点击右上角 **"+"** → **"New repository"**
   - 填写信息：
     ```
     Repository name: poultry-agent
     Description: 兽医康康 - 禽病问诊AI助手
     Visibility: Public ☑️（必选）
     ```
   - 点击 **"Create repository"**

3. **获取仓库地址**
   - 创建成功后，复制仓库地址：
     ```
     https://github.com/YOUR_USERNAME/poultry-agent.git
     ```

### 第二步：初始化本地 Git 仓库

在**你的电脑**上打开终端（Terminal），执行：

```bash
# 1. 进入项目目录
cd /path/to/your/poultry-agent

# 2. 初始化 Git
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial commit: 兽医康康禽病问诊AI助手 v1.0"

# 5. 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/poultry-agent.git

# 6. 推送代码
git branch -M main
git push -u origin main
```

### 第三步：部署到 Streamlit Cloud

1. **访问 Streamlit Cloud**
   - 打开 [share.streamlit.io](https://share.streamlit.io)
   - 点击 **"Sign up"** 或 **"Login"**
   - 使用 **GitHub 账号登录**

2. **授权 GitHub 访问**（首次使用）
   - 在弹出窗口中授权 Streamlit Cloud 访问你的仓库

3. **创建新应用**
   - 点击 **"New app"** 按钮

4. **配置部署**
   - 在配置页面填写：
     ```
     Repository: YOUR_USERNAME/poultry-agent
     Branch: main
     Main file path: app.py
     ```

5. **高级设置（可选）**
   - 点击 **"Advanced settings"**：
     - Python version: `3.11`
     - Secrets: 如果需要 API key，在这里添加

6. **部署！**
   - 点击 **"Deploy!"** 按钮
   - 等待 2-3 分钟部署完成

### 第四步：访问你的应用

部署成功后，你会获得一个 URL：
```
https://YOUR_USERNAME-poultry-agent.streamlit.app
```

🎉 **恭喜！你的应用已经上线！**

---

## 🔄 更新和重新部署

每次修改代码后：

```bash
# 1. 添加修改的文件
git add .

# 2. 提交
git commit -m "更新描述"

# 3. 推送到 GitHub
git push
```

**Streamlit Cloud 会自动检测到更新并重新部署！**

---

## ⚙️ 配置环境变量（可选）

如果你的应用需要 API keys 或其他密钥：

1. 在 Streamlit Cloud 的 **Advanced settings** 中添加：
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

2. 在代码中读取：
   ```python
   import os
   api_key = os.getenv("OPENAI_API_KEY")
   ```

---

## 🆘 常见问题排查

### ❌ 部署失败

**问题**: 部署时显示错误

**解决方案**:
1. 检查 `requirements.txt` 是否正确
2. 查看 Streamlit Cloud 的部署日志
3. 确保代码没有语法错误
4. 本地测试：`streamlit run app.py`

### ❌ 应用空白

**问题**: 页面加载但没有内容

**解决方案**:
1. 检查浏览器控制台错误
2. 查看 Streamlit Cloud 日志
3. 确保所有依赖都写在 `requirements.txt` 中

### ❌ GitHub 仓库访问错误

**问题**: Streamlit Cloud 无法访问仓库

**解决方案**:
1. 确保仓库是 **Public**
2. 在 Streamlit Cloud 设置中重新授权 GitHub
3. 检查仓库名称是否正确

### ❌ 依赖安装失败

**问题**: requirements.txt 中的包无法安装

**解决方案**:
1. 检查包名和版本是否正确
2. 移除不必要的依赖
3. 使用更稳定的版本号

---

## 💡 性能优化建议

### 1. 减少依赖

只安装必要的包：
```txt
streamlit>=1.28.0
pandas>=2.0.0
```

### 2. 优化代码

- 避免在主线程中进行耗时操作
- 使用 `@st.cache` 缓存数据
- 尽量减少 API 调用

### 3. Streamlit Cloud 限制

- **免费版**: CPU 有限制，适合轻量应用
- **睡眠模式**: 7天无访问会自动休眠
- **带宽限制**: 免费版有流量限制

---

## 🌐 自定义域名（可选）

Streamlit Cloud 免费版不支持自定义域名。

如需自定义域名，需要升级到付费计划。

---

## 📞 获取帮助

- 📖 [Streamlit 官方文档](https://docs.streamlit.io/)
- 💬 [Streamlit 社区](https://discuss.streamlit.io/)
- 🐛 [GitHub Issues](https://github.com/streamlit/streamlit/issues)

---

## ✅ 部署检查清单

部署前确认：

- [ ] GitHub 仓库已创建且为 Public
- [ ] `app.py` 文件存在且可运行
- [ ] `requirements.txt` 包含所有依赖
- [ ] `.streamlit/config.toml` 配置正确
- [ ] `README.md` 已更新
- [ ] `.gitignore` 已创建
- [ ] 本地测试通过

---

**祝你部署成功！🎉**
