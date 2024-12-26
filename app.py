from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging

# Set your API key directly
api_key = "AIzaSyBnfNFKT7I_u3pp9jguM5OxP_-EEyJDm6A"

# Configure the API
genai.configure(api_key=api_key)

# Define the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="Create a conversational chatbot API that guides candidates through a recruitment process. The chatbot should ask a series of structured questions related to the job position, including but not limited to: 'Tell me about yourself', 'What experience do you have in this field?', 'Why do you want to work with us?', 'Can you explain a challenging situation you’ve encountered at work?', 'What are your salary expectations?', 'What is your availability?', and 'Do you have any questions for us?'. Each response should be tailored based on the candidate’s previous answer, and the chatbot should provide appropriate follow-up questions. Ensure that the questions sound professional and foster a natural, engaging conversation. The system should also handle user errors gracefully, encouraging further engagement and clarification if needed."
    )
    print("Model initialized successfully.")
except Exception as e:
    print(f"Failed to initialize the model: {e}")
    exit()

# Initialize Flask app
app = Flask(__name__)

# Initialize history for the conversation
history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user input from the request
        user_input = request.json.get("user_input")
        
        if not user_input:
            return jsonify({"error": "No user input provided"}), 400
        
        # Create a new chat session and send the message to the model
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)
        model_response = response.text

        # Append the user input and bot response to the history
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [model_response]})

        return jsonify({"response": model_response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
