# -*- coding: utf-8 -*-

from ij import IJ, ImagePlus
from ij.plugin import ChannelSplitter, RGBStackConverter
#from AddScaleDynamically import AddScaleDynamically
import math
import os

def AddScaleDynamically (imp = IJ.getImage()):

    # Get calibration info
    cal = imp.getCalibration()
    pixel_width_um = cal.pixelWidth  # in microns
    image_width_px = imp.getWidth()

    # Define possible scale bar lengths in microns (descending)
    scale_options_um = [1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]

    # Calculate the maximum bar length allowed (1/3 of image width, in microns)
    max_um = (image_width_px / 3.0) * pixel_width_um

    # Pick the largest scale bar that fits
    selected_um = next((s for s in scale_options_um if s <= max_um), scale_options_um[-1])

    # Convert to pixels for scale bar thickness
    # (We’ll use a thickness = 2% of image height, capped reasonably)
    height_px = imp.getHeight()
    bar_thickness_px = max(2, int(0.02 * height_px))  # min thickness of 2 px

    # Optional: Choose a font size based on image size
    font_size = max(12, int(image_width_px / 40))  # scale with width

    # Add the scale bar
    IJ.run(imp, "Scale Bar...", 
        "width=" + str(selected_um) +
        " height=" + str(bar_thickness_px) +
        " font=" + str(font_size) +
        " color=White background=None location=[Lower Right] bold draw")
    
    return


def SavetoRGB (imp = IJ.getImage()):    

    # Copy calibration for later scale bar information
    cal = imp.getCalibration().copy()

    # Get save directory from OriginalFileInfo
    file_info = imp.getOriginalFileInfo()
    if file_info is not None and file_info.directory is not None:
        directory = file_info.directory
    else:
        directory = os.getcwd() + os.sep

    filename = imp.getTitle()

    # Save merged RGB composite
    merged_copy = imp.duplicate()
    RGBStackConverter.convertToRGB(merged_copy)
    AddScaleDynamically(merged_copy)
    IJ.saveAs(merged_copy, "Tiff", os.path.join(directory, "merged_" + filename))

    # Split channels
    channels = ChannelSplitter.split(imp)

    channel_prefixes = {
        0: "DAPI_",
        1: "AF488_",
        2: "AF568_",
        3: "AF647_"
    }

    for i, ch in enumerate(channels):
        # Convert single-channel grayscale to RGB by duplicating it to R, G, B
        ch_stack = ch.getProcessor().convertToByte(True)
        IJ.run(ch, "RGB Color", "")
        ch.setCalibration(cal)
        AddScaleDynamically(ch)

        prefix = channel_prefixes.get(i, "CH%d_" % (i+1))
        output_path = os.path.join(directory, prefix + filename)
        IJ.saveAs(ch, "Tiff", output_path)

if __name__ == "__main__":
    SavetoRGB()