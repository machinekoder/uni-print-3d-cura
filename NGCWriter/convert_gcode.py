#!/usr/bin/env python

import sys
import os
import argparse

parser = argparse.ArgumentParser(description="""
convert a RepRap/Marlin flavor GCode file to a Machinekit/Velocity-Extrusion flavor GCode file
""")
parser.add_argument('-i', '--input', help='Input file', required=True)
parser.add_argument('-o', '--output', help='Output file', default=None)
parser.add_argument('-nv', '--no-velocity-extrusion', help='Disable velocity extrusion', action='store_true')
args = parser.parse_args()

sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
from converter.gcode2ngc import GCode2Ngc
from converter.ngc2ve import Ngc2Ve

input_name = args.input
output_name = args.output
if output_name is None:
    (path, _) = os.path.splitext(input_name)
    output_name = '%s.ngc' % path

print('converting %s -> %s' % (input_name, output_name))

input_file = open(input_name, 'rt')
gcode_list = input_file.readlines()  # fix maybe
input_file.close()

output_file = open(output_name, 'wt')

# TODO: add prefix

gcodeConverter = GCode2Ngc()
veConverter = Ngc2Ve()
gcodeConverter.process(gcode_list)
veConverter.process(gcode_list)

for gcode in gcode_list:
    output_file.write(gcode)

# TODO: add postfix

output_file.close()
