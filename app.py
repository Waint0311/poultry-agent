"""
兽医康康 - 禽病问诊AI助手
Streamlit Cloud 部署版本 - 优化版
"""

import streamlit as st
import pandas as pd

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
    /* 主样式 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 标题样式 */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #11998e, #38ef7d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* 报告卡片样式 */
    .report-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: none;
    }
    
    .report-title {
        color: #11998e;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #11998e;
        padding-bottom: 0.5rem;
    }
    
    .report-section {
        margin: 1.2rem 0;
        padding: 1rem;
        background: #f8fffe;
        border-radius: 10px;
        border-left: 4px solid #11998e;
    }
    
    .report-section h4 {
        color: #11998e;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    /* 紧急警告样式 */
    .emergency-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(255,107,107,0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .emergency-title {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .emergency-list {
        background: rgba(255,255,255,0.2);
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    
    .emergency-list li {
        margin: 0.8rem 0;
        font-size: 1.1rem;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(90deg, #11998e, #38ef7d);
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.8rem 2rem;
        border-radius: 30px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(17,153,142,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(17,153,142,0.4);
    }
    
    /* 示例按钮样式 */
    .example-btn {
        background: white !important;
        color: #11998e !important;
        border: 2px solid #11998e !important;
        font-size: 1rem !important;
        margin: 0.5rem 0 !important;
        transition: all 0.3s ease !important;
    }
    
    .example-btn:hover {
        background: #11998e !important;
        color: white !important;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #11998e;
        box-shadow: 0 0 0 3px rgba(17,153,142,0.1);
    }
    
    /* 信息框样式 */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    /* 底部样式 */
    .footer {
        text-align: center;
        padding: 2rem;
        color: white;
        font-size: 0.9rem;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
    }
    
    .footer-links span {
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 20px;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .sub-header {
            font-size: 1rem;
        }
    }
    
    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 加载动画 */
    .spinner {
        border: 4px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top: 4px solid #11998e;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# ==================== 初始化 session_state ====================
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.poultry_type = "鸡（蛋鸡）"
    st.session_state.age = ""
    st.session_state.bird_count = ""
    st.session_state.death_count = ""
    st.session_state.symptoms = ""

# ==================== 主界面 ====================
st.markdown('<h1 class="main-header">🐔 兽医康康</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">面向基层养殖户的智能禽病问诊助手</p>', unsafe_allow_html=True)

# 免责声明
st.markdown("""
<div class="info-box">
    <strong>⚠️ 免责声明：</strong>本AI仅供参考，不能替代执业兽医现场诊断。紧急情况请立即联系当地畜牧兽医站或拨打<strong>12316</strong>。
</div>
""", unsafe_allow_html=True)

# ==================== 输入区域 ====================
st.markdown("## 📝 请填写病禽信息")

col1, col2 = st.columns([1, 1])

with col1:
    poultry_type = st.selectbox(
        "🐤 禽类品种",
        ["鸡（蛋鸡）", "鸡（肉鸡）", "鸡（土鸡/种鸡）", "鸭（蛋鸭）", "鸭（肉鸭/番鸭）", "鹅", "鸽/鹌鹑"],
        index=["鸡（蛋鸡）", "鸡（肉鸡）", "鸡（土鸡/种鸡）", "鸭（蛋鸭）", "鸭（肉鸭/番鸭）", "鹅", "鸽/鹌鹑"].index(st.session_state.poultry_type) if st.session_state.poultry_type in ["鸡（蛋鸡）", "鸡（肉鸡）", "鸡（土鸡/种鸡）", "鸭（蛋鸭）", "鸭（肉鸭/番鸭）", "鹅", "鸽/鹌鹑"] else 0
    )
    age = st.text_input("📅 日龄/阶段", placeholder="例如：30天、2个月、产蛋期", value=st.session_state.age)
    bird_count = st.text_input("🐔 群体规模", placeholder="例如：200只、500只", value=st.session_state.bird_count)

with col2:
    symptoms = st.text_area(
        "🔍 主要症状",
        placeholder="请描述症状，例如：拉血便、精神不好、不吃料、呼吸道异常等",
        height=120,
        value=st.session_state.symptoms
    )
    death_count = st.text_input("💀 已死亡数量", placeholder="如果没有死亡请留空", value=st.session_state.death_count)

# 提交按钮
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("🔍 开始问诊", use_container_width=True):
        
        # 保存到 session_state
        st.session_state.poultry_type = poultry_type
        st.session_state.age = age
        st.session_state.bird_count = bird_count
        st.session_state.death_count = death_count
        st.session_state.symptoms = symptoms
        
        # 群体死亡检测 - 最高优先级
        if death_count and death_count.isdigit() and int(death_count) > 0:
            st.markdown("""
            <div class="emergency-box">
                <div class="emergency-title">
                    🚨 紧急提示 - 疑似重大动物疫病
                </div>
                <p style="font-size: 1.2rem; margin-bottom: 1rem;">
                    <strong>检测到群体死亡事件，请立即采取以下措施：</strong>
                </p>
                <ol class="emergency-list">
                    <li>📞 立即拨打 <strong>12316</strong> 上报当地畜牧兽医站</li>
                    <li>🚫 <strong>不要移动</strong>病死禽</li>
                    <li>💀 进行<strong>深埋无害化处理</strong></li>
                    <li>🧴 对全场进行<strong>严格消毒</strong></li>
                    <li>🔒 <strong>禁止销售</strong>病死禽及产品</li>
                    <li>🚧 必要时进行<strong>隔离封锁</strong></li>
                </ol>
                <hr style="border-color: rgba(255,255,255,0.3); margin: 1.5rem 0;">
                <p style="font-size: 1.1rem;">
                    <strong>📞 紧急联系方式：</strong><br>
                    • 全国农业系统服务热线：<strong>12316</strong><br>
                    • 当地畜牧兽医站（请查询当地电话）
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # 正常问诊
        elif symptoms:
            st.markdown("""
            <div class="report-card">
                <div class="report-title">🐔 禽病初诊报告卡</div>
                
                <div class="report-section">
                    <h4>📋 病禽基本信息</h4>
                    <ul style="list-style: none; padding-left: 0;">
                        <li><strong>品种：</strong>{poultry_type}</li>
                        <li><strong>日龄/阶段：</strong>{age if age else '未提供'}</li>
                        <li><strong>群体规模：</strong>{bird_count if bird_count else '未提供'}</li>
                    </ul>
                </div>
                
                <div class="report-section">
                    <h4>🔍 初步判断</h4>
                    <p>根据您描述的<strong>"{symptoms}"</strong>，为了更准确诊断，请帮我确认以下信息：</p>
                </div>
                
                <div class="report-section">
                    <h4>❓ 请回答以下问题</h4>
                    <ol>
                        <li><strong>粪便形态：</strong>水样便 / 糊状便 / 带血便 / 绿色便？</li>
                        <li><strong>精神状态：</strong>正常 / 精神差 / 不吃不喝？</li>
                        <li><strong>鸡冠颜色：</strong>正常 / 苍白 / 发紫？</li>
                        <li><strong>传播情况：</strong>周围其他禽类有同样症状吗？</li>
                    </ol>
                </div>
                
                <div class="report-section" style="background: #fff3cd; border-left-color: #ffc107;">
                    <h4>💡 温馨提示</h4>
                    <p>回复以上问题，我将为您提供更准确的诊断建议和用药参考。</p>
                </div>
            </div>
            """.format(poultry_type=poultry_type, age=age, bird_count=bird_count, symptoms=symptoms))
        
        else:
            st.warning("👆 请在上方填写症状信息，然后点击'开始问诊'获取帮助")

# ==================== 快捷示例 ====================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("## 💡 快速案例（点击即可填入）")

examples = [
    ("🐔 案例1：鸡拉血便", "鸡（蛋鸡）", "28天", "200只", "3只", "拉血便，肛门羽毛沾血，采食量明显下降"),
    ("🦆 案例2：鸭神经症状", "鸭（肉鸭）", "20天", "500只", "10只", "一直摇头，像看天一样，拉绿色稀粪"),
    ("🦢 案例3：鹅腿瘫", "鹅", "3个月", "100只", "0", "有几只腿站不起来，出现瘫痪"),
]

cols = st.columns(3)
for i, (title, pt, a, bc, dc, s) in enumerate(examples):
    with cols[i]:
        if st.button(title, key=f"example_{i}", use_container_width=True):
            st.session_state.poultry_type = pt
            st.session_state.age = a
            st.session_state.bird_count = bc
            st.session_state.death_count = dc
            st.session_state.symptoms = s
            st.rerun()

# ==================== 底部信息 ====================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <h3>📚 知识库来源</h3>
    <p>基于 ima《禽病》Avian Disease 禽病知识库</p>
    
    <div class="footer-links">
        <span>🚨 群体死亡立即提示12316上报</span>
        <span>💊 食品动物用药必填休药期</span>
        <span>⚠️ 处方药不给具体剂量</span>
    </div>
    
    <hr style="border-color: rgba(255,255,255,0.3); margin: 2rem 0;">
    
    <p><strong>🔒 安全说明</strong></p>
    <p>本AI仅供参考，不能替代执业兽医现场诊断</p>
    <p style="margin-top: 1rem; opacity: 0.7;">
        Made with ❤️ for poultry farmers | 2026
    </p>
</div>
""", unsafe_allow_html=True)
