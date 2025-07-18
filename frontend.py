import streamlit as st
import os
from backend import CareerNavigatorBackend
from datetime import datetime
import time

st.set_page_config(
    page_title="Career Navigator AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #e7f3ff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    
    .question-box {
        background: #fff3cd;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    .evaluation-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #667eea;
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'backend' not in st.session_state:
    st.session_state.backend = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'interview_questions' not in st.session_state:
    st.session_state.interview_questions = []
if 'interview_answers' not in st.session_state:
    st.session_state.interview_answers = []
if 'interview_evaluations' not in st.session_state:
    st.session_state.interview_evaluations = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'interview_active' not in st.session_state:
    st.session_state.interview_active = False

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Career Navigator AI</h1>
        <p>Your AI-Powered Career Advancement Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### 🔧 Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Enter GROQ API Key",
            type="password",
            help="Your GROQ API key for AI services"
        )
        
        if api_key:
            if st.session_state.backend is None:
                try:
                    with st.spinner("Initializing AI backend..."):
                        st.session_state.backend = CareerNavigatorBackend(api_key)
                    st.success("✅ AI Backend initialized successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to initialize: {str(e)}")
                    return
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📋 Navigation")
        page = st.radio(
            "Select Feature",
            ["📄 Resume Analysis", "🎯 ATS Feedback", "📝 Resume Summary", "🎤 Interview Simulation"]
        )
        
        st.markdown("---")
        
        # Info section
        st.markdown("### ℹ️ Features")
        st.markdown("""
        - **Resume Analysis**: Complete resume evaluation
        - **ATS Feedback**: Applicant Tracking System scoring
        - **Resume Summary**: Professional summary generation
        - **Interview Simulation**: AI-powered interview practice
        """)

    # Main content area
    if not api_key:
        st.markdown("""
        <div class="info-box">
            <h3>🔑 Welcome to Career Navigator AI</h3>
            <p>Please enter your GROQ API key in the sidebar to get started.</p>
            <p>This platform provides comprehensive career services including:</p>
            <ul>
                <li>Resume Analysis & Optimization</li>
                <li>ATS Compatibility Scoring</li>
                <li>Professional Resume Summaries</li>
                <li>AI-Powered Interview Simulations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return

    if st.session_state.backend is None:
        st.warning("⚠️ Please wait for the AI backend to initialize...")
        return

    # File upload section (common for most features)
    if page in ["📄 Resume Analysis", "🎯 ATS Feedback", "📝 Resume Summary", "🎤 Interview Simulation"]:
        st.markdown("### 📁 Upload Your Resume")
        
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx'],
            help="Upload PDF or DOCX format resume"
        )
        
        if uploaded_file is not None:
            with st.expander("📋 File Details", expanded=False):
                st.write(f"**Filename:** {uploaded_file.name}")
                st.write(f"**File Size:** {uploaded_file.size} bytes")
                st.write(f"**File Type:** {uploaded_file.type}")

    # Page routing
    if page == "📄 Resume Analysis":
        show_resume_analysis(uploaded_file)
    elif page == "🎯 ATS Feedback":
        show_ats_feedback(uploaded_file)
    elif page == "📝 Resume Summary":
        show_resume_summary(uploaded_file)
    elif page == "🎤 Interview Simulation":
        show_interview_simulation(uploaded_file)

def show_resume_analysis(uploaded_file):
    st.markdown("### 📊 Complete Resume Analysis")
    
    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("🔍 Analyze Resume", key="analyze_btn"):
                with st.spinner("🔄 Analyzing your resume..."):
                    results = st.session_state.backend.analyze_resume(uploaded_file)
                    st.session_state.analysis_results = results
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            if results.get('success'):
                st.markdown('<div class="success-message">✅ Resume analysis completed successfully!</div>', unsafe_allow_html=True)
                
                # Display results in organized sections
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Role identification
                    st.markdown("#### 🎯 Identified Role")
                    st.markdown(f"**{results['role']}**")
                    
                    # ATS Feedback
                    st.markdown("#### 📈 ATS Feedback")
                    st.markdown(f"```\n{results['ats_feedback']}\n```")
                    
                    # Resume Summary
                    st.markdown("#### 📝 Professional Summary")
                    st.markdown(f"```\n{results['summary']}\n```")
                
                with col2:
                    # Keywords
                    st.markdown("#### 🔑 Extracted Keywords")
                    if results['keywords']:
                        for keyword in results['keywords'][:10]:  # Show top 10
                            st.markdown(f"• {keyword}")
                    else:
                        st.markdown("No keywords extracted")
                    
                    # Quick stats
                    st.markdown("#### 📊 Quick Stats")
                    st.markdown(f"**Text Length:** {len(results['resume_text'])} characters")
                    st.markdown(f"**Keywords Found:** {len(results['keywords'])}")
                    st.markdown(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                
            else:
                st.markdown(f'<div class="error-message">❌ Analysis failed: {results.get("error", "Unknown error")}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">📁 Please upload a resume file to begin analysis.</div>', unsafe_allow_html=True)

def show_ats_feedback(uploaded_file):
    st.markdown("### 🎯 ATS Compatibility Analysis")
    
    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("📊 Get ATS Score", key="ats_btn"):
                with st.spinner("🔄 Analyzing ATS compatibility..."):
                    resume_text = st.session_state.backend.extract_text_from_file(uploaded_file)
                    ats_feedback = st.session_state.backend.get_ats_feedback(resume_text)
                    st.session_state.ats_result = ats_feedback
        
        if hasattr(st.session_state, 'ats_result'):
            st.markdown("#### 📈 ATS Analysis Results")
            st.markdown(f"```\n{st.session_state.ats_result}\n```")
            
            # Additional tips
            st.markdown("#### 💡 ATS Optimization Tips")
            st.markdown("""
            - Use standard section headings (Experience, Education, Skills)
            - Include relevant keywords from job descriptions
            - Use simple, clean formatting
            - Avoid images, tables, and complex layouts
            - Save in ATS-friendly formats (PDF or DOCX)
            - Use standard fonts (Arial, Calibri, Times New Roman)
            """)
    else:
        st.markdown('<div class="info-box">📁 Please upload a resume file to get ATS feedback.</div>', unsafe_allow_html=True)

def show_resume_summary(uploaded_file):
    st.markdown("### 📝 Professional Resume Summary")
    
    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("📄 Generate Summary", key="summary_btn"):
                with st.spinner("🔄 Generating professional summary..."):
                    resume_text = st.session_state.backend.extract_text_from_file(uploaded_file)
                    summary = st.session_state.backend.summarize_resume(resume_text)
                    st.session_state.summary_result = summary
        
        if hasattr(st.session_state, 'summary_result'):
            st.markdown("#### 📋 Generated Summary")
            st.markdown(f"```\n{st.session_state.summary_result}\n```")
            
            # Copy to clipboard button
            if st.button("📋 Copy Summary"):
                st.success("Summary copied to clipboard! (Feature simulated)")
            
            # Usage tips
            st.markdown("#### 💡 How to Use This Summary")
            st.markdown("""
            - Add to your LinkedIn profile
            - Use in cover letters
            - Include in email signatures
            - Adapt for different job applications
            - Use as elevator pitch talking points
            """)
    else:
        st.markdown('<div class="info-box">📁 Please upload a resume file to generate a summary.</div>', unsafe_allow_html=True)

def show_interview_simulation(uploaded_file):
    st.markdown("### 🎤 AI Interview Simulation")
    
    if uploaded_file is not None:
        # First, analyze resume to get role
        if st.session_state.analysis_results is None:
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🔍 Analyze for Interview", key="interview_analyze_btn"):
                    with st.spinner("🔄 Analyzing resume for interview preparation..."):
                        results = st.session_state.backend.analyze_resume(uploaded_file)
                        st.session_state.analysis_results = results
        
        if st.session_state.analysis_results and st.session_state.analysis_results.get('success'):
            role = st.session_state.analysis_results['role']
            
            st.markdown(f"#### 🎯 Interview Role: **{role}**")
            
            # Interview controls
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                if st.button("🎤 Start Interview", key="start_interview"):
                    st.session_state.interview_active = True
                    st.session_state.current_question_index = 0
                    st.session_state.interview_questions = []
                    st.session_state.interview_answers = []
                    st.session_state.interview_evaluations = []
            
            with col2:
                if st.button("📝 Generate New Question", key="new_question"):
                    if st.session_state.interview_active:
                        with st.spinner("🔄 Generating new question..."):
                            question_result = st.session_state.backend.conduct_interview_session(role)
                            if question_result['success']:
                                st.session_state.interview_questions.append(question_result['question'])
            
            with col3:
                if st.button("🛑 End Interview", key="end_interview"):
                    st.session_state.interview_active = False
            
            # Interview session
            if st.session_state.interview_active:
                st.markdown("---")
                
                # Current question
                if st.session_state.interview_questions:
                    current_q_index = len(st.session_state.interview_questions) - 1
                    current_question = st.session_state.interview_questions[current_q_index]
                    
                    st.markdown(f"""
                    <div class="question-box">
                        <h4>❓ Interview Question {current_q_index + 1}</h4>
                        <p><strong>{current_question}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Answer input
                    answer = st.text_area(
                        "Your Answer:",
                        key=f"answer_{current_q_index}",
                        height=100,
                        placeholder="Type your answer here..."
                    )
                    
                    if st.button("✅ Submit Answer", key=f"submit_{current_q_index}"):
                        if answer.strip():
                            with st.spinner("🔄 Evaluating your answer..."):
                                evaluation = st.session_state.backend.evaluate_answer(role, current_question, answer)
                                st.session_state.interview_answers.append(answer)
                                st.session_state.interview_evaluations.append(evaluation)
                        else:
                            st.warning("Please provide an answer before submitting.")
                
                # Show previous Q&As
                if st.session_state.interview_evaluations:
                    st.markdown("#### 📊 Previous Questions & Evaluations")
                    
                    for i, (q, a, e) in enumerate(zip(
                        st.session_state.interview_questions[:-1] if len(st.session_state.interview_questions) > 1 else [],
                        st.session_state.interview_answers,
                        st.session_state.interview_evaluations
                    )):
                        with st.expander(f"Question {i+1}: {q[:50]}..."):
                            st.markdown(f"**Question:** {q}")
                            st.markdown(f"**Your Answer:** {a}")
                            st.markdown(f"""
                            <div class="evaluation-box">
                                <h5>📋 Evaluation</h5>
                                <p>{e}</p>
                            </div>
                            """, unsafe_allow_html=True)
            
            # Interview tips
            st.markdown("#### 💡 Interview Tips")
            st.markdown("""
            - **Be Specific**: Use concrete examples and numbers
            - **STAR Method**: Situation, Task, Action, Result
            - **Ask Questions**: Show genuine interest in the role
            - **Stay Calm**: Take your time to think before answering
            - **Practice**: The more you practice, the more confident you'll become
            """)
    else:
        st.markdown('<div class="info-box">📁 Please upload a resume file to start interview simulation.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()