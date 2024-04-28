# ComfyBridge

ComfyBridge is a Python-based service that acts as a bridge to the ComfyUI API, facilitating image generation requests. It manages the lifecycle of image generation requests, polls for their completion, and returns the final image as a base64-encoded string. This wrapper is designed to simplify integration with ComfyUI for developers needing a synchronous-like behavior over an inherently asynchronous operation.

## Features

- **Asynchronous Handling**: Manages asynchronous image generation tasks and provides a synchronous HTTP interface to clients.
- **Base64 Encoding**: Returns images in a base64-encoded format, ready for use in web applications or for further processing.
- **Polling with Timeout**: Implements efficient polling with customizable timeouts to check for image generation completion.

## Getting Started

### Prerequisites

- Python 3.6+
- Flask
- Requests
- Pillow

### Installation and Running

Clone the repository:

```bash
git clone https://github.com/RayKitajima/ComfyBridge.git
cd ComfyBridge
```

Install the required packages and run the Flask application:

```bash
$ python -m venv sandbox
$ cd sandbox/
$ source bin/activate
(sandbox) $ pip3 install flask requests pillow
(sandbox) $ cd ..
(sandbox) $ sandbox/bin/python app.py
```

And also, you need to have the ComfyUI API running on your local machine.

```bash
$ python main.py --listen
```

### Usage

Send a POST request to `/generate` with the appropriate JSON payload:

```bash
curl --location --request POST 'http://localhost:5000/generate' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": {
        "3": {
            "inputs": {
                "seed": 598407938235545,
                "steps": 20,
                "cfg": 8,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
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
                    "5",
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
                "ckpt_name": "PVCStyleModelMovable_beta25Realistic.safetensors"
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {
                "title": "Load Checkpoint"
            }
        },
        "5": {
            "inputs": {
                "width": 512,
                "height": 512,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage",
            "_meta": {
                "title": "Empty Latent Image"
            }
        },
        "6": {
            "inputs": {
                "text": "icon portrait of Female, surreal,amazing quality,masterpiece,best quality,awesome,inspiring,cinematic composition,soft shadows,Film grain,shallow depth of field,highly detailed,high budget,cinemascope,epic,color graded cinematic,atmospheric lighting,natural,figure,natural lighting,exqusite visual effect,delicate details,\n1girl, hoshino ai \\(oshi no ko\\), oshi no ko,star (symbol),solo,hair ornament,purple hair,rabbit hair ornament,gloves,long hair,star-shaped pupils,tongue,tongue out,pink gloves,dress,symbol-shaped pupils,heart,purple eyes,idol clothes,idol,pink dress,star hair ornament,heart hands,sleeveless,brooch,frills,heart brooch,armpits,frilled dress,looking at viewer,hair between eyes,sidelocks,blush,turtleneck dress,sleeveless dress,frilled gloves,smile,closed mouth,jewelry,one side up,multicolored hair,upper body,ribbon, White background",
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
                "text": "lowres,(bad),text,error,fewer,extra,missing,worst quality,jpeg artifacts,low quality,watermark,unfinished,displeasing,oldest,early,chromatic aberration,signature,extra digits,artistic error,username,scan,[abstract],cleavage,nipples,",
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
        }
    }
}'
```

## API Reference

### POST `/generate`

Accepts a JSON payload with the generation request details and returns a base64-encoded image.

#### Input

- `prompt`: JSON object representing the image generation prompt and configuration.

#### Output

- `image`: Base64-encoded string of the generated image.
