from flask import Flask, request, jsonify
import requests
import base64
from io import BytesIO
from PIL import Image
import json
import time
from requests.exceptions import RequestException

import logging

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.get_json()
    url = 'http://127.0.0.1:8188/prompt'  # ComfyUI API endpoint

    # Send generation request to ComfyUI
    response = requests.post(url, json=data)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to submit prompt'}), 500

    prompt_id = response.json().get('prompt_id')
    if not prompt_id:
        return jsonify({'error': 'No prompt ID returned'}), 500

    # Poll for result completion
    image_data = poll_for_completion(prompt_id)
    if image_data is None:
        return jsonify({'error': 'Failed to retrieve image'}), 500

    # Return base64-encoded image
    return jsonify({'image': base64.b64encode(image_data).decode('utf-8')})

def poll_for_completion(prompt_id):
    history_url = f'http://127.0.0.1:8188/history/{prompt_id}'
    start_time = time.time()
    
    while time.time() - start_time < 20:  # 20 seconds timeout
        try:
            res = requests.get(history_url)
            if res.status_code == 200:
                response_json = res.json()
                if prompt_id in response_json and 'outputs' in response_json[prompt_id]:
                    output_info = response_json[prompt_id]['outputs']
                    for key in output_info:
                        if 'images' in output_info[key]:
                            image_info = output_info[key]['images'][0]  # Assuming first image is the target
                            image_path = image_info['filename']
                            if image_info['subfolder']:
                                image_path = f"{image_info['subfolder']}/{image_path}"
                            return get_image_data(image_path)
            time.sleep(1)  # 1 second delay between polling attempts
        except RequestException as e:
            print(f"Failed to poll history: {e}")  # Debug print
            break  # Exit the loop if there's a network error

    return None  # Return None if the image isn't ready in time or there's an error

def get_image_data(image_path):
    """Retrieve the actual image from the ComfyUI server and return as bytes."""
    view_url = f'http://127.0.0.1:8188/view?filename={image_path}'
    response = requests.get(view_url)
    if response.status_code == 200:
        return response.content
    return None

if __name__ == '__main__':
    app.run(debug=True, port=8189)
