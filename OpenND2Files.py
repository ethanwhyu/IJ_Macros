from ij import IJ, WindowManager
from java.awt import Frame
from java.io import File
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
            IJ.open(file.getAbsolutePath())
        
    else:
        IJ.showMessage("No files were selected.")
else:
    IJ.showMessage("File selection canceled.")
