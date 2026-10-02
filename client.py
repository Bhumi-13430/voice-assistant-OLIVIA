from openai import OpenAI

client = OpenAI(
    api_key="<YOUR_OPENAI_API_KEY>",
)


completion = client.chat.completions.create(
    model="gpt-5.6-luna",
    messages=[
        {
            "role": "system",
            "content": "You are a general assistant named Olivia, skilled in general tasks like Alexa and Google Assistant."
        },
        {
            "role": "user",
            "content": "Who is BTS?"
        }
    ]
)

print(completion.choices[0].message.content)


