import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
def load_css(theme="Dark"):
    # Theme colors
    if theme == "Dark":
        bg_gradient = "linear-gradient(135deg, #1e1e1e 0%, #0d0d0d 100%)"
        sidebar_bg = "#111111"
        card_bg = "#252525"
        text_color = "#ffffff"
        border_color = "#333333"
        secondary_text = "#bbbbbb"
        accent_blue = "#25F4EE"
    else:  # Light Mode
        bg_gradient = "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)"
        sidebar_bg = "#ffffff"
        card_bg = "#ffffff"
        text_color = "#1a1a1a"
        border_color = "#dee2e6"
        secondary_text = "#495057"
        accent_blue = "#007bff"

    tiktok_red = "#FE2C55"

    st.markdown(f"""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /* Global Styles - Cross-browser compatible */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            color: {text_color} !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* Specific text overrides for Streamlit components */
        .stMarkdown, .stText, p, span, label, .stMetric, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {text_color} !important;
        }}

        /* Gradient Background with vendor prefixes */
        .stApp {{
            background: {bg_gradient};
            background: -webkit-{bg_gradient};
            background: -moz-{bg_gradient};
            background: -o-{bg_gradient};
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {border_color};
        }}
        
        /* Sidebar Text Overrides */
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {{
            color: {text_color} !important;
        }}

        /* Custom Buttons with vendor prefixes */
        .stButton > button {{
            background: linear-gradient(90deg, {tiktok_red} 0%, #FF0050 100%);
            background: -webkit-linear-gradient(90deg, {tiktok_red} 0%, #FF0050 100%);
            background: -moz-linear-gradient(90deg, {tiktok_red} 0%, #FF0050 100%);
            color: white !important;
            border: none;
            border-radius: 0.625rem;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            -webkit-transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 0.25rem 0.9375rem rgba(254, 44, 85, 0.2);
            cursor: pointer;
        }}
        .stButton > button:hover {{
            transform: translateY(-0.125rem);
            -webkit-transform: translateY(-0.125rem);
            box-shadow: 0 0.5rem 1.5625rem rgba(254, 44, 85, 0.4);
            filter: brightness(1.1);
            -webkit-filter: brightness(1.1);
        }}

        /* Secondary Buttons */
        button[kind="secondary"] {{
            background: transparent !important;
            border: 2px solid {tiktok_red} !important;
            color: {tiktok_red} !important;
        }}

        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
            font-weight: 700 !important;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 2rem;
            letter-spacing: -0.0625rem;
        }}
        
        /* Custom Card Component */
        .custom-card {{
            background-color: {card_bg};
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 0.625rem 1.875rem rgba(0,0,0,0.05);
            border: 1px solid {border_color};
            transition: all 0.3s ease;
            -webkit-transition: all 0.3s ease;
            margin-bottom: 1rem;
        }}
        .custom-card p {{
            color: {secondary_text} !important;
        }}
        .custom-card:hover {{
            transform: translateY(-0.3125rem);
            -webkit-transform: translateY(-0.3125rem);
            box-shadow: 0 0.9375rem 2.1875rem rgba(0,0,0,0.1);
            border-color: {tiktok_red}50;
        }}

        /* Expander Styling */
        .streamlit-expanderHeader {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border-radius: 0.75rem;
            border: 1px solid {border_color};
        }}
        
        /* Data Editor/Frame */
        [data-testid="stDataFrame"] {{
            border: 1px solid {border_color};
            border-radius: 0.75rem;
            overflow: hidden;
            background-color: {card_bg};
        }}

        /* Metrics - Consistent sizing */
        [data-testid="stMetric"] {{
            background-color: {card_bg};
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid {border_color};
        }}
        [data-testid="stMetricValue"] {{
            font-weight: 800 !important;
            color: {tiktok_red} !important;
            font-size: 1.5rem !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {secondary_text} !important;
            font-size: 0.875rem !important;
        }}

        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 1.5rem;
        }}
        .stTabs [data-baseweb="tab"] {{
            color: {secondary_text} !important;
            padding: 0.75rem 1.5rem;
        }}
        .stTabs [aria-selected="true"] {{
            border-bottom: 3px solid {tiktok_red} !important;
            color: {tiktok_red} !important;
        }}

        /* Success/Info Messages */
        .stSuccess, .stInfo, .stWarning, .stError {{
            border-radius: 0.75rem;
            border: none;
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border-left: 0.3125rem solid {tiktok_red} !important;
            padding: 1rem;
        }}

        /* Selectbox/Input Styling */
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{
            background-color: {card_bg} !important;
            border-radius: 0.625rem !important;
            border-color: {border_color} !important;
            color: {text_color} !important;
        }}
        
        /* Fix for input text visibility */
        input {{
            color: {text_color} !important;
            background-color: {card_bg} !important;
        }}
        
        /* Tooltip */
        .stTooltipIcon {{
            color: {tiktok_red};
        }}

        /* Loading Spinner */
        .stSpinner > div {{
            border-top-color: {tiktok_red} !important;
        }}

        /* File Uploader */
        [data-testid="stFileUploader"] {{
            background-color: {card_bg};
            border: 2px dashed {border_color};
            border-radius: 0.75rem;
            padding: 2rem;
        }}

        /* Download Button */
        .stDownloadButton > button {{
            background: linear-gradient(90deg, {accent_blue} 0%, #00D4FF 100%);
            background: -webkit-linear-gradient(90deg, {accent_blue} 0%, #00D4FF 100%);
            color: white !important;
            border: none;
            border-radius: 0.625rem;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
        }}

        /* Toggle Switch - Fix for Light Mode Visibility */
        .stCheckbox {{
            color: {text_color} !important;
        }}
        
        /* Toggle switch track and thumb */
        input[type="checkbox"] {{
            background-color: {border_color} !important;
        }}
        
        /* For light mode - make toggle switch visible with dark border */
        section[data-testid="stSidebar"] input[type="checkbox"] {{
            border: 2px solid {'#333333' if theme == 'Light' else border_color} !important;
            background-color: {'#e0e0e0' if theme == 'Light' else card_bg} !important;
        }}
        
        section[data-testid="stSidebar"] label[data-baseweb="checkbox"] {{
            border: 2px solid {'#333333' if theme == 'Light' else 'transparent'} !important;
        }}

        </style>
    """, unsafe_allow_html=True)

# Apply selected theme
load_css(st.session_state.get('theme', 'Dark'))

# ==============================================================================
# SESSION STATE MANAGEMENT
# ==============================================================================
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'file_name' not in st.session_state:
    st.session_state['file_name'] = "data.csv"
if 'theme' not in st.session_state:
    st.session_state['theme'] = "Dark"

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

def parse_metric_value(value):
    """Parse string metrics like '1.2M', '$1K' into floats."""
    if pd.isna(value):
        return 0.0
    
    s = str(value).upper().replace('$', '').replace(',', '').replace('%', '').strip()
    
    multiplier = 1
    if 'K' in s:
        multiplier = 1000
        s = s.replace('K', '')
    elif 'M' in s:
        multiplier = 1000000
        s = s.replace('M', '')
    elif 'B' in s:
        multiplier = 1000000000
        s = s.replace('B', '')
        
    try:
        return float(s) * multiplier
    except:
        return 0.0

