import random
import gtts
from pydub import AudioSegment
import wave
import sqlite3

db = sqlite3.connect('stihoplet.db', check_same_thread=False)
sql = db.cursor()

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


def para(str_count, stepSize, stressSyll): #O(N), O(N)
    output = ''
    data_keys = list(map(lambda x: x[0], sql.execute("SELECT DISTINCT end FROM formal").fetchall()))
    key_word = ''
    for string in range(str_count):
        if (string + 1) % 2 == 1:
            key = random.choice(data_keys)
        count_words = random.randint(3,4) 
        for w in range(count_words):
            if w == 0:
                words = sql.execute("SELECT word, upperID, syllables_count FROM formal WHERE upperID = ? AND syllables_count != 1", (stressSyll, )).fetchall()
                word = random.choice(words)
                output += word[0].title() + ' '
            elif w != count_words-1:
                l = word[2] - word[1] - stepSize + stressSyll
                l = l % stepSize if l >= 0 else l
                l = stressSyll - l if stressSyll > l else stressSyll + stepSize - l
                words = sql.execute("SELECT word, upperID, syllables_count FROM formal WHERE upperID = ?  AND syllables_count != 1", (l, )).fetchall()
                word = random.choice(words)
                output += word[0] + ' '
            else: 
                l = word[2] - word[1] - stepSize + stressSyll
                l = l % stepSize if l >= 0 else l
                l = stressSyll - l if stressSyll > l else stressSyll + stepSize - l
                words = list(set(sql.execute("SELECT word FROM formal WHERE end = ? AND upperID = ?  AND syllables_count != 1", (key, l)).fetchall()) - set((key_word,)))
                words = list(set(sql.execute("SELECT word FROM formal WHERE end = ?", (key, )).fetchall()) - set((key_word,))) if len(words) == 0 else words
                words = sql.execute("SELECT word FROM formal WHERE end = ? AND upperID = ?  AND syllables_count != 1", (key, l)).fetchall() if len(words) == 0 else words
                words = sql.execute("SELECT word FROM formal WHERE end = ?", (key, )).fetchall() if len(words) == 0 else words
                key_word = random.choice(words)[0]
                output += key_word
        output += random.choice(['.','?', '!', ',', '']) if (string+1) % 4 != 0 else random.choice(['.','?', '!', '...'])
        if (string + 1) % 4 == 0:
            output += '\n\n'
        else:
            output += '\n'
    return output

def perek(str_count, stepSize, stressSyll): #O(N), O(N)
    output = ''
    data_keys = list(map(lambda x: x[0], sql.execute("SELECT DISTINCT end FROM formal").fetchall()))
    keys = [None, None]
    key_words = ['', '']
    for string in range(str_count):
        if (string + 1) % 4 == 1:
            keys = [random.choice(data_keys), random.choice(data_keys)]
        count_words = random.randint(3,4) 
        for w in range(count_words):
            if w == 0:
                words = sql.execute("SELECT word, upperID, syllables_count FROM formal WHERE upperID = ? AND syllables_count != 1", (stressSyll, )).fetchall()
                word = random.choice(words)
                output += random.choice(words)[0].title() + ' '
            elif w != count_words-1:
                l = word[2] - word[1] - stepSize + stressSyll
                l = l % stepSize if l >= 0 else l
                l = stressSyll - l if stressSyll > l else stressSyll + stepSize - l
                words = sql.execute("SELECT word, upperID, syllables_count FROM formal WHERE upperID = ?  AND syllables_count != 1", (l, )).fetchall()
                output += random.choice(words)[0] + ' '
            else: 
                key = keys[abs((string + 1) % 2 - 1)]
                key_word = key_words[abs((string + 1) % 2 - 1)]
                l = word[2] - word[1] - stepSize + stressSyll
                l = l % stepSize if l >= 0 else l
                l = stressSyll - l if stressSyll > l else stressSyll + stepSize - l
                words = list(set(sql.execute("SELECT word FROM formal WHERE end = ? AND upperID = ?  AND syllables_count != 1", (key, l)).fetchall()) - set((key_word,)))
                words = list(set(sql.execute("SELECT word FROM formal WHERE end = ?", (key, )).fetchall()) - set((key_word,))) if len(words) == 0 else words
                words = sql.execute("SELECT word FROM formal WHERE end = ? AND upperID = ?  AND syllables_count != 1", (key, l)).fetchall() if len(words) == 0 else words
                words = sql.execute("SELECT word FROM formal WHERE end = ?", (key, )).fetchall() if len(words) == 0 else words
                key_words[abs((string + 1) % 2 - 1)] = random.choice(words)[0]
                output += key_words[abs((string + 1) % 2 - 1)]
        output += random.choice(['.','?', '!', ',', '']) if (string+1) % 4 != 0 else random.choice(['.','?', '!', '...'])
        if (string + 1) % 4 == 0:
            output += '\n\n'
        else:
            output += '\n'
    return output

