"""
Ghost Protocol - Streamlit Frontend (Notion-Style Minimal + Emoji Icons)
Professional black & white UI, fully responsive, backend-connected.
"""

import streamlit as st
import httpx
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
import time
import json


# ========================================================================
# CONFIGURATION
# ========================================================================

API_BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="Ghost Protocol",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ========================================================================
# NOTION THEME (HIGH CONTRAST)
# ========================================================================

def inject_notion_theme():
    """Inject Notion-style high-contrast theme with maximum visibility."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Reset - High Contrast */
    * {
        font-family: 'Inter', sans-serif !important;
    }

    /* Main App Background */
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* All Text Elements - Pure Black on White */
    * {
        color: #000000 !important;
    }
    
    body, div, p, span, label, input, textarea, select, button, a, li, ul, ol {
        color: #000000 !important;
    }
    
    /* Override any Streamlit-specific classes */
    .st-emotion-cache-1pr8puy,
    .st-emotion-cache-1pr8puy *,
    [class*="st-emotion"],
    [class*="emotion"] {
        color: #000000 !important;
    }
    
    /* Force all paragraph and text elements */
    p, span, div, label, input, textarea {
        color: #000000 !important;
    }

    /* Headers - Bold Black */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Sidebar - Light Gray Background */
    [data-testid="stSidebar"] {
        background-color: #F5F5F5 !important;
        border-right: 2px solid #CCCCCC;
        padding: 1.5rem;
    }

    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    [data-testid="stSidebar"] h1 {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        font-size: 17px !important;
        font-weight: 500 !important;
        color: #000000 !important;
    }

    /* Buttons - Teal/Cyan Brand Color */
    .stButton > button {
        background-color: #2af5ba !important;
        color: #000000 !important;
        border: 2px solid #2af5ba !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #1ad9a3 !important;
        border-color: #1ad9a3 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(42, 245, 186, 0.3) !important;
    }

    /* Input Fields - Black Text on White */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #CCCCCC !important;
        border-radius: 6px !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #000000 !important;
        box-shadow: 0 0 0 2px rgba(0,0,0,0.1) !important;
    }

    /* Multi-select */
    .stMultiSelect > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #CCCCCC !important;
    }

    /* Checkboxes */
    .stCheckbox label {
        color: #000000 !important;
        font-weight: 500 !important;
    }

    /* Cards */
    .notion-card {
        background: #FFFFFF !important;
        border: 2px solid #DDDDDD !important;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        transition: 0.2s ease;
    }

    .notion-card h3 {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    .notion-card p {
        color: #333333 !important;
    }

    .notion-card:hover {
        border-color: #000000 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }

    /* Status Banners */
    .backend-offline-banner {
        background: #FFE5E5 !important;
        border: 2px solid #FF0000 !important;
        border-radius: 8px;
        padding: 16px;
        color: #CC0000 !important;
        font-weight: 600 !important;
        margin-bottom: 20px;
    }

    .backend-online-banner {
        background: #E0FFE0 !important;
        border: 2px solid #00AA00 !important;
        border-radius: 8px;
        padding: 16px;
        color: #006600 !important;
        font-weight: 600 !important;
        margin-bottom: 20px;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* Progress Bars */
    .stProgress > div > div {
        background-color: #000000 !important;
    }

    /* Tables/DataFrames */
    .dataframe {
        color: #000000 !important;
        border: 2px solid #CCCCCC !important;
    }

    .dataframe th {
        background-color: #F0F0F0 !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: 1px solid #CCCCCC !important;
    }

    .dataframe td {
        color: #000000 !important;
        border: 1px solid #E5E5E5 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #F5F5F5 !important;
        color: #000000 !important;
        border: 2px solid #DDDDDD !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-color: #000000 !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #F5F5F5 !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border: 2px solid #DDDDDD !important;
    }

    .streamlit-expanderContent {
        background-color: #FAFAFA !important;
        border: 2px solid #DDDDDD !important;
        color: #000000 !important;
    }

    /* Code Blocks */
    code {
        background-color: #F5F5F5 !important;
        color: #000000 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid #DDDDDD !important;
    }

    pre {
        background-color: #F5F5F5 !important;
        color: #000000 !important;
        border: 2px solid #DDDDDD !important;
        padding: 12px !important;
        border-radius: 6px !important;
    }

    /* Alerts/Info/Warning/Success */
    .stAlert {
        color: #000000 !important;
        font-weight: 500 !important;
    }

    [data-testid="stNotification"] {
        background-color: #F0F0F0 !important;
        color: #000000 !important;
        border: 2px solid #CCCCCC !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #000000 !important;
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: #F5F5F5 !important;
        border: 2px solid #DDDDDD !important;
        color: #000000 !important;
    }

    /* Links */
    a {
        color: #0066CC !important;
        font-weight: 600 !important;
        text-decoration: underline !important;
    }

    a:hover {
        color: #0044AA !important;
    }

    /* Dividers */
    .section-divider {
        border-top: 2px solid #DDDDDD;
        margin: 30px 0;
    }

    hr {
        border-color: #DDDDDD !important;
        border-width: 2px !important;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.3s ease-in-out;
    }
    
    /* FINAL OVERRIDE - Kill all cyan/blue colors, force black text */
    * {
        color: #000000 !important;
    }
    
    /* Specific overrides for common elements */
    body *, 
    .stApp *, 
    .main *, 
    [data-testid] *, 
    div, p, span, label, input, textarea, select, button, a, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Kill any specific cyan/blue/red colors */
    [style*="#73e8f1"],
    [style*="#b1e5ec"],
    [style*="#be5050"],
    [style*="rgb(115, 232, 241)"],
    [style*="rgb(177, 229, 236)"],
    [style*="rgb(190, 80, 80)"] {
        color: #000000 !important;
    }
    
    /* Extra aggressive override for all elements */
    html *, body *, div *, p *, span *, label *, 
    .stApp *, .main *, [data-testid] *,
    input, textarea, select, button, a, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* NUCLEAR OPTION - Override EVERYTHING with black text */
    html, body, div, p, span, label, input, textarea, select, a, li, ul, ol,
    h1, h2, h3, h4, h5, h6, strong, em, code, pre, blockquote,
    .stMarkdown, .stText, .stCaption, .stTitle, .stHeader,
    [class*="st"], [class*="emotion"], [data-testid] {
        color: #000000 !important;
    }
    
    /* Preserve button text as black even with colored backgrounds */
    button, .stButton button, input[type="button"], input[type="submit"] {
        color: #000000 !important;
    }
    
    /* Streamlit alert boxes - keep colored backgrounds but ensure text is readable */
    .stAlert, [data-baseweb="notification"] {
        color: #000000 !important;
    }
    
    /* Object inspector container background */
    div.object-key-val {
        background-color: #ADD8E6 !important;
    }
    
    /* Success messages - keep green background, black text */
    .stSuccess, [kind="success"] {
        background-color: #E0FFE0 !important;
        color: #006600 !important;
        border: 2px solid #00AA00 !important;
    }
    
    /* Warning messages - keep yellow background, black text */
    .stWarning, [kind="warning"] {
        background-color: #FFF9E6 !important;
        color: #997700 !important;
        border: 2px solid #FFCC00 !important;
    }
    
    /* Error messages - keep red background, dark red text */
    .stError, [kind="error"] {
        background-color: #FFE5E5 !important;
        color: #CC0000 !important;
        border: 2px solid #FF0000 !important;
    }
    
    /* Info messages - keep blue background, dark blue text */
    .stInfo, [kind="info"] {
        background-color: #E6F3FF !important;
        color: #004085 !important;
        border: 2px solid #0066CC !important;
    }
    </style>
    """, unsafe_allow_html=True)


