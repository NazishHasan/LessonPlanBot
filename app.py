import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="EduSpark AI Studio - ADPA Lesson Plan Generator",
    page_icon="🇦🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Secure API Key Management (Groq)
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.sidebar.warning("Groq API Key not found in Secrets. Please provide it below:")
    user_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    if user_key:
        client = Groq(api_key=user_key)
    else:
        client = None

# Initialize Session State variables
if "lesson_plan" not in st.session_state:
    st.session_state.lesson_plan = ""
if "component_output" not in st.session_state:
    st.session_state.component_output = ""
if "active_component_name" not in st.session_state:
    st.session_state.active_component_name = "Framework Component Output"

# Helper function to query Groq
def call_groq(prompt_text):
    if not client:
        return "⚠️ Error: Groq API client is not configured. Please add your key."
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_text}],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error communicating with Groq API: {str(e)}"

# 3. Sidebar UI (Lesson Parameters)
with st.sidebar:
    st.markdown("### 🇦🇪 EduSpark AI Studio")
    st.caption("ADPA UAE-Aligned Smart Lesson Builder")
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
    generate_btn = st.button("⚡ Generate Full ADPA Lesson Plan", type="primary", use_container_width=True)

# 4. Layout: 3 Columns
# Left: Full Workspace | Center: Specific Component Tools | Right: Copilot
col_workspace, col_components, col_copilot = st.columns([1.5, 1.2, 1.1])

# --- COLUMN 1: FULL WORKSPACE OUTPUT ---
with col_workspace:
    st.subheader("📝 Main Workspace Plan")
    
    if generate_btn:
        if not topic or not objectives:
            st.error("⚠️ Please fill in both the Topic and Learning Objectives to start.")
        else:
            with st.spinner("Generating full framework via Groq..."):
                base_prompt = f"""
                You are an expert curriculum designer specializing in the UAE ADPA (Abu Dhabi Performance Assessment) Framework.
                Generate a comprehensive, structured lesson plan based on these parameters:
                - Grade: {grade}
                - Subject: {subject}
                - Topic: {topic}
                - Learning Objectives: {objectives}
                - Duration: {time_duration} minutes
                - Focus: {', '.join(differentiation)}
                
                Organize clearly into standard sections.
                """
                st.session_state.lesson_plan = call_groq(base_prompt)
    
    if st.session_state.lesson_plan:
        st.markdown(st.session_state.lesson_plan)
        st.divider()
        st.download_button(
            label="📥 Download Full Plan (.txt)",
            data=st.session_state.lesson_plan,
            file_name=f"ADPA_{topic.replace(' ', '_')}_Lesson_Plan.txt",
            mime="text/plain"
        )
    else:
        st.info("👋 Fill out the sidebar and click 'Generate Full ADPA Lesson Plan' to start your macro setup, or use the component panel to build it piece by piece!")

