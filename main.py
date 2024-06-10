import numpy as np
import os
from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine
from tqdm import tqdm

# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '0': '-----', ', ': '--..--',
    '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-', ',': '--..--', ':': '---...', ';': '-.-.-.', '+': '.-.-.',
    '=': '-...-', '!': '-.-.--', '?': '..--..', '/': '-..-.',
    '@': '.--.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '&': '.-...', "'": '.----.', '(': '-.--.',
    ')': '-.--.-', 'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.',
    'Д': '-..', 'Е': '.','Ё': '.-.-', 'Ж': '...-', 'З': '--..', 'И': '..',
    'Й': '.---', 'К': '-.-', 'Л': '.-..', 'М': '--', 'Н': '-.',
    'О': '---', 'П': '.--.', 'Р': '.-.', 'С': '...', 'Т': '-',
    'У': '..-', 'Ф': '..-.', 'Х': '....', 'Ц': '-.-.', 'Ч': '---.',
    'Ш': '----', 'Щ': '--.-', 'Ъ': '--.--', 'Ы': '-.--', 'Ь': '-..-',
    'Э': '..-..', 'Ю': '..--', 'Я': '.-.-', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '0': '-----'
}

# function to encode a string into Morse code
def textToMorse(text):
    morseText = ''
    for char in text.upper():
        if char != ' ':
            if char == '\n':
                pass
            else:
                morseText += MORSE_CODE_DICT[char] + ' '
        else:
            morseText += ' '
    return morseText

# create an empty AudioSegment
combined = AudioSegment.silent(duration=0)

# function to encode a string into Morse code and then into audio 
def encodeToAudioWithPydub(morseText, frequency=550, unit_duration=170, fade_duration=10, output_path=os.getcwd() + '\\sound'):
    # define durations based on the Morse code timing rules
    duration_dot = unit_duration  # 1 time unit
    duration_dash = unit_duration * 2  # 2 time units
    #duration_symbol_space = unit_duration  # space between symbols in a letter
    duration_letter_space = unit_duration * 2  # space between letters
    duration_word_space = unit_duration * 3  # space between words

    # create a list to hold the individual audio segments
    segments = []

    # wrap morseText with tqdm for a progress bar
    for character in tqdm(morseText, desc="Encoding Morse Code", unit="signal"):
        if character == '.':
            # create a short beep
            beep = Sine(frequency).to_audio_segment(duration=duration_dot)
        elif character == '-':
            # create a long beep
            beep = Sine(frequency).to_audio_segment(duration=duration_dash)
        elif character == ' ':
            # add a space between words
            beep = AudioSegment.silent(duration=duration_word_space)
        else:
            # add a space between letters
            beep = AudioSegment.silent(duration=duration_letter_space)
            continue  # skip any unknown characters

        # apply fade in and fade out
        beep = beep.fade_in(fade_duration).fade_out(fade_duration)
        # add the beep to the list of segments
        segments.append(beep)

    # le faster
    combined = sum(segments)
    # export the combined audio to a file
    combined.export(output_path + '\\audio.wav', format='wav')
    print(f"Audio file exported to {output_path}")

    return combined


text = """
SOS SOS SOS SOS
"""
morseText = textToMorse(text)
print(morseText)
combinedAudio = encodeToAudioWithPydub(morseText)

# play the combined audio
play(combinedAudio)


