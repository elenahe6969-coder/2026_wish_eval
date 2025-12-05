import streamlit as st
from transformers import pipeline
import pyperclip  # For copying to clipboard
import urllib.parse
import time

# Initialize session state for tracking support
if 'supported_wishes' not in st.session_state:
    st.session_state.supported_wishes = {}
if 'my_wish_probability' not in st.session_state:
    st.session_state.my_wish_probability = 0
if 'my_wish_text' not in st.session_state:
    st.session_state.my_wish_text = ""
if 'wish_id' not in st.session_state:
    st.session_state.wish_id = None

st.set_page_config(
    page_title="🎄 Christmas Wish 2026",
    page_icon="🎄",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #FF5252;
        transform: scale(1.05);
    }
    .wish-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    .share-link {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        word-break: break-all;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.title("2026 Wish Facilitator")
st.markdown("### Hi there, my friend! Merry Christmas!🎄")

# Function to generate unique wish ID
def generate_wish_id(wish_text):
    import hashlib
    import time
    unique_str = f"{wish_text}_{time.time()}"
    return hashlib.md5(unique_str.encode()).hexdigest()[:10]

# Function to create shareable link
def create_share_link(wish_id, wish_text):
    base_url = "https://your-app-name.streamlit.app"
    encoded_wish = urllib.parse.quote(wish_text[:50])  # Encode first 50 chars
    return f"{base_url}?wish_id={wish_id}&wish={encoded_wish}"

# Check for incoming shared wish
query_params = st.query_params
shared_wish_id = query_params.get("wish_id", [None])[0]
shared_wish_text = query_params.get("wish", [None])[0]

# If there's a shared wish, show support page
if shared_wish_id and shared_wish_text:
    st.markdown("---")
    st.markdown(f"### ❤️ **Share Your Luck!**")
    st.markdown(f"*A friend needs your support for their 2026 wish!*")
    
    with st.container():
        st.markdown('<div class="wish-card">', unsafe_allow_html=True)
        st.markdown(f"**🎯 Their Wish:**")
        st.markdown(f"> *{urllib.parse.unquote(shared_wish_text)}...*")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
    💌 **Message from your friend:**  
    *"Merry Christmas! I just made a wish for 2026. Please click the heart button to share your luck and increase the probability of my wish coming true!"*
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
# Support button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        support_button = st.button(
            "❤️ **CLICK HERE TO SHARE YOUR LUCK** ❤️",
            type="primary",
            use_container_width=True,
            help="Your click will increase your friend's wish probability!"
        )
    
    if support_button:
        if shared_wish_id not in st.session_state.supported_wishes:
            # Animate the button click
            with st.spinner("🎁 Sending your luck..."):
                time.sleep(1)
            
            st.session_state.supported_wishes[shared_wish_id] = True
            
            # Show success message with animation
            st.balloons()
            st.success("""
            🎉 **Thank you for sharing your luck!**  
            *Your friend's wish probability has increased!*
            
            **✨ Christmas Blessing:**  
            *May your kindness return to you threefold in 2026!*
            """)
            st.markdown("### Now it's your turn to make a wish by clicking below link.")
            st.markdown("### https://2026wisheval-elena-python.streamlit.app/")
          
