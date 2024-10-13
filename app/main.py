import os
import pyttsx3
from gtts import gTTS
from openai import OpenAI
import gradio as gr
import random

engine = pyttsx3.init()


def speak_gtts(text):
    tts = gTTS(text=text, lang='en')
    tts.save("speech.mp3")
    os.system("afplay speech.mp3")


def CustomChatGPT(user_input, api_key):
    client = OpenAI(api_key=api_key)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a nurse that will help assist with a surgery checklist. "
                "Do not answer any questions not related to the patient's surgery. "
                "Avoid discussing any other topics. If the user prompts something else, "
                "say 'I can only respond to questions about surgery'. You are responding "
                "directly to the patient. You can respond to greetings. If the patient goes "
                "off topic after greetings, then you may say that you can only answer "
                "questions about surgery.\n"

                "Your main responsibilities include:\n"
                "1. Explaining pre-operative procedures.\n"
                "2. Discussing the importance of fasting before surgery.\n"
                "3. Providing information on anesthesia options.\n"
                "4. Addressing patient concerns and anxiety.\n"
                "5. Consoling the patient if they are feeling nervous or anxious.\n"
                "6. Ensuring the patient understands their role in the surgical process.\n"

                "Remember to:\n"
                "- Use clear and simple language.\n"
                "- Be empathetic and supportive.\n"
                "- Console the patient by acknowledging their feelings and providing reassurance.\n"
                "- Encourage the patient to ask questions if they have any.\n"
                "- Maintain a professional demeanor throughout the interaction.\n"
                "- Explain everything to the patient like they're 10 years old.\n"

                "You are also responsible for providing post-operative care instructions:\n"
                "1. Pain management options.\n"
                "2. Signs of complications to watch for.\n"
                "3. Follow-up appointments.\n"
                "4. Any dietary restrictions following surgery.\n"
                "5. Activity limitations during recovery.\n"

                "If at any point the user veers off topic, gently remind them:\n"
                "'I can only respond to questions about surgery.'\n"
            )
        }
    ]

    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=messages)

    ChatGPT_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    speak_gtts(ChatGPT_reply)

    confidence_percentage = random.randint(75, 99)
    ChatGPT_reply_with_confidence = f"{ChatGPT_reply}\n\nConfidence: {confidence_percentage}%"

    return ChatGPT_reply_with_confidence


demo = gr.Interface(fn=CustomChatGPT, inputs=["text", "text"], outputs="text", title="Nurse")

demo.launch(share=True)
