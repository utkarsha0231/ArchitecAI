import streamlit as st
import os
import time

from ai_engine import (
    generate_system_design,
    generate_feature_analysis,
    generate_project_code
)
from diagram_generator import show_architecture_diagram
from pdf_generator import generate_pdf
from zip_generator import generate_project_zip


# ==========================================
# 1. PAGE SETTINGS
# ==========================================
st.set_page_config(
    page_title="ArchitecAI | AI System Architect",
    page_icon="🏗️",
    layout="wide"
)

os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"


# ==========================================
# 2. PREMIUM PINK LUXURY UI
# ==========================================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 10% 5%, rgba(255,65,170,.13), transparent 40%),
        radial-gradient(ellipse at 90% 85%, rgba(255,125,205,.10), transparent 40%),
        linear-gradient(135deg,#0B080D,#170D18,#211020,#100A12);
    color:#FFF0F8;
}
.block-container { max-width:1350px; padding-top:2rem; padding-bottom:3rem; }

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#100B13,#211020,#2A1024);
    border-right:1px solid rgba(255,105,180,.25);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span { color:#FFE1F0 !important; }

h1,h2,h3 { color:#FFC3E1 !important; letter-spacing:-.5px; }
p,label,li { color:#F4DFEB; }

.hero {
    position:relative; overflow:hidden;
    background:linear-gradient(120deg,#1B101A,#40152F,#721D4D,#4B1838,#190E1B);
    background-size:300% 300%; animation:heroGradient 12s ease infinite;
    padding:40px; border-radius:26px;
    border:1px solid rgba(255,145,205,.45);
    box-shadow:0 10px 45px rgba(255,45,155,.12),inset 0 0 35px rgba(255,100,190,.07);
    margin-bottom:28px;
}
.hero::before {
    content:""; position:absolute; top:-80%; left:-130%; width:65%; height:250%;
    transform:rotate(25deg);
    background:linear-gradient(90deg,transparent,rgba(255,255,255,.05),rgba(255,190,225,.25),rgba(255,255,255,.12),transparent);
    animation:heroShine 8s ease-in-out infinite; pointer-events:none;
}
.hero-tag { color:#FF9FD0;font-size:12px;font-weight:800;letter-spacing:3px;text-transform:uppercase; }
.hero-title {
    font-size:48px;font-weight:900;margin:10px 0;
    background:linear-gradient(90deg,#FFFFFF,#FFC3E1,#FF70BD,#FFFFFF,#FFB6DC);
    background-size:300% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
    animation:textShine 6s linear infinite;
}
.hero-desc { color:#F7D6E9;font-size:16px;line-height:1.8; }
.section-label { color:#FF9FD0;font-size:12px;letter-spacing:2.5px;font-weight:800;text-transform:uppercase; }

.feature-card {
    position:relative;overflow:hidden;isolation:isolate;
    background:linear-gradient(145deg,rgba(66,24,49,.96),rgba(28,15,27,.98),rgba(80,25,57,.94));
    border:1px solid rgba(255,125,190,.40);border-radius:20px;padding:24px 16px;
    text-align:center;min-height:140px;
    box-shadow:0 8px 24px rgba(0,0,0,.25),inset 0 1px 0 rgba(255,255,255,.08);
    backdrop-filter:blur(18px);transition:transform .4s ease,box-shadow .4s ease,border .4s ease;
    animation:cardPulse 5s ease-in-out infinite;
}
.feature-card::before {
    content:"";position:absolute;z-index:-1;top:-20%;left:-160%;width:75%;height:150%;
    transform:skewX(-25deg);
    background:linear-gradient(110deg,transparent,rgba(255,255,255,.05),rgba(255,180,220,.30),rgba(255,255,255,.15),transparent);
    animation:cardShine 6s ease-in-out infinite;
}
.feature-card::after {
    content:"";position:absolute;top:0;left:15%;width:70%;height:1px;
    background:linear-gradient(90deg,transparent,#FFB5DA,transparent);opacity:.8;
}
.feature-card:hover {
    transform:translateY(-9px) scale(1.035);border-color:rgba(255,190,225,.95);
    box-shadow:0 12px 30px rgba(255,50,160,.20),0 0 22px rgba(255,105,180,.30),inset 0 0 22px rgba(255,100,180,.10);
}
.feature-card:hover::before { animation-duration:1.5s; }
.feature-icon { font-size:32px;margin-bottom:12px;filter:drop-shadow(0 0 9px rgba(255,135,200,.45));transition:transform .3s ease; }
.feature-card:hover .feature-icon { transform:scale(1.18); }
.feature-name { font-size:14px;font-weight:800;color:#FFE2F1;letter-spacing:.3px; }

.stButton > button {
    position:relative;overflow:hidden;
    background:linear-gradient(110deg,#C92C79,#F0449A,#FF70BD,#D93688);
    background-size:250% 100%;color:white !important;
    border:1px solid rgba(255,190,225,.75);border-radius:14px;min-height:50px;
    font-weight:800;letter-spacing:.3px;box-shadow:0 5px 22px rgba(255,45,150,.20);
    transition:.3s ease;
}
.stButton > button:hover {
    transform:translateY(-3px);background-position:100% 0;border-color:#FFD0E8;
    box-shadow:0 8px 28px rgba(255,65,165,.40),0 0 15px rgba(255,100,185,.28);
}
.stButton > button::before {
    content:"";position:absolute;top:0;left:-130%;width:80%;height:100%;
    background:linear-gradient(110deg,transparent,rgba(255,255,255,.35),transparent);
    transform:skewX(-25deg);transition:left .6s ease;
}
.stButton > button:hover::before { left:150%; }

.stDownloadButton > button {
    background:linear-gradient(135deg,#32152A,#70264E,#9B356D);
    color:#FFF0F8 !important;border:1px solid #E77AB4;border-radius:13px;
    min-height:46px;font-weight:700;transition:.3s ease;
}
.stDownloadButton > button:hover {
    transform:translateY(-2px);border-color:#FFC3E1;
    box-shadow:0 0 22px rgba(255,100,185,.32);
}

textarea {
    background:rgba(19,12,21,.96) !important;color:white !important;
    border:1px solid rgba(232,105,175,.55) !important;border-radius:16px !important;
}
textarea:focus { border-color:#FF9FD0 !important;box-shadow:0 0 16px rgba(255,70,170,.22) !important; }
input { color:white !important; }

[data-testid="stRadio"] label {
    background:rgba(199,56,129,.08);border:1px solid rgba(255,145,205,.18);
    border-radius:12px;padding:10px 12px;margin:5px 0;transition:.25s;
}
[data-testid="stRadio"] label:hover {
    background:rgba(235,75,160,.18);border-color:#F472B6;
    box-shadow:0 0 12px rgba(255,105,180,.18);
}
div[data-testid="stExpander"] {
    background:rgba(27,16,29,.88);border:1px solid rgba(255,135,195,.27);border-radius:16px;
}
[data-testid="stAlert"] { border-radius:13px; }
hr { border-color:rgba(255,145,205,.20); }

/* AI loader */
.ai-loader-box {
    position:relative;overflow:hidden;padding:30px 20px;margin:15px 0;border-radius:22px;
    background:linear-gradient(135deg,#180D18,#35132B,#521A3D,#241020);
    border:1px solid rgba(255,120,190,.55);
    box-shadow:0 0 18px rgba(255,40,155,.18),0 0 45px rgba(255,40,155,.12),inset 0 0 30px rgba(255,105,180,.08);
    text-align:center;animation:loaderBoxPulse 2s ease-in-out infinite;
}
.ai-loader-box::before {
    content:"";position:absolute;top:0;left:-120%;width:70%;height:100%;
    background:linear-gradient(100deg,transparent,rgba(255,255,255,.09),rgba(255,170,220,.22),transparent);
    transform:skewX(-25deg);animation:loaderShine 3s ease-in-out infinite;
}
.ai-orb-wrap { position:relative;width:95px;height:95px;margin:0 auto 18px; }
.ai-orb {
    position:absolute;inset:19px;border-radius:50%;
    background:radial-gradient(circle at 30% 30%,#FFF0FA,#FF9DD1,#F0449A,#8A174F);
    box-shadow:0 0 15px #FF70BD,0 0 35px rgba(255,70,170,.75),0 0 60px rgba(255,70,170,.35);
    animation:orbPulse 1.4s ease-in-out infinite;
}
.ai-ring {
    position:absolute;inset:2px;border-radius:50%;border:2px solid transparent;
    border-top-color:#FFB5DA;border-right-color:rgba(255,100,180,.6);
    animation:ringSpin 1.5s linear infinite;
}
.ai-ring2 { position:absolute;inset:10px;border-radius:50%;border:1px dashed rgba(255,190,225,.75);animation:ringSpinReverse 3s linear infinite; }
.ai-loader-title { position:relative;color:#FFD2E8;font-size:20px;font-weight:900;letter-spacing:4px;text-shadow:0 0 12px rgba(255,100,185,.7);animation:titleGlow 1.5s ease-in-out infinite; }
.ai-loader-subtitle { position:relative;color:#EFB3D2;font-size:13px;margin-top:8px;letter-spacing:1px; }
.ai-dots span { display:inline-block;color:#FF70BD;font-size:24px;animation:dotBounce 1.2s infinite; }
.ai-dots span:nth-child(2) { animation-delay:.2s; }
.ai-dots span:nth-child(3) { animation-delay:.4s; }
.ai-progress-track { position:relative;overflow:hidden;height:5px;max-width:300px;margin:20px auto 0;background:rgba(255,130,190,.15);border-radius:20px; }
.ai-progress-bar { width:40%;height:100%;border-radius:20px;background:linear-gradient(90deg,#B51E69,#FF70BD,#FFE1F0,#FF70BD);box-shadow:0 0 12px rgba(255,100,185,.65);animation:progressFlow 1.6s ease-in-out infinite; }
.ai-loader-caption { color:#C98EAF;font-size:11px;margin-top:16px;letter-spacing:2px; }

.success-glow {
    padding:15px;text-align:center;border-radius:14px;
    background:linear-gradient(120deg,rgba(80,20,55,.5),rgba(170,40,110,.3));
    border:1px solid rgba(255,150,210,.45);box-shadow:0 0 20px rgba(255,70,170,.12);
    color:#FFD6EA;animation:successAppear .6s ease-out;
}

/* PROGRESS STAGE UI */
.stage-box {
    background:linear-gradient(135deg,#180D18,#35132B,#521A3D,#241020);
    border:1px solid rgba(255,120,190,.55);border-radius:22px;
    padding:24px 20px;text-align:center;margin:12px 0;
    box-shadow:0 0 22px rgba(255,40,155,.16),inset 0 0 25px rgba(255,105,180,.06);
    animation:successAppear .4s ease-out;
}
.stage-title { color:#FFD2E8;font-size:21px;font-weight:900;letter-spacing:3px;text-shadow:0 0 15px #F472B6; }
.stage-subtitle { color:#FBCFE8;font-size:14px;margin-top:8px; }
.stage-track { background:#3A1830;height:10px;border-radius:20px;overflow:hidden;margin-top:22px; }
.stage-fill { height:10px;border-radius:20px;background:linear-gradient(90deg,#BE185D,#F472B6,#FFD1E8);box-shadow:0 0 15px #F472B6;transition:width .6s; }
.stage-percent { color:#F9A8D4;margin-top:12px;font-weight:bold;letter-spacing:1px; }
.stage-steps { display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:15px; }
.stage-pill { border:1px solid #A83B72;border-radius:30px;padding:7px 12px;color:#FBCFE8;background:#341329;font-size:12px; }
.stage-pill.active { background:#B52B70;border-color:#FFC3E1;box-shadow:0 0 12px #F472B6;color:white; }
.stage-pill.done { background:#68234B;color:#FFD6EA;border-color:#FF9FD0; }

.footer { text-align:center;color:#C08EAD;padding-top:25px;font-size:13px;line-height:2; }

@keyframes cardShine { 0%,15%{left:-160%;}45%,100%{left:160%;} }
@keyframes cardPulse { 0%,100%{box-shadow:0 8px 24px rgba(0,0,0,.20);}50%{box-shadow:0 8px 28px rgba(255,70,160,.12);} }
@keyframes heroShine { 0%,20%{left:-130%;}55%,100%{left:150%;} }
@keyframes textShine { 0%{background-position:0% center;}100%{background-position:300% center;} }
@keyframes heroGradient { 0%,100%{background-position:0% 50%;}50%{background-position:100% 50%;} }
@keyframes ringSpin { to{transform:rotate(360deg);} }
@keyframes ringSpinReverse { to{transform:rotate(-360deg);} }
@keyframes orbPulse { 0%,100%{transform:scale(.88);filter:brightness(1);}50%{transform:scale(1.12);filter:brightness(1.4);} }
@keyframes titleGlow { 0%,100%{text-shadow:0 0 8px rgba(255,100,185,.4);}50%{text-shadow:0 0 22px rgba(255,100,185,.9);} }
@keyframes dotBounce { 0%,60%,100%{transform:translateY(0);opacity:.4;}30%{transform:translateY(-8px);opacity:1;} }
@keyframes progressFlow { 0%{transform:translateX(-120%);}50%{transform:translateX(100%);}100%{transform:translateX(280%);} }
@keyframes loaderShine { 0%,15%{left:-120%;}55%,100%{left:150%;} }
@keyframes loaderBoxPulse { 0%,100%{box-shadow:0 0 18px rgba(255,40,155,.12),0 0 40px rgba(255,40,155,.08);}50%{box-shadow:0 0 28px rgba(255,40,155,.25),0 0 60px rgba(255,40,155,.15);} }
@keyframes successAppear { from{opacity:0;transform:translateY(10px) scale(.97);}to{opacity:1;transform:translateY(0) scale(1);} }

@media(max-width:768px) {
    .hero{padding:24px 20px;}
    .hero-title{font-size:34px;}
    .feature-card{padding:18px 10px;min-height:120px;}
    .feature-name{font-size:12px;}
    .ai-loader-title{font-size:17px;}
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. AI PROGRESS STAGES + LOADER
# ==========================================
def render_progress_stage(placeholder, task_name, stage_index, completed=False):
    stages = [
        ("🧠 PLANNING", "Understanding your project idea..."),
        ("🔍 ANALYZING", "Analyzing requirements and architecture..."),
        ("✨ GENERATING", "Creating your AI-powered result..."),
        ("💖 COMPLETED", "Your result is ready!")
    ]

    title, subtitle = stages[stage_index]
    percent = [25, 50, 85, 100][stage_index]

    pills = ""
    for i, (stage_title, _) in enumerate(stages):
        if i < stage_index or completed:
            css_class = "done"
        elif i == stage_index:
            css_class = "active"
        else:
            css_class = ""
        pills += f'<span class="stage-pill {css_class}">{stage_title}</span>'

    placeholder.markdown(f"""
    <div class="stage-box">
        <div class="stage-title">{title}</div>
        <div class="stage-subtitle">{subtitle}</div>
        <div class="stage-steps">{pills}</div>
        <div class="stage-track">
            <div class="stage-fill" style="width:{percent}%;"></div>
        </div>
        <div class="stage-percent">{percent}% Complete</div>
    </div>
    """, unsafe_allow_html=True)


def run_with_ai_loader(task_title, task_subtitle, function, *args, **kwargs):
    stage_placeholder = st.empty()

    # Stage 1: Planning
    render_progress_stage(stage_placeholder, task_title, 0)
    time.sleep(0.6)

    # Stage 2: Analyzing
    render_progress_stage(stage_placeholder, task_title, 1)
    time.sleep(0.6)

    # Stage 3: Generating
    render_progress_stage(stage_placeholder, task_title, 2)
    time.sleep(0.4)

    # Show premium animated AI loader during actual AI task
    loader_placeholder = st.empty()
    loader_placeholder.markdown(f"""
    <div class="ai-loader-box">
        <div class="ai-orb-wrap">
            <div class="ai-ring"></div>
            <div class="ai-ring2"></div>
            <div class="ai-orb"></div>
        </div>
        <div class="ai-loader-title">{task_title}</div>
        <div class="ai-loader-subtitle">{task_subtitle}</div>
        <div class="ai-dots"><span>.</span><span>.</span><span>.</span></div>
        <div class="ai-progress-track">
            <div class="ai-progress-bar"></div>
        </div>
        <div class="ai-loader-caption">ARCHITECAI • PREMIUM AI ENGINE</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        result = function(*args, **kwargs)

        # Stage 4: Completed
        loader_placeholder.empty()
        render_progress_stage(stage_placeholder, task_title, 3, completed=True)
        time.sleep(0.8)

        return result

    except Exception as e:
        loader_placeholder.empty()
        stage_placeholder.error(f"AI Task Error: {e}")
        raise

    finally:
        time.sleep(0.4)
        stage_placeholder.empty()


def show_success(message):
    st.markdown(f"""
    <div class="success-glow">
        ✨ {message} ✨
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 4. SESSION STATE
# ==========================================
if "project_idea" not in st.session_state:
    st.session_state.project_idea = ""

if "design_result" not in st.session_state:
    st.session_state.design_result = None

if "feature_results" not in st.session_state:
    st.session_state.feature_results = {}

if "generated_code" not in st.session_state:
    st.session_state.generated_code = None

if "diagram_ready" not in st.session_state:
    st.session_state.diagram_ready = False


# ==========================================
# 5. SIDEBAR
# ==========================================
st.sidebar.markdown("## 🏗️ ArchitecAI")
st.sidebar.caption("ADVANCED AI SYSTEM ARCHITECT")
st.sidebar.markdown("---")

feature_list = [
    "🧠 AI System Design",
    "🛠️ Tech Stack Recommendation",
    "🗄️ Database Design",
    "🔐 Security Analysis",
    "📊 Architecture Diagram",
    "📄 PDF Report",
    "💻 AI Code Generation"
]

selected_feature = st.sidebar.radio(
    "NAVIGATION",
    feature_list,
    key="architecai_feature_selector"
)

st.sidebar.markdown("---")
st.sidebar.markdown("✨ AI-Powered Developer Toolkit")
st.sidebar.caption("Python • Streamlit • Groq AI")


# ==========================================
# 6. HERO HEADER
# ==========================================
st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ AI-POWERED DEVELOPER TOOL</div>
    <div class="hero-title">🏗️ ArchitecAI</div>
    <div class="hero-desc">
        Turn your idea into a complete software blueprint.<br>
        Design systems, explore technologies, analyze security,
        visualize architecture and generate code — all in one place.
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 7. FEATURE SHOWCASE
# ==========================================
feature_cards = [
    ("🧠", "AI System Design"),
    ("⚙️", "Tech Stack"),
    ("🗄️", "Database Design"),
    ("🛡️", "Security Analysis"),
    ("📊", "Architecture"),
    ("📑", "PDF Reports"),
    ("💻", "Code Generation"),
    ("✨", "AI-Powered")
]

feature_cols = st.columns(4)

for col, (icon, name) in zip(feature_cols, feature_cards[:4]):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

feature_cols2 = st.columns(4)

for col, (icon, name) in zip(feature_cols2, feature_cards[4:]):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")


# ==========================================
# 8. PROJECT IDEA INPUT
# ==========================================
st.markdown('<div class="section-label">✦ START BUILDING</div>', unsafe_allow_html=True)
st.header("💡 Describe Your Project")

st.session_state.project_idea = st.text_area(
    "What do you want to build?",
    value=st.session_state.project_idea,
    placeholder="Example: Build an AI-powered online shopping recommendation system with user login, product catalog, personalized recommendations, and admin dashboard.",
    height=130,
    key="project_input"
)

if st.button("🚀 Generate AI System Design", key="system_design_button", use_container_width=True):
    if not st.session_state.project_idea.strip():
        st.warning("Please enter your project idea first.")
    else:
        try:
            result = run_with_ai_loader(
                "AI IS THINKING",
                "Designing your software architecture...",
                generate_system_design,
                st.session_state.project_idea
            )

            st.session_state.design_result = result
            st.session_state.feature_results = {}
            st.session_state.generated_code = None
            st.session_state.diagram_ready = False

            show_success("System design generated successfully!")
        except Exception as e:
            st.error(f"System Design Error: {e}")


# ==========================================
# 9. GENERATED SYSTEM DESIGN
# ==========================================
if st.session_state.design_result:
    with st.expander("🧠 View Generated System Design", expanded=False):
        st.markdown(st.session_state.design_result)

st.markdown("---")


# ==========================================
# 10. AI SYSTEM DESIGN
# ==========================================
if selected_feature == "🧠 AI System Design":
    st.header("🧠 AI System Design")
    st.write("Create an AI-powered system blueprint for your idea.")

    if st.session_state.design_result:
        st.success("System design is ready.")
        st.markdown(st.session_state.design_result)


# ==========================================
# 11. TECH STACK
# ==========================================
elif selected_feature == "🛠️ Tech Stack Recommendation":
    st.header("🛠️ Tech Stack Recommendation")

    if not st.session_state.design_result:
        st.warning("Generate the system design first.")
    else:
        if st.button("🔧 Recommend Tech Stack"):
            try:
                answer = run_with_ai_loader(
                    "AI IS THINKING",
                    "Finding the best technology stack for your project...",
                    generate_feature_analysis,
                    st.session_state.project_idea,
                    "Tech Stack Recommendation"
                )
                st.session_state.feature_results["Tech Stack Recommendation"] = answer
                show_success("Tech Stack recommendation is ready!")
            except Exception as e:
                st.error(f"Tech Stack Error: {e}")

        answer = st.session_state.feature_results.get("Tech Stack Recommendation")
        if answer:
            st.markdown(answer)


# ==========================================
# 12. DATABASE DESIGN
# ==========================================
elif selected_feature == "🗄️ Database Design":
    st.header("🗄️ Database Design")

    if not st.session_state.design_result:
        st.warning("Generate the system design first.")
    else:
        if st.button("🗃️ Generate Database Design"):
            try:
                answer = run_with_ai_loader(
                    "AI IS THINKING",
                    "Building database tables and relationships...",
                    generate_feature_analysis,
                    st.session_state.project_idea,
                    "Database Design"
                )
                st.session_state.feature_results["Database Design"] = answer
                show_success("Database design is ready!")
            except Exception as e:
                st.error(f"Database Error: {e}")

        answer = st.session_state.feature_results.get("Database Design")
        if answer:
            st.markdown(answer)


# ==========================================
# 13. SECURITY ANALYSIS
# ==========================================
elif selected_feature == "🔐 Security Analysis":
    st.header("🔐 Security Analysis")

    if not st.session_state.design_result:
        st.warning("Generate system design first.")
    else:
        if st.button("🛡️ Analyze Security"):
            try:
                answer = run_with_ai_loader(
                    "AI IS THINKING",
                    "Scanning your project for security risks...",
                    generate_feature_analysis,
                    st.session_state.project_idea,
                    "Security Analysis"
                )
                st.session_state.feature_results["Security Analysis"] = answer
                show_success("Security analysis completed!")
            except Exception as e:
                st.error(f"Security Error: {e}")

        answer = st.session_state.feature_results.get("Security Analysis")
        if answer:
            st.markdown(answer)


# ==========================================
# 14. ARCHITECTURE DIAGRAM
# ==========================================
elif selected_feature == "📊 Architecture Diagram":
    st.header("📊 Architecture Diagram")

    if not st.session_state.design_result:
        st.warning("Generate system design first.")
    else:
        if st.button("🎨 Generate Architecture Diagram"):
            try:
                run_with_ai_loader(
                    "BUILDING ARCHITECTURE",
                    "Creating your visual system architecture...",
                    show_architecture_diagram,
                    st.session_state.project_idea
                )
                st.session_state.diagram_ready = True
                show_success("Architecture diagram generated!")
            except Exception as e:
                st.error(f"Diagram Error: {e}")

        if st.session_state.diagram_ready:
            try:
                show_architecture_diagram(st.session_state.project_idea)
            except Exception as e:
                st.error(f"Diagram Error: {e}")


# ==========================================
# 15. PDF REPORT
# ==========================================
elif selected_feature == "📄 PDF Report":
    st.header("📄 PDF Report")

    if not st.session_state.design_result:
        st.warning("Generate system design first.")
    else:
        st.write("Create a downloadable report for your project.")

        if st.button("📑 Create PDF Report"):
            try:
                os.makedirs("reports", exist_ok=True)
                pdf_path = os.path.join("reports", "ArchitecAI_System_Report.pdf")
                diagram_path = os.path.join("reports", "architecture_diagram.png")

                if os.path.exists(diagram_path):
                    run_with_ai_loader(
                        "GENERATING REPORT",
                        "Preparing your premium PDF report...",
                        generate_pdf,
                        st.session_state.design_result,
                        pdf_path,
                        diagram_path=diagram_path
                    )
                else:
                    run_with_ai_loader(
                        "GENERATING REPORT",
                        "Preparing your premium PDF report...",
                        generate_pdf,
                        st.session_state.design_result,
                        pdf_path
                    )

                st.session_state.feature_results["PDF Report"] = pdf_path
                show_success("PDF created successfully!")
            except Exception as e:
                st.error(f"PDF Error: {e}")

        pdf_path = st.session_state.feature_results.get("PDF Report")

        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf:
                st.download_button(
                    "⬇️ Download PDF Report",
                    data=pdf,
                    file_name="ArchitecAI_System_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )


# ==========================================
# 16. AI CODE GENERATION + ZIP
# ==========================================
elif selected_feature == "💻 AI Code Generation":
    st.header("💻 AI Code Generation")

    if not st.session_state.design_result:
        st.warning("Generate the system design first.")
    else:
        st.write("Generate project source code from your idea and system design.")

        if st.button("⚡ Generate Project Code"):
            try:
                code = run_with_ai_loader(
                    "GENERATING CODE",
                    "Writing your project files and source code...",
                    generate_project_code,
                    st.session_state.project_idea,
                    st.session_state.design_result
                )
                st.session_state.generated_code = code
                show_success("Project code generated successfully!")
            except Exception as e:
                st.error(f"Code Generation Error: {e}")

        if st.session_state.generated_code:
            st.markdown("### ✨ Generated Code")
            st.markdown(st.session_state.generated_code)

            st.download_button(
                "⬇️ Download Generated Code (Markdown)",
                data=st.session_state.generated_code,
                file_name="ArchitecAI_Project_Code.md",
                mime="text/markdown",
                use_container_width=True
            )

            try:
                project_zip = generate_project_zip(
                    st.session_state.generated_code,
                    project_name="ArchitecAI_Generated_Project"
                )

                st.download_button(
                    "📦 Download Complete Project ZIP",
                    data=project_zip,
                    file_name="ArchitecAI_Generated_Project.zip",
                    mime="application/zip",
                    use_container_width=True,
                    key="complete_project_zip_download"
                )

                st.success("Complete Project ZIP is ready!")
            except Exception as e:
                st.error(f"ZIP Generation Error: {e}")


# ==========================================
# 17. FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div class="footer">
    🏗️ ArchitecAI &nbsp;|&nbsp; Built with Python, Streamlit & Groq AI<br>
    <span style="color:#D982AD;">Transform ideas into intelligent software architecture.</span>
</div>
""", unsafe_allow_html=True)