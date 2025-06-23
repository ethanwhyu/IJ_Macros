from ij import IJ
from ij.io import OpenDialog, FileSaver
from ij.plugin import ChannelSplitter
import os

# Prompt user to open a file
od = OpenDialog("Choose a multichannel TIFF file", None)
input_path = od.getPath()

if input_path is None:
    IJ.error("No file was selected.")
else:
    # Extract file name and directory
    input_dir = os.path.dirname(input_path)
    input_name = os.path.basename(input_path)
    base_name, ext = os.path.splitext(input_name)

    # Create output directory
    output_dir = os.path.join(input_dir, base_name + " Split Components")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Open image
    imp = IJ.openImage(input_path)
    if imp is None:
        IJ.error("Failed to open image.")
    else:
        # Split channels
        channels = ChannelSplitter.split(imp)

        # Define color names typically assigned to channels (adjust if needed)
        color_names = ["gray", "red", "green", "blue", "cyan", "magenta", "yellow"]
        num_channels = len(channels)

        # Process each channel
        for i in range(num_channels):
            c_imp = channels[i]

            # Convert to RGB to preserve LUT display
            IJ.run(c_imp, "RGB Color", "")

            # Assign color name or fallback
            prefix = color_names[i] if i < len(color_names) else "ch{}".format(i+1)

            # Build save path
            save_name = "{}_{}.tif".format(prefix, base_name)
            save_path = os.path.join(output_dir, save_name)

            # Save image
            fs = FileSaver(c_imp)
            fs.saveAsTiff(save_path)

            c_imp.close()

        imp.close()
        IJ.log("Saved {} RGB split channels to:\n{}".format(num_channels, output_dir))
