# Copyright (c) 2016 Alexander Roessler
# Cura is released under the terms of the AGPLv3 or higher.

from UM.Mesh.MeshWriter import MeshWriter
from UM.Logger import Logger
from UM.Application import Application

import os
import sys
sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
from converter.gcode2ngc import GCode2Ngc
from converter.ngc2ve import Ngc2Ve


class NGCWriter(MeshWriter):
    version = 3

    def __init__(self):
        super().__init__()

    def write(self, stream, node, mode=MeshWriter.OutputMode.TextMode):
        if mode != MeshWriter.OutputMode.TextMode:
            Logger.log("e", "NGC Writer does not support non-text mode.")
            return False

        #Get the g-code.
        scene = Application.getInstance().getController().getScene()
        gcode_list = getattr(scene, "gcode_list")
        if gcode_list:
            gcodeConverter = GCode2Ngc()
            veConverter = Ngc2Ve()
            gcodeConverter.process(gcode_list)
            veConverter.process(gcode_list)

            for gcode in gcode_list:
                stream.write(gcode)

            return True

        return False
