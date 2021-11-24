from conductor import Conductor
from instruments.instrument import Bass, Piano

piano = Piano("chords", "piano")
synthbass = Bass("bass", "synthbass")

instruments = [piano, synthbass]


if __name__ == '__main__':
    # todo: make a ref to conductor in instruments to pass socketio object
    
    conductor = Conductor(instruments)
    conductor.start()
    