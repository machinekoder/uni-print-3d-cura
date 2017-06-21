import pytest

@pytest.fixture
def converter():
    from converter.ngc2ve import Ngc2Ve
    return Ngc2Ve()

def test_outputLineIncresesLineCount(converter):
    converter.outputData = []

    converter._prepare_processing()
    converter._output_line('foo')

    assert len(converter.outputData) == 1
    assert converter.output_line_count == 1

@pytest.fixture
def gcode1():
    layer = \
    """G1 Z0.0
    G1 F6000 A5.4796
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
    gcode_list = [layer]
    return gcode_list

def test_retractingFilamentWorks(converter, gcode1):
    gcode_list = gcode1

    converter.cross_tolerance = 0.05
    converter.process(gcode_list)

    layer = gcode_list[0].split('\n')
    assert 'G23' in layer[1]
    assert 'G22' in layer[5]
    assert 'G1 Z1.25' in layer[6]
    assert 'G23' in layer[10]

@pytest.fixture
def gcode2():
    layer = \
    """G1 X0.0 Y0.0 Z0.0
    G1 F6000 A1.0000 ; unretract
    G1 X10.0 A2.0100
    G1 X0.0 A3.0000
    G1 X10.0 A4.0200
    G1 X0.0 A5.0100
    G1 X10.0 A6.0300
    G1 X0.0 A7.0000
    G1 X10.0 A8.0000
    G1 X0.0
    """
    gcode_list = [layer]
    return gcode_list

def test_optimizingCrossSectionValuesWithoutRetractionAndEndMoveWorks(converter, gcode2):
    gcode_list = gcode2

    converter.enable_cross_optimization = True
    converter.cross_tolerance = 0.05
    converter.process(gcode_list)

    layer = gcode_list[0].split('\n')
    assert 'M700 P0.240528' in layer[2]

@pytest.fixture
def gcode3():
    layer = \
    """G1 X0.0 Y0.0 Z0.0
    G1 F6000 A1.0000 ; unretract
    G1 X10.0 A2.0100
    G1 X0.0 A3.0000
    G1 X10.0 A4.0200
    G1 X0.0 A5.0100
    G1 X10.0 A6.0300
    G1 X0.0 A7.0000
    G1 X10.0 A8.0000
    """
    gcode_list = [layer]
    return gcode_list

def test_optimizingCrossSectionValuesWithoutRetractionAndNoEndMoveWorks(converter, gcode3):
    gcode_list = gcode3

    converter.enable_cross_optimization = True
    converter.cross_tolerance = 0.05
    converter.process(gcode_list)

    layer = gcode_list[0].split('\n')
    assert 'M700 P0.240528' in layer[2]

@pytest.fixture
def gcode4():
    layer = \
    """G1 X0.0 Y0.0 Z0.0
    G1 F6000 A1.0000 ; unretract
    G1 X10.0 A2.0100
    G1 X0.0 A3.0000
    G1 X10.0 A4.0200
    G1 X0.0 A5.0100
    G1 X10.0 A6.0300
    G1 X0.0 A7.0000
    G1 X10.0 A8.0000
    G1 F6000 A7.0000 ; retract
    G1 F6000 A8.0000 ; unretract
    G1 X0.0 A10.000
    G1 X10.0 A11.000
    """
    gcode_list = [layer]
    return gcode_list

def test_optimizingCrossSectionValuesWithRetractionWorks(converter, gcode4):
    gcode_list = gcode4

    converter.enable_cross_optimization = True
    converter.cross_tolerance = 0.05
    converter.process(gcode_list)

    layer = gcode_list[0].split('\n')
    assert 'M700 P0.240528' in layer[2]

