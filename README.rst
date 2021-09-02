==========
STouchTool
==========

.. image:: https://app.travis-ci.com/jtplaarj/STouchTool.svg?branch=master
    :target: https://app.travis-ci.com/jtplaarj/STouchTool
    :alt: Travis
.. image:: https://coveralls.io/repos/github/jtplaarj/STouchTool/badge.svg?branch=master
    :target: https://coveralls.io/github/jtplaarj/STouchTool?branch=master
    :alt: Coveralls
.. image:: https://readthedocs.org/projects/stouchtool/badge/?version=latest
    :target: https://stouchtool.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/STouchTool.svg
    :target: https://pypi.org/project/STouchTool/
    :alt: Latest Version
.. image:: http://www.mypy-lang.org/static/mypy_badge.svg
    :target: http://mypy-lang.org/
    :alt: Checked with mypy
.. image:: https://img.shields.io/github/license/jtplaarj/STouchTool?style=flat
    :target: https://mit-license.org/
    :alt: GitHub

Collection of tools to manipulate Touchstone files


Description
===========

This projects aims to collect several utilities to manage Touchstone files. They are mainly wrappers around `scikit-rf <http://scikit-rf.org/>`_ to make them command line friendly.

Commands
========

The list of available commands are:

* ``s_cat``: This command generates an n-port Touchstone file from the appropriate number of two-port files.
* ``s_plot``: This command will plot a Touchstone file into a PDF file.

``s_cat``
---------

This command generates an n-port Touchstone file from the appropriate number of two-port files.

For example, to generate a three-port file from three s2p files::

    s_cat P12_FILE.s2p P13_FILE.s2p P23_FILE.s2p --output output.s3p


The order of the files is important, it must begin with all the combinations of the first port, then the second,...

The number of ports is calculates automatically, if more than 10 ports are used, the explicit number of ports must be provided::

    s_cat *.s2p -n 12 -o test.s12p

The complete list of options is obtained using ``s_cat -h``. The input files to process are mandatory:
    * ``--help, -h``: List of options.
    * ``--numports, -p``: Number of ports, if omitted it will be guessed from number of files.
    * ``--output, -o``: Output file to write result, if none given, it will be the input file with the PDF extension.
    * ``--version``: Package version.
    * ``-v/-vv``: Verbose or very verbose mode.

``s_plot``
----------

This command will plot a Touchstone file into a PDF file.

A simple example is::

    s_plot test.s2p

This will produce a file called ``test.pdf`` plotting the data.

The complete list of options is obtained using ``s_plot -h``. The input file to process are mandatory:
    * ``--help, -h``: List of options.
    * ``--output, -o``: Output file to write result, if none given, it will be the input file with the PDF extension.
    * ``--title, -t``: Title of the plot. If it is not provided, the file name will be used.
    * ``--version``: Package version.
    * ``-v/-vv``: Verbose or very verbose mode.

Installation
============

The easiest way to install this package is to use ``pip``::

    pip install STouchTool
