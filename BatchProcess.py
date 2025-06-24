# This script takes all the images that are currently open and then converts them to TIFF format.
# The script then saves each TIFF to a new directory in the original directory. Each merged image
# and individual channels are then saved as RGB images with a scale bar in the same directory.

# Assumptions: files are in .nd2 format, are stacks, and have 4 channels (in DAPI, AF488, AF568, 
# and AF647 order). 


import sys
import os

# Dynamically get the current script directory and add it to sys.path
import inspect
script_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from ij import IJ, WindowManager
from MergeND2toTIFF import MergeND2toTIFF
from SavetoRGB import SavetoRGB

from ij import IJ

# Get all open image IDs
image_ids = WindowManager.getIDList()

if image_ids is None:
        print("No images are currently open.")
else:
    for image_id in image_ids:
        imp = WindowManager.getImage(image_id)
        imp_tiff = MergeND2toTIFF(imp)
        SavetoRGB(imp_tiff)
        file_info = imp.getOriginalFileInfo()
        if file_info is not None:
            filename = file_info.fileName
        else:
            # fallback if the image was created in memory or no original file info is available
            filename = imp.getTitle()
        print("Saved " + filename)
        imp_tiff.close()