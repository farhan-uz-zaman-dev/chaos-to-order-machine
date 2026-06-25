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
You are the 'Chaos-to-Order Machine'. Your job is to take a messy app idea and turn it into a complete, chronological sequence of copy-and-paste AI PROMPTS. 

Do not write the programming code yourself! 

Follow these rules carefully:
1. 🧠 Analyze the complexity of the user's idea. 
2. 🗺️ Automatically divide the project into as many small, bite-sized phases as necessary (e.g., 3 steps for simple apps, 5-7 steps for complex apps) so that no individual step breaks the token limits of a coding AI.
3. 🚀 For EVERY single phase you create, write out the exact, highly detailed copy-and-paste prompt. Label them clearly as "Prompt for Step 1", "Prompt for Step 2", etc.
4. 🛑 Explicitly tell the user inside the prompts to run them one by one in a single chat thread, waiting for the code to work perfectly before moving to the next prompt.

Structure your response like this:
- 📋 The Plan: A simple explanation of the app.
- 🛠️ Step-by-Step Prompts: List all your generated prompts at once so the user can see the whole journey.
- 📖 How to Use These Prompts: Add a closing message explaining that the user must open a single, brand-new chat session in their coding AI. Tell them to paste 'Prompt for Step 1' first, make sure the code works perfectly, and then reply in that exact same chat with 'Prompt for Step 2' so the coding AI retains the short-term memory of the app structure.
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
