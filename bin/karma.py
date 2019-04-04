#!/usr/bin/env python3

# colors
RESET, GREEN, RED = '\033[0m', '\033[92m', '\033[91m'

project = 'Karma'
version = '15.03.19'
author  = 'decoxviii'

usage = """Karma
Usage:
    karma.py target <target> [-o FILENAME] [--proxy=<proxy>]
    karma.py search <target> (--password | --local-part | --domain) 
                             [-o FILENAME] [--proxy=<proxy>]
    karma.py (-h | --help)
    karma.py --version

Options:
    -o --output         Save output in json format.
    --proxy=<proxy>     Set Tor proxy [default: localhost:9050].
    -h --help           Show this screen.
    --version           Show version.
"""

from os import path
import json
import time
import sys

try:
    sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))
    from texttable import Texttable
    from docopt import docopt
    from karma import banner
    from karma import core
except ModuleNotFoundError as error:
    print("{}> Error:{}".format(RED, error))
    print(" - Verify the existence of the directory: karma/")
    print(" - Please install the requirements:\n\t$ sudo -H pip3 install -r requirements.txt")
    sys.exit(1)


def print_result_table(result, end):
    
    if not result or result == '':
        print('{}> No results found.{}'.format(RED, RESET))
        return None
    
    print('{}> Results:{}\n'.format(GREEN, RESET))
    
    table = Texttable()                     # create table
    table.header(['Email', 'Password'])     # add two columns
    table.set_cols_dtype(['t', 't'])        # data type is text
    table.set_deco(                         # set table decoration
        Texttable.BORDER | 
        Texttable.HEADER |
        Texttable.VLINES)
    
    for key in result.keys():
        email = result[key]['email']        # get email
        passw = str(result[key]['passw'])   # get password
        row   = (email, passw)              # create tuple with email and password
        table.add_row(row)                  # add new row to the table

    print(table.draw())
    print('\n{}> {} Results found in {:.2f} segs.{}'.format(
        GREEN, len(result.keys()), end, RESET ))


def generate_json_file(result, filename):
    
    if not filename:
        filename = time.strftime('%d%m%y-%H%M%S')   # if not filename: create new file name
    output = json.dumps(result, indent=2)           # get results in json format
    f = open('%s.json' % filename, 'w')             # create new file
    f.write(output)                                 # write results
    f.close()

    print('{}> The file {}.json was created.{}'.format(GREEN, filename, RESET))


def main():
    
    start = time.time()                             # get program start time
    args  = docopt(usage, version=version)          # get arguments
    pwndb = core.pwndb(args)                        # load functions
    banner.print_banner(project, version, author)   # print sexy banner
    
    print('{}> Searching{}'.format(GREEN, RESET))

    result = pwndb.search_info()                    # start search and get results
    end = time.time() - start                       # get time within the program
    print_result_table(result, end)                      # print results
    
    if args['--output']:
        filename = args['FILENAME']             # get file name 
        generate_json_file(result, filename)    # generate json file with the results

if __name__ == "__main__":
    main()

