# bvh importer for maya

## how to use
 1. Download [bvh_importer.py](./bvh_importer.py), put it any path in your file system, e.g. /Users/Shared/Autodesk/maya/2019/scripts/

 2. Run Autodesk Maya, open the "Script Editor", create a python script window, copy the following script into the window, and run:
 ```python
 import sys
sys.path.append(r'/Users/Shared/Autodesk/maya/2019/scripts/')

import bvh_importer
bvh_importer.BVHImporterDialog()
 ```
3. In the dialog window, choose your .bvh file and import it.