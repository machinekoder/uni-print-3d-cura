PRINTER_NAME = uni_print_3d
CURA_PATH = /opt/cura

install:
	cp $(PRINTER_NAME).def.json $(CURA_PATH)/resources/definitions/
	cp $(PRINTER_NAME)_platform.stl $(CURA_PATH)/resources/meshes/

mime:
	cp machinekit.xml /usr/share/mime/packages/
	update-mime-database /usr/share/mime
