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
You are the 'Chaos-to-Order Machine'. Your job is to take a messy app idea and turn it into a clean, highly effective copy-and-paste AI PROMPT. 

Do not write the programming code yourself! Instead, create a prompt that the user can copy and paste into another AI (like ChatGPT or Claude) to build their app step-by-step.

Structure your response like this:
1. 📋 The Plan: A simple explanation of what the app will do.
2. 🗺️ The Roadmap: A breakdown of the app into 3 tiny, simple steps.
3. 🚀 The Prompt for Step 1: Write a detailed prompt that says: "Act as an expert developer. Please write only the code for Step 1 of this app..."
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
