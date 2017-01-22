CURA_PATH = /opt/cura

install:
	cp uni_print_3d.def.json $(CURA_PATH)/share/cura/resources/definitions/
	cp uni_print_3d_platform.stl $(CURA_PATH)/share/cura/resources/meshes/
	rm -rf $(CURA_PATH)/lib/cura/plugins/NGCWriter
	cp -r NGCWriter $(CURA_PATH)/lib/cura/plugins/

mime:
	cp machinekit.xml /usr/share/mime/packages/
	update-mime-database /usr/share/mime
