from java.io import File
from ij.io import DirectoryChooser
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from ij import IJ, ImagePlus
from ij.process import ImageProcessor
from ij.plugin import RGBStackMerge
from ij.gui import GenericDialog
from ij.plugin import ChannelSplitter
from ij.io import FileSaver

# Fixed colors for channels 0-3
color_map = {
    0: "Blue",
    1: "Green",
    2: "Yellow",
    3: "Red"
}

#def set_channel_brightness(imp, channel_index, min_val, max_val):
#    channels = ChannelSplitter.split(imp)   # split channels correctly
#    ip = channels[channel_index].getProcessor()
#    ip.setMinAndMax(min_val, max_val)
#    channels[channel_index].setProcessor(ip)
#    merged = RGBStackMerge.mergeChannels(channels, False)
#    merged.setTitle(imp.getTitle())
#    return merged

dc = DirectoryChooser("Choose folder with ND2 files")
directory = dc.getDirectory()

if not directory:
    print("No directory selected, exiting.")
    exit()

folder = File(directory)
files = folder.listFiles()

merged_images = []
adjusted_images = []

for f in files:
    name = f.getName()
    if f.isFile() and name.lower().endswith(".nd2") and not name.startswith("._"):
        path = f.getAbsolutePath()
        print("Loading (split channels):", path)

        options = ImporterOptions()
        options.setId(path)
        options.setSplitChannels(True)
        options.setColorMode(ImporterOptions.COLOR_MODE_DEFAULT)
        options.setOpenAllSeries(False)
        options.setStackOrder("XYCZT")

        imps = BF.openImagePlus(options)
        
        # Ask user once for min/max values per channel (4 channels)
		gd = GenericDialog("Set brightness/contrast per channel for all images")
		for i in range(4):
		    gd.addNumericField(color_map[i] + " min:", 0, 0)
		    gd.addNumericField(color_map[i] + " max:", 4095, 0)
		gd.showDialog()
		if gd.wasCanceled():
		    print("User canceled input, exiting.")
		    exit()
		
		# Retrieve user input
		user_minmax = []
		for i in range(4):
		    user_min = gd.getNextNumber()
		    user_max = gd.getNextNumber()
		    user_minmax.append((user_min, user_max))
		
		adjusted_images = []
		# Apply user brightness/contrast to each merged image
		for imp in merged_images:
		    channels = ChannelSplitter.split(imp)   # fix here too
		    for i, (min_val, max_val) in enumerate(user_minmax):
		        if i < len(channels):
		            ip = channels[i].getProcessor()
		            ip.setMinAndMax(min_val, max_val)
		            channels[i].setProcessor(ip)
		    adjusted_merged = RGBStackMerge.mergeChannels(channels, False)
		    adjusted_merged.setTitle(imp.getTitle())
		    adjusted_merged.show()
		    adjusted_images.append(imp)

        # Apply LUT colors to each split channel and prepare for merge
        channels_for_merge = []
        for i, imp in enumerate(imps):
            if i in color_map:
                IJ.run(imp, color_map[i], "")
            else:
                IJ.run(imp, "Grays", "")
            channels_for_merge.append(imp)

        # Merge channels into one RGB composite
        merged_imp = RGBStackMerge.mergeChannels(channels_for_merge, False)
        merged_imp.setTitle(name + "_merged")
        merged_images.append(merged_imp)

output_dir = File(directory + "TIFF Processed Exports/")
if not output_dir.exists():
    output_dir.mkdir()

for imp in adjusted_images:  # assuming you stored them in adjusted_images
    # Set display min/max values per channel
    imp.setDisplayMode(IJ.COLOR)

    for c in range(1, 5):  # ImageJ channels are 1-indexed
        imp.setC(c)
        min_val, max_val = user_minmax[c - 1]
        imp.setDisplayRange(min_val, max_val)

    # Save as TIFF with display metadata
    filename = imp.getTitle() + ".tif"
    save_path = output_dir.getAbsolutePath() + "/" + filename

    fs = FileSaver(imp)
    if fs.saveAsTiff(save_path):
        print("Saved with display range:", save_path)
    else:
        print("Failed to save:", save_path)