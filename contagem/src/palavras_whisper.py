import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
out={}
for f in sys.argv[1:]:
    raw=subprocess.run(["ffmpeg","-loglevel","error","-i",f,"-ar","16000","-ac","1","-f","s16le","-"],capture_output=True).stdout
    a=np.frombuffer(raw,dtype="int16").astype("float32")/32768
    segs,_=m.transcribe(a,language="pt",word_timestamps=True)
    out[f]=[(w.word.strip(),round(w.start,2),round(w.end,2)) for s in segs for w in s.words]
    print(f, len(a)/16000, " ".join(w[0] for w in out[f]))
json.dump(out,open("words.json","w"),ensure_ascii=False)
