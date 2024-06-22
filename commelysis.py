import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai

# Directly specify the API keys (for testing purposes only)
GOOGLE_API_KEY = 'AIzaSyDbMa95_4sF1AtHpDOxKDRov7mRh0ldcqY'
YOUTUBE_API_KEY = 'AIzaSyDCvbnrh3_ynhBqozI6dRFCKtrf_GHyrNU'

# Configure the API key for generative AI (assuming it's correctly set up)
genai.configure(api_key=GOOGLE_API_KEY)

# Create an instance of the GenerativeModel (assuming 'gemini-pro' is correct)
model = genai.GenerativeModel('gemini-pro')

# Streamlit UI
st.title('YouTube Comment Analyzer')

# النقطة 3: إضافة مؤشر التحميل
with st.spinner("Loading results..."):
    keyword = st.text_input('Enter a keyword to search on YouTube:', '')

if st.button('Search and Analyze'):
    if keyword:
        with st.spinner("Loading results..."):
            # Authenticate and build the YouTube service
            youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

            # Search for videos using the keyword
            search_response = youtube.search().list(
                q=keyword,
                part='id,snippet',
                maxResults=1,
                type='video',  # Search only for videos
                regionCode='SA',  # Example: Saudi Arabia
                relevanceLanguage='ar'  # Arabic language
            ).execute()

            # Check for items in search response
            if 'items' in search_response and search_response['items']:
                # Get video ID from the first search result
                video_id = search_response['items'][0]['id'].get('videoId', None)

                if video_id:
                    # Get comments from the video
                    comments = []
                    comment_response = youtube.commentThreads().list(
                        videoId=video_id,
                        part='snippet',
                        maxResults=200
                    ).execute()

                    for item in comment_response.get('items', []):
                        comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])

                    # Join comments into a single string for analysis
                    comments_text = "\n".join(comments)

                    # Use the model to analyze comments
                    prompt = f"{comments_text}\n\nRead all the comments, then deduce what the users want from these comments and what their requests and desires are. Analyze them and generate titles and content ideas based on the comments. For each idea, include the following format: Title: 'put here the title that you generated', Comment that inspired the idea: 'put here the comment that inspired you', Tip: 'put here some tips for YouTubers to execute this idea', put it in table from 3 columns, extract as you can ideas in the results, at least more than 150 items."
                    response = model.generate_content(prompt)

                    # Display the result
                    st.subheader('Analysis Result:')
                    st.write(response.text)
                else:
                    st.error('No video ID found in the search results.')
            else:
                st.error('No videos found for the given keyword in Arabic.')
        
        # النقطة رقم 6: الإشارة إلى انتهاء العملية
        st.write("Search Finish!")
    else:
        st.error('Please enter a keyword to search.')

# CSS مخصص لإخفاء الروابط عند تمرير الفأرة
hide_links_style = """
    <style>
    a {
        text-decoration: none;
        color: inherit;
        pointer-events: none;
    }
    a:hover {
        text-decoration: none;
        color: inherit;
        cursor: default;
    }
    </style>
    """
st.markdown(hide_links_style, unsafe_allow_html=True)
