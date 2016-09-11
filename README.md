## Cura plugin for Machinekit and the UNI-PRINT-3D
This plugin enables to use Cura with Machinekit and velocity
extrusion. Furthermore, it also adds a machine configuration for the
[UNI-PRINT-3D 3d printer](https://github.com/thecooltool/UNI-PRINT-3D).
For more details please take a look at [my blog post](http://machinekoder.com/?p=9).

### Install
Use following command to install the files to your Cura installation.
The make argument `CURA_PATH` specifies the path of your cura installation.

``` bash
sudo make install CURA_PATH=/opt/cura
```

On **Windows** please copy the corresponding files to your Cura
installation:

```
uni_print_3d.json -> <cura_path>/share/cura/resources/machines
uni_print_3d_platform.stl <cura_path>/share/cura/resources/meshes/
NGCWriter -> <cura_path>/lib/cura/plugins/
```

On Linux you can optionally install the Machinekit MIME type by running:

``` bash
sudo make mime
```
