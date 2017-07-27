PRINTER_NAME := uni_print_3d
CURA_PATH := /opt/cura

install:
	cp -v $(PRINTER_NAME).def.json $(CURA_PATH)/usr/bin/resources/definitions/
	cp -v $(PRINTER_NAME)_platform.stl $(CURA_PATH)/usr/bin/resources/meshes/
	rm -rf $(CURA_PATH)/usr/bin/plugins/plugins/NGCWriter
	cp -vr NGCWriter $(CURA_PATH)/usr/bin/plugins/plugins
	cp -v SimpleTweak.py $(CURA_PATH)/usr/bin/plugins/plugins/PostProcessingPlugin/scripts/SimpleTweak.py

mime:
	cp machinekit.xml /usr/share/mime/packages/
	update-mime-database /usr/share/mime
