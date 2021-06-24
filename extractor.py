from tkinter import *
from tkinter import filedialog
import os

def genAutoexec():
    defaultSavePath = r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\csgo\cfg"

    #returns an open file object with the name and selected path
    file = filedialog.asksaveasfile(mode="r+",initialdir = defaultSavePath, initialfile = 'autoexec.cfg')
    savePath = file.name

    # comment out the old autoexec if keep backup is enabled
    if keepBackup.get():
        print('Keeping backup')
        existingLines = file.readlines()
    file.close()

    #reopen the file in truncate mode (start by erasing it all)
    file = open(savePath,'w')
    if keepBackup.get():
        for line in existingLines:
            file.write(r"// " + line)
    file.write('\n')

    # add quickswap if requested
    if quickswap.get():
        file.write('alias +knife slot3; alias -knife lastinv; bind q +knife;\n')
    
    #read in current settings
    defConfFile = open(defaultConfigPath, 'r')
    defLines = defConfFile.readlines()
    defConfFile.close()

    #remove first two lines (not needed)
    defLines.pop(0)
    defLines.pop(0)

    #add in default settings
    for line in defLines:
        file.write(line)
    file.write('host_writeconfig')
    file.close()

    exit()


root = Tk()

defaultConfigPath = r"C:\Program Files (x86)\Steam\userdata\\"

autoFoundSuccess = False
#if only one is found, then assume it is their steamid
if os.path.isdir(defaultConfigPath) and len(os.listdir(defaultConfigPath)) == 1:
    defaultConfigPath += os.listdir(defaultConfigPath)[0]
    defaultConfigPath += r"\730\local\cfg\config.cfg"
    if os.path.isfile(defaultConfigPath):
        file = open(defaultConfigPath)
        if 'cfgver' in file.readline():
            file.close()
            autoFoundSuccess = True



if autoFoundSuccess:
    foundLabel = Label(root, text="Your settings were automatically found.")
    foundLabel.pack()
else:
    notFoundLabel = Label(root, text=r"Your settings could not be found automatically. The are usually found in C:\Program Files (x86)\Steam\userdata\STEAMID\\730\local\cfg\conifg.cfg")
    notFoundLabel.pack()
    notFoundLabel2 = Label(root, text=r"Please maunually select your settings config file")
    notFoundLabel2.pack()
    
    defaultConfigPath = filedialog.askopenfilename(initialdir=defaultConfigPath,
                                          title="Select your config file")
    
    notFoundLabel.destroy()
    notFoundLabel2.destroy()

    file = open(defaultConfigPath)
    if 'cfgver' in file.readline():
        file.close()
        foundLabel = Label(root, text="Your settings were manually found.")
        foundLabel.pack()
    else:
        file.close()
        errLabel = Label(root, text="This does not appear to be a csgo settings files.")
        errLabel.pack()
        root.mainloop()
    

quickswap = IntVar()
quickswapCheck = Checkbutton(root, text = "Add quickswap alias with keybind q", variable=quickswap)
quickswapCheck.pack()

#keep backup of existing autoexec, defaults to true
keepBackup = IntVar()
keepBackupCheck = Checkbutton(root, text = "Keep a backup of existing autoexec.cfg", variable=keepBackup)
keepBackupCheck.select()
keepBackupCheck.pack()

#generate autoexec file (this will overwrite)
genFileButton = Button(root, text="Generate autoexec.cfg file",command=lambda: genAutoexec())
genFileButton.pack()

#set window size
root.geometry("400x400+120+120")
root.mainloop()