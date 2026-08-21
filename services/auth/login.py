import streamlit as st
from services.persistence.exercise_repo import get_or_create_user


def render_login_page():
    if st.session_state.get("user_id") is not None:
        return True

    # Landing Page Hero Section
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 30px 10px 10px 10px;
        ">
            <div style="
                display: inline-block;
                padding: 6px 16px;
                border-radius: 30px;
                background: rgba(0, 242, 254, 0.1);
                border: 1px solid rgba(0, 242, 254, 0.3);
                color: #00F2FE;
                font-size: 0.85rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                margin-bottom: 20px;
                box-shadow: 0 0 20px rgba(0, 242, 254, 0.15);
            ">
                ⚡ NEXT-GEN AI FITNESS COACH
            </div>
            <h1 style="
                font-size: 3.2rem !important;
                font-weight: 800 !important;
                background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 16px;
            ">
                Master Every Rep with Real-Time AI Form Coaching
            </h1>
            <p style="
                font-size: 1.15rem;
                color: #94A3B8;
                max-width: 680px;
                margin: 0 auto 36px auto;
                line-height: 1.6;
            ">
                Instant computer vision pose tracking meets proactive AI voice cues. Elevate your posture, prevent injury, and maximize gains effortlessly.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Feature Grid Showcase
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style="
                background: rgba(18, 24, 38, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 24px;
                height: 100%;
                text-align: left;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            ">
                <div style="font-size: 2.2rem; margin-bottom: 12px;">📹</div>
                <h3 style="margin-bottom: 8px; color: #F8FAFC;">Precision Pose Tracking</h3>
                <p style="font-size: 0.9rem; color: #94A3B8; margin: 0;">
                    33-point MediaPipe pose landmarker tracks joint angles, hip depth, and back curvature in real time.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div style="
                background: rgba(18, 24, 38, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 24px;
                height: 100%;
                text-align: left;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            ">
                <div style="font-size: 2.2rem; margin-bottom: 12px;">🎙️</div>
                <h3 style="margin-bottom: 8px; color: #F8FAFC;">Proactive Voice AI</h3>
                <p style="font-size: 0.9rem; color: #94A3B8; margin: 0;">
                    Groq LLM coach speaks audio feedback directly to correct your posture during workouts.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div style="
                background: rgba(18, 24, 38, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 24px;
                height: 100%;
                text-align: left;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            ">
                <div style="font-size: 2.2rem; margin-bottom: 12px;">📊</div>
                <h3 style="margin-bottom: 8px; color: #F8FAFC;">Automated Logging</h3>
                <p style="font-size: 0.9rem; color: #94A3B8; margin: 0;">
                    Seamless rep & set progress persistence with historical workout analytics for long-term growth.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Login / Access Section
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 12px;">
                <h3 style="margin-bottom: 4px;">🚀 Launch Your Session</h3>
                <p style="font-size: 0.9rem; color: #64748B;">Enter your profile name to start training</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "Profile Name",
                placeholder="e.g. Alex, Rohpin, Sarah",
                key="username_input"
            )

            submit_button = st.form_submit_button(
                "⚡ Enter AI Gym Studio",
                width="stretch",
                type="primary"
            )

        if submit_button:
            if not username or not username.strip():
                st.error("Please enter a valid profile name.")
                return False

            user = get_or_create_user(username.strip())

            st.session_state["user_name"] = user["username"]
            st.session_state["user_id"] = user["id"]

            st.rerun()

    return False