from flask import Flask, request, render_template, jsonify
import os
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize Flask app
app = Flask(__name__)

class SkillsExtractor:
    def __init__(self):
        self.common_skills = [
            'python', 'java', 'javascript', 'html', 'css', 'sql', 'react', 'angular',
            'node.js', 'express', 'django', 'flask', 'aws', 'azure', 'docker', 'kubernetes',
            'machine learning', 'data analysis', 'agile', 'scrum', 'git', 'ci/cd',
            'leadership', 'communication', 'problem solving', 'teamwork', 'project management',
            'tensorflow', 'pytorch', 'pandas', 'numpy', 'mongodb', 'postgresql', 'redis',
            'typescript', 'vue', 'bootstrap', 'tailwind', 'graphql', 'rest', 'api'
        ]
        
    def extract_skills(self, text):
        """Extract key skills and keywords"""
        text = text.lower()
        found_skills = [skill for skill in self.common_skills if skill in text]
        return found_skills

# Initialize the skills extractor
skills_extractor = SkillsExtractor()

def analyze_match(resume_text, job_description):
    """
    Analyze the match between resume and job description using ML.
    Returns a dictionary with analysis results.
    """
    try:
        # Extract skills
        resume_skills = skills_extractor.extract_skills(resume_text)
        job_skills = skills_extractor.extract_skills(job_description)
        
        # Calculate semantic similarity using TF-IDF and cosine similarity
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        match_percentage = similarity * 100
        
        # Find matching and missing skills
        matching_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))
        
        # Generate specific suggestions
        suggestions = []
        if missing_skills:
            if len(missing_skills) <= 3:
                suggestions.append(f"Add these missing skills: {', '.join(missing_skills)}")
            else:
                suggestions.append(f"Focus on these top missing skills: {', '.join(missing_skills[:3])}")
        
        if match_percentage < 60:
            suggestions.append("Use more keywords from the job description in your resume")
            suggestions.append("Quantify your achievements with specific numbers and metrics")
        elif match_percentage > 80:
            suggestions.append("Excellent match! Your resume aligns well with this position")
        else:
            suggestions.append("Good match! Consider tweaking some sections for better alignment")
            
        if len(matching_skills) < 3:
            suggestions.append("Highlight more relevant technical skills in your resume")

        return {
            "percentage": round(match_percentage, 1),
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions
        }
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")  # Debug print
        return {
            "percentage": 0,
            "matching_skills": [],
            "missing_skills": [],
            "suggestions": [f"Analysis error: {str(e)}"]
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        resume = data.get('resume', '').strip()
        job_description = data.get('job_description', '').strip()
        
        if not resume or not job_description:
            return jsonify({'error': 'Both resume and job description are required'}), 400
        
        analysis = analyze_match(resume, job_description)
        return jsonify({'analysis': analysis})
        
    except Exception as e:
        print(f"Error in /analyze route: {str(e)}")  # Debug print
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("Created templates directory")
    
    print("Starting Flask server...")
    app.run(debug=True, host='127.0.0.1', port=5000)