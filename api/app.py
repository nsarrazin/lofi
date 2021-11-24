from conductor import Conductor
from player_midi import PlayerMIDIChord, PlayerMIDI
    
piano = PlayerMIDIChord(path='midi-piano', loc="dump2.mid")

bass = PlayerMIDI(path='midi-bass', loc="dump.mid")

instruments = [piano, bass]


if __name__ == '__main__':
    # todo: make a ref to conductor in instruments to pass socketio object
    
    conductor = Conductor(instruments)
    conductor.start()
    