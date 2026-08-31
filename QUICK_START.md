# 🚀 Streamlit Cloud 部署快速开始指南

## ✅ 部署包检查清单

我已经为你准备好了以下文件：

- [x] `app.py` - Streamlit 主应用
- [x] `requirements.txt` - Streamlit 依赖
- [x] `.streamlit/config.toml` - Streamlit 配置
- [x] `README.md` - 项目说明
- [x] `.gitignore` - Git 忽略文件
- [x] `DEPLOYMENT_GUIDE.md` - 详细部署指南

---

## 🎯 三步完成部署

### 第一步：创建 GitHub 仓库

1. 打开 [github.com](https://github.com) 并登录
2. 点击 **"+"** → **"New repository"**
3. 填写：
   - Repository name: `poultry-agent`
   - 选择 **Public** ☑️
4. 点击 **"Create repository"**

### 第二步：推送代码到 GitHub

在你的电脑上打开终端，执行：

```bash
# 1. 进入项目目录（替换为你的实际路径）
cd /Users/wangteng/your/path/poultry-agent

# 2. 初始化 Git
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial commit: 兽医康康禽病问诊AI助手"

# 5. 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/poultry-agent.git

# 6. 推送
git branch -M main
git push -u origin main
```

### 第三步：部署到 Streamlit Cloud

1. 打开 [share.streamlit.io](https://share.streamlit.io)
2. 使用 **GitHub 账号登录**
3. 点击 **"New app"**
4. 配置：
   - Repository: `YOUR_USERNAME/poultry-agent`
   - Branch: `main`
   - Main file path: `app.py`
5. 点击 **"Deploy!"**
6. 等待 2-3 分钟

🎉 **完成！获得你的应用 URL！**

---

## 📱 部署后访问

你的应用将获得一个类似这样的 URL：
```
https://YOUR_USERNAME-poultry-agent.streamlit.app
```

---

## 🔄 更新代码

每次修改代码后：

```bash
git add .
git commit -m "更新描述"
git push
```

**Streamlit Cloud 会自动重新部署！**

---

## 🆘 遇到问题？

### ❌ 部署失败

检查清单：
- [ ] `requirements.txt` 是否正确？
- [ ] `app.py` 是否有语法错误？
- [ ] 本地能否运行 `streamlit run app.py`？

### ❌ GitHub 访问错误

- [ ] 仓库是否为 Public？
- [ ] Streamlit Cloud 是否授权 GitHub？

### ❌ 依赖安装失败

- [ ] 包名和版本是否正确？
- [ ] 是否有版本冲突？

---

## 📚 详细文档

查看 `DEPLOYMENT_GUIDE.md` 获取完整的故障排查指南！

---

## 🌟 下一步

部署成功后，你可以：

1. **测试应用**：访问你的 URL，确保一切正常
2. **分享链接**：将链接分享给朋友或用户
3. **自定义域名**：升级到付费计划
4. **添加功能**：继续开发更多功能

---

**祝你部署成功！🐔**
