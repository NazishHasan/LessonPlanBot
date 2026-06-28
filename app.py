import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="TeacherBot - UAE Schools' Lesson Plan Generator",
    page_icon="🇦🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Secure API Key Management (Groq)
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["Teacher_API"])
else:
    # Fallback for local testing
    st.sidebar.warning("Groq API Key not found in Secrets. Please provide it below:")
    user_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    if user_key:
        client = Groq(api_key=user_key)
    else:
        client = None

# Initialize Session State variables to store the generated outputs
if "lesson_plan" not in st.session_state:
    st.session_state.lesson_plan = ""

# Helper function to query Groq using Llama 3.3 70B
def call_groq(prompt_text):
    if not client:
        return "⚠️ Error: Groq API client is not configured. Please add your key."
    try:
        # llama-3.3-70b-versatile is excellent for curriculum and complex structuring
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_text,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error communicating with Groq API: {str(e)}"

# 3. Sidebar UI (Lesson Parameters)
with st.sidebar:
    st.markdown("### 🇦🇪 EduSpark AI Studio")
    st.caption("ADPA UAE-Aligned Smart Lesson Builder (Powered by Groq)")
    st.divider()
    
    st.markdown("#### **Lesson Parameters**")
    grade = st.selectbox("Grade Level / Year", [f"Grade {i}" for i in range(1, 13)] + [f"Year {i}" for i in range(1, 14)])
    subject = st.selectbox("Subject / Course", ["Mathematics", "Science", "English Language Arts", "Social Studies", "Moral Education", "Islamic Studies", "Arabic Language", "Computing / ICT"])
    topic = st.text_input("Lesson Topic", placeholder="e.g., Sustainable Eco-Cities")
    objectives = st.text_area("Learning Objectives (LOs)", placeholder="What should students know or be able to do?")
    
    with st.expander("Advanced Settings"):
        time_duration = st.slider("Lesson Duration (Minutes)", 30, 120, 60, step=5)
        differentiation = st.multiselect("Differentiation Focus", ["SEN Support", "G&T (Gifted & Talented)", "ELL / Language Support"], default=["SEN Support"])

    st.write("")
    generate_btn = st.button("⚡ Generate ADPA Lesson Plan", type="primary", use_container_width=True)

# 4. Main Workspace UI Layout
col_workspace, col_copilot = st.columns([2, 1])

# Left Column: Workspace & Output Preview
with col_workspace:
    st.subheader("📝 Workspace Output Preview")
    
    if generate_btn:
        if not topic or not objectives:
            st.error("⚠️ Please fill in both the Topic and Learning Objectives to start.")
        else:
            with st.spinner("Analyzing parameters & mapping to ADPA framework via Groq..."):
                base_prompt = f"""
                You are an expert curriculum designer specializing in the UAE ADPA (Abu Dhabi Performance Assessment) Framework.
                Generate a highly comprehensive, structured lesson plan based on these parameters:
                - Grade: {grade}
                - Subject: {subject}
                - Topic: {topic}
                - Learning Objectives: {objectives}
                - Duration: {time_duration} minutes
                - Special Alignment Focus: {', '.join(differentiation)}
                
                Please organize the output perfectly using clear markdown sections (Objectives, Direct Instruction, Guided Practice, Differentiation, Formative Assessment).
                """
                st.session_state.lesson_plan = call_groq(base_prompt)
    
    if st.session_state.lesson_plan:
        st.markdown(st.session_state.lesson_plan)
        st.divider()
        st.download_button(
            label="📥 Download Lesson Plan (.txt)",
            data=st.session_state.lesson_plan,
            file_name=f"ADPA_{topic.replace(' ', '_')}_Lesson_Plan.txt",
            mime="text/plain"
        )
    else:
        st.info("👋 Welcome to EduSpark AI Studio! Fill out the fields in the left sidebar and click 'Generate' to create your lesson framework.")

# Right Column: Copilot & Real-Time Refinements
with col_copilot:
    st.subheader("🤖 AI Copilot")
    st.caption("Refine or adjust your active workspace setup instantly")
    
    st.write("✨ **Quick Refinements:**")
    chip_col1, chip_col2 = st.columns(2)
    with chip_col1:
        add_quiz = st.button("📝 Add 5-Question Quiz", use_container_width=True)
        more_sen = st.button("🤝 Expand SEN Accommodations", use_container_width=True)
    with chip_col2:
        make_interactive = st.button("🎮 Add Interactive Activity", use_container_width=True)
        time_breakdown = st.button("⏱️ Create Timing Breakdown", use_container_width=True)
    
    st.divider()
    
    chip_instruction = ""
    if add_quiz: chip_instruction = "Add a 5-question multiple choice quiz with an answer key at the end of the current lesson plan."
    if more_sen: chip_instruction = "Expand the differentiation section to include highly specific, actionable strategies for SEN (Special Educational Needs) students."
    if make_interactive: chip_instruction = "Include a hands-on, interactive student activity or gamified element aligned with this lesson topic."
    if time_breakdown: chip_instruction = "Provide a minute-by-minute timeline structure detailing how to pace this entire lesson framework."

    user_instruction = st.text_input("💬 Ask Copilot to rewrite or add something...", placeholder="e.g., Translate the vocabulary to Arabic...")
    submit_instruction = st.button("Apply Instruction", use_container_width=True)
    
    final_instruction = user_instruction if submit_instruction else chip_instruction
    
    if final_instruction:
        if not st.session_state.lesson_plan:
            st.error("Please generate a base lesson plan first before applying adjustments.")
        else:
            with st.spinner("Copilot adapting your script via Groq..."):
                refinement_prompt = f"""
                You are a co-editor helping refine a teacher's lesson plan.
                Here is the CURRENT lesson plan:
                ---
                {st.session_state.lesson_plan}
                ---
                The user wants you to modify/update it with this instruction: "{final_instruction}"
                Return the completely updated, full lesson plan integrating this new adjustment cleanly. Maintain proper markdown structure.
                """
                st.session_state.lesson_plan = call_groq(refinement_prompt)
                st.rerun()
