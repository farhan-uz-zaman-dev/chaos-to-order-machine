import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Idea Organizer", page_icon="🧠")

st.title("🧠 The Chaos-to-Order Machine")
st.write("Dump your messy thoughts here, and I will give you perfect AI prompts!")

# Sidebar for the secret key
with st.sidebar:
    st.header("🔑 Setup")
    api_key = st.text_input("Paste your Secret API Key here:", type="password")

# The instructions telling the AI how to behave
SYSTEM_INSTRUCTION = """
You are an expert Prompt Helper. The user will give you a messy, chaotic brain dump of an idea. 
Turn it into a detailed, step-by-step sequence of prompts (Prompt 1, Prompt 2, Prompt 3) 
inside markdown code blocks so they can easily copy and paste them into ChatGPT or Claude.
"""

# The input box
user_idea = st.text_area("👇 Type your messy gibberish thoughts here:")

if st.button("✨ Fix My Idea!", type="primary"):
    if not api_key:
        st.error("Oops! You forgot to paste your Secret Key in the sidebar!")
    elif not user_idea:
        st.warning("Type something first!")
    else:
        with st.spinner("Thinking... 🧠"):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_idea,
                    config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
                )
                st.success("Done! Here is your plan:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Something went wrong: {e}")