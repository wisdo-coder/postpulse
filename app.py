# Minimal Streamlit app for Day 1: caption generator using OpenAI.

import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.warning("OPENAI_API_KEY not set. Set it as an environment variable or in a .env file before running.")

openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="AI Social Engine — Starter", layout="centered")
st.title("AI Social Engine — Caption Generator (Day 1)")
st.write("Enter basic business info and get a week's worth of social captions.")

with st.form(key='gen_form'):
    business_name = st.text_input('Business name')
    business_desc = st.text_area('Short description of the business (1-2 sentences)')
    tone = st.selectbox('Tone', ['Professional', 'Casual', 'Playful'])
    posts_per_week = st.slider('Posts per week', 1, 7, 3)
    submit = st.form_submit_button('Generate')

if submit:
    if not OPENAI_API_KEY:
        st.error('OpenAI API key missing — please add OPENAI_API_KEY environment variable.')
    elif not business_name or not business_desc:
        st.error('Please provide both business name and description.')
    else:
        prompt = f"Generate {posts_per_week} social media post captions for a business named {business_name}. "
        prompt += f"Business description: {business_desc}. Tone: {tone}. For each post give: caption, 2 hashtags, a short CTA. Return in JSON format." 

        with st.spinner('Generating...'):
            try:
                resp = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{'role':'system','content':'You are a helpful assistant that outputs JSON only.'},
                              {'role':'user','content':prompt}],
                    max_tokens=600,
                    temperature=0.3
                )
                text = resp['choices'][0]['message']['content']
            except Exception as e:
                st.error(f'OpenAI API error: {e}')
                text = None

        if text:
            st.subheader('Generated Output')
            st.code(text, language='json')
            st.download_button('Download captions.json', text)
