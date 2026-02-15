import speech_recognition as sr

r = sr.Recognizer()

# Show all available microphones
mic_names = sr.Microphone.list_microphone_names()
print("Microphones:")
for i, name in enumerate(mic_names):
    print(f"{i}: {name}")

# Pick your correct mic index based on above
mic_index = 5  # ← Change this if needed

with sr.Microphone(device_index=mic_index) as source:
    print("Say something...")
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)

try:
    print("Recognizing...")
    text = r.recognize_google(audio, language='en-in')
    print("You said:", text)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))

