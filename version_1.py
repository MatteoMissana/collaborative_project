from utils import registra_audio
import whisper

#registra_audio()

model = whisper.load_model("base")

result = model.transcribe(r"C:\Users\User\cartelle_matteo\collaborative_project\registrazione.wav")
print(result["text"])

