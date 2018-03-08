# Copyright (c) 2016-2018 Alexander Roessler
# Cura is released under the terms of the AGPLv3 or higher.

from UM.Mesh.MeshWriter import MeshWriter
from UM.Logger import Logger
from UM.Application import Application

import os
import sys
path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
    sys.path.append(path)
from converter.gcode2ngc import GCode2Ngc
from converter.ngc2ve import Ngc2Ve


class NGCWriter(MeshWriter):
    version = 3

    def __init__(self):
        super().__init__()

    def write(self, stream, nodes, mode=MeshWriter.OutputMode.TextMode):
        if mode != MeshWriter.OutputMode.TextMode:
            Logger.log("e", "NGC Writer does not support non-text mode.")
            return False

        # Get the g-code.
        active_build_plate = Application.getInstance().getBuildPlateModel().activeBuildPlate
        scene = Application.getInstance().getController().getScene()
        gcode_dict = getattr(scene, "gcode_dict")
        if not gcode_dict:
            return False
        gcode_list = gcode_dict.get(active_build_plate, None)
        if gcode_list is None:
            return False

        gcodeConverter = GCode2Ngc()
        veConverter = Ngc2Ve()
        gcodeConverter.process(gcode_list)
        veConverter.process(gcode_list)

        for gcode in gcode_list:
            stream.write(gcode)

        return True
