import sys

if len(sys.argv) != 2:
    print("Please include only the string to translate!")
    exit(0)

ENGLISH_TO_BRAILLE = {
    "a": "O.....",
    "b": "O.O...",
    "c": "OO....",
    "d": "OO.O..",
    "e": "O..O..",
    "f": "OOO...",
    "g": "OOOO..",
    "h": "O.OO..",
    "i": ".OO...",
    "j": ".OOO..",
    "k": "O...O.",
    "l": "O.O.O.",
    "m": "OO..O.",
    "n": "..O.O.",
    "o": "O..OO.",
    "p": "OOO.O.",
    "q": "OOOOO.",
    "r": "O.OOO.",
    "s": ".OO.O.",
    "t": ".OOOO.",
    "u": "O...OO",
    "v": "O.O.OO",
    "w": ".OOO.O",
    "x": "OO..OO",
    "y": "OO.OOO",
    "z": "O..OOO",
    ".": "..OO.O",
    # removed since not required + non-uniqueness ex: ">" similar to "o"
    # ",": "..O...",
    # "!": "..OOO.",
    # ":": "..OO..",
    # ";": "..O.O.",
    # "-": "....OO",
    # "/": ".O..O.",
    # "<": ".OO..O",
    # ">": "O..OO.",
    # "(": "O.O..O",
    # ")": ".O.OO.",
    " ": "......",
}

NUMBER_TO_BRAILLE = {
    "1": "O.....",
    "2": "O.O...",
    "3": "OO....",
    "4": "OO.O..",
    "5": "O..O..",
    "6": "OOO...",
    "7": "OOOO..",
    "8": "O.OO..",
    "9": ".OO...",
    "0": ".OOO..",
}

CAPITAL = ".....O"
DECIMAL = ".O...O"
NUMBER = ".O.OOO"

def englishFromBraille(s):
    BRAILLE_TO_ENGLISH = {b:a for a,b in ENGLISH_TO_BRAILLE.items()}
    BRAILLE_TO_NUMBER = {b:a for a,b in NUMBER_TO_BRAILLE.items()}

    res = ""
    i = 0

    while i < len(s):
        el = s[i:i+6]

        if el in BRAILLE_TO_ENGLISH:
            res += BRAILLE_TO_ENGLISH[el]
            i+=6
        elif el == CAPITAL:
            i+=6
            el = s[i:i+6]
            res += BRAILLE_TO_ENGLISH[el].upper()
            i+=6
        elif el == NUMBER:
            i+=6
            subString = ""
            while i+6 < len(s) and s[i:i+6] in BRAILLE_TO_NUMBER:
                subString += BRAILLE_TO_NUMBER[s[i:i+6]]
                i+=6
            
            if len(subString) == 0:
                return "" # not a correct braille string
            
            res += subString
        elif el == DECIMAL:
            i+=6
            subString = ""
            while i+6 < len(s) and s[i:i+6] in BRAILLE_TO_NUMBER:
                subString += BRAILLE_TO_NUMBER[s[i:i+6]]
                i+=6
            
            if i+6 >= len(s) or s[i:i+6] != ENGLISH_TO_BRAILLE["."]:
                return "" # not a correct braille string
            
            i+=6
            subString += "."
            
            while i+6 < len(s) and s[i:i+6] in BRAILLE_TO_NUMBER:
                subString += BRAILLE_TO_NUMBER[s[i:i+6]]
                i+=6
            
            if not subString[-1].isdigit():
                return "" # not a correct braille string

            res += subString
        else:
            return "" # not a correct braille string
    
    return res

def brailleFromEnglish(s):
    res = ""
    i = 0
    while i < len(s):
        el = s[i]
        if el in ENGLISH_TO_BRAILLE:
            # lower case character
            res += ENGLISH_TO_BRAILLE[el]
            i+=1
        elif el.lower() in ENGLISH_TO_BRAILLE:
            # upper case character
            res += CAPITAL
            res += ENGLISH_TO_BRAILLE[el.lower()]
            i+=1
        elif el in NUMBER_TO_BRAILLE:
            # either number or decimal
            subString = ""
            while i < len(s) and s[i] in NUMBER_TO_BRAILLE:
                subString += NUMBER_TO_BRAILLE[s[i]]
                i+=1
            
            # either space (number) or . followed by numbers (decimal)
            if i < len(s) and s[i] == "." and \
                (i+1 < len(s) and s[i+1] in NUMBER_TO_BRAILLE):
                # implemented decimal (NOT SURE IF REQUIRED)
                subString += ENGLISH_TO_BRAILLE[s[i]]
                i+=1
                while i < len(s) and s[i] in NUMBER_TO_BRAILLE:
                    subString += NUMBER_TO_BRAILLE[s[i]]
                    i+=1
                res += DECIMAL + subString
            else:
                res += NUMBER + subString

    return res

text = ""

if len(sys.argv[1]) % 6 == 0:
    text = englishFromBraille(sys.argv[1])

if len(text) == 0:
    text = brailleFromEnglish(sys.argv[1])

print(text)
