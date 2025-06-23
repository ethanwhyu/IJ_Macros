from ij import IJ, WindowManager
from java.awt import Frame
from java.io import File
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from javax.swing import JFileChooser
from javax.swing.filechooser import FileNameExtensionFilter

# Prompt user to select multiple ND2 files
chooser = JFileChooser()
chooser.setMultiSelectionEnabled(True)
chooser.setFileFilter(FileNameExtensionFilter("ND2 files", ["nd2"]))
chooser.setDialogTitle("Select .nd2 files to open")

ret = chooser.showOpenDialog(None)

if ret == JFileChooser.APPROVE_OPTION:
    selected_files = chooser.getSelectedFiles()

    if selected_files:
        for file in selected_files:
            path = file.getAbsolutePath()

            options = ImporterOptions()
            options.setId(path)
            options.setSplitChannels(False)
            options.setColorMode(ImporterOptions.COLOR_MODE_DEFAULT)
            options.setAutoscale(False)
            options.setOpenAllSeries(False)
            options.setStackOrder("XYCZT")

            imps = BF.openImagePlus(options)

            # Show all imported image(s) from the current file
            for imp in imps:
                imp.show()
        
    else:
        IJ.showMessage("No files were selected.")
else:
    IJ.showMessage("File selection canceled.")
