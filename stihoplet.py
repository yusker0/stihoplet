import random
import gtts
from pydub import AudioSegment
import wave

def sorting(data, sort_data = {}): #O(N), O(N)
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
    key_word = ''
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
                key_word = random.choice(list(set(data[key]) - set([key_word]))) if len(data[key]) > 1 else random.choice(data[key])
                output += key_word
        output += random.choice(['.','?', '!', ',', '']) if (string+1) % 4 != 0 else random.choice(['.','?', '!', '...'])
        if (string + 1) % 4 == 0:
            output += '\n\n'
        else:
            output += '\n'
    return output

def perek(data, str_count): #O(N), O(N)
    output = ''
    data_keys = list(data.keys())
    keys = [None, None]
    key_words = ['', '']
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
                key_words[abs((string + 1) % 2 - 1)] = random.choice(list(set(data[keys[abs((string + 1) % 2 - 1)]]) - set([key_words[abs((string + 1) % 2 - 1)]]))) if len(data[keys[abs((string + 1) % 2 - 1)]]) > 1  else random.choice(data[keys[abs((string + 1) % 2 - 1)]]) 
                output += key_words[abs((string + 1) % 2 - 1)]
        output += random.choice(['.','?', '!', ',', '']) if (string+1) % 4 != 0 else random.choice(['.','?', '!', '...'])
        if (string + 1) % 4 == 0:
            output += '\n\n'
        else:
            output += '\n'
    return output
def kolco(data, str_count): #O(N), O(N)
    output = ''
    data_keys = list(data.keys())
    keys = [None, None]
    key_words = ['', '']
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
                key_words[(string % 2 + max(0, string % 4 - 1)) % 3] = random.choice(list(set(data[keys[(string % 2 + max(0, string % 4 - 1)) % 3]]) - set([key_words[(string % 2 + max(0, string % 4 - 1)) % 3]]))) if len(data[keys[(string % 2 + max(0, string % 4 - 1)) % 3]]) > 1  else random.choice(data[keys[(string % 2 + max(0, string % 4 - 1)) % 3]]) 
                output += key_words[(string % 2 + max(0, string % 4 - 1)) % 3]
        output += random.choice(['.','?', '!', ',', '']) if (string+1) % 4 != 0 else random.choice(['.','?', '!', '...'])
        if (string + 1) % 4 == 0:
            output += '\n\n'
        else:
            output += '\n'
    return output

formal = open('dict/formal.txt', 'r', encoding='utf-8')
f_data = formal.read().split('\n')
formal.close()
formal_data = sorting(f_data)

informal = open('dict/informal.txt', 'r', encoding='utf-8')
in_data = informal.read().split('\n')
informal.close()
informal_data = formal_data
informal_data = sorting(in_data, informal_data)
print('Dictionaries loaded')
def stihoplet(lang, cens, rifm, str_count, user_id):
    if cens == 'cens':
        text = eval(rifm)(formal_data, str_count)
    elif cens == 'uncens':
        text = eval(rifm)(informal_data, str_count)
    gtts.gTTS(text, lang=lang).save(f'audio/{user_id}.mp3') 
    print('audio++')
    changeSpeed(f'audio/{user_id}.mp3', 1.05)
    return {
        'audio': open(f'audio/{user_id}.mp3', 'rb'),
        'text': text }
