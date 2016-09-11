PRINTER_NAME = uni_print_3d
CURA_PATH = /opt/cura

install:
	cp $(PRINTER_NAME).def.json $(CURA_PATH)/resources/definitions/
	cp $(PRINTER_NAME)_platform.stl $(CURA_PATH)/resources/meshes/
	rm -rf $(CURA_PATH)/plugins/plugins/NGCWriter
	cp -r NGCWriter $(CURA_PATH)/plugins/plugins
	cp TweakAtZ.py $(CURA_PATH)/lib/cura/plugins/PostProcessingPlugin/scripts/TweakAtZ.py

mime:
	cp machinekit.xml /usr/share/mime/packages/
	update-mime-database /usr/share/mime
