#!/usr/bin/env python3

from string import ascii_letters, digits

import random
import time

GREEN, RESET = "\033[92m", "\033[0m"

char = lambda i: " ".join(random.sample(ascii_letters + digits, k=i)).upper()


def shuffle(line, name_length):

    for x in range(0, random.randint(1, 4)):
        print("\t{}".format(char(name_length)), end="\r")
        time.sleep(0.1)

    print("\t" + line)


def print_banner(name="Nameless", version="00.00.00", author="unknown"):

    name_length = len(name) + 4  # name legnth + four chars
    name = " ".join(name.upper())  # space between letters
    name = "{} \033[1m{} \033[0m{}".format(char(2), name, char(2))

    print("\n")
    lines = [char(name_length), name, char(name_length)]
    [shuffle(line, name_length) for line in lines]
    print("\n\t{}".format(author))
    print("\t{}\n".format(version))
