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

def main():
    """Main Streamlit app"""
    st.title("Snowflake Stage File Downloader")
    st.write("Download files from Snowflake stages to your local machine")
    
    # Initialize session
    if 'session' not in st.session_state:
        try:
            st.session_state.session = create_snowflake_session()
            st.success("Connected to Snowflake successfully!")
        except Exception as e:
            st.error(f"Failed to connect to Snowflake: {str(e)}")
            st.stop()
    
    session = st.session_state.session
    
    # Local folder selection
    st.subheader("Download Settings")
    default_download_path = os.path.expanduser("~/Downloads")
    download_folder = st.text_input(
        "Local download folder:",
        value=default_download_path,
        help="Specify the local folder where files will be downloaded"
    )
    
    # Validate download folder
    if download_folder:
        try:
            os.makedirs(download_folder, exist_ok=True)
            st.success(f"✅ Download folder: {download_folder}")
        except Exception as e:
            st.error(f"❌ Invalid download folder: {str(e)}")
            return
    
    # Stage selection
    st.subheader("Select Stage")
    stages = get_stages_list(session)
    
    if not stages:
        st.warning("No stages found in the current schema.")
        return
    
    selected_stage = st.selectbox("Choose a stage:", stages)
    
    if selected_stage:
        st.subheader(f"Files in stage: {selected_stage}")
        
        # Get files from selected stage
        files_df = get_stage_files(session, selected_stage)
        
        if files_df.empty:
            st.info("No files found in the selected stage.")
            return
        
        # Display files count and select all option
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"Found {len(files_df)} files:")
        with col2:
            select_all = st.checkbox("Select All", key="select_all_files")
        
        # Add selection column
        files_df_display = files_df.copy()
        files_df_display.insert(0, 'Select', select_all)
        
        # Create editable dataframe for selection
        edited_df = st.data_editor(
            files_df_display,
            column_config={
                "Select": st.column_config.CheckboxColumn(
                    "Select",
                    help="Select files to download",
                    default=select_all,
                )
            },
            disabled=["File Name", "File Size", "File Type", "Last Modified", "File Path"],
            hide_index=True,
        )
        
        # Get selected files
        selected_files = edited_df[edited_df['Select'] == True]
        
        if len(selected_files) > 0:
            st.subheader("Download Selected Files")
            st.write(f"Selected {len(selected_files)} file(s) for download to: `{download_folder}`")
            
            if st.button("Download Selected Files"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                success_count = 0
                total_files = len(selected_files)
                downloaded_files = []
                
                for idx, (_, file_row) in enumerate(selected_files.iterrows()):
                    file_path = file_row['File Path']
                    file_name = file_row['File Name']
                    
                    status_text.text(f"Downloading {file_name}...")
                    
                    # Download file to local folder
                    if download_file_from_stage(session, selected_stage, file_path, download_folder, file_name):
                        success_count += 1
                        downloaded_files.append(file_name)
                    
                    # Update progress
                    progress = (idx + 1) / total_files
                    progress_bar.progress(progress)
                
                # Show final status
                if success_count > 0:
                    status_text.text(f"✅ Successfully downloaded {success_count}/{total_files} files to {download_folder}")
                    st.success("Download completed!")
                    
                    # Show list of downloaded files
                    if downloaded_files:
                        st.write("**Downloaded files:**")
                        for file_name in downloaded_files:
                            st.write(f"• {file_name}")
                else:
                    status_text.text("❌ No files downloaded successfully")
                    st.error("Download failed!")

if __name__ == "__main__":
    main()
