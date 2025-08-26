from snowflake.snowpark import Session

# example usage of get
# # Download one file from a stage.
# get_result1 = session.file.get("@myStage/prefix1/test2CSV.csv", "tests/downloaded/target1")
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_snowflake_session():
    """Create and return a Snowflake session using environment variables"""
    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA")
    }
    
    # Remove None values from connection parameters
    connection_parameters = {k: v for k, v in connection_parameters.items() if v is not None}
    
    # Create and return the session
    session = Session.builder.configs(connection_parameters).create()
    return session

def get_stages_list(session: Session) -> List[str]:
    """Get list of all stages in the current schema"""
    try:
        result = session.sql("SHOW STAGES").collect()
        stages = [row['name'] for row in result]
        return stages
    except Exception as e:
        st.error(f"Error fetching stages: {str(e)}")
        return []

def get_stage_files(session: Session, stage_name: str) -> pd.DataFrame:
    """Get list of files in the specified stage"""
    try:
        query = f"LIST @{stage_name}"
        result = session.sql(query).collect()
        
        files_data = []
        for row in result:
            file_path = row['name']
            file_name = file_path.split('/')[-1] if '/' in file_path else file_path
            file_size = row['size']
            last_modified = row['last_modified']
            
            # Determine file type from extension
            file_extension = file_name.split('.')[-1].lower() if '.' in file_name else 'unknown'
            file_type = file_extension
            
            files_data.append({
                'File Name': file_name,
                'File Size': f"{file_size:,} bytes",
                'File Type': file_type,
                'Last Modified': last_modified,
                'File Path': file_path
            })
        
        return pd.DataFrame(files_data)
    except Exception as e:
        st.error(f"Error fetching files from stage {stage_name}: {str(e)}")
        return pd.DataFrame()

def download_file_from_stage(session: Session, stage_name: str, file_path: str, local_directory: str, file_name: str) -> bool:
    """Download a single file from Snowflake stage to local directory"""
    try:
        # Ensure local directory exists
        os.makedirs(local_directory, exist_ok=True)
        
        # Create full local path
        local_file_path = os.path.join(local_directory, file_name)
        
        # Use session.file.get() to download file from stage
        stage_file_path = f"@{file_path}"
        get_result = session.file.get(stage_file_path, local_directory)
        
        # Check if file was downloaded successfully
        if os.path.exists(local_file_path):
            return True
        else:
            st.error(f"File {file_name} was not found after download")
            return False
    except Exception as e:
        st.error(f"Error downloading file {file_path}: {str(e)}")
        return False

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def get_file_icon(file_type):
    """Get appropriate icon for file type"""
    icons = {
        'csv': '📊',
        'json': '📋',
        'txt': '📄',
        'pdf': '📕',
        'xlsx': '📗',
        'xls': '📗',
        'png': '🖼️',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'mp4': '🎬',
        'mp3': '🎵',
        'wav': '🎵',
        'zip': '📦',
        'sql': '🗃️',
        'py': '🐍',
        'parquet': '📊'
    }
    return icons.get(file_type.lower(), '📁')

