import sys
import linecache
import configargparse

def _parse_url(url):
    """ This function extracts certain 
        components from a given URL.
    """
    authority = url.split('/')[2]
    uri = '/'.join(url.split('/')[3:])

    if ':' not in authority:
        port = 80
        host = authority
    else:
        host, port = authority.split(':')

    return host, port, authority, uri

def _print_exception(extra_details=[]):
    """ This function prints exception details
        including the line number where the exception
        is raised, which is helpful in most cases.
    """
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}, {}'.format(filename, lineno, line.strip(), exc_obj, extra_details))

def _parse_args(): 
    """ This function is for parsing the command
        line arguments fed into the script.
    """
    parser = configargparse.ArgParser(description='T-Reqs: Grammar-based HTTP Fuzzer')

    parser.add('-c', dest="config", required=True, help='config file path')
    parser.add('-i', action="store_true", dest="individual_mode", help="Turns the individual mode on where the fuzzer is run only for specified seeds.")
    parser.add('-s', dest="seed", type=int, help="Only needed for individual mode. Seed parameter for random number generator.")
    parser.add('-v', action="store_true", dest="verbose", help="Only needed for individual mode. Adds verbosity.")
    parser.add('-o', dest="outfilename", help = "Only needed for individual mode. File to write output.")
    parser.add('-f', dest="seedfile", help = "Only needed for individual mode. Input file containing seeds.")

    args = parser.parse_args()

    return args
