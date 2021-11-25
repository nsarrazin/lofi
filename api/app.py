from conductor import Conductor
from instruments.instrument import synthbass, piano

import eventlet

eventlet.monkey_patch()

instruments = [piano, synthbass]


if __name__ == "__main__":
    conductor = Conductor(instruments)
    conductor.start()
