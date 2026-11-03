import configparser
import time

from timeutil import parse_duration


def load(path="config/defaults.ini"):
    cfg = configparser.ConfigParser()
    cfg.read(path)
    return cfg


def run_forever(poll_once):
    cfg = load()
    timeout = parse_duration(cfg["worker"]["timeout"])
    pause = parse_duration(cfg["worker"]["poll"])
    while True:
        poll_once(timeout=timeout)
        time.sleep(pause)
