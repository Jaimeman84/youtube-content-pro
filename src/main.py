import streamlit as st
import os
from services.video_service import VideoProcessor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_services():
    """Initialize services"""
    # Default download path relative to the current directory
    download_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
    return {
        'video': VideoProcessor(api_key=os.getenv('OPENAI_API_KEY'), download_path=download_path)
    }

def main():
    # Configure page with no navigation menu and custom width
    st.set_page_config(
        page_title="YouTube Content Pro",
        page_icon="🎥",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Hide navigation and set content width with custom CSS
    st.markdown("""
        <style>
            /* Hide all navigation elements */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Remove sidebar */
            section[data-testid="stSidebar"] {
                display: none;
            }
            
            /* Center content and set width */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 1000px;
                margin: 0 auto;
            }
            
            /* Center title and text */
            h1, h2, h3, p {
                text-align: center !important;
            }
            
            .stMarkdown {
                text-align: center;
            }
            
            /* Center text inputs */
            .stTextInput input {
                display: block;
                margin: 0 auto;
                max-width: 800px;
                text-align: center;
            }
            
            /* Center text areas */
            .stTextArea textarea {
                display: block;
                margin: 0 auto;
                max-width: 800px;
            }
            
            /* Center metrics */
            [data-testid="stMetricValue"] {
                justify-content: center;
            }
            
            /* Center metric labels */
            [data-testid="stMetricLabel"] {
                text-align: center;
                justify-content: center;
            }
            
            /* Center tabs */
            .stTabs [data-baseweb="tab-list"] {
                justify-content: center;
            }
            
            /* Center tab content */
            .stTabs [data-baseweb="tab-panel"] {
                text-align: center;
            }
            
            /* Center buttons */
            .stButton button {
                display: block;
                margin: 0 auto;
            }
            
            /* Center multiselect */
            .stMultiSelect {
                max-width: 800px;
                margin: 0 auto;
                text-align: center;
            }
            
            /* Center expanders */
            .streamlit-expanderHeader {
                justify-content: center;
            }
            
            /* Center info boxes */
            .stAlert {
                text-align: center;
            }
            
            /* Add some spacing between elements */
            .element-container {
                margin-bottom: 1rem;
            }
            
            /* Center subheaders */
            .css-10trblm {
                text-align: center;
            }
            
            /* Center error messages */
            .stException, .stError {
                text-align: center;
            }
            
            /* Center metrics container */
            [data-testid="metric-container"] {
                width: 100%;
                display: flex;
                justify-content: center;
                margin: 0 auto;
            }
            
            /* Adjust info box width and alignment */
            .stAlert {
                width: 80%;
                margin: 0 auto;
                text-align: center;
            }
            
            /* Center metric columns */
            [data-testid="column"] {
                text-align: center;
                width: 50%;
                flex: none !important;
            }
            
            /* Container for statistics columns */
            [data-testid="column-container"] {
                display: flex !important;
                justify-content: center !important;
                gap: 2rem !important;
                max-width: 1200px !important;
                margin: 0 auto !important;
            }
            
            /* Individual column styling */
            [data-testid="column"] {
                flex: 1 1 calc(50% - 1rem) !important;
                min-width: 300px !important;
            }
            
            /* Info box styling */
            div.stAlert {
                height: 100% !important;
                margin: 0 !important;
                padding: 1.5rem !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize services
    services = init_services()
    
    # App title and description
    st.title("YouTube Content Pro")
    st.markdown("""
    Transform your YouTube content:
    
    — Get instant video transcripts —
    
    — Generate engaging social media posts —
    
    — Get trending hashtag suggestions —
    """)
    
    # Main content area
    video_url = st.text_input("Enter YouTube URL")
    
    if video_url:
        # Create tabs
        tab1, tab2 = st.tabs(["Get Transcript", "Social Media"])
        
        # Tab 1: Get Transcript
        with tab1:
            try:
                transcript = services['video'].get_video_transcript(video_url)
                st.text_area("Video Transcript", transcript, height=300)
                
                # Center container for statistics
                st.markdown("""
                    <style>
                        /* Center metrics container */
                        [data-testid="metric-container"] {
                            width: 100%;
                            display: flex;
                            justify-content: center;
                            margin: 0 auto;
                        }
                        
                        /* Adjust info box width and alignment */
                        .stAlert {
                            width: 100%;
                            margin: 0 auto;
                            text-align: center;
                        }
                        
                        /* Center metric columns */
                        [data-testid="column"] {
                            text-align: center;
                            nin-width: 100%;
                            flex: none !important;
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                # Display transcript statistics in centered columns
                st.markdown("### Transcript Overview")
                
                # Calculate statistics
                words = len(transcript.split())
                minutes = words / 150  # Assuming average speaking rate of 150 words per minute
        
                # Create two equal columns for statistics
                col1, col2 = st.columns([1, 1])
                
                # Display statistics in columns
                with col1:
                    st.info(
                        "📝 **Word Statistics**\n\n"
                        f"— Total Words: {words:,} —\n\n"
                        f"— Speaking Rate: 150 words/minute —"
                    )
                
                with col2:
                    st.info(
                        "⏱️ **Duration Statistics**\n\n"
                        f"— Total Duration: {minutes:.1f} minutes —\n\n"
                        f"— Seconds: {minutes * 60:.0f} seconds —"
                    )
                
            except Exception as e:
                st.error(str(e))
        
        # Tab 2: Social Media
        with tab2:
            platforms = st.multiselect(
                "Select platforms",
                ["Twitter", "Instagram", "LinkedIn", "Facebook"],
                default=["Twitter", "Instagram"]
            )
            
            if st.button("Generate Social Media Posts"):
                try:
                    # Get transcript first if we don't have it
                    if 'transcript' not in locals():
                        transcript = services['video'].get_video_transcript(video_url)
                    
                    with st.spinner("Generating social media content..."):
                        result = services['video'].generate_social_posts(
                            video_url,
                            transcript,
                            platforms
                        )
                        
                        # Display hashtags at the top
                        st.markdown("""
                            <div style='text-align: center; margin: 2rem 0;'>
                                <h3>Generated Hashtags</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Display hashtags in a centered paragraph
                        with st.expander("Generated Hashtags", expanded=True):
                            st.markdown(f"<p style='text-align: center;'>{result['hashtags']}</p>", unsafe_allow_html=True)
                        
                        # Iterate over platforms to display posts in full section width
                        for platform in platforms:
                            with st.expander(f"📱 {platform}", expanded=True):
                                st.text_area(
                                    label="",
                                    value=result['posts'][platform],
                                    height=200,
                                    key=f"post_{platform}"
                                )
                except Exception as e:
                    st.error(str(e))

    # Clear data button
    if st.sidebar.button("Clear Data"):
        if st.session_state:
            st.session_state.clear()
            st.experimental_rerun()

if __name__ == "__main__":
    main()