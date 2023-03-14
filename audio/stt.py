import sys
import torch
import wenetruntime as asr
import time
import json
import tempfile
from pydub import AudioSegment


def speech_to_text(wav_file):
    decoder = asr.Decoder(lang='en')
    ans = decoder.decode_wav(wav_file)
    ans = json.loads(ans)
    return ans["nbest"][0]["sentence"]

def rescaleAudio(input, output, bitrate="16k"):
    audio = AudioSegment.from_file(input)
    output_audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    output_audio.export(output, format="wav", bitrate=bitrate)

def main(input):
    rescaled_temp = tempfile.NamedTemporaryFile()
    rescaleAudio(input, rescaled_temp.name)
    text = speech_to_text(rescaled_temp.name)
    rescaled_temp.close()
    return text

if __name__ == '__main__':
    print(main("../check/out.wav"))
