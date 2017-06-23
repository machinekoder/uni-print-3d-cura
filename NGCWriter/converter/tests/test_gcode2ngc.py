import pytest

@pytest.fixture
def converter():
    from converter.gcode2ngc import GCode2Ngc
    return GCode2Ngc()

def test_generalConversionWorks(converter):
    data = ['G1 X2 Y1 E100\n',
            'G0 F7200 X20 Y10\n',
            'M106 S200\n',
            'M2\n']

    converter.process(data)

    assert data[0] == 'G1 X2 Y1 A100\n'
    assert data[1] == 'G1 F7200 X20 Y10\n'
    assert data[2] == 'M106 P200\n'
