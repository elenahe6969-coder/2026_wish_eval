import streamlit as st
from transformers import pipeline
import pyperclip
import urllib.parse
import time
import random

# Initialize session state
if 'supported_wishes' not in st.session_state:
    st.session_state.supported_wishes = {}
if 'my_wish_probability' not in st.session_state:
    st.session_state.my_wish_probability = 0
if 'my_wish_text' not in st.session_state:
    st.session_state.my_wish_text = ""
if 'wish_id' not in st.session_state:
    st.session_state.wish_id = None
if 'support_clicks' not in st.session_state:
    st.session_state.support_clicks = {}

st.set_page_config(
    page_title="🎄 Christmas Wish 2026",
    page_icon="🎄",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: bold;
    }
    .wish-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Functions
def get_random_increment():
    return round(random.uniform(1.0, 10.0), 1)

def generate_wish_id(wish_text):
    import hashlib
    unique_str = f"{wish_text}_{time.time()}"
    return hashlib.md5(unique_str.encode()).hexdigest()[:10]

def create_share_link(wish_id, wish_text):
    base_url = "https://2026wisheval-elena-python.streamlit.app"
    encoded_wish = urllib.parse.quote(wish_text[:50])
    return f"{base_url}?wish_id={wish_id}&wish={encoded_wish}"

# Main App
st.title("2026 Wish Facilitator")
st.markdown("### Hi there, my friend! Merry Christmas! 🎄")

# Wish input for everyone
wish_prompt = st.text_area(
    "Tell me your wish for 2026, and I'll assess how likely it is to come true.",
    placeholder="E.g., I wish to learn a new language in 2026...",
    key="wish_input"
)

if st.button("Evaluate the probability", type="primary"):
    if wish_prompt and len(wish_prompt.strip()) > 3:
        with st.spinner("Evaluating..."):
            time.sleep(1)
            
            try:
                pipe = pipeline("sentiment-analysis")
                wish_result = pipe(wish_prompt[:512])[0]
                
                if wish_result['label'] == 'POSITIVE':
                    base_probability = (60.0 + wish_result['score'] * 100) / 2
                    
                    st.success("🌟 Nice work! That's a wonderful wish.")
                    st.info(f"Initial probability: **{base_probability:.1f}%**")
                    
                    # Save wish data
                    st.session_state.my_wish_text = wish_prompt
                    st.session_state.my_wish_probability = base_probability
                    st.session_state.wish_id = generate_wish_id(wish_prompt)
                    
                    # Support section
                    st.markdown("---")
                    st.markdown("### Increase The Probability!")
                    st.markdown("*Click hearts to add random luck (1-10% each)*")
                    
                    # Generate 5 support buttons with random increments
                    support_cols = st.columns(5)
                    
                    # Initialize or get existing support clicks for this session
                    current_support_key = f"wish_{st.session_state.wish_id}"
                    if current_support_key not in st.session_state.support_clicks:
                        st.session_state.support_clicks[current_support_key] = {}
                    
                    # Create support buttons
                    for i in range(5):
                        with support_cols[i]:
                            # Get random increment for this button
                            if i not in st.session_state.support_clicks[current_support_key]:
                                increment = get_random_increment()
                                # Store the increment for this button
                                st.session_state.support_clicks[current_support_key][i] = {
                                    'increment': increment,
                                    'used': False
                                }
                            
                            button_data = st.session_state.support_clicks[current_support_key][i]
                            
                            if not button_data['used']:
                                if st.button(f"❤️\n+{button_data['increment']}%", key=f"support_{i}"):
                                    # Update probability
                                    st.session_state.my_wish_probability = min(
                                        99.9, 
                                        st.session_state.my_wish_probability + button_data['increment']
                                    )
                                    # Mark button as used
                                    st.session_state.support_clicks[current_support_key][i]['used'] = True
                                    st.rerun()
                            else:
                                st.button(f"❤️\nUsed", key=f"used_{i}", disabled=True)
                    
                    # Display current probability
                    current_prob = st.session_state.my_wish_probability
                    st.markdown(f"**Current probability: {current_prob:.1f}%**")
                    
                    # Progress bar
                    progress = current_prob / 100
                    st.progress(progress)
                    
                    if current_prob >= 80:
                        st.balloons()
                        st.success("🎉 **Your friends shared their luck with you! Just do it to make it happen. Good luck!**")
                    
                    # Share section
                    st.markdown("---")
                    st.markdown("### Share with Friends")
                    st.markdown("*Get more luck from friends!*")
                    
                    share_link = create_share_link(st.session_state.wish_id, wish_prompt)
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.code(share_link)
                    with col2:
                        if st.button("📋 Copy"):
                            try:
                                pyperclip.copy(share_link)
                                st.success("Copied!")
                            except:
                                st.info("Link ready to share")
                    
                    st.markdown("*Send this link to friends. Each click adds random luck!*")
                    
                else:
                    st.warning("Hmm, You might want to think of a more specific one.")
                        
            except Exception as e:
                st.error(f"Error: {str(e)[:100]}")
                # Fallback
                st.info("🎄 Your wish has been recorded! Probability: 60%")
    else:
        st.warning("Please enter a wish (at least 4 characters)")
        
# Check for shared wish
query_params = st.query_params
shared_wish_id = query_params.get("wish_id", [None])[0]
shared_wish_text = query_params.get("wish", [None])[0]

# If shared wish exists, show support page
if shared_wish_id and shared_wish_text:
    st.markdown("---")
    st.markdown("### ❤️ **Share Your Luck!**")
    
    with st.container():
        st.markdown('<div class="wish-card">', unsafe_allow_html=True)
        st.markdown(f"**Their Wish:**")
        st.markdown(f"> *{urllib.parse.unquote(shared_wish_text)}...*")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("*Merry Christmas! I just made a wish for 2026. Please click the heart button to share your luck!*")
    st.markdown("---")
    
    # Generate random increment
    increment = get_random_increment()
    
    # Support button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"❤️ **Click to Add +{increment}% Luck** ❤️", type="primary", use_container_width=True):
            if shared_wish_id not in st.session_state.supported_wishes:
                with st.spinner("Sending your luck..."):
                    time.sleep(1)
                
                st.session_state.supported_wishes[shared_wish_id] = increment
                st.balloons()
                st.success(f"🎉 Thank you! You added +{increment}% luck!")
                time.sleep(2)
                st.markdown("---")
                st.markdown("### Now make your own wish!")
            else:
                st.info("You've already supported this wish!")
    
else:
    # Main wish input (only show when no shared wish is being viewed)
    st.markdown("### Make Your Wish for 2026")



# Footer
st.markdown("---")
st.markdown("*🎄 Share the Christmas spirit with friends! Elena*")
