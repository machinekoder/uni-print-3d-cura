## Cura plugin for Machinekit and the UNI-PRINT-3D
This plugin enables to use Cura with Machinekit and velocity
extrusion. Furthermore, it also adds a machine configuration for the
[UNI-PRINT-3D 3d printer](https://github.com/thecooltool/UNI-PRINT-3D).
For more details please take a look at [my blog post](http://machinekoder.com/?p=9).

### Install
Use following command to install the files to your Cura installation.
The make argument `CURA_PATH` specifies the path of your cura installation.

Additionally make sure to install the **NGCWriter** plugin via the Cura plugin repository from within Cura (*Plugins > Browse Plugins...*).

``` bash
sudo make install CURA_PATH=/opt/cura
```

On **Windows** please copy the corresponding files to your Cura
installation:

```
uni_print_3d.def.json -> <cura_path>/resources/definitions/
uni_print_3d_platform.stl <cura_path>/resources/meshes/
```

On Linux you can optionally install the Machinekit MIME type by running:

``` bash
sudo make mime
```
