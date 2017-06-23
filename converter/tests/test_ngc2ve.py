import pytest

@pytest.fixture
def converter():
    from converter.ngc2ve import Ngc2Ve
    return Ngc2Ve()


def test_retractingFilamentWorks(converter):
    lines = \
    """G1 Z0.0
    G1 F6000 A1.0000
    G1 X-0.041 Y11.403 A6.07960
    G1 X-0.177 Y11.400 A6.08667
    G1 F6000 A3.28667
    G1 Z1.250
    G1 F9000 X5.501 Y5.105
    ;TYPE:FILL
    G1 Z0.250
    G1 F6000 A6.08667
    G1 F1200 X6.559 Y4.047 A6.16442
    """
    gcode_list = lines.split('\n')

    converter.process(gcode_list)

    assert 'G23' in gcode_list[1], gcode_list
    assert 'G22' in gcode_list[4], gcode_list
    assert 'G1 Z1.25' in gcode_list[5], gcode_list
    assert 'G23' in gcode_list[9], gcode_list
