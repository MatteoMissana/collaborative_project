from utils import registra_audio
import whisper


nome_file = "registrazione.wav"
#registra_audio(nome_file= nome_file)
model = whisper.load_model("base")


#result = model.transcribe(nome_file)

audio = whisper.load_audio(nome_file)

#print(result["text"])