inject_notion_theme()


# ========================================================================
# SESSION STATE
# ========================================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "user_id" not in st.session_state:
    st.session_state.user_id = "user_demo_123"

if "death_confirmed" not in st.session_state:
    st.session_state.death_confirmed = False

if "assets_scanned" not in st.session_state:
    st.session_state.assets_scanned = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "backend_online" not in st.session_state:
    st.session_state.backend_online = None

if "system_mode" not in st.session_state:
    st.session_state.system_mode = None

if "diagnostics" not in st.session_state:
    st.session_state.diagnostics = None

if "last_memorial_message" not in st.session_state:
    st.session_state.last_memorial_message = None


# ========================================================================
# BACKEND HEALTH CHECK
# ========================================================================

def check_backend_health() -> bool:
    health_url = "http://localhost:8000/health"
    try:
        with httpx.Client(timeout=2.0) as client:
            res = client.get(health_url)
            return res.status_code == 200
    except:
        return False


def api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Optional[Dict]:
    """Make API request using httpx (synchronous for Streamlit compatibility)"""
    url = f"{API_BASE_URL}/{endpoint}"
    
    # Set longer timeout for POST requests (death detection, asset scan can take 2-5 minutes)
    timeout_seconds = 300.0 if method == "POST" else 30.0  # 5 minutes for POST, 30s for GET
    
    try:
        with httpx.Client(timeout=timeout_seconds) as client:
            if method == "POST":
                response = client.post(url, json=data)
            else:
                response = client.get(url)
            
            response.raise_for_status()
            return response.json()
    
    except httpx.TimeoutException:
        st.error(f"⚠️ Request timed out after {timeout_seconds} seconds. The operation is taking longer than expected.")
        return None
    except httpx.ConnectError:
        st.error("⚠️ Backend not reachable. Please ensure the backend server is running at http://localhost:8000")
        return None
    except httpx.RequestError as e:
        st.error(f"⚠️ Network error: {str(e)}")
        return None
    except httpx.HTTPStatusError as e:
        error_msg = f"⚠️ API Error: {e.response.status_code}"
        try:
            error_detail = e.response.json().get("detail", "No details provided")
            error_msg += f"\n\n**Details:** {error_detail}"
        except:
            pass
        st.error(error_msg)
        return None
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {str(e)}")
        return None


