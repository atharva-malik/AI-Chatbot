"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
import speech_recognition as sr
import pyttsx3, threading
import arduinochat as ac

genai.configure(api_key="YOUR_API_KEY")

r = sr.Recognizer()
engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# print(voices)
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
engine.setProperty('rate', 150)
pulse_mode = "pulse"

def pulse_in_background():
    while True:
        if pulse_mode == "pulse":
            ac.backgroundPulse()
        elif pulse_mode == "listening":
            ac.listening()
        elif pulse_mode == "talking":
            ac.talking()
        else:
            break


def aOutput(output):
    print("Gemini: " + output)
    engine.say(output)
    engine.runAndWait()

def aInput():
    with sr.Microphone() as source:
        print("Now listening...")
        audio = r.listen(source)
        print("Now processing...")
    try:
        output = r.recognize_google(audio)
        if "hey jarvis" in output.lower():
            pulse_mode = "listening"
            output = output.lower()
            output = output[output.find("hey jarvis"):]
            output.replace("hey jarvis ", "")
        else:
            pulse_mode = "pulse"
            output = "_e " + output
    except sr.UnknownValueError:
        output = "_e Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        output = "_e Could not request results from Google Speech Recognition service; {0}".format(e)
    return output



# Set up the model
generation_config = {
    "temperature": 0.9, #* How random the bot can be
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    }
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[])

pulse_thread = threading.Thread(target=pulse_in_background)
pulse_thread.start()

while True:
    pulse_mode = "pulse"
    try:
        inp = aInput()
        #pulse_mode = "listening"
        #inp = input("You: ")
        if inp[0] == "_" and inp[1] == "e":
            raise Exception("Nothing Detected!")
        if "stop" in inp.lower():
            pulse_mode = "stop"
            break
        print("You: " + inp)
        convo.send_message(inp)
        pulse_mode = "talking"
        aOutput((convo.last.text).replace("**", "").replace("* ", ""))
        pulse_mode = "pulse"
    except Exception as e:
        pulse_mode = "pulse"
        print(e)
        print("Could not send message, restarting conversation...")

pulse_thread.join()
