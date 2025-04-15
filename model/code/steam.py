import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
import logging
from PIL import Image
import time
from collections import Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="Dog Behavior AI Analyzer",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI/UX with improved text visibility
st.markdown("""
    <style>
    :root {
        --primary: #4a6fa5;
        --secondary: #166088;
        --accent: #4fc3f7;
        --background: #f8f9fa;
        --card-bg: #ffffff;
        --text: #333333;
    }
    
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Roboto, sans-serif;
        word-wrap: break-word;
    }
    
    .main {
        background-color: var(--background);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--primary), var(--secondary));
        color: white;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: white;
        border-radius: 8px;
        padding: 12px 28px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .header-container {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-align: center;
        word-break: break-word;
        line-height: 1.2;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 0;
        line-height: 1.4;
    }
    
    .info-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 5px solid var(--accent);
        color: var(--text);
    }
    
    .result-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        color: var(--text);
    }
    
    .behavior-item {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        background-color: #f5f9ff;
        transition: all 0.3s ease;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: normal;
    }
    
    .dominant-behavior {
        background-color: #e3f2fd;
        border-left: 4px solid var(--accent);
        transform: scale(1.01);
    }
    
    .progress-container {
        height: 8px;
        background: #e0e0e0;
        margin-top: 8px;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--accent), var(--primary));
        border-radius: 4px;
    }
    
    .video-preview {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .timeline {
        background-color: #f5f9ff;
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        overflow-x: auto;
        white-space: normal;
        word-break: break-word;
    }
    
    .timeline-chunk {
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.8rem;
        }
        .header-subtitle {
            font-size: 1rem;
        }
        .info-card, .result-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_behavior_model():
    try:
        model = load_model("D:/Final_year project/trained_model.h5")
        logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        st.error("Failed to load the behavior recognition model")
        return None

# TensorFlow Model Prediction
def model_prediction(frame, model):
    try:
        if model is None:
            logger.error("Model not loaded")
            return None
            
        input_arr = tf.keras.preprocessing.image.img_to_array(frame)
        input_arr = np.expand_dims(input_arr, axis=0)
        predictions = model.predict(input_arr)
        return np.argmax(predictions)
    except Exception as e:
        logger.error(f"Error in model prediction: {str(e)}")
        return None

# Sidebar - Simplified navigation
with st.sidebar:
    st.title("🐶 Dog Behavior AI")
    st.markdown("---")
    st.markdown("### Navigation")
    app_mode = st.radio("", ["Behavior Analysis"])
    
    st.markdown("---")
    st.markdown("### Model Info")
    st.info("""
    This AI model analyzes dog behaviors:
    - Aggressive
    - Digging/Chewing
    - Fear
    - Resting
    - Tail Tucking
    """)

# Main Content
st.markdown("""
<div class="header-container">
    <h1 class="header-title">Dog Behavior AI Analyzer</h1>
    <p class="header-subtitle">Upload a dog video to analyze its behavior using advanced AI</p>
</div>
""", unsafe_allow_html=True)

# Info card
st.markdown("""
<div class="info-card">
    <h3>How to use</h3>
    <ol>
        <li>Upload a video of a dog (MP4, MOV, or AVI format)</li>
        <li>The system will process 1 frame per second</li>
        <li>View the detailed behavior analysis results</li>
    </ol>
    <p><small>For best results, use clear, well-lit videos with the dog clearly visible.</small></p>
</div>
""", unsafe_allow_html=True)

uploaded_video = st.file_uploader(
    "📁 Upload Dog Video", 
    type=["mp4", "mov", "avi"],
    help="Clear, well-lit videos work best for accurate analysis"
)

if uploaded_video is not None:
    # Display video preview
    st.markdown("### Video Preview")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="video-preview">', unsafe_allow_html=True)
        tfile = uploaded_video.name
        with open(tfile, "wb") as f:
            f.write(uploaded_video.read())
        st.video(tfile)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        cap = cv2.VideoCapture(tfile)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame, caption="Sample Frame", use_container_width=True)
        cap.release()
    
    # Process video
    if st.button("🔍 Analyze Behavior", key="analyze_btn"):
        model = load_behavior_model()
        if model is None:
            st.error("Failed to load model. Please check the logs.")
            st.stop()
        
        cap = cv2.VideoCapture(tfile)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        
        st.info(f"📊 Video Info: {total_frames} frames at {frame_rate} FPS")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        results = []
        class_names = ['Aggressive', 'Digging/Chewing', 'Fear', 'Resting', 'Tail Tucking']
        
        try:
            for i in range(total_frames):
                ret, frame = cap.read()
                if not ret:
                    break
                
                if i % frame_rate == 0:  # Process 1 frame per second
                    frame_resized = cv2.resize(frame, (224, 224))
                    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                    result_index = model_prediction(frame_rgb, model)
                    
                    if result_index is not None:
                        results.append(class_names[result_index])
                
                # Update progress
                progress = int((i + 1) / total_frames * 100)
                progress_bar.progress(progress)
                status_text.text(f"🔄 Processing frame {i+1}/{total_frames} ({progress}%)")
            
            cap.release()
            
            if results:
                # Calculate behavior statistics
                behavior_counts = Counter(results)
                total_detections = len(results)
                dominant_behavior = max(behavior_counts, key=behavior_counts.get)
                
                # Display results
                st.markdown("""
                <div class="result-card">
                    <h2>📊 Analysis Results</h2>
                    <p>Based on analysis of {total_detections} video frames (1 per second)</p>
                </div>
                """.format(total_detections=total_detections), unsafe_allow_html=True)
                
                # Overall prediction card
                st.markdown(f"""
                <div class="result-card" style="background: linear-gradient(135deg, #f5f9ff, #e3f2fd);">
                    <h3>🏆 Dominant Behavior</h3>
                    <div style="display: flex; align-items: center; gap: 1rem; margin: 1rem 0;">
                        <div style="font-size: 2.5rem; color: var(--primary);">🐕</div>
                        <div>
                            <h2 style="margin: 0; color: var(--secondary);">{dominant_behavior}</h2>
                            <p style="margin: 0; color: var(--text);">
                                Detected in {behavior_counts[dominant_behavior]} of {total_detections} frames 
                                ({behavior_counts[dominant_behavior]/total_detections:.1%})
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed breakdown
                st.markdown("""
                <div class="result-card">
                    <h3>📈 Behavior Distribution</h3>
                    <p>Percentage of time spent in each behavior:</p>
                """, unsafe_allow_html=True)
                
                for behavior, count in behavior_counts.most_common():
                    percentage = count / total_detections * 100
                    is_dominant = behavior == dominant_behavior
                    div_class = "behavior-item dominant-behavior" if is_dominant else "behavior-item"
                    
                    st.markdown(f"""
                    <div class="{div_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-weight: {'600' if is_dominant else '500'};">
                                {behavior}
                            </div>
                            <div style="font-weight: {'600' if is_dominant else '500'};">
                                {count} ({percentage:.1f}%)
                            </div>
                        </div>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {percentage}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)  # Close result-card div
                
                # Timeline visualization
                st.markdown("""
                <div class="result-card">
                    <h3>⏱ Behavior Timeline</h3>
                    <p>Sequence of detected behaviors (1 detection per second):</p>
                    <div class="timeline">
                """, unsafe_allow_html=True)
                
                # Display timeline in chunks to prevent overflow
                chunk_size = 10
                for i in range(0, len(results), chunk_size):
                    chunk = results[i:i + chunk_size]
                    st.markdown(f"""
                    <div class="timeline-chunk">
                        {" → ".join(chunk)}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)  # Close timeline and result-card divs
            else:
                st.warning("No behaviors detected in the video. Please try with a different video.")
        
        except Exception as e:
            logger.error(f"Error in video processing: {str(e)}")
            st.error("An error occurred during video processing. Please check the logs.")
            if cap.isOpened():
                cap.release()