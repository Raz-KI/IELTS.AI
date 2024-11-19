import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key="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")

@app.route("/")
def allmockai():
    return render_template("home.html")

@app.route("/speaking")
def speaking():
    return render_template("speaking.html")

@app.route("/writing")
def writing():
    return render_template("writing.html")


# SPEAKING
interview_data = [{"question": "Hello, Introduce Yourself", "answer": None}]

# Function to get AI-generated interview question from Groq. We give prompt to this function
def get_ai_question(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an IELTS interviewer. You have to generate only questions no other text."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

@app.route('/api/start_interview', methods=['GET'])
def start_interview():
    first_question = "Hello Candidate! Introduce yourself."
    interview_data.append({"question": first_question, "answer": None})  # Store first question
    return jsonify({'question': first_question})

# API route for asking follow-up questions based on candidate's answer
@app.route('/api/answer', methods=['POST'])
def receive_answer():
    candidate_answer = request.json.get('answer')
    follow_count = request.json.get('follow_up_count', 0)
    
    # Process candidate's answer and store it
    last_entry = interview_data[-1]  # Get the last question-answer entry

    # Store the candidate's answer for the last question
    last_entry['answer'] = candidate_answer  
    
    # Collect emotion data for the last question (if implemented on frontend)
    # emotion_data = request.json.get('emotion_data')
    # last_entry['emotion'] = emotion_data

    # Increment follow-up count
    follow_count += 1
    
    if follow_count <= 2:
        follow_up = get_ai_question(f"The candidate said: '{candidate_answer}'. Now ask a question which can be asked in IELTS speaking section")
    else:
        follow_up = get_ai_question(f"The candidate said: '{candidate_answer}'. Now ask a question which can be asked in IELTS speaking section")
    
    # Add the new question (either follow-up or new) to the interview data
    interview_data.append({"question": follow_up, "answer": None})

    return jsonify({'follow_up': follow_up, 'follow_up_count': follow_count})

if __name__ == '__main__':
    app.run(debug=True)
