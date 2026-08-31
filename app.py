"""
兽医康康 - 禽病问诊AI助手
简约对话式设计 - HuggingFace 风格
"""

import streamlit as st

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
    /* 重置默认样式 */
    .stApp {
        background: white;
    }
    
    /* 主容器 */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        min-height: 100vh;
    }
    
    /* 头部标题 */
    .header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    
    .header h1 {
        font-size: 2.5rem;
        color: #1f2937;
        margin: 0;
        font-weight: 700;
    }
    
    .header p {
        color: #6b7280;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* 对话气泡 - 用户 */
    .user-message {
        background: #10b981;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 1rem 1rem 0.25rem 1rem;
        margin: 1rem 0;
        max-width: 85%;
        margin-left: auto;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* 对话气泡 - 助手 */
    .assistant-message {
        background: #f3f4f6;
        color: #1f2937;
        padding: 1rem 1.5rem;
        border-radius: 1rem 1rem 1rem 0.25rem;
        margin: 1rem 0;
        max-width: 85%;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* 紧急提示气泡 */
    .emergency-message {
        background: #fef2f2;
        border: 2px solid #ef4444;
        color: #991b1b;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    
    .emergency-message h3 {
        color: #dc2626;
        margin-top: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .emergency-message ol {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    
    .emergency-message li {
        margin: 0.5rem 0;
    }
    
    /* 输入区域 */
    .input-section {
        background: white;
        border-top: 1px solid #e5e7eb;
        padding: 1.5rem;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        box-shadow: 0 -4px 6px -1px rgba(0,0,0,0.1);
    }
    
    .input-box {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 2px solid #e5e7eb;
        border-radius: 0.75rem;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: border-color 0.2s;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16,185,129,0.1);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: #10b981;
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.2s;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #059669;
        transform: translateY(-1px);
    }
    
    /* 底部装饰条 */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #10b981, #34d399, #10b981);
        background-size: 200% 100%;
        animation: gradient-flow 3s ease infinite;
    }
    
    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* 示例按钮 */
    .example-btn {
        background: white !important;
        color: #10b981 !important;
        border: 2px solid #10b981 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1rem !important;
        margin: 0.25rem !important;
        border-radius: 0.5rem !important;
    }
    
    .example-btn:hover {
        background: #10b981 !important;
        color: white !important;
    }
    
    /* 免责声明 */
    .disclaimer {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 0.5rem 0.5rem 0;
        font-size: 0.9rem;
    }
    
    /* 报告卡 */
    .report-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .report-card h4 {
        color: #10b981;
        margin-top: 0;
        border-bottom: 2px solid #10b981;
        padding-bottom: 0.5rem;
    }
    
    /* 间距调整 */
    .element-container {
        margin: 0.5rem 0;
    }
    
    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* 空状态提示 */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #9ca3af;
    }
    
    .empty-state h3 {
        color: #6b7280;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 初始化 session_state ====================
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = True

# ==================== 头部 ====================
st.markdown("""
<div class="header">
    <h1>🐔 兽医康康</h1>
    <p>您的智能禽病问诊助手</p>
</div>
""", unsafe_allow_html=True)

# ==================== 免责声明 ====================
st.markdown("""
<div class="disclaimer">
    ⚠️ <strong>免责声明：</strong>本AI仅供参考，不能替代执业兽医现场诊断。紧急情况请立即拨打<strong>12316</strong>。
</div>
""", unsafe_allow_html=True)

# ==================== 输入表单 ====================
with st.form(key="consultation_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    
    with col1:
        poultry_type = st.selectbox(
            "🐤 禽类品种",
            ["鸡（蛋鸡）", "鸡（肉鸡）", "鸡（土鸡/种鸡）", "鸭（蛋鸭）", "鸭（肉鸭/番鸭）", "鹅", "鸽/鹌鹑"]
        )
        age = st.text_input("📅 日龄/阶段", placeholder="例如：30天、2个月、产蛋期")
        bird_count = st.text_input("🐔 群体规模", placeholder="例如：200只、500只")
    
    with col2:
        symptoms = st.text_area(
            "🔍 主要症状",
            placeholder="请描述症状，例如：拉血便、精神不好、不吃料等",
            height=100
        )
        death_count = st.text_input("💀 已死亡数量", placeholder="如果没有死亡请留空")
    
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 开始问诊")

# ==================== 处理问诊逻辑 ====================
if submitted:
    # 检测群体死亡 - 紧急情况
    if death_count and death_count.isdigit() and int(death_count) > 0:
        st.session_state.chat_history.append({
            "type": "user",
            "content": f"我家的{poultry_type}出问题了，死亡{death_count}只..."
        })
        st.session_state.chat_history.append({
            "type": "emergency",
            "content": {
                "title": "🚨 紧急提示 - 疑似重大动物疫病",
                "message": f"检测到群体死亡事件（{death_count}只），请立即采取以下措施：",
                "steps": [
                    "📞 立即拨打 12316 上报当地畜牧兽医站",
                    "🚫 不要移动病死禽",
                    "💀 深埋无害化处理",
                    "🧴 对全场进行严格消毒",
                    "🔒 禁止销售病死禽及产品"
                ]
            }
        })
    
    # 正常问诊
    elif symptoms:
        st.session_state.chat_history.append({
            "type": "user",
            "content": f"{poultry_type}，{age if age else '日龄不详'}，{bird_count if bird_count else '规模不详'}，症状：{symptoms}"
        })
        
        # 生成初步回复
        response = f"""根据您描述的情况：

**📋 病禽信息**
- 品种：{poultry_type}
- 日龄/阶段：{age if age else '未提供'}
- 群体规模：{bird_count if bird_count else '未提供'}

**🔍 初步分析**
您描述的症状：{symptoms}

**❓ 为更准确诊断，请确认：**
1. 粪便形态：水样便 / 糊状便 / 带血便 / 绿色便？
2. 精神状态：正常 / 精神差 / 不吃不喝？
3. 鸡冠颜色：正常 / 苍白 / 发紫？
4. 传播情况：周围其他禽类有同样症状吗？

请回复以上问题，我将为您提供更准确的诊断建议。"""

        st.session_state.chat_history.append({
            "type": "assistant",
            "content": response
        })
    else:
        st.info("👆 请填写症状信息后开始问诊")

# ==================== 显示对话历史 ====================
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 💬 问诊记录")
    
    for i, msg in enumerate(st.session_state.chat_history):
        if msg["type"] == "user":
            st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        elif msg["type"] == "emergency":
            emergency_data = msg["content"]
            emergency_html = f"""
            <div class="emergency-message">
                <h3>{emergency_data['title']}</h3>
                <p>{emergency_data['message']}</p>
                <ol>
                    {"".join([f'<li>{step}</li>' for step in emergency_data['steps']])}
                </ol>
            </div>
            """
            st.markdown(emergency_html, unsafe_allow_html=True)
        elif msg["type"] == "assistant":
            st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)
else:
    # 空状态
    st.markdown("""
    <div class="empty-state">
        <h3>👋 您好！我是兽医康康</h3>
        <p>请在上方填写病禽信息，开始智能问诊</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== 快捷示例 ====================
st.markdown("---")
st.markdown("### 💡 快速案例")
st.markdown("点击即可自动填入：")

examples = [
    ("🐔 鸡血便", "鸡（蛋鸡）", "28天", "200只", "3只", "拉血便，肛门羽毛沾血"),
    ("🦆 鸭神经症状", "鸭（肉鸭）", "20天", "500只", "10只", "一直摇头，拉绿色稀粪"),
    ("🦢 鹅腿瘫", "鹅", "3个月", "100只", "0", "腿站不起来，出现瘫痪"),
]

cols = st.columns(3)
for i, (title, pt, a, bc, dc, s) in enumerate(examples):
    with cols[i]:
        if st.button(title, key=f"example_{i}"):
            st.session_state.chat_history = []
            st.rerun()

# ==================== 底部装饰 ====================
st.markdown('<div class="bottom-bar"></div>', unsafe_allow_html=True)
