#! /usr/bin/env python

from __future__ import division, print_function # confidence unknown
import os
import sys
import getopt
import subprocess

from stsci.tools import parseinput,teal

"""
Convert an events table of TIMETAG into an integrated ACCUME image.

The input tag file should be in the default directory.  This is not
always necessary, but it will always work.

Examples
--------

In Python without TEAL:

>>> import stistools
>>> stistools.inttag.inttag("od8k51igq_tag.fits", "od8k51gq_out.fits",
                            verbose=True)

In Python with TEAL:

>>> from stistools import inttag
>>> from stsci.tools import teal
>>> teal.teal("inttag")

In Pyraf:

>>> import stistools
>>> teal inttag

From command line::

% ./inttag.py -v od8k51igq_tag.fits od8k51gq_out.fits
% ./inttag.py -r
"""

__taskname__ = "inttag"
__version__ = "1.0"
__vdate__ = "11-April-2017"
__author__ = "Sara Ogaz, STScI, April 2017."

def main(args):

    if len(args) < 2:
        prtOptions()
        print("A tag filename and output filename must be specified.")
        sys.exit()

    try:
        (options, pargs) = getopt.getopt(args, "srtvw:",
                                         ["version"])
    except Exception as error:
        prtOptions()
        sys.exit()

    starttime = None  #-s --starttime
    increment = None  #-i --increment
    rcount = 1      #-r --rcount
    verbose = False
    highres = False  #-h --highres
    allevents = False #-a --allevents


    for i in range(len(options)):
        if options[i][0] == "-v":
            verbose = True
        if options[i][0] == "-s":
            starttime = options[i][1]
        if options[i][0] == "-i":
            increment = options[i][1]
        if options[i][0] == "-r":
            rcount = options[i][1]
        if options[i][0] == "-h":
            highres = True
        if options[i][0] == "-a":
            allevents = True

    nargs = len(pargs)
    if nargs < 1 or nargs > 2:
        prtOptions()
        sys.exit()
    input = pargs[0]
    output = pargs[1]

    status = inttag(input, output, verbose=verbose,
                     starttime=starttime, increment=increment,
                     rcount=rcount, highres=highres,
                     allevents = allevents)

    sys.exit(status)

def prtOptions():
    """Print a list of command-line options and arguments."""

    print("The command-line options are:")
    print("  --version (print the version number and exit)")
    print("  -r (print the full version string and exit)")
    print("  -v (verbose)")
    print("  -t (print timestamps)")
    print("  -s (save temporary files)")
    print("  -w wavecal")
    print("")
    print("Following the options, list one or more input raw file names,")
    print("  enclosed in quotes if more than one file name is specified")
    print("  and/or if wildcards are used.")
    print("An output directory (include a trailing '/') or a root name for")
    print("  the output files may be specified.")


def inttag(input, output, verbose=False, starttime=None,
           increment=None, rcount=1, highres=False,
           allevents=False):
    """Convert an events table of TIMETAG into an integrated ACCUME image.

    Parameters
    ----------
    input: str
        Name of the TIMETAG input file.

    output: str
        Name of the output file.

    starttime: float, optional
        Start time for integrating events, in units of seconds since
        the beginning of the exposure.  The default is for start time
        equal to the first START time in the GTI table.

    increment: float, optional
        Time interval in seconds. The default is to integrate to the
        last STOP time in the GTI table.

    rcount: positive int, optional
        Repeat count, the number of output image sets to create. If
        greater then 1, then 'increment' must also be specified (but
        'starttime' may still be default. Default value is 1.

    highres: bool, optional
        If True, high resolution output image is created. Default is
        False.

    allevents: bool
        If true all events in the input EVENTS table will be
        accumulated into the output image.  The TIME column in the
        EVENTS table will only be used to determine the exposure time,
        and the GTI table will be ignored. Default is False.

    Returns
    -------
    status: int
        0 is OK.
        1 is returned if inttag.e (the inttag executable) returned a
        non-zero status.  If verbose is True, the value returned by
        inttag.e will be printed.
        2 is returned if the specified input file was not found.
    """

    cumulative_status = 0

    if not os.path.isfile(input):
        print("No file name matched the string '%s'" % input)
        return 2

    arglist = ["inttag.e"]

    arglist.append(input)
    arglist.append(output)

    # the following three inputs (starttime, increment, and rcount)
    # are position in the executable call
    # so some carefulness is required here.

    if starttime:
        arglist.append(str(starttime))
    else:
        # this is not ideal, but that's how inttag.e wants the default fed in
        arglist.append('first')

    if increment:
        arglist.append(str(increment))

    # this value does not need to be supplied if value is 1
    if rcount > 1:
        # increment is required if rcount more then one
        if not increment:
            raise SyntaxError("If rcount is defined, increment must also "
                              "be defined.")
        else:
            arglist.append(str(rcount))
    elif rcount < 1:
        raise ValueError("rcount = {}, rcount value must be positive".
                         format(rcount))

    if verbose:
        arglist.append("-v")

    if highres:
        arglist.append("-h")

    if allevents:
        arglist.append("-a")

    if verbose:
        print("Running inttag on %s" % input)
        print("  %s" % str(arglist))

    status = subprocess.call(arglist, stderr=subprocess.STDOUT)

    if status:
        cumulative_status = 1
        if verbose:
            print("Warning:  status = %d" % status)

    return cumulative_status

#-------------------------#
# Interfaces used by TEAL #
#-------------------------#

def getHelpAsString(fulldoc=True):
    """Return documentation on the inttag function."""
    return  inttag.__doc__

def run(configobj=None):
    """TEAL interface for the inttag function."""
    inttag(input=configobj["input"],
            output=configobj["output"],
            starttime=configobj["starttime"],
            increment=configobj['increment'],
            rcount=configobj['rcount'],
            verbose=configobj["verbose"],
            highres=configobj["highres"],
            allevents=configobj["allevents"])

if __name__ == "__main__":

    main(sys.argv[1:])