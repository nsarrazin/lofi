mapping = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B",
}

reversed_mapping = {
    "Cbb": 10,
    "Cb": 11,
    "C": 0,
    "Dbb": 0,
    "Db": 1,
    "D": 2,
    "Ebb": 2,
    "Eb": 3,
    "E": 4,
    "Fb": 4,
    "F": 5,
    "Gb": 6,
    "G": 7,
    "Abb": 7,
    "Ab": 8,
    "A": 9,
    "Bbb": 9,
    "Bb": 10,
    "B": 11,
    "C#": 1,
    "C##": 2,
    "D#": 3,
    "E#": 5,
    "F#": 6,
    "G#": 8,
    "A#": 10,
    "B#": 12,
}


intervalToTuple = {
    "1": (1, 0),
    "b2": (2, 1),
    "2": (2, 2),
    "b3": (3, 3),
    "3": (3, 4),
    "b4": (4, 4),
    "4": (4, 5),
    "b5": (5, 6),
    "5": (5, 7),
    "#5": (5, 8),
    "6": (6, 9),
    "bb7": (7, 9),
    "b7": (7, 10),
    "7": (7, 11),
    "9": (9, 14),
    "b9": (9, 13),
    "#9": (9, 15),
    "11": (11, 17),
    "#11": (11, 18),
    "b13": (13, 20),
    "13": (13, 21),
    "s5": (5, 8),
    "s9": (9, 15),
    "s11": (11, 18),
}


def number_to_name(number):
    name = mapping[number % 12]
    octave = number // 12 - 1
    return name + str(octave)


def name_to_number(name):
    note = name[:-1]
    octave = name[-1]
    return reversed_mapping[note] + (int(octave) + 1) * 12


if __name__ == "__main__":
    assert number_to_name(name_to_number("A0")) == "A0"
    assert number_to_name(name_to_number("C4")) == "C4"
    assert number_to_name(name_to_number("A#3")) == "A#3"
    assert name_to_number("C4") == 60
    assert name_to_number("D5") == 74
    assert name_to_number("A3") == 57
    assert number_to_name(49) == "C#3"
    assert number_to_name(44) == "G#2"
