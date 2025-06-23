from ij import IJ, ImageStack, ImagePlus, CompositeImage
from ij.plugin import ChannelSplitter
import os

# Get the open multichannel image
imp = IJ.getImage()

# Split channels
split = ChannelSplitter.split(imp)

# Define custom order:
# Original channel index → position in composite stack
# C1 (Red) ← split[3]
# C2 (Green) ← split[1]
# C3 (Blue) ← split[0]
# C4 (Yellow) ← split[2]
reordered = [split[0], split[1], split[2], split[3]]
# Create a new stack and ImagePlus
stack = ImageStack(reordered[0].getWidth(), reordered[0].getHeight())

for ch in reordered:
    stack.addSlice(ch.getProcessor())

# Create new ImagePlus with proper dimensions (X, Y, Channels, Slices, Frames)
nChannels = len(reordered)
nSlices = reordered[0].getNSlices()
nFrames = reordered[0].getNFrames()

merged = ImagePlus("Custom Composite", stack)
merged.setDimensions(nChannels, nSlices, nFrames)

# Convert to composite, preserving original LUTs
composite = CompositeImage(merged, CompositeImage.COMPOSITE)

# Copy LUTs from original split images
for i, ch in enumerate(reordered):
    composite.setChannelLut(ch.getProcessor().getLut(), i + 1)

composite.show()

# Get the full path to the current image
info = imp.getOriginalFileInfo()
if info is not None:
    original_dir = info.directory
    original_name = imp.getShortTitle()
else:
    # Fallback if originalFileInfo is missing (e.g. image opened from memory)
    original_dir = IJ.getDirectory("current")
    original_name = imp.getTitle().replace(".tif", "").replace(".nd2", "")

# Build output directory path using os
output_dir = os.path.join(original_dir, "Processed_Exports_" + original_name)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Build full output file path
output_path = os.path.join(output_dir, original_name + ".tif")

# Save the final composite image
IJ.saveAsTiff(composite, output_path)

