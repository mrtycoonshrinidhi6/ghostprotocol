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
# GHOST PROTOCOL THEME (CYBERPUNK DARK)
# ========================================================================

def inject_ghost_theme():
    """Inject Ghost Protocol Dark Theme (Cyberpunk/Futuristic)."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    /* Global Reset */
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main App Background */
    .stApp {
        background-color: #0E1117 !important;
        color: #E0E0E0 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D;
    }

    [data-testid="stSidebar"] * {
        color: #E0E0E0 !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }

    h1 {
        background: linear-gradient(90deg, #FFFFFF, #A0A0A0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Buttons */
    .stButton > button {
        background-color: #1E2127 !important;
        color: #00FFA3 !important;
        border: 1px solid #00FFA3 !important;
        font-weight: 600 !important;
        border-radius: 4px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 14px !important;
    }

    .stButton > button:hover {
        background-color: #00FFA3 !important;
        color: #000000 !important;
        box-shadow: 0 0 15px rgba(0, 255, 163, 0.4) !important;
        border-color: #00FFA3 !important;
    }

    /* Primary Buttons (if any) */
    button[kind="primary"] {
        background-color: #00FFA3 !important;
        color: #000000 !important;
        border: none !important;
    }

    /* Cards */
    .ghost-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .ghost-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: #00FFA3;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .ghost-card:hover {
        transform: translateY(-5px);
        border-color: #00FFA3;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .ghost-card:hover::before {
        opacity: 1;
    }

    .ghost-card h3 {
        color: #00FFA3 !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }

    .ghost-card p {
        color: #8B949E !important;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #0D1117 !important;
        color: #E0E0E0 !important;
        border: 1px solid #30363D !important;
        border-radius: 4px !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00FFA3 !important;
        box-shadow: 0 0 0 1px #00FFA3 !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00FFA3 !important;
        font-family: 'JetBrains Mono', monospace;
    }

    [data-testid="stMetricLabel"] {
        color: #8B949E !important;
    }

    /* Status Banners */
    .backend-online-banner {
        background: rgba(0, 255, 163, 0.1);
        border: 1px solid #00FFA3;
        color: #00FFA3;
        padding: 12px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .backend-offline-banner {
        background: rgba(255, 75, 75, 0.1);
        border: 1px solid #FF4B4B;
        color: #FF4B4B;
        padding: 12px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #161B22 !important;
        color: #E0E0E0 !important;
        border: 1px solid #30363D !important;
        border-radius: 4px !important;
        padding-left: 40px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #0D1117 !important;
        border: 1px solid #30363D !important;
        border-top: none !important;
        color: #E0E0E0 !important;
    }

    /* Code */
    code {
        background-color: #161B22 !important;
        color: #00FFA3 !important;
        border: 1px solid #30363D !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Progress Bar */
    .stProgress > div > div {
        background-color: #00FFA3 !important;
    }

    /* Radio Buttons */
    .stRadio label {
        color: #E0E0E0 !important;
    }

    /* Dividers */
    hr {
        border-color: #30363D !important;
    }
    
    /* JSON */
    .stJson {
        background-color: #0D1117;
        padding: 10px;
        border-radius: 4px;
        border: 1px solid #30363D;
    }

    </style>
    """, unsafe_allow_html=True)


inject_ghost_theme()


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

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏛️ Dashboard"


# ========================================================================
# NAVIGATION CALLBACK
# ========================================================================

def set_page(page_name):
    """Callback to update the current page safely."""
    st.session_state.current_page = page_name


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
        key="current_page"
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
        <div class="ghost-card fade-in">
            <h3>⚰️ Death Detection</h3>
            <p>Multi-source verification using obituaries, email, social media, and death registries.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Launch Death Detection", use_container_width=True, on_click=set_page, args=("⚰️ Death Detection",))

        st.markdown("""
        <div class="ghost-card fade-in">
            <h3>💼 Asset Discovery</h3>
            <p>Automatic scanning of cloud storage, crypto wallets, email accounts, and digital services.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Launch Asset Discovery", use_container_width=True, on_click=set_page, args=("💼 Asset Discovery",))

    with col2:
        st.markdown("""
        <div class="ghost-card fade-in">
            <h3>📜 Smart Contract</h3>
            <p>Decentralized execution of your digital will on Polygon blockchain.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Launch Smart Contract", use_container_width=True, on_click=set_page, args=("📜 Smart Contract",))

        st.markdown("""
        <div class="ghost-card fade-in">
            <h3>🕊️ Memorial Chat</h3>
            <p>AI-driven memory twin providing emotional comfort to loved ones.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Launch Memorial Chat", use_container_width=True, on_click=set_page, args=("🕊️ Memorial Chat",))

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
