import speech_recognition as sr

mic_list = sr.Microphone.list_microphone_names()

for i, name in enumerate(mic_list):
    print(f"\n🎙 Testing device {i}: {name}")
    try:
        with sr.Microphone(device_index=i) as source:
            print("🎤 Say something...")
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)
            print("🔍 Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"✅ You said: {text}")
            break  # If this one worked, stop the loop!
    except Exception as e:
        print(f"❌ Error with device {i}: {e}")
