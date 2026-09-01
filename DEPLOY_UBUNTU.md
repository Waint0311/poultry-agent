# 🚀 兽医康康 Web 应用 - Ubuntu 部署指南（面向大众）

> 养殖户通过浏览器访问，无需安装任何软件。
> 架构：Streamlit Web 应用 + Ollama 本地模型 + ima 知识库

---

## 一、架构总览

```
养殖户（手机/电脑浏览器）
        │
        ▼
Ubuntu 服务器 :8501
├── Streamlit Web 应用（app.py）
│     ├── 调 Ollama（localhost:11434）→ 本地模型生成诊断
│     └── 调 ima 知识库 API → 检索《禽病》教材依据
└── Ollama 服务（systemd 自启）
```

**数据链路**：全程在你的服务器本地，不出公网 ✅

---

## 二、服务器准备

### 1. 安装 Python 依赖

```bash
cd /opt/poultry-agent
pip3 install -r requirements.txt --break-system-packages
```

### 2. 配置环境变量

```bash
cp .env.example .env
nano .env
```

```ini
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:4b
TEMPERATURE=0.2
IMA_CLIENT_ID=你的ClientId
IMA_API_KEY=你的ApiKey
```

加载：
```bash
set -a && source .env && set +a
```

### 3. 确认 Ollama 正常

```bash
curl http://localhost:11434/api/tags   # 返回模型列表 ✅
```

---

## 三、启动 Web 应用

### 方式A：直接运行（测试用）

```bash
cd /opt/poultry-agent
OLLAMA_URL=http://localhost:11434 OLLAMA_MODEL=qwen3.5:4b \
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

浏览器访问：`http://服务器IP:8501`

### 方式B：systemd 服务（推荐，开机自启）

创建服务文件 `/etc/systemd/system/poultry-agent.service`：

```ini
[Unit]
Description=Veterinary KangKang Web App
After=network.target ollama.service

[Service]
Type=simple
User=tzu
WorkingDirectory=/opt/poultry-agent
Environment=OLLAMA_URL=http://localhost:11434
Environment=OLLAMA_MODEL=qwen3.5:4b
Environment=IMA_CLIENT_ID=你的ClientId
Environment=IMA_API_KEY=你的ApiKey
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启用：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now poultry-agent
systemctl status poultry-agent
```

---

## 四、防火墙开放端口

```bash
sudo ufw allow 8501/tcp
```

---

## 五、（可选）配置域名 + HTTPS

推荐用 **Nginx 反向代理 + Caddy 自动 HTTPS**（Caddy 更简单）：

```bash
# 安装 Caddy
sudo apt install -y caddy

# 配置 /etc/caddy/Caddyfile
nano /etc/caddy/Caddyfile
```

```caddyfile
poultry.example.com {
    reverse_proxy localhost:8501
}
```

```bash
sudo systemctl restart caddy
```

之后用户访问 `https://poultry.example.com` 即可（自动 HTTPS）。

---

## 六、验证

1. 浏览器打开 `http://服务器IP:8501`
2. 测试用例：
   - 蛋鸡 28 天拉血便 → 应输出报告卡 + 📚出处 + 休药期
   - 死亡数量 > 0 → 应触发 12316 紧急提示（不走模型，秒出）
3. 手机访问同一地址，检查移动端显示

---

## 七、常见问题

| 问题 | 解决 |
|------|------|
| 页面显示"模型服务未连接" | 检查 `curl localhost:11434/api/tags`、`systemctl status ollama` |
| 提问很慢/超时 | 确认已关思考模式（代码已内置）；换更大显存模型或减小 num_ctx |
| 模型回答质量差 | 换 `qwen3.5:9b` 或 `qwen3:14b`（`OLLAMA_MODEL` 修改即可）|
| 想用系统 Prompt v4 | 放一个 `system_prompt.txt` 到应用目录，自动覆盖内置 v3 |

---

## 八、比赛材料参考（数据安全表述）

> **模型与数据私有化部署**：产品支持将大模型（Ollama）与业务数据完全部署在自有服务器，养殖户问诊数据不出内网；Web 应用形态面向大众开放，扫码即用，无需安装。
