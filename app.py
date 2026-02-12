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

        /* Global Styles */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Inter', sans-serif;
            color: {text_color} !important;
        }}

        /* Specific text overrides for Streamlit components */
        .stMarkdown, .stText, p, span, label, .stMetric, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {text_color} !important;
        }}

        /* Gradient Background */
        .stApp {{
            background: {bg_gradient};
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
        section[data-testid="stSidebar"] span {{
            color: {text_color} !important;
        }}

        /* Custom Buttons */
        .stButton > button {{
            background: linear-gradient(90deg, {tiktok_red} 0%, #FF0050 100%);
            color: white !important;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(254, 44, 85, 0.2);
        }}
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(254, 44, 85, 0.4);
            filter: brightness(1.1);
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
            letter-spacing: -1px;
        }}
        
        /* Custom Card Component */
        .custom-card {{
            background-color: {card_bg};
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            border: 1px solid {border_color};
            transition: all 0.3s ease;
            margin-bottom: 1rem;
        }}
        .custom-card p {{
            color: {secondary_text} !important;
        }}
        .custom-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            border-color: {tiktok_red}50;
        }}

        /* Expander Styling */
        .streamlit-expanderHeader {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border-radius: 12px;
            border: 1px solid {border_color};
        }}
        
        /* Data Editor/Frame */
        [data-testid="stDataFrame"] {{
            border: 1px solid {border_color};
            border-radius: 12px;
            overflow: hidden;
            background-color: {card_bg};
        }}

        /* Metrics */
        [data-testid="stMetricValue"] {{
            font-weight: 800 !important;
            color: {tiktok_red} !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {secondary_text} !important;
        }}

        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 24px;
        }}
        .stTabs [data-baseweb="tab"] {{
            color: {secondary_text} !important;
        }}
        .stTabs [aria-selected="true"] {{
            border-bottom: 3px solid {tiktok_red} !important;
            color: {tiktok_red} !important;
        }}

        /* Success/Info Messages */
        .stSuccess, .stInfo, .stWarning, .stError {{
            border-radius: 12px;
            border: none;
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border-left: 5px solid {tiktok_red} !important;
        }}

        /* Selectbox/Input Styling */
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{
            background-color: {card_bg} !important;
            border-radius: 10px !important;
            border-color: {border_color} !important;
            color: {text_color} !important;
        }}
        
        /* Fix for input text visibility */
        input {{
            color: {text_color} !important;
        }}
        
        /* Tooltip */
        .stTooltipIcon {{
            color: {tiktok_red};
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

    tab1, tab2 = st.tabs(["📤 Upload CSV", "🆕 Create New"])

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
            # Then try partial match
            for c in df.columns:
                if any(x.lower() in c.lower() for x in candidates):
                    return c
            return None

        # 1. Identify Key Columns
        video_count_col = get_col(['video count', 'videos_count']) 
        video_id_col = get_col(['video id', 'item id'])
        
        view_col = get_col(['video views', 'vv', 'views', 'view count'])
        if not view_col: view_col = get_col(['view'])

        gmv_col = get_col(['gross merchandise value (video) ($)', 'gmv', 'gross merchandise value', 'gross mer', 'revenue', 'sales', 'gpm'])
        
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
        
        creators_gt_3_vids = 0
        creators_gt_10_vids = 0
        creators_gt_1k_gmv = 0
        creators_gt_100_gmv = 0
        
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
            
            creators_gt_3_vids = len(creator_stats[creator_stats['video_count'] >= 3])
            creators_gt_10_vids = len(creator_stats[creator_stats['video_count'] >= 10])
            
            if gmv_col:
                creators_gt_1k_gmv = len(creator_stats[creator_stats['total_gmv'] >= 1000])
                creators_gt_100_gmv = len(creator_stats[creator_stats['total_gmv'] >= 100])
                
        elif video_count_col:
            mode = "Aggregated (Creator Level)"
            # Rows are creators already
            df['parsed_videos'] = df[video_count_col].apply(lambda x: pd.to_numeric(x, errors='coerce')).fillna(0)
            total_videos = int(df['parsed_videos'].sum())
            if likes_col: total_likes = int(df['parsed_likes'].sum())
            
            creators_gt_3_vids = len(df[df['parsed_videos'] >= 3])
            creators_gt_10_vids = len(df[df['parsed_videos'] >= 10])
            
            if gmv_col:
                creators_gt_1k_gmv = len(df[df['parsed_gmv'] >= 1000])
                creators_gt_100_gmv = len(df[df['parsed_gmv'] >= 100])
        
        else:
             mode = "Simple (Row Count)"
             total_videos = len(df)
             if creator_col:
                 creator_counts = df[creator_col].value_counts()
                 creators_gt_3_vids = len(creator_counts[creator_counts >= 3])
                 creators_gt_10_vids = len(creator_counts[creator_counts >= 10])
                 
                 if gmv_col:
                     creator_gmv = df.groupby(creator_col)['parsed_gmv'].sum()
                     creators_gt_1k_gmv = len(creator_gmv[creator_gmv >= 1000])
                     creators_gt_100_gmv = len(creator_gmv[creator_gmv >= 100])

        # Debug Info
        with st.expander("🛠️ Debug Information & Column Detection"):
            st.info(f"**Detected Mode:** {mode}")
            st.write(f"**Video ID:** `{video_id_col}` | **Creator:** `{creator_col}`")
            st.write(f"**GMV:** `{gmv_col}` | **Views:** `{view_col}`")
            st.write(f"**Likes:** `{likes_col}` (from 'Likes', 'Like')")
            st.write(f"**Orders:** `{orders_col}` (from 'Orders', 'Order')")

        
        md_c1, md_c2, md_c3, md_c4 = st.columns(4)
        
        with md_c1:
            st.metric('Total Videos', f'{total_videos:,}')
            if gmv_col:
                st.metric('Creators > $1K GMV', creators_gt_1k_gmv)

        with md_c2:
            st.metric('Creators > 3 Videos', creators_gt_3_vids)
            if gmv_col:
                 st.metric('Creators > $100 GMV', creators_gt_100_gmv)

        with md_c3:
            st.metric('Creators > 10 Videos', creators_gt_10_vids)
            if likes_col:
                st.metric('Total Likes', f'{total_likes:,}')

        with md_c4:
            if orders_col:
                 st.metric('Total Orders', f'{total_orders:,}')
            elif view_col:
                vids_10k = len(df[df['parsed_views'] >= 10000])
                st.metric('Videos > 10k Views', vids_10k)



        # --- VISUALIZATIONS ---
        st.markdown('### Visualizations')
        
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
                fig2 = px.histogram(df, x='parsed_views', nbins=20, title='View Count Distribution',
                                    color_discrete_sequence=['#FE2C55'])
                st.plotly_chart(fig2, use_container_width=True)
            elif gmv_col:
                fig2 = px.histogram(df, x='parsed_gmv', nbins=20, title='GMV Distribution',
                                    color_discrete_sequence=['#25F4EE'])
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info('Distribution chart requires Views or GMV column.')
        
        # Cleanup temp columns
        cols_to_drop = [c for c in ['parsed_videos', 'parsed_views', 'parsed_gmv'] if c in df.columns]
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)

        # Download Processed
        st.markdown('### Export Processed Data')
        fname = st.text_input('Filename', 'processed_' + st.session_state['file_name'])
        to_csv_download_link(df, fname, ' Download Processed CSV')
