### i2i Demo

This script demonstrates the synchronous-like image-to-image generation using the ComfyBridge service and ComfyUI. The script takes user-defined prompts and a source image, encodes the image to base64, and sends a request to the ComfyBridge service. ComfyBridge manages the lifecycle of image generation requests, polling for their completion, and returns the final image as a base64-encoded string.

### Instructions to Run the Script

1. **Install @Acly's [comfyui-tooling-nodes](https://github.com/Acly/comfyui-tooling-nodes)** to enable Load Image base64
   ```
   cd custom_nodes
   git clone https://github.com/Acly/comfyui-tooling-nodes.git
   ``` 
2. **Run ComfyBridge Service.**
3. **Create sandbox and Install the `requests` library** if you haven't already:
   ```sh
   cd demo/i2i
   python -m venv venv
   source venv/bin/activate
   pip3 install requests
   ```
4. **Prepare your `request.json` file** with the appropriate values:
   ```json
   {
     "ckpt_name": "sd_xl_base_1.0.safetensors",
     "positive_prompt": "A beautiful landscape with mountains",
     "negative_prompt": "blurry, low resolution",
     "base_image": "./sample.png"
   }
   ```
5. **Run the script** using the command:
   ```sh
   python3 i2i.py request.json
   ```

This script will read the `request.json` file, encode the provided image, generate a request with the specified prompts and a random seed, and then make a POST request to your ComfyUI service through ComfyBridge.
The final image will be saved as `output_image.png` in the same directory.
