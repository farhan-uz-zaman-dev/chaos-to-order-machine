import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Idea Organizer", page_icon="🧠")

st.title("🧠 The Chaos-to-Order Machine")
st.write("Dump your messy thoughts here, and I will give you perfect AI prompts!")

# Pull the secret key automatically from the secure vault!
api_key = st.secrets["GEMINI_API_KEY"]

# The instructions telling the AI how to behave
SYSTEM_INSTRUCTION = """
You are the 'Chaos-to-Order Machine'. Your job is to take a messy app idea and break it down into 4 short, simple steps.

1. 📋 The Plan: Explain the idea simply.
2. 🗺️ The Roadmap: Give 3 tiny steps to build it.
3. 🚀 Step 1 Code: Give ONLY the code for Step 1. Do not write the whole app at once so we don't break the token limits!
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
