from ij import IJ
from ij.plugin import ChannelSplitter, RGBStackMerge
from ij.process import LUT
from java.awt import Color

# Define your custom color map
color_map = {
    0: Color.blue,
    1: Color.green,
    2: Color.yellow,
    3: Color.red
}

# Get the current image
imp = IJ.getImage()

# Split channels
channels = ChannelSplitter.split(imp)
num_channels = len(channels)

# Assign LUTs to each channel
for i in range(num_channels):
    c_imp = channels[i]
    color = color_map.get(i, Color.white)  # Default to white if not mapped
    lut = LUT(color)
    c_imp.setLut(lut)
    c_imp.show()

# Merge channels back together
merged = RGBStackMerge.mergeChannels(channels, True)
merged.setTitle("Merged Image")
merged.show()
