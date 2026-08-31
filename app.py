"""
兽医康康 - 禽病问诊AI助手
Streamlit Cloud 部署版本
"""

import streamlit as st
import pandas as pd

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="兽医康康 - 禽病问诊AI助手",
    page_icon="🐔",
    layout="wide"
)

# ==================== 自定义样式 ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #11998e;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .report-box {
        background-color: #f0fdf4;
        border-left: 5px solid #11998e;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .warning-box {
        background-color: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .stButton>button {
        background-color: #11998e;
        color: white;
        font-size: 1.1rem;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0d7c6f;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 主界面 ====================
st.markdown('<p class="main-header">🐔 兽医康康</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">面向基层养殖户的智能禽病问诊助手</p>', unsafe_allow_html=True)

# 免责声明
st.warning("⚠️ 免责声明：本AI仅供参考，不能替代执业兽医现场诊断。紧急情况请立即联系当地畜牧兽医站或拨打12316。")

# ==================== 输入区域 ====================
st.markdown("### 📝 请填写病禽信息")

col1, col2 = st.columns(2)

with col1:
    poultry_type = st.selectbox(
        "🐤 禽类",
        ["鸡（蛋鸡）", "鸡（肉鸡）", "鸡（土鸡/种鸡）", "鸭（蛋鸭）", "鸭（肉鸭/番鸭）", "鹅", "鸽/鹌鹑"]
    )
    age = st.text_input("📅 日龄/阶段", placeholder="如：30天、2个月、产蛋期")
    bird_count = st.text_input("🐔 群体规模", placeholder="如：200只、500只")

with col2:
    symptoms = st.text_area(
        "🔍 主要症状",
        placeholder="请描述症状，如：拉血便、精神不好、不吃料、呼吸道异常等",
        height=100
    )
    death_count = st.text_input("💀 已死亡数量", placeholder="如果没有死亡请留空")

# 提交按钮
st.markdown("---")
if st.button("🔍 开始问诊", use_container_width=True):
    
    # 群体死亡检测 - 最高优先级
    if death_count and death_count.isdigit() and int(death_count) > 0:
        st.markdown("""
        <div class="warning-box">
            <h2>🚨 紧急提示</h2>
            <p><strong>这是疑似重大动物疫病！</strong></p>
            <p>请立即执行以下操作：</p>
            <ol>
                <li>📞 拨打 <strong>12316</strong> 上报当地畜牧兽医站</li>
                <li>🚫 不要移动病死禽</li>
                <li>💀 深埋无害化处理</li>
                <li>🧴 全场严格消毒</li>
                <li>🔒 禁止销售病死禽及产品</li>
            </ol>
            <hr>
            <p><strong>📞 紧急联系方式：</strong></p>
            <ul>
                <li>拨打 <strong>12316</strong>（全国农业系统服务热线）</li>
                <li>联系当地畜牧兽医站</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 正常问诊
    elif symptoms:
        st.markdown(f"""
        <div class="report-box">
            <h2>🐔 禽病初诊报告卡</h2>
            
            <h3>📋 病禽信息</h3>
            <ul>
                <li><strong>种类：</strong>{poultry_type}</li>
                <li><strong>日龄/阶段：</strong>{age if age else '未提供'}</li>
                <li><strong>群体规模：</strong>{bird_count if bird_count else '未提供'}</li>
            </ul>
            
            <h3>🔍 初步判断</h3>
            <p>根据您描述的<strong>"{symptoms}"</strong>，建议进一步了解以下信息：</p>
            <ol>
                <li>粪便颜色是什么样？（水样/糊状/带血/绿色）</li>
                <li>精神状态如何？（正常/精神差/不吃不喝）</li>
                <li>鸡冠颜色？（正常/苍白/发紫）</li>
                <li>周围其他鸡有同样症状吗？</li>
            </ol>
            
            <h3>💡 回复以上问题，我会给您更准确的诊断</h3>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.info("👆 请在上方填写症状信息，然后点击'开始问诊'")

# ==================== 快捷示例 ====================
st.markdown("---")
st.markdown("### 💡 快捷示例")

examples = [
    ("鸡（蛋鸡）", "28天", "200只", "3只", "拉血便，肛门羽毛沾血，采食量下降"),
    ("鸭（肉鸭）", "20天", "500只", "10只", "一直摇头，像看天一样，拉绿色稀粪"),
    ("鹅", "3个月", "100只", "0", "有几只腿站不起来，瘫痪"),
]

for i, (pt, a, bc, dc, s) in enumerate(examples):
    if st.button(f"示例{i+1}：{pt} - {s[:10]}...", key=f"example_{i}"):
        st.session_state.poultry_type = pt
        st.session_state.age = a
        st.session_state.bird_count = bc
        st.session_state.death_count = dc
        st.session_state.symptoms = s
        st.rerun()

# ==================== 底部信息 ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><strong>📚 知识库来源</strong></p>
    <p>基于ima《禽病》Avian Disease禽病知识库</p>
    <hr>
    <p><strong>🔒 安全说明</strong></p>
    <ul style="list-style: none; padding: 0;">
        <li>🚨 群体死亡立即提示12316上报</li>
        <li>💊 食品动物用药必填休药期</li>
        <li>⚠️ 处方药不给具体剂量</li>
    </ul>
</div>
""", unsafe_allow_html=True)
