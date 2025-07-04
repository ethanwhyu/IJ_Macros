# -*- coding: utf-8 -*-
from ij import IJ

def AddScaleDynamically(imp, burn_into_pixels=True):
    """
    Adds a scale bar to the ImagePlus `imp`.
    If `burn_into_pixels` is True the bar is drawn into the pixels (recommended
    for exports).  Otherwise it is added as an overlay.
    """

    # --- use the image that was passed in, not the active window ---
    cal = imp.getCalibration()
    pixel_width_um  = cal.pixelWidth
    image_width_px  = imp.getWidth()
    image_height_px = imp.getHeight()

    # choose the largest bar ≤ ⅓ of the image width
    max_um = (image_width_px / 3.0) * pixel_width_um
    for s in (1000, 500, 200, 100, 50, 20, 10, 5, 2, 1):
        if s <= max_um:
            selected_um = s
            break

    bar_thickness_px = max(2, int(0.02 * image_height_px))
    font_size        = max(12, int(image_width_px / 40))

    mode = "draw" if burn_into_pixels else "overlay"
    IJ.run(
        imp, "Scale Bar...",
        "width={} height={} font={} color=White "
        "background=None location=[Lower Right] bold {}".format(
            selected_um, bar_thickness_px, font_size, mode)
    )

    # return the same ImagePlus so the caller can continue working with it
    return imp
