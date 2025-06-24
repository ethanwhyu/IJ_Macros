from ij import IJ
import math
import os

def AddScaleDynamically (imp):
    # Get the currently active image
    imp = IJ.getImage()

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
        " color=White background=None location=[Lower Right] bold")

    # Get original file path
    original_path = imp.getOriginalFileInfo().directory + imp.getOriginalFileInfo().fileName

    # Construct new path (overwrite or save new)
    output_path = original_path  # This will overwrite the original

    # Save as TIFF
    IJ.saveAs(imp, "Tiff", output_path)