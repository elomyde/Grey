import numpy

def emojiconverter(text, emoji, blank) :
    converted_text = ["","","","",""]
    e = emoji
    b = blank
    items = {
    "A" : [[b,e,e,e,b],[e,b,b,b,e],[e,e,e,e,e],[e,b,b,b,e],[e,b,b,b,e]],
    "B" : [[e,e,e,e,b],[e,b,b,b,e],[e,e,e,e,b],[e,b,b,b,e],[e,e,e,e,b]],
    "C" : [[b,e,e,e,e],[e,b,b,b,b],[e,b,b,b,b],[e,b,b,b,b],[b,e,e,e,e]],
    "D" : [[e,e,e,e,b],[e,b,b,b,e],[e,b,b,b,e],[e,b,b,b,e],[e,e,e,e,b]],
    "E" : [[e,e,e,e,e],[e,b,b,b,b],[e,e,e,e,e],[e,b,b,b,b],[e,e,e,e,e]],
    "F" : [[e,e,e,e,e],[e,b,b,b,b],[e,e,e,e,e],[e,b,b,b,b],[e,b,b,b,b]],
    "G" : [[e,e,e,e,e],[e,b,b,b,b],[e,b,e,e,e],[e,b,b,b,e],[e,e,e,e,e]],
    "H" : [[e,b,b,b,e],[e,b,b,b,e],[e,e,e,e,e],[e,b,b,b,e],[e,b,b,b,e]],
    "I" : [[e,e,e,e,e],[b,b,e,b,b],[b,b,e,b,b],[b,b,e,b,b],[e,e,e,e,e]],
    "J" : [[e,e,e,e,e],[b,b,e,b,b],[b,b,e,b,b],[e,b,e,b,b],[e,e,e,b,b]],
    "K" : [[e,b,b,e,e],[e,b,e,b,b],[e,e,b,b,b],[e,b,e,b,b],[e,b,b,e,e]],
    "L" : [[e,b,b,b,b],[e,b,b,b,b],[e,b,b,b,b],[e,b,b,b,b],[e,e,e,e,e]],
    "M" : [[b,e,b,e,b],[e,b,e,b,e],[e,b,e,b,e],[e,b,e,b,e],[e,b,e,b,e]],
    "N" : [[e,b,b,b,e],[e,e,b,b,e],[e,b,e,b,e],[e,b,b,e,e],[e,b,b,b,e]],
    "O" : [[b,e,e,e,b],[e,b,b,b,e],[e,b,b,b,e],[e,b,b,b,e],[b,e,e,e,b]],
    "P" : [[e,e,e,e,b],[e,b,b,b,e],[e,e,e,e,b],[e,b,b,b,b],[e,b,b,b,b]],
    "Q" : [[b,e,e,e,b],[e,b,b,b,e],[e,b,e,b,e],[e,b,b,e,b],[b,e,e,b,e]],
    "R" : [[e,e,e,e,b],[e,b,b,b,e],[e,e,e,e,e],[e,b,b,b,e],[e,b,b,b,e]],
    "S" : [[e,e,e,e,e],[e,b,b,b,b],[e,e,e,e,e],[b,b,b,b,e],[e,e,e,e,e]],
    "T" : [[e,e,e,e,e],[b,b,e,b,b],[b,b,e,b,b],[b,b,e,b,b],[b,b,e,b,b]],
    "U" : [[e,b,b,b,e],[e,b,b,b,e],[e,b,b,b,e],[e,b,b,b,e],[b,e,e,e,b]],
    "V" : [[e,b,b,b,e],[e,b,b,b,e],[b,e,b,e,b],[b,e,b,e,b],[b,b,e,b,b]],
    "W" : [[e,b,e,b,e],[e,b,e,b,e],[e,b,e,b,e],[e,b,e,b,e],[b,e,b,e,b]],
    "X" : [[e,b,b,b,e],[b,e,b,e,b],[b,b,e,b,b],[b,e,b,e,b],[e,b,b,b,e]],
    "Y" : [[e,b,b,b,e],[b,e,b,e,b],[b,b,e,b,b],[b,b,e,b,b],[b,b,e,b,b]],
    "Z" : [[e,e,e,e,e],[b,b,b,e,b],[b,b,e,b,b],[b,e,b,b,b],[e,e,e,e,e]],
    "0" : [[e,e,e],[e,b,e],[e,b,e],[e,b,e],[e,e,e]],
    "1" : [[e,e,b],[b,e,b],[b,e,b],[b,e,b],[e,e,e]],
    "2" : [[e,e,e],[b,b,e],[e,e,e],[e,b,b],[e,e,e]],
    "3" : [[e,e,e],[b,b,e],[e,e,e],[b,b,e],[e,e,e]],
    "4" : [[e,b,e],[e,b,e],[e,e,e],[b,b,e],[b,b,e]],
    "5" : [[e,e,e],[e,b,b],[e,e,e],[b,b,e],[e,e,e]],
    "6" : [[e,e,e],[e,b,b],[e,e,e],[e,b,e],[e,e,e]],
    "7" : [[e,e,e],[b,b,e],[b,b,e],[b,b,e],[b,b,e]],
    "8" : [[e,e,e],[e,b,e],[e,e,e],[e,b,e],[e,e,e]],
    "9" : [[e,e,e],[e,b,e],[e,e,e],[b,b,e],[b,b,e]],
    "+" : [[b,b,b],[b,e,b],[e,e,e],[b,e,b],[b,b,b]],
    "-" : [[b,b,b],[b,b,b],[e,e,e],[b,b,b],[b,b,b]],
    "_" : [[b,b,b],[b,b,b],[b,b,b],[b,b,b],[e,e,e]],
    }
    padding = [[b],[b],[b],[b],[b]]
    converted_matrix = [[],[],[],[],[]]
    text = text.upper()
    for char in text :
        char = str(char)
        try :
            templist = items.get(char)
            converted_matrix = numpy.hstack((converted_matrix,templist))
            converted_matrix = numpy.hstack((converted_matrix,padding))
        except :
            pass
    i = 0
    for lines in converted_matrix :
        for item in lines :
            converted_text[i] += item
        converted_text[i] += '‍'
        i += 1
    
    return converted_text

