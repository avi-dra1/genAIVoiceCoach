from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import requests
# Import any other necessary libraries

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.json
    image_data = data['image']

    # The image is base64 encoded. Decode it for processing.
    image_data = image_data.split(",")[1]
    print(image_data)
    #image_bytes = base64.b64decode(image_data)

    # Process the image here...
    # For example, analyze the image, store it, or generate an audio response

    analysis = analyze_with_ai(image_data)
    print(analysis)
    # Send back a response
    #return jsonify({"message": "Image processed successfully"})
    #return jsonify({"message": str(analysis)})

    # Generate and return audio response
    audio_data = generate_audio(analysis)
    return jsonify({"audioData": audio_data})

def analyze_with_ai(image):
    from openai import OpenAI
    client = OpenAI()

    prompt_message = f"Context: You are a game industry expert, analyze the screen and suggest the closest match for the game name"
    PROMPT_MESSAGES = {
            "role": "user",
            "content": [
                prompt_message,
                #{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame}"}}
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}
            ],
        }

    # Parameters for API call
    params = {
            "model": "gpt-4-vision-preview",
            "messages": [PROMPT_MESSAGES],
            "max_tokens": 500,
        }

    # Make the API call
    result = client.chat.completions.create(**params)
    return result.choices[0].message.content


def generate_audio(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/2EiwWnXFnvU5JabPnv8n"
    payload = {
        "text": text,
        "voice_settings": {"similarity_boost": 1, "stability": 1},
        "model_id": "eleven_monolingual_v1"
    }
    #headers = {"Content-Type": "application/json"}
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": "b8de3743a695ecff01991dcd1b3f51cf"}
    response = requests.request("POST", url, json=payload, headers=headers)

    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True, port=5001)
