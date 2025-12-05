import streamlit as st
from transformers import pipeline

st.title("🎄 Christmas 2026 Wish Evaluator")
st.markdown("### Hello! My friend, Wish you a very Merry Christmas!")

wish_prompt = st.text_area(
    "Write down a wish in 2026, I will evaluate the probability:",
    placeholder="E.g., I wish to learn a new language in 2026..."
)

if st.button("Evaluate Wish"):
    if wish_prompt:
        with st.spinner("Evaluating your wish..."):
            try:
                pipe = pipeline("sentiment-analysis")
                wish_result = pipe(wish_prompt)[0]
                
                if wish_result['label'] == 'POSITIVE':
                    base_probability = max(60.0, wish_result['score'] * 100)
                    
                    st.success(f"🌟 Positive wish detected!")
                    st.info(f"Initial probability: **{base_probability:.1f}%**")
                    
                    # Support section
                    st.markdown("---")
                    st.markdown("### Increase Your Probability!")
                    st.markdown("*Share with friends to increase probability*")
                    
                    support_cols = st.columns(5)
                    current_prob = base_probability
                    
                    for i, col in enumerate(support_cols):
                        with col:
                            if st.button(f"❤️\n+9.9%", key=f"support_{i}"):
                                current_prob = min(99.9, current_prob + 9.9)
                                st.session_state[f'prob_{i}'] = True
                                
                    # Calculate final probability
                    final_prob = base_probability
                    for i in range(5):
                        if f'prob_{i}' in st.session_state:
                            final_prob = min(99.9, final_prob + 9.9)
                    
                    if final_prob >= 99.9:
                        st.balloons()
                        st.success("🎉 **The probability is increased to 99.9%! So go for it, and good luck!**")
                    else:
                        st.info(f"Current probability after support: **{final_prob:.1f}%**")
                        
                else:
                    st.warning("Hmm, let's think more positively!")
                    new_wish = st.text_input("Dear, you deserve a better wish: ")
                    if new_wish:
                        st.info("That's the spirit! Now re-evaluate your new wish.")
                        
            except Exception as e:
                st.error(f"Error evaluating wish: {e}")
    else:
        st.warning("Please enter a wish first!")
