from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import os.path
import sys

#WINDOW
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Estop Generator")  # window title
        self.geometry('540x280')  # window size

        self.labelFrame = ttk.LabelFrame(self, text="Choose a CSV File")  # browser frame
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)  # frame size

        self.labelFrame2 = ttk.LabelFrame(self, text="Choose Where to Save XMLs")  # save file frame
        self.labelFrame2.grid(column=0, row=2, padx=20, pady=20)  # frame size

        self.filebutton()  # Browse Button
        self.drop_menu()  # Resolution Drop Down
        self.start()  # Start Button
        self.drop_fact()  # Factory Talk Drop Down
        self.savebutton()  #Save button

    def savebutton(self):
        self.button = ttk.Button(self.labelFrame2, text="...", command=self.savedialog)  # save button
        self.button.grid(column=2, row=2)  # button position

    def savedialog(self):
        self.savename = filedialog.askdirectory()
        self.label2 = ttk.Label(self.labelFrame2, text="")  # add filename chosen to window
        self.label2.grid(column=1, row=2)  # position of filename
        self.label2.configure(text=self.savename)  # add filename to window
        global save  # use s in other functions
        save = self.savename  # store filename to read

    # CSV BROWSE BUTTON
    def filebutton(self):
        self.button = ttk.Button(self.labelFrame, text="...", command=self.filedialog)  # browser button
        self.button.grid(column=2, row=1)  # button position

    # FILE DIALOG WINDOW
    def filedialog(self):
        self.filename = filedialog.askopenfilename(initialdir="Desktop", title="Select CSV File", filetype=(
        ("csv", "*.csv"), ("All Files", "*.*")))  # file browse dialog
        self.label = ttk.Label(self.labelFrame, text="")  # add filename chosen to window
        self.label.grid(column=1, row=1)  # position of filename
        self.label.configure(text=self.filename)  # add filename to window
        global s  # use s in other functions
        s = self.filename  # store filename to read

    # DROP DOWN MENU
    def drop_menu(self):
        def change_res(res, option_menu, self):
            global resolution
            global fresolution
            resolution = "%s" % (var.get())
            if resolution == 'E00 - Blank 640x480.xml':
                fresolution = 'E00 - Blank 640x480.xml'
                if hasattr(sys, '_MEIPASS'):
                    # PyInstaller >= 1.6
                    os.chdir(sys._MEIPASS)
                    fresolution = os.path.join(sys._MEIPASS, fresolution)
                elif '_MEIPASS2' in os.environ:
                    # PyInstaller < 1.6 (tested on 1.5 only)
                    os.chdir(os.environ['_MEIPASS2'])
                    fresolution = os.path.join(os.environ['_MEIPASS2'], fresolution)
                else:
                    os.chdir(os.dirname(sys.argv[0]))
                    fresolution = os.path.join(os.dirname(sys.argv[0]), fresolution)
            elif resolution == 'E00 - Blank 1280x800.xml':
                fresolution = 'E00 - Blank 1280x800.xml'
                if hasattr(sys, '_MEIPASS'):
                    # PyInstaller >= 1.6
                    os.chdir(sys._MEIPASS)
                    fresolution = os.path.join(sys._MEIPASS, fresolution)
                elif '_MEIPASS2' in os.environ:
                    # PyInstaller < 1.6 (tested on 1.5 only)
                    os.chdir(os.environ['_MEIPASS2'])
                    fresolution = os.path.join(os.environ['_MEIPASS2'], fresolution)
                else:
                    os.chdir(os.dirname(sys.argv[0]))
                    fresolution = os.path.join(os.dirname(sys.argv[0]), fresolution)

        res = ['E00 - Blank 640x480.xml', 'E00 - Blank 1280x800.xml']  # resolutions

        var = StringVar(self)  # add res to window
        var.set("Set Resolution")  # set 640x480 as default
        var.trace("w", change_res)

        self.option_menu = OptionMenu(self, var, *res)  # place all resolutions in drop down
        self.option_menu.grid(column=0, row=3)  # position of menu

    # START BUTTON
    def start(self):
        self.button = ttk.Button(text="Start", command=Estop)  # start button runs estop script
        self.button.grid(column=0, row=5)  # position of start button

    # DROP DOWN FACTORYTALK
    def drop_fact(self):
        def change_vers(vers, option_menu, self):
            global version
            version = "%s" % (variable.get())

        vers = ["FT.11", "FT.10", "FT.9", "FT.8", "FT.7", "FT.6"]

        variable = StringVar(self)
        variable.set("Choose Version of FactoryTalk Studio")
        variable.trace("w", change_vers)

        self.option_menu = OptionMenu(self, variable, *vers)
        self.option_menu.grid(column=0, row=4)