def main():
    """Main Streamlit app"""
    # Page configuration
    st.set_page_config(
        page_title="Snowflake Stage File Downloader",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #29B5E8 0%, #1E88E5 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #29B5E8;
        margin: 0.5rem 0;
    }
    .success-container {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-container {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-container {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with styling
    st.markdown("""
    <div class="main-header">
        <h1>❄️ Snowflake Stage File Downloader</h1>
        <p>Easily browse and download files from your Snowflake stages to your local machine</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Connection status container
    with st.container():
        st.markdown("### 🔌 Connection Status")
        
        # Initialize session
        if 'session' not in st.session_state:
            with st.spinner("🔄 Connecting to Snowflake..."):
                try:
                    st.session_state.session = create_snowflake_session()
                    st.markdown("""
                    <div class="success-container">
                        <strong>✅ Successfully connected to Snowflake!</strong><br>
                        Ready to browse and download files from your stages.
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-container">
                        <strong>❌ Failed to connect to Snowflake</strong><br>
                        Error: {str(e)}<br>
                        Please check your environment variables and connection settings.
                    </div>
                    """, unsafe_allow_html=True)
                    st.stop()
        else:
            st.markdown("""
            <div class="success-container">
                <strong>✅ Connected to Snowflake</strong><br>
                Session is active and ready for file operations.
            </div>
            """, unsafe_allow_html=True)
    
    session = st.session_state.session
    
    st.markdown("---")
    
    # Download Settings Section
    with st.container():
        st.markdown("### ⚙️ Download Settings")
        
        default_download_path = os.path.expanduser("~/Downloads")
        download_folder = st.text_input(
            "📁 Local download folder:",
            value=default_download_path,
            help="Specify the local folder where files will be downloaded. The folder will be created if it doesn't exist."
        )
        
        # Validate download folder
        if download_folder:
            try:
                os.makedirs(download_folder, exist_ok=True)
                st.markdown(f"""
                <div class="success-container">
                    <strong>✅ Download folder validated:</strong> {download_folder}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-container">
                    <strong>❌ Invalid download folder:</strong> {str(e)}
                </div>
                """, unsafe_allow_html=True)
                return
    
    st.markdown("---")
    
    # Stage Selection Section
    with st.container():
        st.markdown("### 🗂️ Stage Selection")
        
        with st.spinner("🔍 Loading available stages..."):
            stages = get_stages_list(session)
        
        if not stages:
            st.markdown("""
            <div class="info-container">
                <strong>ℹ️ No stages found</strong><br>
                No stages were found in the current schema. Please check your permissions or create a stage first.
            </div>
            """, unsafe_allow_html=True)
            return
        
        stage_col1, stage_col2 = st.columns([2, 1])
        
        with stage_col1:
            selected_stage = st.selectbox(
                "🎯 Choose a stage:",
                stages,
                help="Select the Snowflake stage from which you want to download files"
            )
        
        with stage_col2:
            st.metric(
                label="📊 Available Stages",
                value=len(stages),
                help="Total number of stages in your current schema"
            )
    
    st.markdown("---")
    
    # File Browser Section
    if selected_stage:
        with st.container():
            st.markdown(f"### 📋 Files in Stage: `{selected_stage}`")
            
            # Get files from selected stage
            with st.spinner(f"📖 Loading files from {selected_stage}..."):
                files_df = get_stage_files(session, selected_stage)
            
            if files_df.empty:
                st.markdown("""
                <div class="info-container">
                    <strong>📂 No files found</strong><br>
                    The selected stage appears to be empty or you don't have access to view its contents.
                </div>
                """, unsafe_allow_html=True)
                return
            
            # File statistics
            total_files = len(files_df)
            file_types = files_df['File Type'].value_counts()
            
            # Display metrics
            metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
            
            with metrics_col1:
                st.metric(
                    label="📁 Total Files",
                    value=total_files,
                    help="Total number of files in the stage"
                )
            
            with metrics_col2:
                st.metric(
                    label="🗂️ File Types",
                    value=len(file_types),
                    help="Number of different file types"
                )
            
            with metrics_col3:
                if not files_df.empty:
                    # Calculate total size (convert from formatted string back to bytes for calculation)
                    total_size = sum(int(row['File Size'].replace(',', '').replace(' bytes', '')) 
                                   for _, row in files_df.iterrows())
                    st.metric(
                        label="💾 Total Size",
                        value=format_file_size(total_size),
                        help="Combined size of all files"
                    )
            
            with metrics_col4:
                if not file_types.empty:
                    most_common_type = file_types.index[0]
                    st.metric(
                        label="🏆 Most Common",
                        value=f".{most_common_type}",
                        delta=f"{file_types.iloc[0]} files",
                        help="Most common file type in the stage"
                    )
            
            st.markdown("---")
            
            # File selection interface
            selection_col1, selection_col2 = st.columns([3, 1])
            
            with selection_col1:
                st.markdown("#### 🎯 Select Files to Download")
            
            with selection_col2:
                select_all = st.checkbox(
                    "✅ Select All Files",
                    key="select_all_files",
                    help="Select or deselect all files at once"
                )
            
            # Prepare display dataframe with icons
            files_df_display = files_df.copy()
            files_df_display['File Type'] = files_df_display['File Type'].apply(
                lambda x: f"{get_file_icon(x)} {x.upper()}"
            )
            files_df_display.insert(0, 'Select', select_all)
            
            # Create editable dataframe for selection
            edited_df = st.data_editor(
                files_df_display,
                column_config={
                    "Select": st.column_config.CheckboxColumn(
                        "📌 Select",
                        help="Select files to download",
                        default=select_all,
                    ),
                    "File Name": st.column_config.TextColumn(
                        "📄 File Name",
                        help="Name of the file",
                        max_chars=100,
                    ),
                    "File Size": st.column_config.TextColumn(
                        "💾 Size",
                        help="File size in bytes",
                    ),
                    "File Type": st.column_config.TextColumn(
                        "🏷️ Type",
                        help="File type/extension",
                    ),
                    "Last Modified": st.column_config.DatetimeColumn(
                        "📅 Modified",
                        help="Last modification date",
                    ),
                    "File Path": st.column_config.TextColumn(
                        "📍 Path",
                        help="Full path in the stage",
                    )
                },
                disabled=["File Name", "File Size", "File Type", "Last Modified", "File Path"],
                hide_index=True,
                use_container_width=True,
            )
            
            # Get selected files
            selected_files = edited_df[edited_df['Select'] == True]
            
            if len(selected_files) > 0:
                st.markdown("---")
                
                # Download section
                with st.container():
                    st.markdown("### 📥 Download Selected Files")
                    
                    st.markdown(f"""
                    <div class="info-container">
                        <strong>📋 Download Summary</strong><br>
                        • Files selected: <strong>{len(selected_files)}</strong><br>
                        • Destination: <code>{download_folder}</code><br>
                        • Stage: <strong>{selected_stage}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-container">
                    <strong>💡 No files selected</strong><br>
                    Please select one or more files from the table above to enable the download option.
                </div>
                """, unsafe_allow_html=True)
            
            # Download button at the bottom
            if len(selected_files) > 0:
                st.markdown("---")
                if st.button("🚀 Start Download", type="primary", use_container_width=True):
                    # Download process
                    progress_container = st.container()
                    
                    with progress_container:
                        st.markdown("#### 📊 Download Progress")
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        success_count = 0
                        total_files = len(selected_files)
                        downloaded_files = []
                        failed_files = []
                        
                        for idx, (_, file_row) in enumerate(selected_files.iterrows()):
                            file_path = file_row['File Path']
                            file_name = file_row['File Name']
                            
                            status_text.markdown(f"⬇️ **Downloading:** `{file_name}`")
                            
                            # Download file to local folder
                            if download_file_from_stage(session, selected_stage, file_path, download_folder, file_name):
                                success_count += 1
                                downloaded_files.append(file_name)
                            else:
                                failed_files.append(file_name)
                            
                            # Update progress
                            progress = (idx + 1) / total_files
                            progress_bar.progress(progress)
                        
                        # Show final status
                        if success_count > 0:
                            status_text.markdown(f"✅ **Download Complete:** {success_count}/{total_files} files")
                            
                            st.markdown(f"""
                            <div class="success-container">
                                <strong>🎉 Download Completed Successfully!</strong><br>
                                Downloaded <strong>{success_count}</strong> out of <strong>{total_files}</strong> files to:<br>
                                <code>{download_folder}</code>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show list of downloaded files
                            if downloaded_files:
                                with st.expander(f"📋 View Downloaded Files ({len(downloaded_files)})", expanded=False):
                                    for file_name in downloaded_files:
                                        st.markdown(f"✅ `{file_name}`")
                            
                            # Show failed files if any
                            if failed_files:
                                with st.expander(f"❌ Failed Downloads ({len(failed_files)})", expanded=True):
                                    for file_name in failed_files:
                                        st.markdown(f"❌ `{file_name}`")
                        else:
                            status_text.markdown("❌ **Download Failed**")
                            st.markdown("""
                            <div class="error-container">
                                <strong>❌ Download Failed</strong><br>
                                No files were downloaded successfully. Please check the error messages above and try again.
                            </div>
                            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
