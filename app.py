from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):

    if uploaded_file is not None:
        # Convert pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')

        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts

    else:
        raise FileNotFoundError("No file found!!")
    

st.set_page_config(page_title="ATS Resume review")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Successfully uploaded")

submit1 = st.button("Tell me about the resume")

submit2 = st.button("How can I improve my skill?")

submit3 = st.button("Percentage match")

input_1_prompt = """
You are an experienced HR with data science, your task is to review the provided resume against the job description for the profile.
Please share your professional experience on whether the candidate's profile aligns with the job description. highlight the strengths and weaknesses of the applicant in relation to this job description. 
"""

input_2_prompt = """
You are an experienced HR with data science, your task is to review the provided resume against the job description for the profile.
"""

input_3_prompt = """
You are a skilled ATS (applicant tracking system) scanner with a deep understanding of data science. your task is to evaluate the given resume 
against the provided job description. give me the percentage match of the resume against the job description. First the output should come as a percentage and then keywords missing, and then detailed review. 
"""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_1_prompt, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)

    else:
        st.write("Please upload a resume in PDF format")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_2_prompt, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)

    else:
        st.write("Please upload a resume in PDF format")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_3_prompt, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)

    else:
        st.write("Please upload a resume in PDF format")