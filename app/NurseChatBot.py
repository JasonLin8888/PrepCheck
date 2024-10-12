import os

# Import the OpenAI library to interact with OpenAI's API
from openai import OpenAI

#client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
import gradio


messages = [{"role": "system", "content": "You are a nurse that will help assist with a surgery checklist"}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model = "gpt-3.5-turbo",
    messages = messages)

    ChatGPT_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

demo = gradio.Interface(fn=CustomChatGPT, inputs = "text", outputs = "text", title = "Nurse ")

demo.launch(share=True)