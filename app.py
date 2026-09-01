"""
兽医康康 - 禽病问诊AI助手
Web 应用版：Streamlit + Ollama 本地模型 + ima 知识库
部署：Ubuntu 服务器（模型同机调用 localhost）
"""

import os
import requests
import streamlit as st

from system_prompt import SYSTEM_PROMPT_V3
from ima_client import search_ima_multi

# ==================== 配置（环境变量） ====================
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
# 可选：用外部文件覆盖系统提示词（放 system_prompt.txt 即可，方便迭代 v4）
SYSTEM_PROMPT = SYSTEM_PROMPT_V3
if os.path.exists("system_prompt.txt"):
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()

# ==================== Ollama 调用 ====================
# 局域网直连，禁用系统代理（Mac 代理软件会拦截局域网请求）
NO_PROXY = {"http": None, "https": None}


def ollama_available() -> bool:
    """检测 Ollama 服务是否可达"""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3, proxies=NO_PROXY)
        return r.status_code == 200
    except Exception:
        return False


def chat_with_ollama(user_text: str, history: list) -> str:
    """调用 Ollama 生成回答（带系统提示词 + 最近对话历史）"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # 保留最近 8 条对话（4 轮），避免超出上下文
    for msg in history[-8:]:
        if msg.get("role") in ("user", "assistant"):
            messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_text})

    resp = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "think": False,  # 关闭思考模式（qwen3.5 默认思考，会超长超时）
            "options": {"temperature": TEMPERATURE, "num_ctx": 8192},
        },
        timeout=600,
        proxies=NO_PROXY,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def build_consultation(user_text: str) -> str:
    """组装问诊文本：先检索 ima 知识库，把命中文档作为上下文"""
    # 用"主要症状"部分作为检索词（命中率更高）
    query = user_text
    if "【主要症状】" in user_text:
        query = user_text.split("【主要症状】")[-1].strip()
    kb_hits = search_ima_multi(query)
    if kb_hits:
        return (
            "【知识库检索结果（以下文档来自 ima《禽病》知识库，请在回答中优先参考并标注出处）】\n"
            f"{kb_hits}\n\n"
            f"【用户问诊】\n{user_text}"
        )
    return user_text


# ==================== 页面配置 ====================
st.set_page_config(
    page_title="兽医康康 - 禽病问诊AI助手",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== 自定义样式 ====================
st.markdown("""
<style>
    .stApp { background: white; }

    .header { text-align: center; padding: 1.5rem 0; border-bottom: 1px solid #e5e7eb; margin-bottom: 1rem; }
    .header h1 { font-size: 2rem; color: #1f2937; margin: 0; font-weight: 700; }
    .header p { color: #6b7280; font-size: 1rem; margin: 0.5rem 0 0 0; }

    .user-message {
        background: #10b981; color: white; padding: 1rem 1.5rem;
        border-radius: 1rem 1rem 0.25rem 1rem; margin: 1rem 0;
        max-width: 80%; margin-left: auto; font-size: 1rem; line-height: 1.6;
    }
    .assistant-message {
        background: #f3f4f6; color: #1f2937; padding: 1rem 1.5rem;
        border-radius: 1rem 1rem 1rem 0.25rem; margin: 1rem 0;
        max-width: 80%; font-size: 1rem; line-height: 1.6;
    }
    .emergency-message {
        background: #fef2f2; border: 2px solid #ef4444; color: #991b1b;
        padding: 1.5rem; border-radius: 1rem; margin: 1rem 0;
    }
    .emergency-message h3 { color: #dc2626; margin-top: 0; }

    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border: 2px solid #e5e7eb; border-radius: 0.5rem;
        padding: 0.6rem 0.8rem; font-size: 0.95rem;
    }
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #10b981; box-shadow: 0 0 0 3px rgba(16,185,129,0.1);
    }
    .stTextArea > div > div > textarea {
        border: 2px solid #e5e7eb; border-radius: 0.5rem;
        padding: 0.6rem 0.8rem; font-size: 0.95rem; height: 120px;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #10b981; box-shadow: 0 0 0 3px rgba(16,185,129,0.1);
    }

    .stButton > button {
        background: #10b981; color: white; border: none; border-radius: 0.5rem;
        padding: 0.75rem 1.5rem; font-size: 1rem; font-weight: 600; transition: all 0.2s;
    }
    .stButton > button:hover { background: #059669; }

    .stButton[key^="example_"] > button {
        background: white; color: #10b981; border: 2px solid #10b981;
        font-size: 0.9rem; padding: 0.5rem 1rem;
    }
    .stButton[key^="example_"] > button:hover { background: #10b981; color: white; }

    .bottom-bar {
        position: fixed; bottom: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, #10b981, #34d399, #10b981);
        background-size: 200% 100%; animation: gradient-flow 3s ease infinite;
    }
    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .disclaimer {
        background: #fef3c7; border-left: 4px solid #f59e0b; padding: 0.75rem 1rem;
        margin: 0.5rem 0; border-radius: 0 0.5rem 0.5rem 0; font-size: 0.9rem;
    }
    .model-status {
        text-align: center; color: #9ca3af; font-size: 0.8rem; padding: 0.5rem;
    }

    .element-container { margin: 0.5rem 0; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    @media (max-width: 768px) {
        .header h1 { font-size: 1.5rem; }
        .user-message, .assistant-message { max-width: 95%; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== 初始化 session_state ====================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # [{role, content}]

# ==================== 头部 ====================
st.markdown("""
<div class="header">
    <h1>🐔 兽医康康</h1>
    <p>您的智能禽病问诊助手</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    ⚠️ <strong>免责声明：</strong>本AI仅供参考，不能替代执业兽医现场诊断。紧急情况请立即拨打<strong>12316</strong>。
</div>
""", unsafe_allow_html=True)

# ==================== 第1部分：禽病信息 ====================
st.markdown("## 📝 填写病禽信息")

col1, col2 = st.columns([1, 1])

with col1:
    poultry_type = st.selectbox(
        "🐤 禽类品种",
        ["鸡（蛋鸡）", "鸡（肉鸡）", "鸡（土鸡/种鸡）", "鸭（蛋鸭）", "鸭（肉鸭/番鸭）", "鹅", "鸽/鹌鹑"]
    )
    age = st.text_input("📅 日龄/阶段", placeholder="例如：30天、2个月、产蛋期")

with col2:
    bird_count = st.text_input("🐔 群体规模", placeholder="例如：200只、500只")
    death_count = st.text_input("💀 已死亡数量", placeholder="如果没有死亡请留空")

# ==================== 第2部分：问诊记录 ====================
st.markdown("---")
st.markdown("### 💬 问诊记录")

# 显示问诊记录
if st.session_state.chat_history:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        elif msg["role"] == "emergency":
            st.markdown(f'<div class="emergency-message">{msg["content"]}</div>', unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(
                f'<div class="assistant-message">🤖 <strong>兽医康康：</strong><br><br>'
                f'{msg["content"].replace(chr(10), "<br>")}</div>',
                unsafe_allow_html=True
            )
else:
    st.info("👆 请在下方填写主要症状后点击'开始问诊'")

st.markdown("<br>", unsafe_allow_html=True)

# ==================== 主要症状 + 按钮（并行） ====================
col_symptoms, col_button = st.columns([4, 1])

with col_symptoms:
    symptoms = st.text_area(
        "🔍 主要症状",
        placeholder="请描述症状，例如：拉血便、精神不好、不吃料等"
    )

with col_button:
    st.markdown("<br>" * 3, unsafe_allow_html=True)
    submitted = st.button("🔍 开始问诊", use_container_width=True)

# ==================== 处理问诊 ====================
if submitted:
    # ---- 紧急规则（最高优先级，不依赖模型）----
    if death_count and death_count.isdigit() and int(death_count) > 0:
        emergency_html = (
            "<h3>🚨 紧急提示 - 疑似重大动物疫病</h3>"
            f"<p><strong>检测到群体死亡事件（{death_count}只），请立即采取以下措施：</strong></p>"
            "<ol style='margin:1rem 0; padding-left:1.5rem;'>"
            "<li>📞 立即拨打 <strong>12316</strong> 上报当地畜牧兽医站</li>"
            "<li>🚫 不要移动病死禽</li>"
            "<li>💀 深埋无害化处理</li>"
            "<li>🧴 对全场进行严格消毒</li>"
            "<li>🔒 禁止销售病死禽及产品</li>"
            "</ol>"
        )
        st.session_state.chat_history.append({"role": "user", "content": f"我家的{poultry_type}出问题了，死亡{death_count}只..."})
        st.session_state.chat_history.append({"role": "emergency", "content": emergency_html})
        st.rerun()

    elif symptoms:
        # 组装用户文本（含表单信息）
        user_text = (
            f"【病禽信息】品种：{poultry_type}；日龄/阶段：{age if age else '未提供'}；"
            f"群体规模：{bird_count if bird_count else '未提供'}；已死亡：{death_count if death_count else '0'}只。\n"
            f"【主要症状】{symptoms}"
        )
        st.session_state.chat_history.append({"role": "user", "content": user_text})

        with st.spinner("🔍 兽医康康正在检索知识库并分析..."):
            try:
                if not ollama_available():
                    raise RuntimeError(f"无法连接模型服务（{OLLAMA_URL}），请检查 Ollama 是否运行")
                prompt = build_consultation(user_text)
                answer = chat_with_ollama(prompt, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"⚠️ 模型服务暂时不可用：{e}\n\n请确认 Ubuntu 上的 Ollama 已启动（`ollama serve`），且本应用配置的 OLLAMA_URL 正确。"
                })
        st.rerun()
    else:
        st.warning("👆 请填写症状信息后开始问诊")

# ==================== 第3部分：快速案例 ====================
st.markdown("---")
st.markdown("### 💡 快速案例")
st.markdown("点击下方按钮，快速体验问诊流程：")

examples = [
    ("🐔 鸡血便案例", "鸡（蛋鸡）", "28天", "200只", "3只", "拉血便，肛门羽毛沾血，采食量下降"),
    ("🦆 鸭神经症状", "鸭（肉鸭）", "20天", "500只", "10只", "一直摇头，拉绿色稀粪"),
    ("🦢 鹅腿瘫案例", "鹅", "3个月", "100只", "0", "腿站不起来，出现瘫痪"),
]

cols = st.columns(3)
for i, (title, pt, a, bc, dc, s) in enumerate(examples):
    with cols[i]:
        if st.button(title, key=f"example_{i}"):
            user_text = f"【病禽信息】品种：{pt}；日龄/阶段：{a}；群体规模：{bc}；已死亡：{dc}只。\n【主要症状】{s}"
            st.session_state.chat_history.append({"role": "user", "content": user_text})
            with st.spinner("🔍 兽医康康正在检索知识库并分析..."):
                try:
                    if not ollama_available():
                        raise RuntimeError(f"无法连接模型服务（{OLLAMA_URL}），请检查 Ollama 是否运行")
                    prompt = build_consultation(user_text)
                    answer = chat_with_ollama(prompt, st.session_state.chat_history)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"⚠️ 模型服务暂时不可用：{e}"
                    })
            st.rerun()

# ==================== 底部 ====================
st.markdown('<div class="bottom-bar"></div>', unsafe_allow_html=True)

_ok = ollama_available()
_status = f"模型：{OLLAMA_MODEL} @ {OLLAMA_URL}" if _ok else f"⚠️ 模型服务未连接（{OLLAMA_URL}）"
st.markdown(f'<div class="model-status">{_status}</div>', unsafe_allow_html=True)