# --- COLUMN 2: SPECIFIC ADPA FRAMEWORK COMPONENTS ---
with col_components:
    st.subheader("🛠️ Framework Blocks")
    st.caption("Click a button to generate a specific sub-framework element")
    
    # Grid Layout for your 13 options
    comp_col1, comp_col2 = st.columns(2)
    
    # We will track which button is clicked and what prompt context it needs
    selected_component = None
    component_instruction = ""
    
    with comp_col1:
        if st.button("📋 Matching Standards", use_container_width=True):
            selected_component = "📋 Matching Standards"
            component_instruction = "Generate highly relevant curriculum benchmarks and educational standards alignment for this grade and topic."
            
        if st.button("💡 Essential Question", use_container_width=True):
            selected_component = "💡 Essential Question / Big Idea"
            component_instruction = "Develop deep, inquiry-driven core statements and open-ended big questions that challenge student critical thinking."

        if st.button("🌍 Real-Life Connections", use_container_width=True):
            selected_component = "🌍 Real-Life Connections"
            component_instruction = "Provide actionable ways to apply these academic concepts directly to real-world industries, technologies, or societal contexts."

        if st.button("🔗 Interdisciplinary", use_container_width=True):
            selected_component = "🔗 Interdisciplinary Connections"
            component_instruction = "Show direct links mapping this topic cleanly into another learning subject (e.g., connecting Science with Art or Math with History)."

        if st.button("🇦🇪 UAE National Identity", use_container_width=True):
            selected_component = "🇦🇪 UAE National Identity"
            component_instruction = "Incorporate UAE culture, local history, heritage, environmental achievements, or national strategy initiatives connected to this topic."

        if st.button("🌟 Learner Profiles", use_container_width=True):
            selected_component = "🌟 Learner Profile Attributes"
            component_instruction = "Outline student-centric attributes (like IB Learner profile descriptions or 21st-century skills) targeted across this task."

        if st.button("📝 Pre-Assessment (5 MCQ)", use_container_width=True):
            selected_component = "📝 Pre-Assessment (5 MCQs)"
            component_instruction = "Draft a 5-question multiple choice diagnostic test complete with an answer key to gauge prior student understanding."

    with comp_col2:
        if st.button("🔥 Independent Task", use_container_width=True):
            selected_component = "🔥 Independent Learning Task"
            component_instruction = "Design a differentiated individual learning assignment split into 3 student tiers: Mild (Scaffolded), Medium (Standard/Targeted), and Spicy (Extension/Challenge)."

        if st.button("👥 Group Practice", use_container_width=True):
            selected_component = "👥 Group Practice (Max 20 mins)"
            component_instruction = "Construct a high-collaboration single-session interactive group challenge engineered to be accomplished inside a 20-minute window."

        if st.button("🚀 PBL Ideas", use_container_width=True):
            selected_component = "🚀 PBL Ideas"
            component_instruction = "Propose creative, long-term Project-Based Learning experiences and student project prompts tied to this subject framework."

        if st.button("♿ Students of Det. (SOD)", use_container_width=True):
            selected_component = "♿ Students of Determination (SOD)"
            component_instruction = "Provide strict inclusive support mechanisms, assistive accommodations, and concrete scaffolding instructions for SOD requirements."

        if st.button("🎫 Exit Ticket", use_container_width=True):
            selected_component = "🎫 Exit Ticket"
            component_instruction = "Formulate a quick, highly reflective, 3-minute check-for-understanding prompt or exit card assignment."

        if st.button("🎯 Post-Assessment (3 MCQ)", use_container_width=True):
            selected_component = "🎯 Post-Assessment (3 MCQs)"
            component_instruction = "Compose a 3-question multiple choice summative evaluation tool along with an answer key for direct post-lesson feedback."

    # If any component button was selected, make the API call right away
    if selected_component and component_instruction:
        if not topic or not objectives:
            st.error("⚠️ Make sure you have entered a Topic and Objectives in the sidebar first!")
        else:
            with st.spinner(f"Generating {selected_component}..."):
                prompt = f"""
                You are a premium curriculum architect aligning content with UAE standards.
                Task: Generate the '{selected_component}' element.
                Context parameters:
                - Grade/Year: {grade}
                - Subject: {subject}
                - Lesson Topic: {topic}
                - Stated Learning Objectives: {objectives}
                
                Instruction: {component_instruction}
                Return ONLY clean text/markdown ready for copy-pasting.
                """
                st.session_state.component_output = call_groq(prompt)
                st.session_state.active_component_name = selected_component

    # --- THE INTERACTIVE TEXT AREA WITH COPY OPTION ---
    st.divider()
    st.markdown(f"##### 🔲 {st.session_state.active_component_name}")
    
    # Render the interactive text area filled with the generated component data
    # (Users can edit it manually if they want, or select all to copy)
    text_content = st.text_area(
        label="Copy or edit the snippet text below:", 
        value=st.session_state.component_output, 
        height=320,
        help="Select the text area text, or copy directly using the right-side layout tool."
    )
    
    # Built-in Streamlit Copy Link alternative: download or standard system block copy support
    if st.session_state.component_output:
        st.caption("💡 *Tip: Streamlit's built-in code/text boxes let you mouse over the top-right corner to copy with 1-click, or you can manually use Ctrl+A & Ctrl+C inside the box.*")

# --- COLUMN 3: AI COPILOT REFINEMENT PANEL ---
with col_copilot:
    st.subheader("🤖 AI Copilot")
    st.caption("Apply sweeping fixes to the main active layout")
    
    st.write("✨ **Quick Refinements:**")
    add_quiz = st.button("📝 Add Extra Quiz Items", use_container_width=True)
    more_sen = st.button("🤝 Deepen Support Strategies", use_container_width=True)
    time_breakdown = st.button("⏱️ Create Detailed Pacing", use_container_width=True)
    
    st.divider()
    
    chip_instruction = ""
    if add_quiz: chip_instruction = "Expand the assessment metrics by attaching additional custom quiz tracking options."
    if more_sen: chip_instruction = "Deepen inclusion scaffolding adjustments across all target lesson blocks."
    if time_breakdown: chip_instruction = "Provide an exact, comprehensive minute-by-minute pace structure tracking how to guide this entire agenda."

    user_instruction = st.text_input("💬 Custom adjustments...", placeholder="e.g., Translate vocabulary to Arabic...")
    submit_instruction = st.button("Apply to Plan", use_container_width=True)
    
    final_instruction = user_instruction if submit_instruction else chip_instruction
    
    if final_instruction:
        if not st.session_state.lesson_plan:
            st.error("Please generate a full base plan in the workspace column before requesting edits.")
        else:
            with st.spinner("Copilot adapting layout..."):
                refinement_prompt = f"""
                You are editing a master lesson plan draft.
                CURRENT PLAN:
                ---
                {st.session_state.lesson_plan}
                ---
                USER AMENDMENT DIRECTION: "{final_instruction}"
                Return the fully reconstructed, integrated markdown text schema cleanly.
                """
                st.session_state.lesson_plan = call_groq(refinement_prompt)
                st.rerun()
