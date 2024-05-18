import json
import base64
import sys
import random
import requests

# Function to encode an image to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

# Function to create the request JSON
def create_request_json(user_data):
    # Load the JSON template
    template = {
        "prompt": {
            "3": {
                "inputs": {
                    # Generating a random seed
                    "seed": random.randint(0, 4294967295),
                    "steps": 20,
                    "cfg": 8,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 0.6,
                    "model": [
                        "4",
                        0
                    ],
                    "positive": [
                        "6",
                        0
                    ],
                    "negative": [
                        "7",
                        0
                    ],
                    "latent_image": [
                        "11",
                        0
                    ]
                },
                "class_type": "KSampler",
                "_meta": {
                    "title": "KSampler"
                }
            },
            "4": {
                "inputs": {
                    "ckpt_name": user_data["ckpt_name"],
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {
                    "title": "Load Checkpoint"
                }
            },
            "6": {
                "inputs": {
                    "text": user_data["positive_prompt"],
                    "clip": [
                        "4",
                        1
                    ]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Prompt)"
                }
            },
            "7": {
                "inputs": {
                    "text": user_data["negative_prompt"],
                    "clip": [
                        "4",
                        1
                    ]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Prompt)"
                }
            },
            "8": {
                "inputs": {
                    "samples": [
                        "3",
                        0
                    ],
                    "vae": [
                        "4",
                        2
                    ]
                },
                "class_type": "VAEDecode",
                "_meta": {
                    "title": "VAE Decode"
                }
            },
            "9": {
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": [
                        "8",
                        0
                    ]
                },
                "class_type": "SaveImage",
                "_meta": {
                    "title": "Save Image"
                }
            },
            "11": {
                "inputs": {
                    "pixels": [
                        "13",
                        0
                    ],
                    "vae": [
                        "4",
                        2
                    ]
                },
                "class_type": "VAEEncode",
                "_meta": {
                    "title": "VAE Encode"
                }
            },
            "13": {
                "inputs": {
                    "image": encode_image_to_base64(user_data["base_image"])
                },
                "class_type": "ETN_LoadImageBase64",
                "_meta": {
                    "title": "Load Image (Base64)"
                }
            }
        }
    }

    return template

# Function to save base64 image to PNG file
def save_base64_image(base64_image, output_path):
    image_data = base64.b64decode(base64_image)
    with open(output_path, "wb") as output_file:
        output_file.write(image_data)

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python i2i.py request.json")
        return

    # Load user data from the JSON file
    user_data_path = sys.argv[1]
    with open(user_data_path, "r") as user_data_file:
        user_data = json.load(user_data_file)

    # Create the request JSON
    request_json = create_request_json(user_data)

    # POST the request to the ComfyBridge service
    response = requests.post(
        "http://localhost:8189/generate", json=request_json)

    # Check the response
    if response.status_code == 200:
        print("Image generated successfully.")
        # Save the response image if needed
        response_data = response.json()
        save_base64_image(response_data["image"], "output_image.png")
        print("Output image saved to output_image.png")
    else:
        print("Failed to generate image. Status code:", response.status_code)
        print("Response:", response.text)


if __name__ == "__main__":
    main()