# FUNCTION
def Estop():
    firstIndex = 0  # index to find tags
    secondIndex = 0  # index to find
    thirdIndex = 0
    lst_tagstr = []
    lst_desstr = []
    # read chosen file
    with open(s) as f:
        # line by line
        for line in f:
            # start finding tags and descriptions
            if "DCS" in line:
                if ("TAG,," in line):
                    newstr = line.replace("TAG,,", "")
                    firstIndex = newstr.find(",")
                    tagstr = (newstr[0:firstIndex])
                    newstr2 = newstr[0:firstIndex]
                    newstr = newstr.replace(newstr2, "")
                    newstr = newstr[1:]
                    secondIndex = newstr.find(",")
                    desqstr = newstr[0:secondIndex]
                    desstr = desqstr.replace('"', '')
                    lst_tagstr.append(tagstr)
                    lst_desstr.append(desstr)
                    # print lst_tagstr
                    # print lst_desstr
                    thirdIndex = thirdIndex + 1
                    # done finding tags and descriptions
    thirdIndex = thirdIndex  # 166
    endarr = thirdIndex - 1
    mod = thirdIndex % 8  # 6: last tags
    num = thirdIndex / 8  # =20: number of tags incremented by 8
    if mod > 0:
        num = num + 1  # number of pages
    elif mod == 0:
        num = num  # number of pages
    cntarr = 0
    cntpg = 0
    cnt8 = 0
    ilength = 0
    newline = '\n'  # new line notation for batch file
    lines = '<gfxImport>' + newline  # first line of batch file
    while cntarr <= endarr:  # steps through tag/des arr
        while cntpg <= num:  # creates new pages
            cntpg = cntpg + 1
            pgfilnum = 'E0%d-Estops PG%d' % (cntpg, cntpg)  # pg with number
            spgfilenum = '/E0%d-Estops PG%d' % (cntpg, cntpg)
            pgfile = pgfilnum + '.xml'  # page file name
            spgfile = spgfilenum + '.xml'  # page file name with a slash (for path to write files)
            batchname = save + "/XMLBatchImport.xml"  # batch file path
            with open(batchname, "a") as z:
                qpgfile = '"' + pgfile + '"'  # add quotes to page file name for batch import
                nextline0 = "    <import importFile=""%s""/>" % qpgfile
                nextline = nextline0 + newline
                lines = lines + nextline
                pgname = save + spgfile
                import shutil
                shutil.copyfile(fresolution, pgname)
                with open(pgname) as x:
                    newtxt = x.read()
                    diff = endarr - cntarr  # find difference between current position and end of arr
                    if diff > 8:
                        cnt8 = 0  # resets counter for new page
                        while cnt8 <= 7:
                            Des = lst_desstr[cntarr]  # pulls des from arr
                            Tag = lst_tagstr[cntarr]  # pulls tag from arr
                            n = cnt8 + 1  # cnt for block number
                            rpltag = "E_Stop_Block_%d_DCS" % (n)  # search for E_Stop_Block_#_DCS
                            rpldes = "E-Stop Block %d" % (n)  # search for E-Stop Block #
                            if "Gfx-" in newtxt:  # change FactoryTalk Version
                                index = newtxt.find("Gfx-")  # find Gfx-ME##
                                ilength = index + 8  # find range in line
                                replace = newtxt[index:ilength]  # string that will be replaced (Gfx-ME##)
                                strversidx = version.find(".")  # find period before number from menu (ex: FT.11)
                                strversstrt = strversidx + 1  # find tens digit of FT
                                length = len(version)  # find end of FT
                                strversnum = version[strversstrt:length]  # grabs number (ex: 11)
                                intversnum = int(strversnum)  # turns number to integer
                                newnum = intversnum + 1  # add one for text file syntax
                                strnewnum = str(newnum)  # convert number to string
                                lennewnum = len(strnewnum)  # find length of str
                                if lennewnum == 2:
                                    newvers = 'Gfx-ME%s' % strnewnum
                                    newtxt = newtxt.replace(replace, newvers)
                                elif lennewnum == 1:
                                    newvers = 'Gfx-ME0%s' % strnewnum
                                    newtxt = newtxt.replace(replace, newvers)
                                if (rpldes) in newtxt:  # if E-Stop Block is in the file
                                    newtxt = newtxt.replace(rpldes, Des)  # replace with des
                                    if (rpltag) in newtxt:  # if E_Stop_Block_DSC in text
                                        newtxt = newtxt.replace(rpltag, Tag)  # replace with tag
                                        with open(pgname, "w") as x:
                                            x.write(newtxt)  # write file with new des and tags
                                            cnt8 = cnt8 + 1  # go to next tag/des on page
                                            cntarr = cntarr + 1  # go to next tag/des in arr
                                            if cntarr >= thirdIndex:  # when at the end exit program
                                                z.write(str(lines))
                                                import sys
                                                sys.exit()

                    elif diff <= mod and diff != 0:
                        cnt8 = 0
                        while cnt8 <= mod:
                            Des = lst_desstr[cntarr]  # pulls des from arr
                            Tag = lst_tagstr[cntarr]  # pulls tag from arr
                            n = cnt8 + 1  # cnt for block number
                            rpltag = "E_Stop_Block_%d_DCS" % (n)
                            rpldes = "E-Stop Block %d" % (n)
                            if "Gfx-" in newtxt:  # change FactoryTalk Version
                                index = newtxt.find("Gfx-")  # find Gfx-ME##
                                ilength = index + 8  # find range in line
                                replace = newtxt[index:ilength]  # string that will be replaced (Gfx-ME##)
                                strversidx = version.find(".")  # find period before number from menu (ex: FT.11)
                                strversstrt = strversidx + 1  # find tens digit of FT
                                length = len(version)  # find end of FT
                                strversnum = version[strversstrt:length]  # grabs number (ex: 11)
                                intversnum = int(strversnum)  # turns number to integer
                                newnum = intversnum + 1  # add one for text file syntax
                                strnewnum = str(newnum)  # convert number to string
                                lennewnum = len(strnewnum)  # find length of str
                                if lennewnum == 2:
                                    newvers = 'Gfx-ME%s' % strnewnum
                                    newtxt = newtxt.replace(replace, newvers)
                                elif lennewnum == 1:
                                    newvers = 'Gfx-ME0%s' % strnewnum
                                    newtxt = newtxt.replace(replace, newvers)
                                if (rpldes) in newtxt:
                                    newtxt = newtxt.replace(rpldes, Des)
                                    if (rpltag) in newtxt:
                                        newtxt = newtxt.replace(rpltag, Tag)
                                        with open(pgname, "w") as x:
                                            x.write(newtxt)
                                            cnt8 = cnt8 + 1
                                            cntarr = cntarr + 1  # next tag/des from arr
                                            if cntarr >= thirdIndex:
                                                batchend = "</gfxImport>"  # last line of batch file
                                                lines = lines + batchend
                                                z.write(str(lines))
                                                import sys
                                                sys.exit()


if __name__ == '__main__':
    root = Root()
    root.mainloop()