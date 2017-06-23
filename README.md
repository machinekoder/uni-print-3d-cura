# NGCWriter
NGC (RS-274 GCode) output plugin for Cura
including velocity extruding

## Converting a GCode file without Cura

You can use the `convert_gcode.py` util to convert a RepRap/Markin
flavor GCode file to Machinekit/Velocity-Extrusion flavor GCode.

```
$ ./convert_gcode.py -h
usage: convert_gcode.py [-h] -i INPUT [-o OUPUT]

convert a RepRap/Marlin flavor GCode file to a Machinekit/Velocity-Extrusion flavor GCode file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file
  -o OUPUT, --ouput OUPUT
                        Output file
```
