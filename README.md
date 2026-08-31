# 🐔 兽医康康 - 禽病问诊AI助手

> 让基层养殖户也能获得专业禽病诊断服务

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=Python&logoColor=white)

## 🌟 功能特点

- 💬 **智能问诊**：基于引导式问诊，获取准确诊断建议
- 🚨 **紧急上报**：群体死亡自动触发12316上报提示
- 💊 **用药参考**：提供用药建议和休药期提醒
- 📱 **移动适配**：手机和电脑都能完美使用
- 🤖 **AI驱动**：基于禽病知识库的智能问答

## 🚀 快速开始

### 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USERNAME/poultry-agent.git
cd poultry-agent

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动应用
streamlit run app.py
```

### Streamlit Cloud 部署

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_github.svg)](https://share.streamlit.io/deploy)

1. 点击上方按钮或访问 [share.streamlit.io](https://share.streamlit.io)
2. 连接你的 GitHub 仓库
3. 点击 Deploy!

## 📖 使用指南

### 基础问诊

1. 选择禽类类型（鸡/鸭/鹅等）
2. 填写日龄/阶段
3. 描述主要症状
4. 点击"开始问诊"

### 紧急情况

当出现群体死亡时，系统会自动提示：
- 🚨 拨打 12316 紧急上报
- 🚫 不要移动病死禽
- 💀 深埋无害化处理
- 🧴 全场严格消毒

### 用药安全

所有食品动物用药建议都会包含：
- 💊 药品名称和剂量
- ⏰ 休药期提醒
- ⚠️ 处方药使用限制

## 🎯 适用人群

- 🐔 家庭养殖户
- 🏠 乡镇养禽场
- 🩺 基层兽医
- 📚 畜牧专业学生

## 🔧 技术架构

- **前端**: Streamlit
- **知识库**: ima《禽病》Avian Disease
- **AI模型**: 集成式禽病知识检索

## 📚 知识库来源

基于 ima《禽病》Avian Disease禽病知识库

包含以下权威教材：
- 《中国禽病学》（刘金华 甘孟侯主编）
- 《家禽传染病防控技术》（张洪让）
- 《鸡病鉴别诊断图谱与安全用药》
- 《AVIAN PATHOLOGY》（兽医病理彩色图谱）

## ⚠️ 免责声明

本AI仅供参考，不能替代执业兽医现场诊断。

紧急情况请立即联系当地畜牧兽医站或拨打12316。

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系我们

- 📧 Email: support@poultry-agent.example.com
- 🌐 Website: https://poultry-agent.example.com

---

**Made with ❤️ for poultry farmers**
