'''
Convert mp3 to wave, down sample, change channel audio file python script
by dangvansam98 - 03/2019
https://github.com/dangvansam98
dangvansam98@gmail.com
'''
import pydub
import wave
import audioop
import sys
import os

def downsampleWav(src, dst, inrate=48000, outrate=16000, inchannels=1, outchannels=1):
    '''
     src: path to file mp3 need to downsample
     dst: path to file wav after downsample
     inrate: sample rate mp3 file
     outrate: sample rate you want for wav file
     inchannels: num of channels mp3 file 1: mono, 2:stereo
     outchannels: num of channels wav file 1: mono, 2:stereo
    '''
    if not os.path.exists(src):
        print ('Source not found!')
        return False
    try:
        s_read = wave.open(src, 'r')
        s_write = wave.open(dst, 'w')
    except:
        print ('Failed to open files!')
        return False

    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)

    try:
        converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)
        if outchannels == 1 & inchannels != 1:
            converted[0] = audioop.tomono(converted[0], 2, 1, 0)
    except:
        print ('Failed to downsample wav')
        return False

    try:
        s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
        s_write.writeframes(converted[0])
    except:
        print ('Failed to write wav')
        return False

    try:
        s_read.close()
        s_write.close()
    except:
        print ('Failed to close wav files')
        return False

    return True


path_in_mp3 = 'D:\\ASR\\dataset ASR\\FPT data\\FPTOpenSpeechData_Set002_V0.1\\FPTOpenSpeechData_Set002_Part2_V0.1\\mp3\\' #path to folder mp3 files
path_out_48 = 'D:\\ASR\\dataset ASR\FPT data\\FPTOpenSpeechData_Set002_V0.1\\FPTOpenSpeechData_Set002_Part2_V0.1\\wav48\\' #path to folder wav files (converted to wav but not downsample, samplerate = sample rate mp3 file)
path_out_16 = 'D:\\ASR\\dataset ASR\\FPT data\\FPTOpenSpeechData_Set002_V0.1\\FPTOpenSpeechData_Set002_Part2_V0.1\\wav\\' #path to folder wav files (converted to wav and downsample, samplerate = outrate)
for file in os.listdir(path_in_mp3):
    if file.endswith(".mp3"):
        print(file)
        sound = pydub.AudioSegment.from_mp3(path_in_mp3 + file) #load mp3 file
        sound.export(path_out_48+file.replace('.mp3','.wav'), format="wav") #export to wav file
        downsampleWav(path_out_48+file.replace('.mp3','.wav'), path_out_16 + file.replace('.mp3','.wav'),48000,16000,1,1) #downsample wav file to samplerate you want...
        #os.remove(path_out_48+file.replace('.mp3','.wav')) #remove file in wav48 folder if full disk
