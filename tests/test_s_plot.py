import PyPDF2
import pytest

from stouchtool.s_plot import main, run, s_plot

__author__ = "Jesús Lázaro"
__copyright__ = "Jesús Lázaro"
__license__ = "MIT"


@pytest.mark.parametrize(
    "inputfile,outputfile,title,ports, expected_outputfile, expected_title",
    [
        (
            "./tests/data/limiter_pin_0dBm.s2p",
            None,
            None,
            2,
            "./tests/data/limiter_pin_0dBm.pdf",
            "limiter_pin_0dBm",
        ),
        (
            "./tests/data/evalboard.s3p",
            "./tests/data/test.pdf",
            None,
            3,
            "./tests/data/test.pdf",
            "evalboard",
        ),
        (
            "./tests/data/limiter_pin_0dBm.s2p",
            "./tests/data/test.pdf",
            "Nice title",
            2,
            "./tests/data/test.pdf",
            "Nice title",
        ),
    ],
)
def test_s_plot_ok(
    inputfile: str,
    outputfile: str,
    title: str,
    ports: int,
    expected_outputfile: str,
    expected_title: str,
):
    """Test the API with correct values - no exception should occur"""

    (inputfile_result, outputfile_result, ports_result) = s_plot(
        inputfile, outputfile, title
    )
    assert (inputfile_result, outputfile_result, ports_result) == (
        inputfile,
        expected_outputfile,
        ports,
    )
    pdfFileObject = open(expected_outputfile, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    """ PDF should have a single page """
    assert pdfReader.numPages == 1
    """ Check for title in page"""
    pageObject = pdfReader.getPage(0)
    assert pageObject.extractText().find(expected_title) > -1


def test_s_plot_except():
    """Test the API with non existing file to check for error"""
    with pytest.raises(SystemExit):
        # non existing file
        assert s_plot("kk.s3p", "./tests/data/test.pdf", None) == (
            "./tests/data/evalboard.s2p",
            "./tests/data/test.pdf",
            2,
        )


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["./tests/data/evalboard.s3p"])
    captured = capsys.readouterr()
    assert (
        "The plot from file ./tests/data/evalboard.s3p has 3 ports and has "
        "been ploted in ./tests/data/evalboard.pdf\n" in captured.out
    )


def test_main_no_args(capsys):
    """CLI Tests, no input arguments"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main([])
    captured = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
    assert captured.out == ""
    assert "usage:" in captured.err


def test_simple_run():
    """Test run entry point"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