def fetch_diagnostics() -> Optional[Dict]:
    """Fetch system mode and API key diagnostics"""
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{API_BASE_URL}/diagnostics/keys")
            response.raise_for_status()
            return response.json()
    except:
        return None


if st.session_state.backend_online is None:
    st.session_state.backend_online = check_backend_health()

# Fetch diagnostics if backend is online
if st.session_state.backend_online and st.session_state.diagnostics is None:
    st.session_state.diagnostics = fetch_diagnostics()
    if st.session_state.diagnostics:
        st.session_state.system_mode = st.session_state.diagnostics.get("mode", "UNKNOWN")


# ========================================================================
# SIDEBAR (Emoji Icons Only)
# ========================================================================

with st.sidebar:
    st.markdown("# 🕊️ Ghost Protocol")
    st.markdown("#### Autonomous Digital Executor")
    st.markdown("---")

    # Backend status
    if st.session_state.backend_online:
        st.success("🟢 Backend Online")
    else:
        st.error("🔴 Backend Offline")

    # System Mode Badge
    if st.session_state.system_mode:
        if st.session_state.system_mode == "REALTIME":
            st.markdown("**🟢 LIVE MODE** - Real APIs")
        else:
            st.markdown("**🟡 DEMO MODE** - Mock Data")
    
    st.markdown("---")
    
    # Mode diagnostics expander
    if st.session_state.backend_online and st.session_state.diagnostics:
        with st.expander("🔧 System Diagnostics", expanded=False):
            diag = st.session_state.diagnostics
            
            st.markdown(f"**Mode:** {diag.get('mode', 'UNKNOWN')}")
            st.markdown(f"**Can use REALTIME:** {'✓' if diag.get('can_use_realtime') else '✗'}")
            
            # API Keys Status
            api_keys = diag.get('api_keys', {})
            st.markdown(f"**API Keys:** {api_keys.get('total_loaded', 0)}/{api_keys.get('total_loaded', 0) + api_keys.get('total_missing', 0)}")
            
            # Critical keys
            critical = api_keys.get('critical', {})
            if critical:
                st.markdown("**Critical Keys:**")
                for key_name, status in critical.items():
                    icon = "✓" if status['available'] else "✗"
                    st.markdown(f"- {icon} {key_name}")
            
            # Refresh button
            if st.button("🔄 Refresh Diagnostics", key="refresh_diag"):
                st.session_state.diagnostics = fetch_diagnostics()
                if st.session_state.diagnostics:
                    st.session_state.system_mode = st.session_state.diagnostics.get("mode")
                st.rerun()

    st.markdown("---")

    # Navigation
    page = st.radio(
        "Navigation",
        [
            "🏛️ Dashboard",
            "⚰️ Death Detection",
            "💼 Asset Discovery",
            "📜 Smart Contract",
            "🕊️ Memorial Chat"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.caption(f"Session: **{st.session_state.user_id}**")

# ========================================================================
# BACKEND OFFLINE BANNER (Displayed on all pages)
# ========================================================================

if not st.session_state.backend_online:
    st.markdown("""
    <div class="backend-offline-banner">
        ⚠️ The backend is offline.  
        Please start the backend server using:  
        <code>python run.py</code>
    </div>
    """, unsafe_allow_html=True)


# ========================================================================
# PAGE: DASHBOARD (🏛️)
# ========================================================================

if page == "🏛️ Dashboard":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.title("🏛️ Dashboard")
    st.markdown("### Welcome to Ghost Protocol")
    st.markdown("A professional autonomous AI system for post-death digital execution.")

    st.markdown("---")

    # Feature cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="notion-card fade-in">
            <h3>⚰️ Death Detection</h3>
            <p>Multi-source verification using obituaries, email, social media, and death registries.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="notion-card fade-in">
            <h3>💼 Asset Discovery</h3>
            <p>Automatic scanning of cloud storage, crypto wallets, email accounts, and digital services.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="notion-card fade-in">
            <h3>📜 Smart Contract</h3>
            <p>Decentralized execution of your digital will on Polygon blockchain.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="notion-card fade-in">
            <h3>🕊️ Memorial Chat</h3>
            <p>AI-driven memory twin providing emotional comfort to loved ones.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # System Health
    st.markdown("## System Health")

    if st.session_state.backend_online:
        st.markdown("""
        <div class="backend-online-banner">
            ✓ All systems operational
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Backend", "Online")

        with col2:
            st.metric("Agents Active", "3")

        with col3:
            st.metric("Tools Loaded", "8")

        with col4:
            st.metric("Version", "1.0.0")

    else:
        st.markdown("""
        <div class="backend-offline-banner">
            ✗ Backend Offline — System features unavailable
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Quick Actions
    st.markdown("## Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Refresh Backend Status", use_container_width=True):
            st.session_state.backend_online = check_backend_health()
            st.rerun()

    with col2:
        st.link_button("📘 API Docs", "http://localhost:8000/docs")

    with col3:
        if st.button("♻️ Reload Page", use_container_width=True):
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ========================================================================
# PAGE: DEATH DETECTION (⚰️)
# ========================================================================

elif page == "⚰️ Death Detection":
    # Page-scoped style: make Death Detection text/titles/labels #be5050
    st.markdown(
        """
        <style>
        #death-detection-page, 
        #death-detection-page h1, 
        #death-detection-page h2,
        #death-detection-page label,
        #death-detection-page p,
        #death-detection-page span {
            color: #be5050 !important;
        }
        
        /* Keep buttons readable on this page */
        #death-detection-page .stButton > button {
            color: #be5050 !important;
        }
        </style>
        <div id="death-detection-page" class="fade-in">
        """,
        unsafe_allow_html=True,
    )

    st.title("⚰️ Death Detection")
    st.markdown("### Multi-Source Verification System")

    st.markdown("---")

    st.markdown("### Detection Sources")

    sources = st.multiselect(
        "Choose verification sources:",
        ["obituary", "email", "social_media", "death_registry"],
        default=["obituary", "death_registry"],
    )

    manual_trigger = st.checkbox("Manual Override (Skip confidence requirement)")

    st.markdown("---")

    st.info("⏱️ This process may take 1–3 minutes depending on source count.")

    run_detection = st.button("Run Death Detection", type="primary", use_container_width=True)

    if run_detection:
        with st.spinner("Analyzing sources… please wait…"):
            result = api_request(
                "detect_death",
                method="POST",
                data={
                    "user_id": st.session_state.user_id,
                    "sources": sources,
                    "manual_trigger": manual_trigger,
                }
            )

        if result:
            st.session_state.session_id = result["session_id"]
            st.session_state.death_confirmed = result["is_confirmed"]

            st.markdown("---")
            st.markdown("## Results")

            confidence = result.get("confidence", 0)
            st.metric("Confidence Score", f"{confidence*100:.1f}%")
            st.progress(confidence)

            # Evidence Found
            if result.get("evidence"):
                st.markdown("## Evidence Found")

                for ev in result["evidence"]:
                    with st.expander(f"📄 {ev.get('source', 'Unknown')} — {ev.get('confidence', 0)*100:.0f}%"):
                        st.json(ev)

            if result["is_confirmed"]:
                st.success("✓ Death Confirmed — You may proceed to Asset Discovery")
            else:
                st.warning("○ Insufficient Evidence — Continuing monitoring")
                
                # If confidence is high but below threshold (85-95%), suggest manual override
                if 0.80 <= confidence < 0.85:
                    st.info("💡 **Tip:** Confidence is close to threshold. You can check **Manual Override** and run detection again to proceed.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================================
# PAGE: ASSET DISCOVERY (💼)
# ========================================================================

elif page == "💼 Asset Discovery":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.title("💼 Asset Discovery")
    st.markdown("### Automated Digital Asset Scanning")

    st.markdown("---")

    if not st.session_state.death_confirmed:
        st.warning("⚠ Death must be confirmed before asset scanning is allowed.")
        st.info("Go to **⚰️ Death Detection** to verify death first.")
    else:

        st.markdown("### Scan Configuration")

        scan_types = st.multiselect(
            "Choose which asset categories to scan:",
            ["email", "cloud", "crypto", "social"],
            default=["email", "cloud", "crypto", "social"],
        )

        st.markdown("---")

        st.info("⏱️ Asset scanning may take 2–5 minutes depending on selected categories.")

        run_scan = st.button("Start Asset Scan", type="primary", use_container_width=True)

        if run_scan:
            with st.spinner("Scanning digital assets… please wait…"):
                result = api_request(
                    "scan_assets",
                    method="POST",
                    data={
                        "user_id": st.session_state.user_id,
                        "session_id": st.session_state.session_id,
                        "scan_types": scan_types
                    }
                )

            if result:
                st.session_state.assets_scanned = True

                st.markdown("---")
                st.markdown(f"## Results — {result.get('total_assets', 0)} Assets Found")

                tab1, tab2, tab3, tab4 = st.tabs([
                    "📧 Email Accounts",
                    "☁️ Cloud Storage",
                    "🪙 Cryptocurrency",
                    "📱 Social Media"
                ])

                # EMAIL ACCOUNTS
                with tab1:
                    st.markdown("### Email Accounts")
                    if result.get("email_accounts"):
                        df = pd.DataFrame(result["email_accounts"])
                        st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No email accounts detected.")

                # CLOUD STORAGE
                with tab2:
                    st.markdown("### Cloud Storage")
                    if result.get("cloud_storage"):
                        df = pd.DataFrame(result["cloud_storage"])
                        st.dataframe(df, use_container_width=True, hide_index=True)

                        total_gb = sum(x.get("size_gb", 0) for x in result["cloud_storage"])
                        st.metric("Total Storage Found", f"{total_gb:.1f} GB")
                    else:
                        st.info("No cloud storage detected.")

                # CRYPTO
                with tab3:
                    st.markdown("### Cryptocurrency Wallets")
                    if result.get("crypto_wallets"):
                        df = pd.DataFrame(result["crypto_wallets"])
                        st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No crypto wallets detected.")

                # SOCIAL MEDIA
                with tab4:
                    st.markdown("### Social Media Accounts")
                    if result.get("social_accounts"):
                        df = pd.DataFrame(result["social_accounts"])
                        st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No social accounts detected.")

    st.markdown("</div>", unsafe_allow_html=True)



# ========================================================================
# PAGE: SMART CONTRACT EXECUTION (📜)
# ========================================================================

elif page == "📜 Smart Contract":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.title("📜 Smart Contract Execution")
    st.markdown("### Deploy will instructions to the Polygon blockchain")

    st.markdown("---")

    if not st.session_state.death_confirmed:
        st.warning("⚠ Death must be confirmed before executing a digital will.")
    else:
        st.markdown("### Beneficiary Setup")

        col1, col2 = st.columns(2)

        with col1:
            beneficiary1 = st.text_input("🏷️ Beneficiary 1 Address", "0x742d35Cc...")
            share1 = st.slider("Share (%)", 0, 100, 50, key="share1_slider")

        with col2:
            beneficiary2 = st.text_input("🏷️ Beneficiary 2 Address", "0x1A1zP1e...")
            share2 = st.slider("Share (%)", 0, 100, 50, key="share2_slider")

        st.markdown("---")

        st.markdown("### Gas Settings")

        colA, colB = st.columns(2)

        with colA:
            st.metric("Current Gas Price", "30 Gwei")

        with colB:
            st.metric("Estimated Cost", "$2.50")

        st.markdown("---")

        execute_now = st.button("Execute Will on Blockchain", type="primary", use_container_width=True)

        if execute_now:
            with st.spinner("Deploying smart contract to Polygon… this may take a few moments…"):
                result = api_request(
                    "execute_will",
                    method="POST",
                    data={
                        "user_id": st.session_state.user_id,
                        "session_id": st.session_state.session_id,
                        "beneficiaries": [
                            {"address": beneficiary1, "share": share1 / 100},
                            {"address": beneficiary2, "share": share2 / 100}
                        ]
                    }
                )

            if result:
                st.success("✓ Smart Contract Successfully Deployed")

                st.markdown("### Transaction Details")

                st.code(f"Contract Address: {result.get('contract_address', '0x...')}")
                st.code(f"Transaction Hash: {result.get('tx_hash', '0x...')}")
                st.code(f"Gas Used: {result.get('gas_used', 'N/A')}")

                st.info("Digital will execution complete. Distribution will occur automatically.")

    st.markdown("</div>", unsafe_allow_html=True)


# ========================================================================
# PAGE: MEMORIAL CHAT (🕊️)
# ========================================================================

elif page == "🕊️ Memorial Chat":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.title("🕊️ Memorial Chat")
    st.markdown("### AI Memory Twin for Emotional Support")

    st.markdown("---")

    # Select Recipient
    recipient = st.selectbox(
        "Choose who the message is for:",
        [
            "Son - Michael",
            "Daughter - Sarah",
            "Partner - Emily",
            "Friend - Jason"
        ],
        help="AI tone and language adapt to the chosen relationship."
    )

    st.markdown("---")

    # Chat History Display
    st.markdown("## Conversation")

    if not st.session_state.chat_history:
        st.info("No messages yet — start the conversation below.")
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="notion-card fade-in" style="border-left: 4px solid #000;">
                    <strong>You</strong><br>
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="notion-card fade-in" style="border-left: 4px solid #555;">
                    <strong>AI Twin</strong><br>
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # User Message Input
    user_message = st.text_area(
        "Your Message",
        height=100,
        placeholder="Type something you'd like to say..."
    )

    send_now = st.button("Send Message", type="primary", use_container_width=True)

    if send_now and user_message:

        # Avoid sending duplicate replies for the same input on reruns
        if user_message != st.session_state.last_memorial_message:
            st.session_state.last_memorial_message = user_message

            # Add user message to session history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_message
            })

            with st.spinner("AI Twin is preparing a compassionate response…"):
                result = api_request(
                    "memorial_chat",
                    method="POST",
                    data={
                        "user_id": st.session_state.user_id,
                        "session_id": st.session_state.session_id or "demo",
                        "recipient": recipient,
                        "message": user_message,
                        "context_type": "general"
                    }
                )

            if result:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result.get("response", "I'm here with you, always.")
                })

                st.rerun()

    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

    # Ethical notice
    st.markdown("---")
    st.caption("⚠️ This AI does not represent the actual voice or consciousness of the deceased. It generates supportive responses based on memories and tone profiles.")


# ========================================================================
# END OF APPLICATION
# ========================================================================
