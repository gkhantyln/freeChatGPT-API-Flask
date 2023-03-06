from flask import Flask, request, jsonify, render_template
import requests
import json
import markdown


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chatbot', methods=['POST'])
def chatbot():
    url = "https://chatgpt-api.shn.hk/v1/"
    headers = {"Content-Type": "application/json"}

    input_text = request.form['input_text']
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": input_text}]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        message = response.json()
        content = message['choices'][0]['message']['content']
        content_md = markdown.markdown(content)  # Markdown format dönüştür
        '''prompt_tokens = message['usage']['prompt_tokens']
        completion_tokens = message['usage']['completion_tokens']
        total_tokens = message['usage']['total_tokens']'''
        output_text = f"AI : <br>{content_md}<br>"
        # <br>Prompt tokens: {prompt_tokens}<br>Completion tokens: {completion_tokens}<br>Total tokens: {total_tokens}
        return jsonify({'response': output_text})
    else:
        error_message = f"Hata olestr: {response.status_code} {response.reason}"
        return jsonify({'error': error_message})


if __name__ == '__main__':
    app.run(debug=True)
