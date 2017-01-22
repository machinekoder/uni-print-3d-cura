from ..Script import Script
class SimpleTweak(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"SimpleTweak (for Alex Uni-Print-3D)",
            "key": "SimpleTweak",
            "metadata":{},
            "version": 2,
            "settings":
            {
                "pause_height":
                {
                    "label": "Weak at height",
                    "description": "At what height should we tweak",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.5
                }
            }
        }"""

    def execute(self, data):
        current_z = 0.0
        is_prefix = True
        pause_z = self.getSettingValueByKey("pause_height")
        for layer in data:
            lines = layer.split("\n")
            for line in lines:
                if not is_prefix or ";LAYER_COUNT:" in line:
                    is_prefix = False
                else:
                    continue

                g = self.getValue(line, 'G')
                if g == 1 or g == 0:
                    current_z = self.getValue(line, 'Z')
                    if current_z is not None:
                        if current_z >= pause_z:
                            custom_gcode = ";TYPE:CUSTOM\n"
                            custom_gcode += "; -- Execute custom GCode at height (%.2f mm) --\n" % pause_z

                            # Insert custom gcode
                            custom_gcode += "M64 P16 ; Turn on the auxillary fan\n"
                            index = data.index(layer) 
                            layer = custom_gcode + layer
                            data[index] = layer # Override the data of this layer with the modified data
                            return data
                        break
        return data