def extract_usernames_from_text(text):
    """
    Extract usernames using smart heuristics (PPS anchor) and fallback to regex.
    Returns: (list of usernames, list of debug strings)
    """
    debug_log = []
    
    if not text:
        return [], ["No text provided"]
        
    lines = [L.strip() for L in text.split('\n') if L.strip()]
    debug_log.append(f"Found {len(lines)} non-empty lines")
    
    smart_matches = []
    
    # Strategy 1: PPS Anchor
    # Pattern: Username is 2 lines above "PPS:"
    pps_found = False
    for i, line in enumerate(lines):
        # Case insensitive check for PPS
        if "PPS:" in line.upper():
            pps_found = True
            if i >= 2:
                candidate = lines[i-2]
                # Basic validation: no spaces, decent length, not a number
                # Usernames shouldn't contain spaces.
                if ' ' not in candidate and len(candidate) >= 3:
                    smart_matches.append(candidate)
                    debug_log.append(f"Line {i} PPS found -> Accepted candidate '{candidate}'")
                else:
                    debug_log.append(f"Line {i} PPS found -> Rejected candidate '{candidate}' (invalid format)")
            else:
                debug_log.append(f"Line {i} PPS found -> No candidate (index < 2)")
                
    if smart_matches:
        debug_log.append(f"Strategy 1 (PPS) Success: {len(smart_matches)} matches")
        return sorted(list(set(smart_matches))), debug_log
        
    debug_log.append("Strategy 1 (PPS) returned 0 valid matches. Falling back to regex.")
        
    # Strategy 2: Fallback Regex with Stronger Filtering
    pattern = r'@?([a-zA-Z0-9_.]+)'
    raw_matches = re.findall(pattern, text)
    debug_log.append(f"Regex found {len(raw_matches)} raw matches")
    
    # Expanded blacklist (lowercase for comparison)
    blacklist_set = {
        'health', 'male', 'female', 'previously', 'invited', 'fast', 'growing', 
        'pps:', 'pps', 'womenswear', 'underwear', 'beauty', 'personal', 'care',
        'sports', 'outdoor', 'ugc', 'level', 'deals', 'next', 'locked', 'mindset',
        'midlifemomgrace', 'soberafjoe', # Keep these if they are actually names in current text? No, safer to exclude if known noise
        'chenbo', 'unknown', 'creator', 'video', 'views', 'follower', 'sale', 'revenue'
    }
    
    cleaned_matches = []
    for m in raw_matches:
        clean = m.strip()
        clean_lower = clean.lower()
        
        # 1. Length Check
        if len(clean) < 3:
            continue
            
        # 2. Character Check (Must have at least one letter)
        if not any(c.isalpha() for c in clean):
            continue
            
        # 3. Blacklist Check (Case Insensitive)
        if clean_lower in blacklist_set:
            continue
            
        # 4. Symbol Check
        if any(x in clean for x in ['/', '%', '$', ',']):
            continue
            
        # 5. Number/Stat Check (e.g. 1.4K, 4.1, 5.0)
        # If it starts with a digit, it's suspicious unless it's mixed with sufficient letters
        if clean[0].isdigit():
            # If matches mostly numbers/dots/K/M/B
            if re.match(r'^[\d.]+[KMBkmb]?$', clean):
                continue
                
        cleaned_matches.append(clean)
            
    debug_log.append(f"Strategy 2 (Regex) Final: {len(cleaned_matches)} matches")
    return sorted(list(set(cleaned_matches))), debug_log

# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/a/a9/TikTok_logo.svg/1200px-TikTok_logo.svg.png", width=150)
st.sidebar.title("Navigation")

# Theme Toggle
col_t1, col_t2 = st.sidebar.columns([1, 1])
with col_t1:
    # Add dark text for light mode visibility
    if st.session_state['theme'] == "Light":
        st.markdown('<p style="color: #333333; margin: 0;">🌓 Theme</p>', unsafe_allow_html=True)
    else:
        st.write("🌓 Theme")
with col_t2:
    theme_choice = st.toggle("Dark Mode", value=(st.session_state['theme'] == "Dark"), label_visibility="collapsed")
    new_theme = "Dark" if theme_choice else "Light"
    if new_theme != st.session_state['theme']:
        st.session_state['theme'] = new_theme
        st.rerun()

