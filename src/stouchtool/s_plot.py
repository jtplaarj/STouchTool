"""
This script aims to pretty plot s params obtained from VSA or Python scikit-rf


References:
    - https://scikit-rf.readthedocs.io
"""

import argparse
import logging
import os
import sys
from typing import List, Tuple

import matplotlib.pyplot as plt
import skrf as rf
from matplotlib import ticker

from stouchtool import __version__

__author__ = "Jesús Lázaro"
__copyright__ = "Jesús Lázaro"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from STouchTool.skeleton import fib`,
# when using this Python module as a library.


def s_plot(input: str, output: str, title: str) -> Tuple[str, str, int]:
    """Generate a plot in pdf with the provided touchstone data

    Args:
        input (str): input file name
        output (str): output file name, if none, it will be derived from input
        title (str): title of the plot, if none, it will derived from input

    Returns:
        Tuple[str, str, int]: input file name, output file name, number of ports
    """

    _logger.info("s_plot: The input file is:{}".format(input))

    # output file may be none, generate correct one
    if output is None:
        _logger.info(
            "s_plot: The output file is not given so a new one will be created"
        )
        output = os.path.splitext(input)[0] + ".pdf"
    _logger.info("s_plot: The output file is:{}".format(output))
    if title is None:
        _logger.info("s_plot: The title is not given so a new one will be created")
        title = os.path.splitext(os.path.basename(input))[0]

    _logger.info("s_plot: The title is:{}".format(title))

    try:
        slot = rf.Network(input)
    except Exception as e:
        _logger.debug("s_plot: Exception {} when opening file: {}".format(e, input))
        sys.exit(1)

    fig, ax = plt.subplots()
    slot.plot_s_db(ax=ax)
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(base=5.0))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=100e6))
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: "{:.0f}".format(x / 1e6))
    )

    ax.grid(which="major", color="#CCCCCC", linestyle="--")
    ax.grid(which="minor", color="#CCCCCC", linestyle=":")

    ax.set_xlabel("Frequency (MHz)")
    ax.set_title(title)

    # Change legend names since the default are very long names with the filename in it
    legend_list = []
    for output_port in range(slot.number_of_ports):
        for input_port in range(slot.number_of_ports):
            legend_list.append("S{}{}".format(output_port + 1, input_port + 1))

    ax.legend(legend_list)

    plt.savefig(output, format="pdf", bbox_inches="tight")

    return (input, output, slot.number_of_ports)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line parameters

    Args:
        args (List[str]): command line parameters as list of strings

    Returns:
        :obj:`argparse.Namespace`: command line parameters namespace
    """

    parser = argparse.ArgumentParser(description="Plot S params")
    parser.add_argument(
        "--version",
        action="version",
        version="STouchTool {ver}".format(ver=__version__),
    )
    parser.add_argument(
        dest="input",
        help="Input file with touchstone params",
        type=str,
        metavar="INPUT FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="Output file to write result, if none given, \
            it will be the input file with the PDF extension",
        type=str,
        metavar="OUTPUT FILE",
    )
    parser.add_argument(
        "-t",
        "--title",
        dest="title",
        help="Title of the plot",
        type=str,
        metavar="TITLE",
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


def main(arguments: List[str]):
    """Wrapper allowing :func:`s_plot` to be called as CLI

    Args:
        arguments (List[str]): command line parameters as list of strings
    """

    args = parse_args(arguments)
    setup_logging(args.loglevel)
    _logger.debug("Starting plotting...")
    inputfilename, outputfilename, numberofports = s_plot(
        args.input, args.output, args.title
    )
    print(
        "The plot from file {} has {} ports and has been ploted in {}".format(
            inputfilename, numberofports, outputfilename
        )
    )
    _logger.info("s_plot: Script ends here")


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
    #     python -m STouchTool.skeleton 42
    #
    run()
