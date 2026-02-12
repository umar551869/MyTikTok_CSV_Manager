import streamlit as st
import pandas as pd
import re
import io
import base64

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="TikTok CSV Manager",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CUSTOM CSS & STYLING
# ==============================================================================
def load_css():
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }

        /* Gradient Background */
        .stApp {
            background: linear-gradient(135deg, #1e1e1e 0%, #0d0d0d 100%);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #111111;
            border-right: 1px solid #333;
        }

        /* Custom Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #FE2C55 0%, #FF0050 100%); /* TikTok Red */
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(254, 44, 85, 0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(254, 44, 85, 0.5);
            background: linear-gradient(90deg, #FF0050 0%, #FE2C55 100%);
        }

        /* Secondary Buttons (Outlines) */
        button[kind="secondary"] {
            background: transparent !important;
            border: 1px solid #FE2C55 !important;
            color: #FE2C55 !important;
        }

        /* Headers */
        h1, h2, h3 {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        h1 {
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }
        
        /* Card-like Containers */
        .css-1r6slb0, .css-12oz5g7 { 
            background-color: #252525;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid #333;
        }

        /* Expander Styling */
        .streamlit-expanderHeader {
            background-color: #252525;
            color: white;
            border-radius: 8px;
        }
        
        /* Data Editor/Frame */
        [data-testid="stDataFrame"] {
            border: 1px solid #333;
            border-radius: 8px;
            overflow: hidden;
        }

        /* Success/Info Messages */
        .stSuccess, .stInfo {
            background-color: #252525;
            color: white;
            border-left: 5px solid #FE2C55;
        }

        </style>
    """, unsafe_allow_html=True)

load_css()

# ==============================================================================
# SESSION STATE MANAGEMENT
# ==============================================================================
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'file_name' not in st.session_state:
    st.session_state['file_name'] = "data.csv"

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def to_csv_download_link(df, filename="data.csv", label="Download CSV"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-btn">{label}</a>'
    return st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime='text/csv',
    )

# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/TikTok_logo.svg/1200px-TikTok_logo.svg.png", width=150)
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "",
    ["🏠 Home", "📂 File Manager", "✍️ Data Editor", "📦 Batch Splitter", "🔍 Username Extractor"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("Developed By Muhammad Umar Ilyas")

# ==============================================================================
# MAIN PAGES
# ==============================================================================

# --- 1. HOME PAGE ---
if menu == "🏠 Home":
    st.markdown("<h1 style='font-size: 3rem;'>TikTok CSV Manager</h1>", unsafe_allow_html=True)
    st.markdown("### The ultimate tool for managing your Affiliate outreach data.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background-color: #252525; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #333;'>
            <h3 style='color: #25F4EE;'>Feature 1</h3>
            <p>Create & Edit CSVs easily with a spreadsheet-like interface.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background-color: #252525; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #333;'>
            <h3 style='color: #FE2C55;'>Feature 2</h3>
            <p>Split massive CSV files into smaller chunks for improved workflow.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background-color: #252525; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #333;'>
            <h3 style='color: #ffffff;'>Feature 3</h3>
            <p>Extract usernames cleanly from raw TikTok text dumps.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state['df'] is not None:
        st.success(f"✅ Active Data Loaded: **{st.session_state['file_name']}** ({st.session_state['df'].shape[0]} rows)")
        st.dataframe(st.session_state['df'].head(), use_container_width=True)
    else:
        st.warning("⚠️ No data loaded. Go to the **File Manager** to get started.")

# --- 2. FILE MANAGER (Create/Upload) ---
elif menu == "📂 File Manager":
    st.title("📂 File Manager")

    tab1, tab2 = st.tabs(["📤 Upload CSV", "🆕 Create New"])

    with tab1:
        st.subheader("Upload an existing CSV file")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state['df'] = df
                st.session_state['file_name'] = uploaded_file.name
                st.success(f"Successfully loaded **{uploaded_file.name}**!")
                st.dataframe(df.head(), use_container_width=True)
            except Exception as e:
                st.error(f"Error loading file: {e}")

    with tab2:
        st.subheader("Create a new CSV from scratch")
        col_names = st.text_input("Enter column names (comma-separated)", "Username, Status, Notes")
        if st.button("Create Empty DataFrame"):
            columns = [c.strip() for c in col_names.split(',')]
            st.session_state['df'] = pd.DataFrame(columns=columns)
            st.session_state['file_name'] = "new_data.csv"
            st.success("Created new empty DataFrame! Go to **Data Editor** to add rows.")
            st.dataframe(st.session_state['df'], use_container_width=True)

# --- 3. DATA EDITOR ---
elif menu == "✍️ Data Editor":
    st.title("✍️ Data Editor")

    if st.session_state['df'] is None:
        st.warning("No data loaded. Please upload or create a file first.")
    else:
        df = st.session_state['df']
        
        # --- Toolbar ---
        with st.expander("🛠️ columns & Tools", expanded=False):
            t1, t2, t3 = st.tabs(["Drop Columns", "Rename Columns", "Filter Rows"])
            
            with t1:
                cols_to_drop = st.multiselect("Select columns to drop", df.columns)
                if st.button("Drop Selected Columns"):
                    st.session_state['df'] = df.drop(columns=cols_to_drop)
                    st.rerun()

            with t2:
                c1, c2, c3 = st.columns([1,1,1])
                with c1: col_rename = st.selectbox("Select column", df.columns)
                with c2: new_name = st.text_input("New name")
                with c3: 
                    st.write("") # Spacer
                    st.write("") # Spacer
                    if st.button("Rename"):
                        st.session_state['df'] = df.rename(columns={col_rename: new_name})
                        st.rerun()

            with t3:
                c1, c2, c3 = st.columns([1,1,1])
                with c1: filter_col = st.selectbox("Filter by column", df.columns)
                with c2: filter_val = st.text_input("Contains value")
                with c3:
                    st.write("")
                    st.write("")
                    if st.button("Apply Filter"):
                        if filter_val:
                            filtered = df[df[filter_col].astype(str).str.contains(filter_val, case=False, na=False)]
                            st.session_state['df'] = filtered.reset_index(drop=True)
                            st.success(f"Filter matched {len(filtered)} rows.")
                            st.rerun()

        st.markdown("### Interactive Editor")
        st.markdown("Double-click cells to edit. Add/Delete rows using the table controls.")
        
        # Editable Dataframe
        edited_df = st.data_editor(
            st.session_state['df'],
            num_rows="dynamic",
            use_container_width=True,
            height=600
        )

        # Update session state with edits
        # Note: In Streamlit, data_editor returns the new dataframe. 
        # We update the session state only if the user manually saves or interacts? 
        # Actually, let's just update the state implicitly or have a save button?
        # Streamlit re-runs on edit, so 'edited_df' is the new state.
        
        if not edited_df.equals(st.session_state['df']):
             st.session_state['df'] = edited_df

        st.markdown("---")
        st.markdown("### Download")
        new_filename = st.text_input("Filename", st.session_state['file_name'])
        to_csv_download_link(edited_df, new_filename, "💾 Download CSV")

# --- 4. BATCH SPLITTER ---
elif menu == "📦 Batch Splitter":
    st.title("📦 Batch Splitter")

    if st.session_state['df'] is None:
        st.warning("No data loaded. Please upload a file first.")
    else:
        df = st.session_state['df']
        st.info(f"Current File: **{st.session_state['file_name']}** | Total Rows: **{len(df)}**")

        col1, col2 = st.columns(2)
        with col1:
            batch_size = st.number_input("Rows per batch", min_value=1, value=100, step=10)
        
        num_files = (len(df) + batch_size - 1) // batch_size
        with col2:
            st.metric("Files to Create", num_files)

        if st.button("🚀 Generate Batches", type="primary"):
            st.markdown("### Download Batches")
            
            # Create a container for the buttons
            grid = st.columns(min(3, num_files)) if num_files > 0 else []
            
            for i in range(0, len(df), batch_size):
                batch_num = (i // batch_size) + 1
                batch_df = df.iloc[i:i+batch_size]
                fname = f"outreach_part_{batch_num}.csv"
                
                # Dynamic column cycling
                col_idx = (batch_num - 1) % 3
                with grid[col_idx] if len(grid) > col_idx else st.container():
                     to_csv_download_link(batch_df, fname, f"⬇️ Part {batch_num} ({len(batch_df)} rows)")

# --- 5. USERNAME EXTRACTOR ---
elif menu == "🔍 Username Extractor":
    st.title("🔍 Username Extractor")
    st.markdown("Paste unstructured text below to extract `@usernames`.")

    text_input = st.text_area("Paste text here", height=300, placeholder="@user1 some text @user2 ...")

    if st.button("✨ Extract Usernames", type="primary"):
        if text_input.strip():
            # Regex pattern
            pattern = r'@?([a-zA-Z0-9_.]+)'
            matches = re.findall(pattern, text_input)

            # Clean and filter
            valid_usernames = []
            for m in matches:
                clean_name = m.strip()
                # Basic validation: length >= 3 and has at least one letter
                if len(clean_name) >= 3 and any(c.isalpha() for c in clean_name):
                    valid_usernames.append(clean_name)
            
            unique_users = sorted(list(set(valid_usernames)))
            
            if unique_users:
                st.success(f"Found {len(unique_users)} unique usernames!")
                
                # Create DataFrame
                result_df = pd.DataFrame({'username': unique_users})
                
                st.dataframe(result_df, use_container_width=True)
                
                # Options
                col1, col2 = st.columns(2)
                with col1:
                    to_csv_download_link(result_df, "extracted_usernames.csv", "💾 Download CSV")
                with col2:
                    if st.button("Load into Data Editor"):
                        st.session_state['df'] = result_df
                        st.session_state['file_name'] = "extracted_usernames.csv"
                        st.success("Loaded! Go to Data Editor to view/edit.")
            else:
                st.warning("No valid usernames found.")
        else:
            st.error("Please paste some text first.")
