import base64
import click
from openai import OpenAI

client = OpenAI()


with open("refrigirator.png", "rb") as f:
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
                    "text": 'My refrigirator should have. Soy Milk, Cheese, fruits, vigetable and chocolate pudding. What\'s missing? response should be a list of items that are missing ["missing item1", "missing item2", "missing item3", "missing item4", "missing item5"]',
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
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
