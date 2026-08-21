import os
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from services.auth.login import render_login_page
from services.state.default_session import initial_session_defaults
from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import inject_webrtc_styles, load_css, inject_audio_autoplayer
from services.persistence.exercise_repo import init_db, get_users_exercises
from services.vision.exercise_video_processor import VideoProcessorClass
from services.tracking.metrics import sync_metrics_update
from groq import Groq
from services.coaching.llm import LLMCoach
from services.coaching.tts import TextToSpeech
from services.coaching.voice_pipeLine import VoicePipeline, autoplay_audio


def main():
    load_dotenv()

    st.set_page_config(
        page_icon="💪",
        page_title="AI Real-Time GYM Assistant",
        initial_sidebar_state="expanded",
        layout="centered"
    )

    load_css(os.path.join("static", "stle.css"))
    inject_audio_autoplayer()
    init_db()
    
    if not render_login_page():
        return
    
    initial_session_defaults()
    
    if not st.session_state.get("voice_pipeline"):
        try:
            api_key = os.environ.get("GROQ_API_KEY", "")

            if not api_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
            
            groq_client = Groq(api_key=api_key)
            llm_coach = LLMCoach(groq_client)
            tts = TextToSpeech()
            st.session_state.voice_pipeline = VoicePipeline(llm_coach, tts)
        except Exception as e:
            st.session_state.voice_pipeline = None
            st.session_state.voice_error = str(e)
    
    workout_started = st.session_state.get("workout_started", False)
    
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 2.5rem; margin-bottom: 4px;">🏋️‍♂️</div>
                <h2 style="margin: 0; font-size: 1.5rem !important;">AI Gym Trainer</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.session_state.get("user_name"):
            st.markdown(
                f"""
                <div style="
                    background: rgba(255, 255, 255, 0.04);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 12px;
                    padding: 12px 14px;
                    margin-bottom: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                ">
                    <div>
                        <div style="font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase;">TRAINER PROFILE</div>
                        <div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC;">👤 {st.session_state.user_name}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button("🚪 Switch Profile", key="logout_btn", width="stretch"):
                st.session_state["user_id"] = None
                st.session_state["user_name"] = None
                st.session_state["workout_started"] = False
                st.rerun()
            
        st.divider()
        
        st.subheader("📋 Exercise Routine")
        
        if not workout_started:
            selected_exercise = st.selectbox(
                "Target Exercise",
                options=EXERCISE_OPTIONS,
                key="plan_exercise",
            )
            
            st.number_input("Target Sets", min_value=1, max_value=50, value=3, key="plan_sets", step=1)
            st.number_input("Reps per Set", min_value=1, max_value=50, value=10, key="plan_reps", step=1)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            start_session_button = st.button("⚡ Start Session", width="stretch", key="start_session_button", type="primary")
            
            if start_session_button:
                st.session_state["target_sets"] = st.session_state["plan_sets"]
                st.session_state["reps_per_set"] = st.session_state["plan_reps"]
                st.session_state["exercise_type"] = selected_exercise
                st.session_state["reps"] = 0
                st.session_state["sets_completed"] = 0
                st.session_state["current_set_reps"] = 0
                st.session_state["last_saved_reps"] = 0
                st.session_state["last_saved_sets_completed"] = 0
                st.session_state["set_cycle_started_at"] = time.time()
                st.session_state["workout_started"] = True

                if st.session_state.get("voice_pipeline"):
                    result = st.session_state.voice_pipeline.process_event(
                        event="workout_started",
                        exercise=selected_exercise,
                        metrics={},
                    )
                    if result:
                        st.session_state.current_audio = result[0]
                        st.session_state.current_audio_id = time.time()
                        st.session_state.coach_feedback = result[1]

                st.rerun()
                
        else:
            exercise = st.session_state.get("exercise_type")
            sets = st.session_state.get("plan_sets")
            reps = st.session_state.get("plan_reps")
            
            st.info(f"🎯 **{exercise}**\n\n📊 Target: {sets} Sets × {reps} Reps")
            
            end_session_button = st.button("🛑 End Session", key="end_session_button", width="stretch")
            
            if end_session_button:
                st.session_state["workout_started"] = False
                st.rerun()

        if workout_started:
            @st.fragment(run_every=1.0)
            def render_sidebar_metrics():
                ex = st.session_state.get("exercise_type", "Squats")
                total_reps = st.session_state.get("reps", 0)
                current_set_reps = st.session_state.get("current_set_reps", 0)
                reps_per_set = st.session_state.get("reps_per_set", 0)
                sets_completed = st.session_state.get("sets_completed", 0)
                target_sets = st.session_state.get("target_sets", 0)

                st.divider()
                st.subheader("🔥 Live Workout Stats")
                st.metric("Total Reps Completed", f"{total_reps}")
                st.metric("Current Set Progress", f"{current_set_reps} / {reps_per_set}")
                st.metric("Sets Finished", f"{sets_completed} / {target_sets}")

                st.divider()

                if ex == "Squats":
                    st.subheader("📐 Squat Posture")
                    st.metric("Knee Angle", f"{st.session_state.get('knee_angle', 0)}°")
                    st.metric("Back Angle", f"{st.session_state.get('back_angle', 0)}°")
                    st.metric("Depth Rating", st.session_state.get("depth_status", "N/A"))

                elif ex == "Push-ups":
                    st.subheader("📐 Push-up Form")
                    st.metric("Elbow Angle", f"{st.session_state.get('elbow_angle', 0)}°")
                    st.metric("Body Alignment", st.session_state.get("body_alignment", "N/A"))
                    st.metric("Hip Position", st.session_state.get("hip_status", "N/A"))

                elif ex == "Biceps Curls (Dumbbell)":
                    st.subheader("📐 Curl Stability")
                    st.metric("Elbow Flexion", f"{st.session_state.get('elbow_angle', 0)}°")
                    st.metric("Shoulder Drift", st.session_state.get("shoulder_status", "N/A"))
                    st.metric("Torso Swing", st.session_state.get("swing_status", "N/A"))

                elif ex == "Shoulder Press":
                    st.subheader("📐 Press Form")
                    st.metric("Elbow Angle", f"{st.session_state.get('elbow_angle', 0)}°")
                    st.metric("Arm Extension", st.session_state.get("extension_status", "N/A"))
                    st.metric("Lower Back Arch", st.session_state.get("back_arch_status", "N/A"))

                elif ex == "Lunges":
                    st.subheader("📐 Lunge Balance")
                    st.metric("Front Knee Flex", f"{st.session_state.get('front_knee_angle', 0)}°")
                    st.metric("Torso Incline", f"{st.session_state.get('torso_angle', 0)}°")
                    st.metric("Lateral Balance", st.session_state.get("balance_status", "N/A"))

            render_sidebar_metrics()

    workout_started = st.session_state.get("workout_started", False)
    if not workout_started:
        st.session_state["exercise_type"] = st.session_state.get("plan_exercise")
    active_exercise = st.session_state.get("exercise_type")

    # App Main Header
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(18, 24, 38, 0.8), rgba(30, 41, 59, 0.5));
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px 28px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            backdrop-filter: blur(16px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        ">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                    <span style="font-size: 1.8rem;">⚡</span>
                    <h2 style="margin: 0; font-size: 1.8rem !important; background: linear-gradient(135deg, #00F2FE, #4FACFE); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI GYM STUDIO</h2>
                </div>
                <p style="margin: 0; color: #94A3B8; font-size: 0.95rem;">Real-Time Computer Vision & Voice Form Feedback</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.session_state.get("voice_error"):
        st.warning("⚠️ Voice coaching API unavailable. Check Groq API configuration.")

    if not workout_started:
        st.markdown(
            """
            <div style="
                background: rgba(18, 24, 38, 0.6);
                border: 2px dashed rgba(0, 242, 254, 0.25);
                border-radius: 18px;
                padding: 48px 32px;
                text-align: center;
                margin: 24px 0;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            ">
                <div style="font-size: 3.2rem; margin-bottom: 12px;">🏋️‍♂️</div>
                <h2 style="color: #F8FAFC; margin-bottom: 8px;">Configure Your Session</h2>
                <p style="font-size: 1.05rem; color: #94A3B8; max-width: 520px; margin: 0 auto 20px auto;">
                    Select your exercise routine in the sidebar and click <strong>Start Session</strong> to activate your live AI camera coach.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        context = webrtc_streamer(
            key="exercise-analysis",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=lambda exercise=active_exercise: VideoProcessorClass(exercise),
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={
                "video": True,
                "audio": False
            },
            async_processing=True
        )

        @st.fragment(run_every=1.0)
        def live_workout_monitor(_ctx):
            sync_metrics_update(_ctx)

            if st.session_state.get("current_audio"):
                autoplay_audio(
                    st.session_state.current_audio,
                    st.session_state.get("current_audio_id")
                )

            if st.session_state.get("coach_feedback"):
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.15));
                        border: 1px solid rgba(16, 185, 129, 0.4);
                        border-radius: 14px;
                        padding: 16px 20px;
                        margin-top: 16px;
                        margin-bottom: 20px;
                        display: flex;
                        align-items: center;
                        gap: 14px;
                        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.15);
                    ">
                        <span style="font-size: 1.8rem;">🤖</span>
                        <div>
                            <div style="font-size: 0.75rem; font-weight: 700; color: #10B981; letter-spacing: 0.05em; text-transform: uppercase;">AI COACH VOICE FEEDBACK</div>
                            <div style="font-size: 1.05rem; font-weight: 600; color: #F8FAFC; margin-top: 2px;">{st.session_state.coach_feedback}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        live_workout_monitor(context)

        inject_webrtc_styles()

    st.divider()
    st.markdown("### 📊 Workout History & Performance")

    user_id = st.session_state.get("user_id", 0)

    if isinstance(user_id, int):
        history_rows = get_users_exercises(user_id)

        arr = [
            {
                "Exercise": row['exercise_name'],
                "Reps": row['reps'],
                "Sets": row['sets'],
                "Time (sec)": row['time'],
                "Date": row['created_at']
            }
            for row in history_rows
        ]

        df = pd.DataFrame(arr)

        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            agg_df = df.groupby(["Exercise", "Date"]).agg({
                "Reps": 'sum',
                "Sets": "sum",
                "Time (sec)": "sum"
            }).reset_index()
            agg_df.index += 1
            st.table(agg_df)
        else:
            st.info("No recorded exercise history yet. Complete a set to log your progress!")
        
    
if __name__=="__main__":
    main()