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
if 'all_wishes' not in st.session_state:
    st.session_state.all_wishes = []  # Track all wishes

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
    .positive-wish {
        border-left: 5px solid #28a745;
        padding-left: 15px;
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

def evaluate_wish_sentiment(wish_text):
    """Custom function to evaluate wish sentiment - more permissive for wishes"""
    try:
        # Try Hugging Face model first
        pipe = pipeline("sentiment-analysis")
        result = pipe(wish_text[:512])[0]
        
        # Store the result
        st.session_state.all_wishes.append({
            'text': wish_text[:100],  # Store first 100 chars
            'label': result['label'],
            'score': result['score']
        })
        
        # For Christmas wishes, be more lenient
        christmas_keywords = ['wish', 'hope', 'want', 'dream', 'would like', 'aspire', 'desire',
                             'merry', 'christmas', 'happy', 'joy', 'peace', 'love', 'health']
        
        # Check if it contains wish-related keywords
        has_wish_keyword = any(keyword in wish_text.lower() for keyword in ['wish', 'hope', 'want', 'dream'])
        
        # Check score - be more lenient (accept anything above 0.3 for positive)
        if result['label'] == 'POSITIVE' and result['score'] > 0.3:
            return 'POSITIVE', result['score']
        elif has_wish_keyword and result['score'] > 0.2:
            # If it has wish keywords, treat as positive even with lower score
            return 'POSITIVE', max(result['score'], 0.5)
        elif 'christmas' in wish_text.lower() or 'merry' in wish_text.lower():
            # Christmas-related wishes are always positive
            return 'POSITIVE', 0.8
        else:
            return result['label'], result['score']
            
    except Exception as e:
        # Fallback: If model fails, assume positive for wishes
        print(f"Model error: {e}")
        return 'POSITIVE', 0.7

# Main App
st.title("2026 Wish Facilitator")
st.markdown("### Hi there, Merry Christmas! 🎄")

# Add some Christmas spirit
st.markdown("*🎅 Santa's elves are ready to evaluate your wish for 2026!*")

# Wish input for everyone
wish_prompt = st.text_area(
    "Tell me your wish for 2026, and I'll assess how likely it is to come true:",
    placeholder="E.g., I wish to learn a new language in 2026...",
    key="wish_input",
    height=100
)

# Add tips for better wishes
with st.expander("💡 Tips for better wishes"):
    st.markdown("""
    **Start your wish with:**
    - I wish to...
    - I hope to...
    - I want to...
    - My dream is to...
    - I would love to...
    
    **Examples of good wishes:**
    - I wish to learn Spanish in 2026
    - I hope to get a promotion at work
    - My dream is to travel around the world
    - I want to improve my health
    """)

if st.button("🎯 Evaluate My Wish", type="primary"):
    if wish_prompt and len(wish_prompt.strip()) > 3:
        with st.spinner("🔮 The magic elves are evaluating your wish..."):
            time.sleep(1.5)
            
            try:
                # Use custom evaluation function
                label, score = evaluate_wish_sentiment(wish_prompt)
                
                if label == 'POSITIVE':
                    # Calculate probability (60-80% range for positive wishes)
                    base_probability = 60.0 + (score * 20)  # 60-80% range
                    
                    st.success("🌟 **Great wish! The Christmas spirit approves!**")
                    st.markdown(f'<div class="positive-wish">🎄 **Your wish:** "{wish_prompt[:200]}..."</div>', unsafe_allow_html=True)
                    st.info(f"**Initial probability:** **{base_probability:.1f}%**")
                    
                    # Save wish data
                    st.session_state.my_wish_text = wish_prompt
                    st.session_state.my_wish_probability = base_probability
                    st.session_state.wish_id = generate_wish_id(wish_prompt)
                    
                    # Support section
                    st.markdown("---")
                    st.markdown("### ❤️ Increase Your Probability!")
                    st.markdown("*Click the hearts to add random Christmas luck (1-10% each)!*")
                    
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
                                if st.button(f"✨\n+{button_data['increment']}%", key=f"support_{i}"):
                                    # Update probability
                                    st.session_state.my_wish_probability = min(
                                        99.9, 
                                        st.session_state.my_wish_probability + button_data['increment']
                                    )
                                    # Mark button as used
                                    st.session_state.support_clicks[current_support_key][i]['used'] = True
                                    st.rerun()
                            else:
                                st.button(f"✅\nUsed", key=f"used_{i}", disabled=True)
                    
                    # Display current probability
                    current_prob = st.session_state.my_wish_probability
                    st.markdown(f"**Current probability: {current_prob:.1f}%**")
                    
                    # Progress bar
                    progress = current_prob / 100
                    st.progress(progress)
                    
                    if current_prob >= 80:
                        st.balloons()
                        st.success("🎉 **Amazing! With this much support, your wish is very likely to come true!**")
                    
                    # Share section
                    st.markdown("---")
                    st.markdown("### 📤 Share with Friends")
                    st.markdown("*Get more Christmas luck from friends!*")
                    
                    share_link = create_share_link(st.session_state.wish_id, wish_prompt)
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.code(share_link, language="text")
                    with col2:
                        if st.button("📋 Copy Link", key="copy_main"):
                            try:
                                pyperclip.copy(share_link)
                                st.success("✅ Copied!")
                            except:
                                st.info("📝 Link ready to share")
                    with col3:
                        if st.button("🔄 New Wish"):
                            # Clear current wish to make a new one
                            st.session_state.my_wish_text = ""
                            st.session_state.my_wish_probability = 0
                            st.rerun()
                    
                    st.markdown("💌 *Send this link to friends. Each friend's click adds random Christmas luck!*")
                    
                else:
                    # Show more helpful feedback
                    st.warning("### 🎄 Let's Make This Wish Even Better!")
                    st.markdown(f"""
                    **Your wish:** "{wish_prompt[:150]}..."
                    
                    **Tips to improve:**
                    1. **Start with positive words** like "I wish", "I hope", "I want"
                    2. **Be specific** about what you want
                    3. **Focus on positive outcomes**
                    4. **Use present tense** as if it's already happening
                    
                    **Example:** Instead of "I don't want to be stressed", try "I wish to find peace and balance in 2026"
                    """)
                    
                    # Quick improvement options
                    st.markdown("### Quick Improvement:")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✨ Rephrase as positive wish"):
                            new_text = wish_prompt
                            # Simple transformation
                            if "don't" in wish_prompt.lower() or "not" in wish_prompt.lower():
                                new_text = wish_prompt.replace("don't", "want to").replace("not", "")
                                new_text = "I wish to " + new_text.lower().split("i ")[-1] if "i " in new_text.lower() else "I wish " + new_text
                            st.text_area("Improved version:", value=new_text, key="improved_wish")
                    with col2:
                        if st.button("🎯 Try Again"):
                            st.rerun()
                        
            except Exception as e:
                st.error(f"⚠️ Technical issue: {str(e)[:100]}")
                # Always positive fallback for Christmas
                st.success("🎄 **Christmas magic says your wish is POSITIVE!**")
                base_probability = 65.0
                st.info(f"**Initial probability: {base_probability:.1f}%**")
                
                # Save anyway
                st.session_state.my_wish_text = wish_prompt
                st.session_state.my_wish_probability = base_probability
                st.session_state.wish_id = generate_wish_id(wish_prompt)
    else:
        st.warning("📝 Please write your wish (at least 4 characters)")

# Check for shared wish (AFTER main wish evaluation)
query_params = st.query_params
shared_wish_id = query_params.get("wish_id", [None])[0]
shared_wish_text = query_params.get("wish", [None])[0]

# If shared wish exists, show support page
if shared_wish_id and shared_wish_text:
    st.markdown("---")
    st.markdown("### ❤️ **Share Your Christmas Luck!**")
    
    with st.container():
        st.markdown('<div class="wish-card">', unsafe_allow_html=True)
        st.markdown(f"**🎯 Friend's Wish:**")
        st.markdown(f"> *{urllib.parse.unquote(shared_wish_text)}...*")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    💌 **Message from your friend:**
    *"Merry Christmas! I just made a wish for 2026. 
    Please click the heart button to share your Christmas luck and help make my wish come true!"*
    """)
    st.markdown("---")
    
    # Generate random increment
    increment = get_random_increment()
    
    # Support button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"🎁 **Click to Add +{increment}% Christmas Luck**", type="primary", use_container_width=True):
            if shared_wish_id not in st.session_state.supported_wishes:
                with st.spinner("🎅 Sending your Christmas luck..."):
                    time.sleep(1)
                
                st.session_state.supported_wishes[shared_wish_id] = increment
                st.balloons()
                st.success(f"""
                🎉 **Thank you for sharing your Christmas luck!** 
                
                *You added +{increment}% to your friend's wish!*
                
                **✨ May your kindness return to you threefold in 2026!**
                """)
                time.sleep(2)
                st.markdown("---")
                st.markdown("### 🎄 Now Make Your Own Wish Above!")
            else:
                st.info("🌟 You've already shared your Christmas luck for this wish! Thank you!")

# Footer
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("*Hope you will have fun with this app! - Elena*")
with col2:
    if st.button("🔄 Reset All"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