def kolco(str_count, stepSize, stressSyll): #O(N), O(N)
    output = ''
    data_keys = list(map(lambda x: x[0], sql.execute("SELECT DISTINCT end FROM formal").fetchall()))
    keys = [None, None]
    key_words = ['', '']
    for string in range(str_count):
        if (string + 1) % 4 == 1:
            keys = [random.choice(data_keys), random.choice(data_keys)]
        count_words = random.randint(3,4) 
        for w in range(count_words):
            if w == 0:
                words = sql.execute("SELECT word, upperID, syllables_count FROM formal WHERE upperID = ? AND syllables_count != 1", (stressSyll, )).fetchall()
                word = random.choice(words)
                output += random.choice(words)[0].title() + ' '
            elif w != count_words-1:
                l = word[2] - word[1] - stepSize + stressSyll
                l = l % stepSize if l >= 0 else l
                l = stressSyll - l if stressSyll > l else stressSyll + stepSize - l
                words = sql.execute("SELECT word, upperID, syllables_count FROM formal WHERE upperID = ?  AND syllables_count != 1", (l, )).fetchall()
                output += random.choice(words)[0] + ' '
            else: 
                key = keys[(string % 2 + max(0, string % 4 - 1)) % 3]
                key_word = key_words[(string % 2 + max(0, string % 4 - 1)) % 3]
                l = word[2] - word[1] - stepSize + stressSyll
                l = l % stepSize if l >= 0 else l
                l = stressSyll - l if stressSyll > l else stressSyll + stepSize - l
                words = list(set(sql.execute("SELECT word FROM formal WHERE end = ? AND upperID = ?  AND syllables_count != 1", (key, l)).fetchall()) - set((key_word,)))
                words = list(set(sql.execute("SELECT word FROM formal WHERE end = ?", (key, )).fetchall()) - set((key_word,))) if len(words) == 0 else words
                words = sql.execute("SELECT word FROM formal WHERE end = ? AND upperID = ?  AND syllables_count != 1", (key, l)).fetchall() if len(words) == 0 else words
                words = sql.execute("SELECT word FROM formal WHERE end = ?", (key, )).fetchall() if len(words) == 0 else words
                key_words[(string % 2 + max(0, string % 4 - 1)) % 3] = random.choice(words)[0]
                output += key_words[(string % 2 + max(0, string % 4 - 1)) % 3]
        output += random.choice(['.','?', '!', ',', '']) if (string+1) % 4 != 0 else random.choice(['.','?', '!', '...'])
        if (string + 1) % 4 == 0:
            output += '\n\n'
        else:
            output += '\n'
    return output

def stihoplet(stepSize, stressSyll, rifm, str_count, filename):
    text = eval(rifm)(str_count, stepSize, stressSyll)
    gtts.gTTS(text, 'ru').save(f'audio/{filename}.mp3')
    changeSpeed(f'audio/{filename}.mp3', 1.05)
    return {
        'audio': open(f'audio/{filename}.mp3', 'rb'),
        'text': text }