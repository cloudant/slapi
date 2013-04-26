import json

config = dict()


def _load_config(configfile):
    global config
    fh = None
    try:
        fh = open(configfile, 'r')
        config = json.load(fh)
    finally:
        if fh:
            fh.close()
