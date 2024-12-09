from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
import fitz  # PyMuPDF

load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    try:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        return text
    except Exception as e:
        return str(e)

def get_gemini_response(input_text, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_text, pdf_content, prompt])
        return response.text
    except Exception as e:
        return f"Error interacting with Gemini: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_request():
    action = request.form.get('action')
    job_description = request.form.get('job_description')
    resume_file = request.files.get('resume')

    if not job_description or not resume_file:
        return jsonify({'error': 'Please provide both a job description and a resume.'}), 400

    resume_text = extract_text_from_pdf(resume_file)
    if not resume_text:
        return jsonify({'error': 'Error extracting text from the resume.'}), 400

    prompts = {
        'analyze': f"Analyze the resume and job description. Job: {job_description}. Resume: {resume_text}.",
        'improve': f"Suggest improvments on the resume based on the given job description. Give a list of improvements to do on the resume. Job: {job_description}. Resume: {resume_text}.",
        'match': f"Evaluate the percentage match between the job description and resume. Job: {job_description}. Resume: {resume_text}."
    }

    prompt = prompts.get(action)
    if not prompt:
        return jsonify({'error': 'Invalid action'}), 400

    try:
        gemini_response = get_gemini_response(job_description, resume_text, prompt)
        return jsonify({'response': gemini_response})
    except Exception as e:
        return jsonify({'error': f"Error processing request: {str(e)}"}), 500

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
