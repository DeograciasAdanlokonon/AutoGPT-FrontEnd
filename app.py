from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import openai
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Assurez-vous que les dossiers existent
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# main AutoGPT def
def perform_task(task, context):
    # Combine context and the task into a single prompt
    prompt = (
        f"You are AutoGPT, an AI assistant capable of breaking down complex goals into smaller tasks "
        f"and autonomously solving them step-by-step. Here is the current task:\n\n{task}\n\n"
        f"Context so far:\n{context}\n\n"
        f"Please provide your next steps and their expected results."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({
            'success': True,
            'filename': filename,
            'size': os.path.getsize(filepath)
        })


# route /chat
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()  # User's input message
        context = data.get('context', [])  # Optional: contextual history
        filename = data.get('filename', None)

        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Process file if provided
        file_content = ""
        if filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as file:
                    file_content = file.read()
            else:
                return jsonify({'error': f'File "{filename}" not found'}), 400

        # Combine file content with the task
        goal = f"{user_message}\n\nThe file content is as follows:\n{file_content}" if file_content else user_message
        subtask_history = []

        # Initial task execution
        task_result = perform_task(goal, context)
        subtask_history.append(task_result)

        # Return the task's result
        return jsonify({
            "success": True,
            "result": task_result,
            "subtask_history": subtask_history
        })

    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
