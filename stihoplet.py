import random
import gtts
from pydub import AudioSegment
import wave

def sorting(data): #O(N), O(N)
    sort_data = {}
    for word in data:
        end=word[-2]+word[-1]
        if not(end in sort_data.keys()):
            sort_data[end]=[]
            sort_data[end].append(word)
        else:
            sort_data[end].append(word)
    return sort_data

def changeSpeed(filename, speed):
    sound = AudioSegment.from_mp3(filename)
    filename = filename.split('.')[0]
    sound.export(f'{filename}.wav', format = 'wav')
    spf = wave.open(f'{filename}.wav', 'rb')
    rate = spf.getframerate()
    signal = spf.readframes(-1)
    wf = wave.open(f'{filename}.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(rate * speed)
    wf.writeframes(signal)
    sound = AudioSegment.from_wav(f'{filename}.wav')
    sound.export(f'{filename}.mp3', format = 'mp3')
    spf.close()
    wf.close()


def para(data, str_count): #O(N), O(N)
    output = ''
    keys = list(data.keys())
    for string in range(str_count):
        if (string + 1) % 2 == 1:
            key = random.choice(keys)
        count_words = random.randint(3,4) 
        for word in range(count_words):
            random_key=random.choice(keys)
            if word == 0:
                output += data[random_key][random.randint(0, len(data[random_key])-1)].title() + ' '
            elif word != count_words-1:
                output += data[random_key][random.randint(0, len(data[random_key])-1)] + ' '
            else: 
                output += data[key][random.randint(0, len(data[key])-1)] + ' '
        output += random.choice(['.','?', '!', ',', ''])
        if (string + 1) % 4 == 0:
            output += '\n\n'
        else:
            output += '\n'
    return output

def perek(data, str_count): #O(N), O(N)
    output = ''
    data_keys = list(data.keys())
    keys = [None, None]
    for string in range(str_count):
        if (string + 1) % 4 == 1:
            keys = [random.choice(data_keys), random.choice(data_keys)]
        count_words = random.randint(3,4) 
        for word in range(count_words):
            random_key=random.choice(data_keys)
            if word == 0:
                output += data[random_key][random.randint(0, len(data[random_key])-1)].title() + ' '
            elif word != count_words-1:
                output += data[random_key][random.randint(0, len(data[random_key])-1)] + ' '
            else: 
                output += data[keys[abs((string + 1) % 2 - 1)]][random.randint(0, len(data[keys[abs((string + 1) % 2 - 1)]])-1)] + ' '
        output += random.choice(['.','?', '!', ',', ''])
        if (string + 1) % 4 == 0:
            output += '\n\n'
        else:
            output += '\n'
    return output
def kolco(data, str_count): #O(N), O(N)
    output = ''
    data_keys = list(data.keys())
    keys = [None, None]
    for string in range(str_count):
        if (string + 1) % 4 == 1:
            keys = [random.choice(data_keys), random.choice(data_keys)]
        count_words = random.randint(3,4) 
        for word in range(count_words):
            random_key=random.choice(data_keys)
            if word == 0:
                output += data[random_key][random.randint(0, len(data[random_key])-1)].title() + ' '
            elif word != count_words-1:
                output += data[random_key][random.randint(0, len(data[random_key])-1)] + ' '
            else: 
                output += data[keys[(string % 2 + max(0, string % 4 - 1)) % 3]][random.randint(0, len(data[keys[(string % 2 + max(0, string % 4 - 1)) % 3]])-1)] + ' '
        output += random.choice(['.','?', '!', ',', ''])
        if (string + 1) % 4 == 0:
            output += '\n\n'
        else:
            output += '\n'
    return output

formal = open('dict/bigFormal.txt', 'r', encoding='utf-8')
f_data = formal.read().split('\n')
formal.close()
formal_data = sorting(f_data)
# informal = open('dict/informal.txt', 'r', encoding='utf-8')
# in_data = informal.read().split('\n')
# informal.close()
# informal_data = sorting(in_data)

def stihoplet(lang, cens, rifm, str_count):
    if cens == 'cens':
        text = eval(rifm)(formal_data, str_count)
    # elif cens == 'uncens':
    #     text = eval(rifm)(informal_data, str_count)
    gtts.gTTS(text, lang=lang).save('audio/stih.mp3')
    changeSpeed('audio/stih.mp3', 1.05)
    return {
        'audio': open('audio/stih.mp3', 'rb'),
        'text': text }
