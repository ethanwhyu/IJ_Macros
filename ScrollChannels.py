from ij import IJ, WindowManager
from ij.gui import GenericDialog

# Prompt the user for desired channel
gd = GenericDialog("Set Channel for All Open Images")
gd.addNumericField("Channel number to set (1-based):", 1, 0)
gd.showDialog()

if gd.wasCanceled():
    print("User canceled.")
else:
    target_channel = int(gd.getNextNumber())

    # Get all open image IDs
    image_ids = WindowManager.getIDList()

    if image_ids is None:
        print("No images are currently open.")
    else:
        for image_id in image_ids:
            imp = WindowManager.getImage(image_id)
            if imp is not None and imp.getNChannels() >= target_channel:
                imp.setC(target_channel)
                imp.updateAndDraw()
                print(imp.getTitle() + ": Set to channel " + str(target_channel))
            else:
                title = imp.getTitle() if imp is not None else "Unknown"
                print(title + ": Not enough channels.")
