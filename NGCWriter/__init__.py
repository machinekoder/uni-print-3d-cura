# Copyright (c) 2015 Ultimaker B.V.
# Cura is released under the terms of the AGPLv3 or higher.

from . import NGCWriter

from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")


def getMetaData():
    return {
        "plugin": {
            "name": "NGC Writer",
            "author": "Strahlex",
            "version": "1.0",
            "description": catalog.i18nc("NGC Writer Plugin Description", "Writes RS-274 GCode to a file"),
            "api": 2
        },

        "mesh_writer": {
            "output": [{
                "extension": "ngc",
                "description": catalog.i18nc("NGC Writer File Description", "RS-274 GCode File"),
                "mime_type": "text/x-ngc",
                "mode": NGCWriter.NGCWriter.OutputMode.TextMode
            }]
        }
    }


def register(app):
    return {"mesh_writer": NGCWriter.NGCWriter()}
