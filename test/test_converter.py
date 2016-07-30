import unittest
import sys
import os
sys.path = [os.path.abspath(os.path.dirname(__file__) + "/..")] + sys.path
from converter.gcode2ngc import GCode2Ngc
from converter.ngc2ve import Ngc2Ve


class TestGCode2Ngc(unittest.TestCase):
    def setUp(self):
        self.converter = GCode2Ngc()

    def test_basic(self):
        data = []
        data.append('G1 X2 Y1 E100')

        self.converter.process(data)

        assert(data[0] == 'G1 X2 Y1 A100')


class TestVelocityExtrusion(unittest.TestCase):
    def setUp(self):
        self.converter = Ngc2Ve()

    def test_basic(self):
        data = []
        data.append('; comment\n')
        data.append('G0 X0 Y0\n')
        data.append('G23\n')
        data.append('G1 X1 A100 F100\n')  # 100 diff
        data.append('G1 Y1 A300\n')  # 200 diff
        data.append('G22\n')

        self.converter.process(data)

        print(data)
        assert(data[0] == '')
