import pytest
import skrf as rf

from stouchtool.s_cat import main, run, s_cat

__author__ = "Jesús Lázaro"
__copyright__ = "Jesús Lázaro"
__license__ = "MIT"


# TODO Test s4p and other properly, with real data
@pytest.mark.parametrize(
    "Inputfile, Outputfile, Golden, ExpectedOutfile, NumPorts",
    [
        (
            [
                "./tests/data/evalboard_in_outp_outn_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_in_outn_outp_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_outp_outn_in_50ohm_5V_pinm20dBm.s2p",
            ],
            "./tests/data/tmp.s3p",
            "./tests/data/golden.s3p",
            "./tests/data/tmp.s3p",
            None,
        ),
        (
            [
                "./tests/data/evalboard_in_outp_outn_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_in_outn_outp_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_outp_outn_in_50ohm_5V_pinm20dBm.s2p",
            ],
            "./tests/data/tmp.s3p",
            "./tests/data/golden.s3p",
            "./tests/data/tmp.s3p",
            3,
        ),
        pytest.param(
            [
                "./tests/data/evalboard_in_outp_outn_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_in_outn_outp_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_outp_outn_in_50ohm_5V_pinm20dBm.s2p",
            ],
            "./tests/data/tmp.s3p",
            "./tests/data/golden.s3p",
            "./tests/data/tmp.s3p",
            4,
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        (
            [
                "./tests/data/evalboard_in_outp_outn_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_in_outn_outp_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_outp_outn_in_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_in_outn_outp_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_outp_outn_in_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_outp_outn_in_50ohm_5V_pinm20dBm.s2p",
            ],
            "./tests/data/tmp.s4p",
            "./tests/data/golden.s4p",
            "./tests/data/tmp.s4p",
            None,
        ),
        pytest.param(
            [
                "./tests/data/evalboard_in_outp_outn_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_outp_outn_in_50ohm_5V_pinm20dBm.s2p",
            ],
            "./tests/data/tmp.s3p",
            "./tests/data/golden.s3p",
            "./tests/data/tmp.s3p",
            None,
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        (
            [
                "./tests/data/evalboard_in_outp_outn_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_in_outn_outp_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_outp_outn_in_50ohm_5V_pinm20dBm.s2p",
            ],
            None,
            "./tests/data/golden.s3p",
            "./tests/data/evalboard_in_out.s3p",
            None,
        ),
    ],
)
def test_s_cat(
    Inputfile: list, Outputfile: str, Golden: str, ExpectedOutfile: str, NumPorts: int
):
    """Test main function against golden results"""
    CalculatedOutputFile = s_cat(Inputfile, Outputfile, NumPorts)

    assert CalculatedOutputFile == ExpectedOutfile
    GoldenS = rf.Network(Golden)
    ResultS = rf.Network(CalculatedOutputFile)
    assert GoldenS == ResultS


def test_main_args_inputfile(capsys):
    """CLI Tests, file input arguments"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(
        [
            "./tests/data/evalboard_in_outp_outn_50ohm_5V_pinm20dBm.s2p",
            "./tests/data/evalboard_in_outn_outp_50ohm_5V_pinm20dBm.s2p",
            "./tests/data/evalboard_outp_outn_in_50ohm_5V_pinm20dBm.s2p",
        ]
    )
    captured = capsys.readouterr()
    assert (
        "The cat from files ["
        "'./tests/data/evalboard_in_outp_outn_50ohm_5V_pinm20dBm.s2p', "
        "'./tests/data/evalboard_in_outn_outp_50ohm_5V_pinm20dBm.s2p', "
        "'./tests/data/evalboard_outp_outn_in_50ohm_5V_pinm20dBm.s2p'"
        "] has been stored in "
        "./tests/data/evalboard_in_out.s3p\n" in captured.out
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


def test_main_wrong_args(capsys):
    """CLI Tests, wrong input file number"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(
            [
                "./tests/data/evalboard_in_outp_outn_50ohm_5V_pinm20dBm.s2p",
                "./tests/data/evalboard_in_outn_outp_50ohm_5V_pinm20dBm.s2p",
            ]
        )
    captured = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert "Wrong number of files" in captured.out


def test_simple_run():
    """Test run entry point"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
