from java.io import File
from ij.io import DirectoryChooser
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from ij import IJ

# Prompt user to choose a directory
dc = DirectoryChooser("Choose folder with ND2 files")
directory = dc.getDirectory()

if directory is None:
    print("No folder selected.")
else:
    folder = File(directory)
    files = folder.listFiles()

    for f in files:
    	name = f.getName()
    	if f.isFile() and name.lower().endswith(".nd2") and not name.startswith("._"):
            nd2_path = f.getAbsolutePath()
            print("Importing ND2 file:", nd2_path)

            # Set up Bio-Formats import options
            options = ImporterOptions()
            options.setId(nd2_path)
            options.setSplitChannels(True)   # Set to True to split channels
            options.setColorMode(ImporterOptions.COLOR_MODE_COMPOSITE)
            options.setStackFormat(ImporterOptions.VIEW_STANDARD)
            options.setQuiet(True)

            # Open the image using Bio-Formats
            imps = BF.openImagePlus(options)
            for imp in imps:
                imp.show()