menu = st.sidebar.radio(
    "",
    ["🏠 Home", "📂 File Manager", "✍️ Data Editor", "📦 Batch Splitter", "🔍 Username Extractor", "📊 Analytics & Processing"],
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
    
    # Theme-dependent card accent colors
    c1_color = "#25F4EE" if st.session_state['theme'] == "Dark" else "#007bff"
    c2_color = "#FE2C55"
    c3_color = "#ffffff" if st.session_state['theme'] == "Dark" else "#1a1a1a"

    with col1:
        st.markdown(f"""
        <div class="custom-card">
            <h3 style='color: {c1_color};'>✨ Data Editing</h3>
            <p>Create & Edit CSVs easily with a fluid spreadsheet interface and real-time validation.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="custom-card">
            <h3 style='color: {c2_color};'>📦 Batch Manager</h3>
            <p>Split massive CSV files into optimized chunks for your affiliate outreach campaigns.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="custom-card">
            <h3 style='color: {c3_color};'>🔍 Smart Extraction</h3>
            <p>High-confidence username extraction using AI-driven position-based heuristics.</p>
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

    tab1, tab2, tab3 = st.tabs(["📤 Upload CSV", "🆕 Create New", "🔗 Merge Files"])

    with tab1:
        st.subheader("Upload an existing CSV or Excel file")
        uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    # Auto-detect header row
                    detected_header = 0
                    try:
                        # Read first 20 rows to scan for headers
                        df_preview = pd.read_excel(uploaded_file, nrows=20, header=None)
                        
                        # Keywords to look for (based on user screenshot/standard TikTok export)
                        expected_cols = ['Creator name', 'Creator ID', 'Video ID', 'GMV', 'VV', 'Likes', 'Gross mer']
                        
                        max_matches = 0
                        for idx, row in df_preview.iterrows():
                            # Convert row to string and check for keywords
                            row_str = " ".join([str(x) for x in row.values if pd.notna(x)])
                            matches = sum(1 for kw in expected_cols if kw.lower() in row_str.lower())
                            
                            if matches > max_matches and matches >= 2: # At least 2 matches to be confident
                                max_matches = matches
                                detected_header = idx
                        
                        # Reset file pointer to beginning so we can read it again
                        uploaded_file.seek(0)
                        
                        if detected_header > 0:
                            st.info(f"💡 Auto-detected headers on Row {detected_header}. If incorrect, adjust below.")

                    except Exception as scan_e:
                        print(f"Header scan failed: {scan_e}")
                        uploaded_file.seek(0) # Ensure reset even on fail

                     # Add option for header row
                    header_row = st.number_input(
                        "Header Row Index (0 for first row, 1 for second, etc.)", 
                        min_value=0, 
                        value=detected_header, 
                        step=1,
                        help="If your Excel file has a title or empty rows at the top, increase this number until the correct headers are shown."
                    )
                    df = pd.read_excel(uploaded_file, header=header_row)

                st.session_state['df'] = df
                st.session_state['file_name'] = uploaded_file.name
                
                # Validation check
                if df.columns.str.contains('^Unnamed').any():
                    st.warning("⚠️ Some columns appear to be unnamed. You might need to adjust the 'Header Row Index' above if this is an Excel file.")

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

    with tab3:
        st.subheader("🔗 Merge Multiple Files")
        st.markdown("Combine multiple CSV/Excel files into one dataset.")
        
        uploaded_files = st.file_uploader(
            "Upload files to merge (2 or more)", 
            type=['csv', 'xlsx'], 
            accept_multiple_files=True,
            key='merge_uploader'
        )
        
        if uploaded_files and len(uploaded_files) >= 2:
            try:
                with st.spinner('Loading files...'):
                    dfs = []
                    file_info = []
                    
                    for file in uploaded_files:
                        if file.name.endswith('.csv'):
                            temp_df = pd.read_csv(file)
                        else:
                            temp_df = pd.read_excel(file)
                        
                        dfs.append(temp_df)
                        file_info.append({
                            'name': file.name,
                            'rows': len(temp_df),
                            'columns': len(temp_df.columns)
                        })
                    
                    # Display file info
                    st.markdown("#### Files to Merge")
                    info_df = pd.DataFrame(file_info)
                    st.dataframe(info_df, use_container_width=True)
                    
                    # Merge options
                    st.markdown("#### Merge Options")
                    merge_col1, merge_col2 = st.columns(2)
                    
                    with merge_col1:
                        merge_method = st.radio(
                            "Merge Method",
                            ["Stack (Append Rows)", "Join (Match Columns)"],
                            help="Stack: Combine all rows. Join: Match on common column."
                        )
                    
                    with merge_col2:
                        if merge_method == "Stack (Append Rows)":
                            handle_columns = st.radio(
                                "Column Handling",
                                ["Keep all columns", "Keep common columns only"],
                                help="How to handle different column names across files"
                            )
                        else:
                            # Get common columns
                            common_cols = set(dfs[0].columns)
                            for df in dfs[1:]:
                                common_cols = common_cols.intersection(set(df.columns))
                            
                            if common_cols:
                                join_col = st.selectbox("Join on Column", sorted(list(common_cols)))
                            else:
                                st.error("No common columns found across all files!")
                                st.stop()
                    
                    # Deduplication option
                    dedupe_after = st.checkbox("Remove duplicates after merge", value=True)
                    if dedupe_after:
                        # Get all columns from first file
                        dedupe_col = st.selectbox("Deduplicate by column", dfs[0].columns.tolist())
                    
                    if st.button("🚀 Merge Files", type="primary"):
                        with st.spinner('Merging files...'):
                            if merge_method == "Stack (Append Rows)":
                                if handle_columns == "Keep common columns only":
                                    # Find common columns
                                    common_cols = set(dfs[0].columns)
                                    for df in dfs[1:]:
                                        common_cols = common_cols.intersection(set(df.columns))
                                    
                                    # Keep only common columns
                                    dfs = [df[list(common_cols)] for df in dfs]
                                
                                merged_df = pd.concat(dfs, ignore_index=True)
                            else:
                                # Join method
                                merged_df = dfs[0]
                                for df in dfs[1:]:
                                    merged_df = merged_df.merge(df, on=join_col, how='outer', suffixes=('', '_dup'))
                            
                            # Deduplicate if requested
                            if dedupe_after and dedupe_col in merged_df.columns:
                                before_count = len(merged_df)
                                merged_df = merged_df.drop_duplicates(subset=[dedupe_col])
                                removed = before_count - len(merged_df)
                                if removed > 0:
                                    st.info(f"Removed {removed} duplicate rows based on '{dedupe_col}'")
                            
                            st.session_state['df'] = merged_df
                            st.session_state['file_name'] = f"merged_{len(uploaded_files)}_files.csv"
                            
                            st.success(f"✅ Successfully merged {len(uploaded_files)} files! Total rows: {len(merged_df)}")
                            st.dataframe(merged_df.head(20), use_container_width=True)
                            
                            # Download option
                            st.markdown("#### Download Merged File")
                            to_csv_download_link(merged_df, st.session_state['file_name'], "💾 Download Merged CSV")
                            
            except Exception as e:
                st.error(f"Error merging files: {e}")
                st.exception(e)
        elif uploaded_files and len(uploaded_files) < 2:
            st.warning("Please upload at least 2 files to merge.")


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
            
            # Store batches for download all functionality
            batch_files = []
            
            # Create a container for the buttons
            grid = st.columns(min(3, num_files)) if num_files > 0 else []
            
            for i in range(0, len(df), batch_size):
                batch_num = (i // batch_size) + 1
                batch_df = df.iloc[i:i+batch_size]
                fname = f"outreach_part_{batch_num}.csv"
                
                # Store batch data
                batch_files.append((fname, batch_df))
                
                # Dynamic column cycling
                col_idx = (batch_num - 1) % 3
                with grid[col_idx] if len(grid) > col_idx else st.container():
                     to_csv_download_link(batch_df, fname, f"⬇️ Part {batch_num} ({len(batch_df)} rows)")
            
            # Download All Button
            st.markdown("---")
            st.markdown("#### 📦 Download All Batches")
            
            if st.button("📥 Download All as ZIP", type="primary", key="download_all_zip"):
                import io
                import zipfile
                
                # Create zip file in memory
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for fname, batch_df in batch_files:
                        # Convert DataFrame to CSV string
                        csv_string = batch_df.to_csv(index=False)
                        # Add to zip
                        zip_file.writestr(fname, csv_string)
                
                # Offer download
                st.download_button(
                    label="💾 Download ZIP File",
                    data=zip_buffer.getvalue(),
                    file_name=f"all_batches_{num_files}_files.zip",
                    mime="application/zip",
                    key="zip_download_button"
                )
                st.success(f"✅ Created ZIP with {num_files} batch files!")


# --- 5. USERNAME EXTRACTOR ---
elif menu == "🔍 Username Extractor":
    st.title("🔍 Username Extractor")
    st.markdown("Paste unstructured text below to extract `@usernames`.")

    text_input = st.text_area("Paste text here", height=300, placeholder="@user1 some text @user2 ...")

    if st.button("✨ Extract Usernames (v2)", type="primary"):
        if text_input.strip():
            unique_users, debug_log = extract_usernames_from_text(text_input)
            
            with st.expander("🛠️ Debug Logs (Check this if results are wrong)"):
                st.code("\n".join(debug_log))
            
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

# --- 6. ANALYTICS & PROCESSING ---
elif menu == "📊 Analytics & Processing":
    st.title("📊 Analytics & Processing")

    if st.session_state['df'] is None:
        st.warning('No data loaded. Please upload or create a file first.')
    else:
        df = st.session_state['df'].copy()
        
        # --- 1. COLUMN SELECTION ---
        st.subheader('1. Column Selection')
        with st.expander('Select Columns to Keep', expanded=True):
            all_columns = df.columns.tolist()
            default_cols = all_columns
            selected_cols = st.multiselect('Choose columns', all_columns, default=default_cols)
            
            if selected_cols:
                df = df[selected_cols]
            else:
                st.warning('Please select at least one column.')
                st.stop()

        # --- 2. DATA PROCESSING ---
        st.subheader('2. Data Processing')
        
        c1, c2, c3 = st.columns(3)
        
        # Deduplication
        with c1:
            st.markdown('#### Deduplication')
            dedup_col = st.selectbox('Remove duplicates by', ['None'] + df.columns.tolist())
            if dedup_col != 'None':
                before_count = len(df)
                df = df.drop_duplicates(subset=[dedup_col])
                st.caption(f'Removed {before_count - len(df)} duplicates.')

        # Filter by Month
        with c2:
            st.markdown('#### Filter by Month')
            date_col = st.selectbox('Select Date Column', ['None'] + df.columns.tolist())
            if date_col != 'None':
                try:
                    # Convert to datetime temporarily
                    temp_dates = pd.to_datetime(df[date_col], errors='coerce')
                    df['bc_temp_date'] = temp_dates
                    
                    # Get unique months
                    available_months = sorted(list(set(df['bc_temp_date'].dt.strftime('%Y-%m').dropna())))
                    
                    selected_months = st.multiselect('Select Month(s)', available_months)
                    
                    if selected_months:
                        mask = df['bc_temp_date'].dt.strftime('%Y-%m').isin(selected_months)
                        df = df[mask]
                        st.caption(f'Filtered to {len(df)} rows.')
                    
                    # Cleanup
                    df = df.drop(columns=['bc_temp_date'])
                except Exception as e:
                    st.error(f'Error parsing dates: {e}')

        # Sorting
        with c3:
            st.markdown('#### Sorting')
            sort_col = st.selectbox('Sort by', ['None'] + df.columns.tolist())
            sort_order = st.radio('Order', ['Ascending', 'Descending'], horizontal=True)
            
            if sort_col != 'None':
                ascending = True if sort_order == 'Ascending' else False
                # Try to sort numerically if possible
                try:
                    # Create temp column for sorting to handle mix of strings/numbers
                    df['temp_sort'] = df[sort_col].apply(parse_metric_value)
                    df = df.sort_values(by='temp_sort', ascending=ascending).drop(columns=['temp_sort'])
                except:
                    # Fallback to standard sort
                    df = df.sort_values(by=sort_col, ascending=ascending)

        # --- ADVANCED FILTERING ---
        st.markdown('---')
        st.subheader('2.5 Advanced Filtering')
        
        with st.expander('🔍 Advanced Filters', expanded=False):
            filter_applied = False
            
            adv_c1, adv_c2, adv_c3 = st.columns(3)
            
            with adv_c1:
                st.markdown('**GMV Filter**')
                # Detect GMV column
                gmv_filter_col = None
                for col in df.columns:
                    if any(x in col.lower() for x in ['gmv', 'gross merchandise', 'revenue']):
                        gmv_filter_col = col
                        break
                
                if gmv_filter_col:
                    df['_temp_gmv'] = df[gmv_filter_col].apply(parse_metric_value)
                    min_gmv = st.number_input('Min GMV ($)', min_value=0, value=0, step=1000)
                    max_gmv = st.number_input('Max GMV ($)', min_value=0, value=1000000, step=10000)
                    
                    if min_gmv > 0 or max_gmv < 1000000:
                        df = df[(df['_temp_gmv'] >= min_gmv) & (df['_temp_gmv'] <= max_gmv)]
                        filter_applied = True
                    
                    df = df.drop(columns=['_temp_gmv'])
                else:
                    st.info('No GMV column detected')
            
            with adv_c2:
                st.markdown('**Video Count Filter**')
                # Detect video count column
                vid_count_col = None
                for col in df.columns:
                    if any(x in col.lower() for x in ['video count', 'videos', 'video id']):
                        vid_count_col = col
                        break
                
                if vid_count_col:
                    min_vids = st.number_input('Min Videos', min_value=0, value=0, step=1)
                    max_vids = st.number_input('Max Videos', min_value=1, value=1000, step=10)
                    
                    if 'video id' in vid_count_col.lower():
                        # Count unique video IDs per creator
                        creator_col_temp = None
                        for col in df.columns:
                            if 'creator' in col.lower() or 'name' in col.lower():
                                creator_col_temp = col
                                break
                        
                        if creator_col_temp:
                            vid_counts = df.groupby(creator_col_temp)[vid_count_col].nunique()
                            valid_creators = vid_counts[(vid_counts >= min_vids) & (vid_counts <= max_vids)].index
                            df = df[df[creator_col_temp].isin(valid_creators)]
                            filter_applied = True
                    else:
                        df['_temp_vids'] = pd.to_numeric(df[vid_count_col], errors='coerce').fillna(0)
                        df = df[(df['_temp_vids'] >= min_vids) & (df['_temp_vids'] <= max_vids)]
                        df = df.drop(columns=['_temp_vids'])
                        filter_applied = True
                else:
                    st.info('No video count column detected')
            
            with adv_c3:
                st.markdown('**Text Search**')
                search_col = st.selectbox('Search in column', ['None'] + df.columns.tolist(), key='adv_search_col')
                search_term = st.text_input('Search term', key='adv_search_term')
                
                if search_col != 'None' and search_term:
                    df = df[df[search_col].astype(str).str.contains(search_term, case=False, na=False)]
                    filter_applied = True
            
            if filter_applied:
                st.success(f'✅ Filters applied. Showing {len(df)} rows.')


        # Apply Changes Button (Implicitly handled by streamlits rerun on interaction, 
        # but good to show current state)
        st.success(f'Processing Complete. Current Rows: {len(df)}')
        
        with st.expander('View Processed Data'):
            st.dataframe(df, use_container_width=True)


        # --- 3. ANALYTICS DASHBOARD ---
        st.markdown('---')
        st.subheader('3. Analytics Dashboard')
        
        # Identify numeric columns for aggregation
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        # Also try to identify columns that look like money or views
        potential_metric_cols = [c for c in df.columns if any(x in c.lower() for x in ['view', 'gmv', 'video', 'follower', 'sale', 'revenue'])]
        
        # --- METRIC CARDS ---
        
        # Pre-calculate common metrics
        # We need to parse columns like 'Videos', 'GMV', 'Views' if they exist
        
        # Helper to get column case-insensitive and partial match
        def get_col(candidates):
            # First try exact match (case-insensitive)
            for c in df.columns:
                if any(x.lower() == c.lower() for x in candidates):
                    return c
            # Then try exact match on full column name
            for c in df.columns:
                for candidate in candidates:
                    if candidate.lower() == c.lower():
                        return c
            # Then try partial match (contains)
            for c in df.columns:
                if any(x.lower() in c.lower() for x in candidates):
                    return c
            return None

        # 1. Identify Key Columns
        video_count_col = get_col(['video count', 'videos_count']) 
        video_id_col = get_col(['video id', 'item id'])
        
        view_col = get_col(['video views', 'vv', 'views', 'view count'])
        if not view_col: view_col = get_col(['view'])

        gmv_col = get_col(['Gross merchandise value (Video) ($)', 'gross merchandise value (video) ($)', 'gmv', 'gross merchandise value', 'gross mer', 'revenue', 'sales', 'gpm', 'merchandise value'])
        
        creator_col = get_col(['creator name', 'creator', 'username', 'user'])
        
        # New: Engagement & Commerce Columns
        likes_col = get_col(['likes', 'like'])
        comments_col = get_col(['comments', 'comment'])
        shares_col = get_col(['shares', 'share'])
        orders_col = get_col(['orders', 'order', 'items sold'])

        # --- DATA PREPARATION ---
        # Clean and Parse Metrics
        if view_col:
            df['parsed_views'] = df[view_col].apply(parse_metric_value)
        
        if gmv_col:
            df['parsed_gmv'] = df[gmv_col].apply(parse_metric_value)
            
        for col, name in [(likes_col, 'parsed_likes'), (comments_col, 'parsed_comments'), (shares_col, 'parsed_shares'), (orders_col, 'parsed_orders')]:
            if col:
                 df[name] = df[col].apply(parse_metric_value)

        # Determine "Total Videos" and Creator Metrics Strategy
        total_videos = 0
        total_likes = 0
        total_orders = 0
        
        creators_1_2_vids = 0
        creators_3_9_vids = 0
        creators_10plus_vids = 0
        creators_10k_99k_gmv = 0
        creators_100k_999k_gmv = 0
        creators_1m_plus_gmv = 0
        
        mode = "Unknown"

        if video_id_col and creator_col:
            mode = "Granular (Video Level)"
            # Group by Creator to get creator-level stats
            agg_dict = {video_id_col: 'nunique'}
            if gmv_col: agg_dict['parsed_gmv'] = 'sum'
            if view_col: agg_dict['parsed_views'] = 'sum'
            if likes_col: agg_dict['parsed_likes'] = 'sum'
            if orders_col: agg_dict['parsed_orders'] = 'sum'
            
            creator_stats = df.groupby(creator_col).agg(agg_dict).rename(columns={video_id_col: 'video_count', 'parsed_gmv': 'total_gmv'})
            
            total_videos = df[video_id_col].nunique()
            if likes_col: total_likes = int(df['parsed_likes'].sum())
            if orders_col: total_orders = int(df['parsed_orders'].sum())
            
            creators_1_2_vids = len(creator_stats[(creator_stats['video_count'] >= 1) & (creator_stats['video_count'] <= 2)])
            creators_3_9_vids = len(creator_stats[(creator_stats['video_count'] >= 3) & (creator_stats['video_count'] <= 9)])
            creators_10plus_vids = len(creator_stats[creator_stats['video_count'] >= 10])
            
            if gmv_col:
                creators_10k_99k_gmv = len(creator_stats[(creator_stats['total_gmv'] >= 10000) & (creator_stats['total_gmv'] < 100000)])
                creators_100k_999k_gmv = len(creator_stats[(creator_stats['total_gmv'] >= 100000) & (creator_stats['total_gmv'] < 1000000)])
                creators_1m_plus_gmv = len(creator_stats[creator_stats['total_gmv'] >= 1000000])
                
        elif video_count_col:
            mode = "Aggregated (Creator Level)"
            # Rows are creators already
            df['parsed_videos'] = df[video_count_col].apply(lambda x: pd.to_numeric(x, errors='coerce')).fillna(0)
            total_videos = int(df['parsed_videos'].sum())
            if likes_col: total_likes = int(df['parsed_likes'].sum())
            
            creators_1_2_vids = len(df[(df['parsed_videos'] >= 1) & (df['parsed_videos'] <= 2)])
            creators_3_9_vids = len(df[(df['parsed_videos'] >= 3) & (df['parsed_videos'] <= 9)])
            creators_10plus_vids = len(df[df['parsed_videos'] >= 10])
            
            if gmv_col:
                creators_10k_99k_gmv = len(df[(df['parsed_gmv'] >= 10000) & (df['parsed_gmv'] < 100000)])
                creators_100k_999k_gmv = len(df[(df['parsed_gmv'] >= 100000) & (df['parsed_gmv'] < 1000000)])
                creators_1m_plus_gmv = len(df[df['parsed_gmv'] >= 1000000])
        
        else:
             mode = "Simple (Row Count)"
             total_videos = len(df)
             if creator_col:
                 creator_counts = df[creator_col].value_counts()
                 creators_1_2_vids = len(creator_counts[(creator_counts >= 1) & (creator_counts <= 2)])
                 creators_3_9_vids = len(creator_counts[(creator_counts >= 3) & (creator_counts <= 9)])
                 creators_10plus_vids = len(creator_counts[creator_counts >= 10])
                 
                 if gmv_col:
                     creator_gmv = df.groupby(creator_col)['parsed_gmv'].sum()
                     creators_10k_99k_gmv = len(creator_gmv[(creator_gmv >= 10000) & (creator_gmv < 100000)])
                     creators_100k_999k_gmv = len(creator_gmv[(creator_gmv >= 100000) & (creator_gmv < 1000000)])
                     creators_1m_plus_gmv = len(creator_gmv[creator_gmv >= 1000000])

        # Debug Info
        with st.expander("🛠️ Debug Information & Column Detection"):
            st.info(f"**Detected Mode:** {mode}")
            st.write(f"**Video ID:** `{video_id_col}` | **Creator:** `{creator_col}`")
            st.write(f"**GMV:** `{gmv_col}` | **Views:** `{view_col}`")
            st.write(f"**Likes:** `{likes_col}` (from 'Likes', 'Like')")
            st.write(f"**Orders:** `{orders_col}` (from 'Orders', 'Order')")

        
        # Display metrics in organized grid
        st.markdown('#### 📈 Key Metrics')
        md_c1, md_c2, md_c3, md_c4, md_c5 = st.columns(5)
        
        with md_c1:
            st.metric('Total Videos', f'{total_videos:,}')
        with md_c2:
            st.metric('Creators (1-2 vids)', creators_1_2_vids)
        with md_c3:
            st.metric('Creators (3-9 vids)', creators_3_9_vids)
        with md_c4:
            st.metric('Creators (10+ vids)', creators_10plus_vids)
        with md_c5:
            if likes_col:
                st.metric('Total Likes', f'{total_likes:,}')
            elif orders_col:
                st.metric('Total Orders', f'{total_orders:,}')

        if gmv_col:
            st.markdown('#### 💰 GMV Segmentation')
            gm_c1, gm_c2, gm_c3, gm_c4 = st.columns(4)
            with gm_c1:
                st.metric('$10K-$99K GMV', creators_10k_99k_gmv)
            with gm_c2:
                st.metric('$100K-$999K GMV', creators_100k_999k_gmv)
            with gm_c3:
                st.metric('$1M+ GMV', creators_1m_plus_gmv)
            with gm_c4:
                total_gmv = df['parsed_gmv'].sum() if 'parsed_gmv' in df.columns else 0
                st.metric('Total GMV', f'${total_gmv:,.0f}')

        # --- COMMISSION CALCULATOR ---
        if gmv_col:
            st.markdown('---')
            st.markdown('#### 💵 Commission Calculator')
            
            comm_c1, comm_c2 = st.columns([1, 2])
            
            with comm_c1:
                commission_rate = st.number_input(
                    'Commission Rate (%)',
                    min_value=0.0,
                    max_value=100.0,
                    value=10.0,
                    step=0.5,
                    help='Enter your commission percentage (e.g., 10 for 10%)'
                )
                
                total_commission = (total_gmv * commission_rate / 100) if total_gmv > 0 else 0
                st.metric('Total Commission', f'${total_commission:,.2f}')
                
                # Export commission report
                if st.button('📊 Generate Commission Report'):
                    if creator_col and mode == "Granular (Video Level)":
                        # Use creator_stats
                        comm_report = creator_stats.reset_index()
                        if 'total_gmv' in comm_report.columns:
                            comm_report['commission'] = comm_report['total_gmv'] * commission_rate / 100
                            comm_report = comm_report.sort_values('commission', ascending=False)
                            
                            # Select relevant columns
                            report_cols = [creator_col, 'video_count', 'total_gmv', 'commission']
                            if 'parsed_views' in comm_report.columns:
                                report_cols.insert(2, 'parsed_views')
                            
                            comm_report_export = comm_report[report_cols].copy()
                            comm_report_export.columns = ['Creator', 'Videos', 'Total Views', 'Total GMV', 'Commission'] if len(report_cols) == 5 else ['Creator', 'Videos', 'Total GMV', 'Commission']
                            
                            st.session_state['commission_report'] = comm_report_export
                    elif 'parsed_gmv' in df.columns:
                        # Create report from main df
                        comm_report = df.copy()
                        comm_report['commission'] = comm_report['parsed_gmv'] * commission_rate / 100
                        
                        if creator_col:
                            comm_summary = comm_report.groupby(creator_col).agg({
                                'parsed_gmv': 'sum',
                                'commission': 'sum'
                            }).reset_index()
                            comm_summary.columns = ['Creator', 'Total GMV', 'Commission']
                            comm_summary = comm_summary.sort_values('Commission', ascending=False)
                            st.session_state['commission_report'] = comm_summary
            
            with comm_c2:
                if 'commission_report' in st.session_state:
                    st.markdown('**Top Earners by Commission**')
                    st.dataframe(st.session_state['commission_report'].head(10), use_container_width=True)
                    
                    # Download button
                    to_csv_download_link(
                        st.session_state['commission_report'],
                        f'commission_report_{commission_rate}pct.csv',
                        '💾 Download Full Commission Report'
                    )
                else:
                    st.info('Click "Generate Commission Report" to see creator-level commissions.')




        # --- VISUALIZATIONS ---
        st.markdown('---')
        st.markdown('### 📊 Visualizations')
        
        # Basic Charts Row
        v1, v2 = st.columns(2)
        
        with v1:
            st.markdown('#### Top Creators')
            if mode == "Granular (Video Level)":
                 # Use the aggregated stats we calculated earlier
                 # creator_stats has index=Creator Name, columns=['video_count', 'total_gmv', 'parsed_views', etc]
                 top_creators = creator_stats.reset_index()
                 
                 # Decide metric to sort/color by
                 y_metric = 'video_count'
                 title_metric = 'Video Count'
                 color = 'video_count'
                 scale = 'Reds'
                 
                 if 'total_gmv' in top_creators.columns and top_creators['total_gmv'].sum() > 0:
                     y_metric = 'total_gmv'
                     title_metric = 'GMV'
                     color = 'total_gmv'
                     scale = 'Greens'
                 
                 top_df = top_creators.nlargest(10, y_metric)
                 
                 fig = px.bar(top_df, x=creator_col, y=y_metric, 
                              title=f'Top 10 Creators by {title_metric}',
                              color=color, color_continuous_scale=scale)
                 fig.update_layout(xaxis_tickangle=-45)
                 st.plotly_chart(fig, use_container_width=True)
                 
            elif mode == "Aggregated (Creator Level)" or (mode == "Simple (Row Count)" and creator_col):
                 # We are working with the main DF
                 # Try to find relevant columns
                 y_metric = None
                 title_metric = ''
                 scale = 'Reds'
                 
                 if 'parsed_gmv' in df.columns and df['parsed_gmv'].sum() > 0:
                     y_metric = 'parsed_gmv'
                     title_metric = 'GMV'
                     scale = 'Greens'
                 elif 'parsed_videos' in df.columns:
                     y_metric = 'parsed_videos'
                     title_metric = 'Video Count'
                     
                 if y_metric:
                     # Attempt to find name col
                     name_col = get_col(['name', 'creator', 'user', 'handle', 'username'])
                     if name_col:
                         top_df = df.nlargest(10, y_metric)
                         fig = px.bar(top_df, x=name_col, y=y_metric, 
                                      title=f'Top 10 Creators by {title_metric}',
                                      color=y_metric, color_continuous_scale=scale)
                         fig.update_layout(xaxis_tickangle=-45)
                         st.plotly_chart(fig, use_container_width=True)
                     else:
                         st.warning("Could not identify Creator Name column for chart.")
                 else:
                     st.info('Top Creators chart requires Videos or GMV column.')
            else:
                st.info("Could not determine Top Creators (needs Creator Name column).")

        with v2:
            st.markdown('#### Distributions')
            if view_col:
                fig2 = px.histogram(df, x='parsed_views', nbins=30, title='View Count Distribution',
                                    color_discrete_sequence=['#FE2C55'],
                                    labels={'parsed_views': 'Views'})
                fig2.update_layout(bargap=0.1)
                st.plotly_chart(fig2, use_container_width=True)
            elif gmv_col:
                fig2 = px.histogram(df, x='parsed_gmv', nbins=30, title='GMV Distribution',
                                    color_discrete_sequence=['#25F4EE'],
                                    labels={'parsed_gmv': 'GMV ($)'})
                fig2.update_layout(bargap=0.1)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info('Distribution chart requires Views or GMV column.')
        
        # --- ENGAGEMENT ANALYSIS ---
        st.markdown('---')
        st.markdown('### 🎯 Engagement Analysis')
        
        eng_c1, eng_c2 = st.columns(2)
        
        with eng_c1:
            # Engagement Rate (Likes/Views)
            if likes_col and view_col:
                st.markdown('#### Engagement Rate (Likes/Views)')
                df['engagement_rate'] = (df['parsed_likes'] / df['parsed_views'] * 100).fillna(0)
                df['engagement_rate'] = df['engagement_rate'].replace([float('inf'), -float('inf')], 0)
                
                fig_eng = px.box(df, y='engagement_rate', 
                                title='Engagement Rate Distribution',
                                labels={'engagement_rate': 'Engagement Rate (%)'},
                                color_discrete_sequence=['#FE2C55'])
                st.plotly_chart(fig_eng, use_container_width=True)
                
                avg_engagement = df['engagement_rate'].mean()
                st.metric('Average Engagement Rate', f'{avg_engagement:.2f}%')
            else:
                st.info('Engagement analysis requires Likes and Views columns.')
        
        with eng_c2:
            # GMV per View (if available)
            if gmv_col and view_col:
                st.markdown('#### Revenue Efficiency (GMV/View)')
                df['gmv_per_view'] = (df['parsed_gmv'] / df['parsed_views']).fillna(0)
                df['gmv_per_view'] = df['gmv_per_view'].replace([float('inf'), -float('inf')], 0)
                
                fig_rev = px.scatter(df, x='parsed_views', y='parsed_gmv',
                                    title='Views vs GMV',
                                    labels={'parsed_views': 'Views', 'parsed_gmv': 'GMV ($)'},
                                    color='gmv_per_view',
                                    color_continuous_scale='Viridis',
                                    hover_data=[creator_col] if creator_col else None)
                fig_rev.update_traces(marker=dict(size=8, opacity=0.7))
                st.plotly_chart(fig_rev, use_container_width=True)
                
                avg_gmv_per_view = df['gmv_per_view'].mean()
                st.metric('Avg GMV per View', f'${avg_gmv_per_view:.4f}')
            elif gmv_col and orders_col:
                st.markdown('#### Order Value Analysis')
                df['gmv_per_order'] = (df['parsed_gmv'] / df['parsed_orders']).fillna(0)
                df['gmv_per_order'] = df['gmv_per_order'].replace([float('inf'), -float('inf')], 0)
                
                fig_order = px.histogram(df, x='gmv_per_order', nbins=25,
                                        title='GMV per Order Distribution',
                                        labels={'gmv_per_order': 'GMV per Order ($)'},
                                        color_discrete_sequence=['#25F4EE'])
                st.plotly_chart(fig_order, use_container_width=True)
                
                avg_order_value = df['gmv_per_order'].mean()
                st.metric('Avg Order Value', f'${avg_order_value:.2f}')
            else:
                st.info('Revenue efficiency requires GMV and Views/Orders columns.')
        

        # --- INTERACTIVE CHART BUILDER ---
        st.markdown('---')
        st.markdown('### 🎨 Custom Chart Builder')
        st.markdown('Create your own visualizations by selecting columns and chart types.')
        
        with st.expander('📈 Build Custom Chart', expanded=False):
            builder_c1, builder_c2 = st.columns(2)
            
            # Get available columns for charting
            all_cols = df.columns.tolist()
            numeric_cols_for_chart = df.select_dtypes(include=['number']).columns.tolist()
            # Add parsed columns
            numeric_cols_for_chart.extend([c for c in df.columns if c.startswith('parsed_')])
            numeric_cols_for_chart = list(set(numeric_cols_for_chart))
            
            with builder_c1:
                chart_type = st.selectbox('Chart Type', [
                    'Scatter Plot',
                    'Line Chart',
                    'Bar Chart',
                    'Box Plot',
                    'Violin Plot',
                    'Histogram',
                    'Pie Chart',
                    'Sunburst',
                    'Treemap',
                    '3D Scatter',
                    '3D Line',
                    '3D Surface'
                ])
                
                x_axis = st.selectbox('X Axis', ['None'] + all_cols, key='custom_x')
                y_axis = st.selectbox('Y Axis', ['None'] + all_cols, key='custom_y')
            
            with builder_c2:
                color_by = st.selectbox('Color By (optional)', ['None'] + all_cols, key='custom_color')
                size_by = st.selectbox('Size By (optional)', ['None'] + numeric_cols_for_chart, key='custom_size')
                
                if chart_type in ['3D Scatter', '3D Line', '3D Surface']:
                    z_axis = st.selectbox('Z Axis', ['None'] + all_cols, key='custom_z')
                else:
                    z_axis = 'None'
            
            if st.button('🚀 Generate Chart', type='primary'):
                try:
                    # Prepare parameters
                    x_col = None if x_axis == 'None' else x_axis
                    y_col = None if y_axis == 'None' else y_axis
                    z_col = None if z_axis == 'None' else z_axis
                    color_col = None if color_by == 'None' else color_by
                    size_col = None if size_by == 'None' else size_by
                    
                    fig_custom = None
                    
                    # 2D Charts
                    if chart_type == 'Scatter Plot' and x_col and y_col:
                        fig_custom = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col,
                                               title=f'{y_col} vs {x_col}',
                                               hover_data=[creator_col] if creator_col else None)
                    
                    elif chart_type == 'Line Chart' and x_col and y_col:
                        fig_custom = px.line(df, x=x_col, y=y_col, color=color_col,
                                            title=f'{y_col} over {x_col}')
                    
                    elif chart_type == 'Bar Chart' and x_col and y_col:
                        fig_custom = px.bar(df, x=x_col, y=y_col, color=color_col,
                                           title=f'{y_col} by {x_col}')
                    
                    elif chart_type == 'Box Plot' and y_col:
                        fig_custom = px.box(df, x=x_col, y=y_col, color=color_col,
                                           title=f'{y_col} Distribution')
                    
                    elif chart_type == 'Violin Plot' and y_col:
                        fig_custom = px.violin(df, x=x_col, y=y_col, color=color_col,
                                              title=f'{y_col} Distribution')
                    
                    elif chart_type == 'Histogram' and x_col:
                        fig_custom = px.histogram(df, x=x_col, color=color_col, nbins=30,
                                                 title=f'{x_col} Distribution')
                    
                    elif chart_type == 'Pie Chart' and x_col and y_col:
                        # Aggregate data for pie chart
                        pie_data = df.groupby(x_col)[y_col].sum().reset_index()
                        fig_custom = px.pie(pie_data, names=x_col, values=y_col,
                                           title=f'{y_col} by {x_col}')
                    
                    elif chart_type == 'Sunburst' and x_col and y_col:
                        # Create path for sunburst
                        path_cols = [x_col]
                        if color_col and color_col != x_col:
                            path_cols.append(color_col)
                        fig_custom = px.sunburst(df, path=path_cols, values=y_col,
                                                title=f'{y_col} Sunburst')
                    
                    elif chart_type == 'Treemap' and x_col and y_col:
                        path_cols = [x_col]
                        if color_col and color_col != x_col:
                            path_cols.append(color_col)
                        fig_custom = px.treemap(df, path=path_cols, values=y_col,
                                               title=f'{y_col} Treemap')
                    
                    # 3D Charts
                    elif chart_type == '3D Scatter' and x_col and y_col and z_col:
                        fig_custom = px.scatter_3d(df, x=x_col, y=y_col, z=z_col,
                                                  color=color_col, size=size_col,
                                                  title=f'3D Scatter: {x_col}, {y_col}, {z_col}',
                                                  hover_data=[creator_col] if creator_col else None)
                        fig_custom.update_traces(marker=dict(size=5))
                    
                    elif chart_type == '3D Line' and x_col and y_col and z_col:
                        fig_custom = px.line_3d(df, x=x_col, y=y_col, z=z_col, color=color_col,
                                               title=f'3D Line: {x_col}, {y_col}, {z_col}')
                    
                    elif chart_type == '3D Surface' and x_col and y_col and z_col:
                        # For surface plot, we need to pivot the data
                        try:
                            pivot_data = df.pivot_table(values=z_col, index=y_col, columns=x_col, aggfunc='mean')
                            fig_custom = go.Figure(data=[go.Surface(z=pivot_data.values, 
                                                                   x=pivot_data.columns, 
                                                                   y=pivot_data.index)])
                            fig_custom.update_layout(title=f'3D Surface: {z_col} by {x_col} and {y_col}',
                                                    scene=dict(xaxis_title=x_col, yaxis_title=y_col, zaxis_title=z_col))
                        except Exception as e:
                            st.error(f'Surface plot requires numeric data that can be pivoted. Error: {e}')
                    
                    if fig_custom:
                        fig_custom.update_layout(height=600)
                        st.plotly_chart(fig_custom, use_container_width=True)
                    else:
                        st.warning('Please select appropriate columns for the chosen chart type.')
                
                except Exception as e:
                    st.error(f'Error generating chart: {e}')
        
        # --- CREATOR SEGMENTATION ---
        if mode == "Granular (Video Level)" and gmv_col and view_col:
            st.markdown('---')
            st.markdown('### 🎯 Creator Performance Segmentation')
            
            # Create segments based on GMV and engagement
            creator_perf = creator_stats.reset_index()
            
            if 'total_gmv' in creator_perf.columns and 'parsed_views' in creator_perf.columns:
                # Calculate percentiles for segmentation
                gmv_median = creator_perf['total_gmv'].median()
                views_median = creator_perf['parsed_views'].median()
                
                def segment_creator(row):
                    if row['total_gmv'] >= gmv_median and row['parsed_views'] >= views_median:
                        return 'Star Performers'
                    elif row['total_gmv'] >= gmv_median:
                        return 'High Revenue'
                    elif row['parsed_views'] >= views_median:
                        return 'High Reach'
                    else:
                        return 'Emerging'
                
                creator_perf['segment'] = creator_perf.apply(segment_creator, axis=1)
                
                seg_c1, seg_c2 = st.columns(2)
                
                with seg_c1:
                    # Segment distribution
                    segment_counts = creator_perf['segment'].value_counts()
                    fig_seg = px.pie(values=segment_counts.values, names=segment_counts.index,
                                    title='Creator Segmentation',
                                    color_discrete_sequence=px.colors.qualitative.Set3)
                    st.plotly_chart(fig_seg, use_container_width=True)
                
                with seg_c2:
                    # Segment performance
                    fig_seg_scatter = px.scatter(creator_perf, x='parsed_views', y='total_gmv',
                                                color='segment', size='video_count',
                                                title='Creator Segments: Views vs GMV',
                                                labels={'parsed_views': 'Total Views', 'total_gmv': 'Total GMV ($)'},
                                                hover_data=[creator_col])
                    fig_seg_scatter.update_traces(marker=dict(opacity=0.7))
                    st.plotly_chart(fig_seg_scatter, use_container_width=True)
        
        # Cleanup temp columns
        cols_to_drop = [c for c in ['parsed_videos', 'parsed_views', 'parsed_gmv', 'parsed_likes', 
                                     'parsed_comments', 'parsed_shares', 'parsed_orders',
                                     'engagement_rate', 'gmv_per_view', 'gmv_per_order'] if c in df.columns]
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)

        # --- BULK EXPORT OPTIONS ---
        st.markdown('---')
        st.markdown('### 📥 Bulk Export Options')
        
        export_c1, export_c2 = st.columns(2)
        
        with export_c1:
            st.markdown('#### Export Templates')
            
            export_template = st.selectbox(
                'Choose Export Template',
                ['Custom Selection', 'Top Performers (Top 50)', 'High GMV Creators', 'High Engagement', 'All Data']
            )
            
            export_format = st.radio('Export Format', ['CSV', 'Excel'], horizontal=True)
            
            # Column selection for custom export
            if export_template == 'Custom Selection':
                export_cols = st.multiselect(
                    'Select Columns to Export',
                    df.columns.tolist(),
                    default=df.columns.tolist()[:5]
                )
            else:
                export_cols = df.columns.tolist()
        
        with export_c2:
            st.markdown('#### Export Preview')
            
            # Prepare export dataframe based on template
            export_df = df.copy()
            
            if export_template == 'Top Performers (Top 50)':
                # Sort by GMV or views
                if gmv_col and 'parsed_gmv' in export_df.columns:
                    export_df['_sort_col'] = export_df[gmv_col].apply(parse_metric_value)
                    export_df = export_df.nlargest(50, '_sort_col').drop(columns=['_sort_col'])
                elif view_col and 'parsed_views' in export_df.columns:
                    export_df['_sort_col'] = export_df[view_col].apply(parse_metric_value)
                    export_df = export_df.nlargest(50, '_sort_col').drop(columns=['_sort_col'])
                else:
                    export_df = export_df.head(50)
                st.info(f'Exporting top 50 rows ({len(export_df)} total)')
            
            elif export_template == 'High GMV Creators':
                if gmv_col:
                    export_df['_temp_gmv'] = export_df[gmv_col].apply(parse_metric_value)
                    export_df = export_df[export_df['_temp_gmv'] >= 10000].drop(columns=['_temp_gmv'])
                    st.info(f'Exporting {len(export_df)} creators with GMV ≥ $10K')
                else:
                    st.warning('No GMV column detected')
            
            elif export_template == 'High Engagement':
                if likes_col and view_col:
                    export_df['_temp_likes'] = export_df[likes_col].apply(parse_metric_value)
                    export_df['_temp_views'] = export_df[view_col].apply(parse_metric_value)
                    export_df['_eng_rate'] = (export_df['_temp_likes'] / export_df['_temp_views'] * 100).fillna(0)
                    export_df = export_df[export_df['_eng_rate'] >= 5].drop(columns=['_temp_likes', '_temp_views', '_eng_rate'])
                    st.info(f'Exporting {len(export_df)} videos with engagement ≥ 5%')
                else:
                    st.warning('Requires Likes and Views columns')
            
            elif export_template == 'Custom Selection':
                if export_cols:
                    export_df = export_df[export_cols]
                    st.info(f'Exporting {len(export_df)} rows with {len(export_cols)} columns')
            
            else:  # All Data
                st.info(f'Exporting all {len(export_df)} rows')
            
            # Show preview
            st.dataframe(export_df.head(5), use_container_width=True)
        
        # Export button
        st.markdown('#### Download Export')
        export_filename = st.text_input('Export Filename', f'export_{export_template.lower().replace(" ", "_")}')
        
        if export_format == 'CSV':
            to_csv_download_link(export_df, f'{export_filename}.csv', '💾 Download CSV Export')
        else:
            # Excel export
            try:
                import io
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    export_df.to_excel(writer, index=False, sheet_name='Export')
                
                st.download_button(
                    label='💾 Download Excel Export',
                    data=buffer.getvalue(),
                    file_name=f'{export_filename}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            except ImportError:
                st.error('openpyxl not installed. Using CSV export instead.')
                to_csv_download_link(export_df, f'{export_filename}.csv', '💾 Download CSV Export')

        # Download Processed (Original functionality)
        st.markdown('---')
        st.markdown('### 📥 Export Processed Data')
        fname = st.text_input('Filename', 'processed_' + st.session_state['file_name'])
        to_csv_download_link(df, fname, '💾 Download Processed CSV')


