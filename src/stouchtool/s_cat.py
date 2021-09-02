# Copyright (c) 2021 Jesús Lázaro
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import argparse
import logging
import sys
from difflib import SequenceMatcher
from typing import List

import skrf as rf
from scipy.special import comb

from stouchtool import __version__

__author__ = "Jesús Lázaro"
__copyright__ = "Jesús Lázaro"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def s_cat(inputfiles: List[str], outputfile: str, NumPort: int) -> str:
    """Concatenate 2 port s files into an n port s file

    Args:
        inputfiles (List[str]): List of files
        outputfile (str): Name of output file - optional
        NumPort (int): Number of ports - optional

    Raises:
        ValueError: In provided number of ports and files do not match

    Returns:
        str: final output file name
    """

    NumFiles = len(inputfiles)
    NumPortFound = False
    if NumPort is None:
        for NumPort in range(1, 10):
            if comb(NumPort, 2) == NumFiles:
                NumPortFound = True
                break
    else:
        if comb(NumPort, 2) == NumFiles:
            NumPortFound = True

    if not NumPortFound:
        _logger.debug("Wrong number of files: {}".format(NumFiles))
        raise ValueError("Wrong number of files: {}".format(NumFiles))

    PortList = list()
    RFNetworks = list()
    for OutputPort in range(1, NumPort + 1):
        for InputPort in range(OutputPort + 1, NumPort + 1):
            PortList.append("p" + str(OutputPort) + str(InputPort))
    _logger.debug(
        "Number of files is {} and number of ports is {}".format(NumFiles, NumPort)
    )
    for (inputfile, port) in zip(inputfiles, PortList):
        _logger.debug("File {} is {}".format(inputfile, port))
        tmpNetwork = rf.Network(inputfile)
        tmpNetwork.name = port
        RFNetworks.append(tmpNetwork)

    if outputfile is None:
        _logger.debug("The output file is not given so a new one will be created")
        match = SequenceMatcher(None, inputfiles[0], inputfiles[1]).find_longest_match(
            0, len(inputfiles[0]), 0, len(inputfiles[1])
        )
        outputfile = (
            inputfiles[0][match.a : match.a + match.size] + ".s" + str(NumPort) + "p"
        )

    _logger.debug("Combining: {}".format(RFNetworks))
    combined = rf.network.n_twoports_2_nport(RFNetworks, nports=NumPort)
    combined.write_touchstone(outputfile)
    return outputfile


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line parameters

    Args:
        args (List[str]): command line parameters as list of strings

    Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """

    parser = argparse.ArgumentParser(description="Concatenate S params")
    parser.add_argument(
        "--version",
        action="version",
        version="RFTools {ver}".format(ver=__version__),
    )
    parser.add_argument(
        dest="inputfiles",
        help="Input file with touchstone params",
        type=str,
        nargs="+",
        metavar="P12_FILE.s2p P13_FILE.s2p P23_FILE.s2p",
    )
    parser.add_argument(
        "-p",
        "--numports",
        dest="numports",
        help="Number of ports, if ommited it will be gussed from number of files",
        type=int,
        metavar="NUM_PORTS",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="Output file to write result, if none given, \
            it will be the input file with the PDF extension",
        type=str,
        metavar="OUTPUT_FILE",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel: int):
    """setup logging

    Args:
        loglevel (int): minimum loglevel for emitting messages
    """

    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(arguments: List[str]):
    """Wrapper allowing :func:`plot_s_cat` to be called as CLI

    Args:
        args (List[str]): command line parameters as list of strings
    """

    args = parse_args(arguments)
    setup_logging(args.loglevel)
    _logger.debug("Starting plotting...")

    try:
        outputfilename = s_cat(args.inputfiles, args.output, args.numports)
    except ValueError as e:
        print(e)
        sys.exit(1)
    print(
        "The cat from files {} has been stored in {}".format(
            args.inputfiles, outputfilename
        )
    )
    _logger.info("plot_ad_data: Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m rftools.skeleton 42
    #
    run()
