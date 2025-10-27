import io
import base64
from PIL import ImageGrab
import requests

def capture_active_window_screenshot():
    # Capture the entire screen (PIL's ImageGrab on Windows/Mac)
    # To capture only the active window, more platform-specific code is needed.
    screenshot = ImageGrab.grab()
    return screenshot

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def send_to_gemini(image_base64, prompt):
    # Placeholder for Gemini API URL and headers
    gemini_api_url = "https://api.gemini.example/v1/analyze"
    headers = {
        "Authorization": "Bearer GEMINI_API_KEY",
        "Content-Type": "application/json"
    }

    payload = {
        "image": image_base64,
        "prompt": prompt
    }

    response = requests.post(gemini_api_url, json=payload, headers=headers)
    return response.json()

def main():
    prompt = "Describe the content of the screenshot"
    screenshot = capture_active_window_screenshot()
    img_base64 = image_to_base64(screenshot)

    result = send_to_gemini(img_base64, prompt)
    print("Gemini response:", result)

if __name__ == "__main__":
    main()
