import base64
import click
from openai import OpenAI

client = OpenAI()

IMAGE_URL =  "https://binaryville.com/images/products/rex-microcontrollers-mug-black.jpg"

with open("rex-microcontrollers-mug-black.jpg", "rb") as f:
    file_content = f.read()
    base64_image = base64.b64encode(file_content).decode("utf-8")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": 'I need to know if this matches my mug-set. What colors are used in this mug? Output should be JSON list: ["color1", "color2"]',
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": IMAGE_URL,
                    },
                },
            ],
        }
    ],
    max_tokens=300,
)
try:
    click.secho(response.choices[0].message.content, fg="cyan")
except:
    print(response.choices[0].message.content)
