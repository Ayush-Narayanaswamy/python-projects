from flask import Flask, request, render_template, jsonify
import requests
from transformers import pipeline # pyright: ignore[reportMissingImports]
import json
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize the text classification pipeline
analyzer = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=-1  # Use CPU
)

def calculate_match_percentage(resume_keywords, job_keywords):
    """Calculate percentage match based on keyword overlap"""
    resume_words = set(resume_keywords.lower().split())
    job_words = set(job_keywords.lower().split())
    common_words = resume_words.intersection(job_words)
    return (len(common_words) / len(job_words)) * 100 if job_words else 0

def analyze_match(resume_text, job_description):
    """
    Analyze the match between resume and job description using FLAN-T5.
    Returns a percentage match and improvement suggestions.
    """
    try:
        # Extract skills from resume
        resume_skills_prompt = f"Extract key skills and experiences from this resume: {resume_text}"
        resume_skills = analyzer(resume_skills_prompt, max_length=100)[0]['generated_text']

        # Extract requirements from job description
        job_skills_prompt = f"Extract key requirements and skills from this job description: {job_description}"
        job_skills = analyzer(job_skills_prompt, max_length=100)[0]['generated_text']

        # Calculate match percentage
        match_percentage = calculate_match_percentage(resume_skills, job_skills)

        # Generate improvement suggestions
        suggestions_prompt = f"What skills are missing from the resume ({resume_skills}) compared to the job requirements ({job_skills})? List specific suggestions for improvement."
        suggestions = analyzer(suggestions_prompt, max_length=150)[0]['generated_text']

        # Format response
        analysis = {
            "percentage": round(match_percentage, 1),
            "matching_skills": [skill.strip() for skill in resume_skills.split(',') if skill.strip()],
            "missing_skills": [skill.strip() for skill in job_skills.split(',') if skill.strip() and skill.strip() not in resume_skills],
            "suggestions": [sugg.strip() for sugg in suggestions.split('.') if sugg.strip()]
        }
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    resume = data.get('resume', '')
    job_description = data.get('job_description', '')
    
    if not resume or not job_description:
        return jsonify({'error': 'Both resume and job description are required'}), 400
    
    analysis = analyze_match(resume, job_description)
    return jsonify({'analysis': analysis})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(debug=True)