from audio import get_audio
import os 

def runStopper():

    while True:
        q1 = get_audio()
        if ('stop listening' in q1):
            print('ok')
            break
        if ('friday stop' in q1 or "Friday stop" in q1):
            print('stopping response')
            os.system("rm response.mp3")

runStopper()