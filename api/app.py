from conductor import Conductor
from instruments.instrument import synthbass, piano

instruments = [piano, synthbass]


if __name__ == "__main__":
    # todo: make a ref to conductor in instruments to pass socketio object

    conductor = Conductor(instruments)
    conductor.start()
