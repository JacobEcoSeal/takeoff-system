# streamlit_app.py
"""EcoSeal Takeoff System - INTERFACE"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="EcoSeal Takeoff System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 0px;
    }
    .step-header {
        color: #2E86AB;
        border-bottom: 2px solid #2E86AB;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .success-box {
        background-color: #D4EDDA;
        border: 1px solid #28A745;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #FFF3CD;
        border: 1px solid #FFC107;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Logo / Header
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.markdown("🔧")
with col2:
    st.title("EcoSeal Insulation Takeoff System")

st.markdown("**Fast, accurate insulation quantity takeoffs from architectural plans**")
st.divider()

# Sidebar
with st.sidebar:
    st.header("📋 Navigation")
    
    page = st.radio(
        "Select section:",
        [
            "New Takeoff",
            "Recent Projects",
            "Settings"
        ],
        key="page_nav"
    )
    
    st.divider()
    st.markdown("### Quick Stats")
    st.metric("Projects this month", "12")
    st.metric("Total takeoffs", "47")
    
    st.divider()
    st.markdown("### About")
    st.info("""
    Streamlit Interface (v0.1)
    
    Backend: Coming soon
    
    [Documentation](#) | [Support](#)
    """)

# ============================================================================
# PAGE: NEW TAKEOFF
# ============================================================================

if page == "New Takeoff":
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'project_data' not in st.session_state:
        st.session_state.project_data = {}
    
    # Progress bar
    progress_pct = (st.session_state.step / 7) * 100
    st.progress(progress_pct / 100, text=f"Step {st.session_state.step} of 7")
    
    # ==================== STEP 0: PROJECT INFO ====================
    if st.session_state.step == 0:
        
        st.markdown("### Step 0️⃣ Project Information", help="Basic project details")
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input(
                "Project Name",
                placeholder="e.g., Riverside Towers Phase 2B",
                value=st.session_state.project_data.get('project_name', '')
            )
            st.session_state.project_data['project_name'] = project_name
        
        with col2:
            project_date = st.date_input(
                "Date",
                value=datetime.now()
            )
            st.session_state.project_data['project_date'] = str(project_date)
        
        st.text_area(
            "Project Notes (optional)",
            placeholder="e.g., Multi-family residential, 5 storeys, wood frame...",
            value=st.session_state.project_data.get('project_notes', ''),
            height=100
        )
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True, disabled=True):
                pass
        with col2:
            if st.button("Next →", use_container_width=True):
                if project_name:
                    st.session_state.step = 1
                    st.rerun()
                else:
                    st.error("Please enter a project name")
    
    # ==================== STEP 1: UPLOAD PDF ====================
    elif st.session_state.step == 1:
        
        st.markdown("### Step 1️⃣ Upload Plan PDF", help="Upload architectural drawings")
        st.divider()
        
        st.info("📄 **Supported formats:** PDF (vector or scanned)")
        
        uploaded_file = st.file_uploader(
            "Upload floor plan PDF",
            type="pdf",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            # Simulate file upload
            st.markdown(f"""
            <div class="success-box">
            ✓ <b>File uploaded:</b> {uploaded_file.name}<br>
            ✓ <b>Format:</b> Vector PDF (extractable)
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.project_data['pdf_name'] = uploaded_file.name
            st.session_state.project_data['pdf_pages'] = 35
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.step = 0
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True, disabled=(not uploaded_file)):
                st.session_state.step = 2
                st.rerun()
    
    # ==================== STEP 2: SELECT SHEETS ====================
    elif st.session_state.step == 2:
        
        st.markdown("### Step 2️⃣ Select Floor Plan & Schedule Sheets", help="Choose which PDF pages to use")
        st.divider()
        
        # Simulate PDF preview
        st.markdown("**Available pages in PDF:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Floor Plan Sheets**")
            floor_plan_1 = st.checkbox("Page 1: Floor Plan L2-3", value=True)
            floor_plan_2 = st.checkbox("Page 2: Floor Plan L3-4", value=True)
            floor_plan_3 = st.checkbox("Page 3: Floor Plan L4-5", value=False)
        
        with col2:
            st.markdown("**Section Sheets**")
            section_1 = st.checkbox("Page 4: Section A-A", value=False)
        
        with col3:
            st.markdown("**Schedule Sheets**")
            schedule = st.checkbox("Page 5: Wall Schedule", value=True)
            details = st.checkbox("Page 6: Details", value=False)
        
        st.markdown("---")
        
        # Show selected floor plans
        st.markdown("**Selected Floor Plans:**")
        selected_plans = []
        if floor_plan_1:
            selected_plans.append("• Page 1: Floor Plan L2-3")
        if floor_plan_2:
            selected_plans.append("• Page 2: Floor Plan L3-4")
        if floor_plan_3:
            selected_plans.append("• Page 3: Floor Plan L4-5")
        
        for plan in selected_plans:
            st.markdown(plan)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True):
                st.session_state.step = 3
                st.rerun()
    
    # ==================== STEP 3: SCALE DETECTION ====================
    elif st.session_state.step == 3:
        
        st.markdown("### Step 3️⃣ Scale Detection & Calibration", help="Ensure measurements are accurate")
        st.divider()
        
        # Create two columns: auto-detect and manual
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔍 Auto-Detect")
            st.markdown("System will look for scale ruler on the plan...")
            
            if st.button("Try Auto-Detect", use_container_width=True, key="auto_detect"):
                st.markdown("""
                <div class="success-box">
                ✓ <b>Scale detected:</b> 1/8" = 1'<br>
                ✓ <b>Confidence:</b> HIGH<br>
                ✓ <b>Scale factor:</b> 0.0533 pixels/foot
                </div>
                """, unsafe_allow_html=True)
                st.session_state.project_data['scale_method'] = 'auto'
                st.session_state.project_data['scale_value'] = '1/8" = 1\''
        
        with col2:
            st.markdown("#### 📏 Manual Calibration")
            st.markdown("If auto-detect fails, calibrate manually:")
            
            st.number_input("Distance between points (pixels):", value=100, key="pixels_dist")
            st.number_input("Actual distance (feet):", value=10.0, key="actual_dist")
            
            if st.button("Set Scale Manually", use_container_width=True, key="manual_scale"):
                st.markdown("""
                <div class="success-box">
                ✓ <b>Scale set:</b> 0.0533 pixels/foot
                </div>
                """, unsafe_allow_html=True)
                st.session_state.project_data['scale_method'] = 'manual'
        
        st.divider()
        
        # Show scale status
        if st.session_state.project_data.get('scale_method'):
            st.info(f"✓ Scale calibrated via {st.session_state.project_data.get('scale_method')} method")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True, disabled=(not st.session_state.project_data.get('scale_method'))):
                st.session_state.step = 4
                st.rerun()
    
    # ==================== STEP 4: EXTRACT BOUNDARY ====================
    elif st.session_state.step == 4:
        
        st.markdown("### Step 4️⃣ Extract Building Boundary", help="System calculates perimeter from plans")
        st.divider()
        
        st.info("Processing floor plan pages...")
        
        # Simulate progress
        progress_bar = st.progress(0)
        for i in range(101):
            progress_bar.progress(i / 100)
        
        st.markdown("""
        <div class="success-box">
        ✓ <b>Boundary extracted from Page 1 (L2-3):</b><br>
        &nbsp;&nbsp; Perimeter: <b>520.0 ft</b><br>
        &nbsp;&nbsp; Area: <b>38,440 sqft</b><br>
        <br>
        ✓ <b>Boundary extracted from Page 2 (L3-4):</b><br>
        &nbsp;&nbsp; Perimeter: <b>520.0 ft</b><br>
        &nbsp;&nbsp; Area: <b>38,440 sqft</b>
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state.project_data['boundary_extracted'] = True
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True):
                st.session_state.step = 5
                st.rerun()
    
    # ==================== STEP 5: WALL SCHEDULE ====================
    elif st.session_state.step == 5:
        
        st.markdown("### Step 5️⃣ Extract Wall Assemblies", help="Read wall types and R-values from schedule")
        st.divider()
        
        st.info("Reading Wall Schedule (Page 5) with Claude...")
        
        progress_bar = st.progress(0)
        for i in range(101):
            progress_bar.progress(i / 100)
        
        st.markdown("""
        <div class="success-box">
        ✓ <b>Schedule extracted successfully</b><br>
        ✓ Found 3 wall types with assemblies
        </div>
        """, unsafe_allow_html=True)
        
        # Show extracted assemblies
        st.markdown("**Detected Wall Assemblies:**")
        
        assemblies_data = {
            'Wall Type': ['EW-1', 'EW-2', 'IW-1'],
            'Description': ['Exterior Wall', 'Parapet', 'Interior Wall (optional)'],
            'Assembly': ['2x4 studs, 1.5" ccSPF, 6mil poly', '2x6 studs, 3.5" ccSPF, 6mil poly', '3.5" batt + 6mil poly'],
            'R-Value': ['R-24', 'R-30', 'R-13'],
            'Material': ['ccSPF', 'ccSPF', 'Batt'],
            'Confirmed': [True, True, False]
        }
        
        assemblies_df = pd.DataFrame(assemblies_data)
        
        # Editable dataframe
        edited_assemblies = st.data_editor(
            assemblies_df,
            use_container_width=True,
            key="assemblies_editor",
            hide_index=True,
            disabled=['Wall Type', 'Description']  # Can't edit these
        )
        
        st.session_state.project_data['assemblies'] = edited_assemblies.to_dict('records')
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.step = 4
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True):
                st.session_state.step = 6
                st.rerun()
    
    # ==================== STEP 6: FLOOR HEIGHTS ====================
    elif st.session_state.step == 6:
        
        st.markdown("### Step 6️⃣ Specify Floor Heights", help="Enter story heights from sections")
        st.divider()
        
        st.markdown("**Enter the height for each floor level:**")
        st.info("Tip: Find these dimensions in the section views (e.g., Section A-A)")
        
        st.divider()
        
        floors_data = {}
        
        col1, col2 = st.columns(2)
        
        # Floor 1
        with col1:
            st.markdown("#### Level 2-3")
            height_1 = st.number_input("Height (feet):", value=10.0, key="height_1")
            assembly_1 = st.selectbox("Wall Assembly:", ['EW-1', 'EW-2', 'IW-1'], key="asm_1")
            floors_data['L2-3'] = {'height': height_1, 'assembly': assembly_1}
        
        with col2:
            st.markdown("#### Level 3-4")
            height_2 = st.number_input("Height (feet):", value=10.5, key="height_2")
            assembly_2 = st.selectbox("Wall Assembly:", ['EW-1', 'EW-2', 'IW-1'], key="asm_2", index=0)
            floors_data['L3-4'] = {'height': height_2, 'assembly': assembly_2}
        
        col1, col2 = st.columns(2)
        
        # Floor 3
        with col1:
            st.markdown("#### Level 4-5")
            height_3 = st.number_input("Height (feet):", value=10.0, key="height_3")
            assembly_3 = st.selectbox("Wall Assembly:", ['EW-1', 'EW-2', 'IW-1'], key="asm_3", index=0)
            floors_data['L4-5'] = {'height': height_3, 'assembly': assembly_3}
        
        with col2:
            st.markdown("#### Roof Parapet")
            height_4 = st.number_input("Height (feet):", value=4.0, key="height_4")
            assembly_4 = st.selectbox("Wall Assembly:", ['EW-1', 'EW-2', 'IW-1'], key="asm_4", index=1)
            floors_data['Parapet'] = {'height': height_4, 'assembly': assembly_4}
        
        st.session_state.project_data['floors'] = floors_data
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.step = 5
                st.rerun()
        with col2:
            if st.button("Next →", use_container_width=True):
                st.session_state.step = 7
                st.rerun()
    
    # ==================== STEP 7: REVIEW & EXPORT ====================
    elif st.session_state.step == 7:
        
        st.markdown("### Step 7️⃣ Review & Export", help="Review takeoff and download results")
        st.divider()
        
        # Summary
        st.markdown("#### 📊 Takeoff Summary")
        
        summary_data = {
            'Material': ['ccSPF (Spray Foam)', 'Batt Insulation', 'Sealant/Firestopping'],
            'Quantity': ['17,140 sqft', '0 sqft', '2,080 lf'],
            'R-Value': ['R-24 avg', 'N/A', 'N/A']
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total ccSPF", "17,140 sqft")
        with col2:
            st.metric("Total Perimeter", "520 ft")
        with col3:
            st.metric("Avg R-Value", "R-27")
        
        st.divider()
        
        # Detail breakdown
        st.markdown("#### 📋 Item Breakdown")
        
        detail_data = {
            'Level': ['L2-3', 'L3-4', 'L4-5', 'Parapet'],
            'Wall Type': ['EW-1', 'EW-1', 'EW-1', 'EW-2'],
            'Material': ['ccSPF', 'ccSPF', 'ccSPF', 'ccSPF'],
            'Perimeter': ['520 ft', '520 ft', '520 ft', '520 ft'],
            'Height': ['10.0 ft', '10.5 ft', '10.0 ft', '4.0 ft'],
            'Quantity': ['5,200 sqft', '5,460 sqft', '5,200 sqft', '2,080 sqft'],
            'R-Value': ['R-24', 'R-24', 'R-24', 'R-30']
        }
        
        detail_df = pd.DataFrame(detail_data)
        st.dataframe(detail_df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Confidence & Source Trail
        st.markdown("#### ✓ Data Confidence")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🟢 **Scale:** Verified (auto-detected)")
        with col2:
            st.markdown("🟢 **Boundary:** Verified (vector PDF)")
        with col3:
            st.markdown("🟢 **Assemblies:** Confirmed (user reviewed)")
        
        st.divider()
        
        # Export buttons
        st.markdown("#### 📥 Download Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 CSV",
                data="Level,Wall Type,Material,Quantity,R-Value\nL2-3,EW-1,ccSPF,5200,R-24\nL3-4,EW-1,ccSPF,5460,R-24\nL4-5,EW-1,ccSPF,5200,R-24\nParapet,EW-2,ccSPF,2080,R-30",
                file_name=f"{st.session_state.project_data.get('project_name', 'takeoff')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                label="📄 PDF Report",
                data=b"PDF content here",
                file_name=f"{st.session_state.project_data.get('project_name', 'takeoff')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        with col3:
            if st.button("💾 Save Project", use_container_width=True, key="save_project"):
                st.success("✓ Project saved")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.step = 6
                st.rerun()
        with col2:
            if st.button("✨ New Takeoff", use_container_width=True):
                st.session_state.step = 0
                st.session_state.project_data = {}
                st.rerun()

# ============================================================================
# PAGE: RECENT PROJECTS
# ============================================================================

elif page == "Recent Projects":
    
    st.markdown("### 📂 Recent Projects", help="Your saved takeoff projects")
    st.divider()
    
    # Sample recent projects
    projects_data = {
        'Project': ['Riverside Towers Phase 2B', 'Downtown Infill (King St)', 'Lakefront Residences'],
        'Date': ['2026-02-24', '2026-02-22', '2026-02-20'],
        'Status': ['✓ Complete', '⏳ In Progress', '✓ Complete'],
        'Total ccSPF': ['17,140 sqft', '8,920 sqft', '12,500 sqft'],
    }
    
    projects_df = pd.DataFrame(projects_data)
    
    st.dataframe(
        projects_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    if st.button("+ Create New Takeoff", use_container_width=True):
        st.session_state.step = 0
        st.rerun()

# ============================================================================
# PAGE: SETTINGS
# ============================================================================

elif page == "Settings":
    
    st.markdown("### ⚙️ Settings", help="Configure system preferences")
    st.divider()
    
    st.markdown("#### API Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="Enter your API key...",
            help="Required for Claude schedule reading"
        )
        
        if api_key:
            st.success("✓ API key configured")
    
    with col2:
        model = st.selectbox(
            "Claude Model",
            ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229"],
            index=0
        )
    
    st.divider()
    
    st.markdown("#### Takeoff Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_material = st.selectbox(
            "Default Insulation Material",
            ["ccSPF", "Batt", "Blown-in", "Polyiso"]
        )
    
    with col2:
        default_tolerance = st.number_input(
            "Measurement Tolerance (%)",
            value=5,
            min_value=1,
            max_value=20
        )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Settings", use_container_width=True):
            st.success("✓ Settings saved")
    
    with col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.info("Reset to default settings")
