import threading
from os.path import isdir
from platform import system as syst
from os import chdir, makedirs, walk, sep, path, listdir,system
from sys import stdout
from time import ctime, sleep, localtime

class MainWindows:
    def __init__(self):
        self.keep = []
        self.problems = []
        self.counter = 5

    def usb_finder(self):
        self.usb_list = []
        self.dest = ""
        drivebits = GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                drname = '%c:\\' % chr(ord('A') + d)
                t = GetDriveType(drname)
                if t == DRIVE_REMOVABLE:
                    self.usb_list.append(drname)

        if self.usb_list.__len__() == 0:
            print("No USB Connected!!!\n")
            self.timer()
            exit()

        favorite = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"

        for usb in self.usb_list:
            chdir(usb)
            if favorite in listdir('.'):
                self.dest = usb + sep + favorite + sep
                file = open(self.dest + "Problems.txt", "w", encoding="utf-8")
                file.write("#####No problem found#####")
                file.close()
        if self.dest == "":
            print("No F-USB!!!\n")
            self.timer()
            exit()

    def timer(self):
        if self.counter >= 0:
            stdout.write('\r' + str("Exiting in " + str(self.counter)))
            t = threading.Timer(1, self.timer)
            t.start()
            self.counter -= 1

    def drives(self, mode,OS):
        win = environ['SYSTEMDRIVE'] + sep
        self.drive_list = []
        drivebits = GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                drname = '%c:\\' % chr(ord('A') + d)
                t = GetDriveType(drname)
                if t == DRIVE_FIXED:
                    self.drive_list.append(drname)

        # region NOT OS
        if OS == "no":
            for i in self.drive_list:
                if i == win:
                    self.drive_list.remove(i)
        else:
            print("====\nTry to run the program as Administrator unless it may not work.\n====")
        # endregion

        # self.drive_list.remove("D:\\")
        # self.drive_list.remove("F:\\")

        # region AutoMinimize
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
        # endregion

        if mode == "normal":
            for driver in self.drive_list:
                self.normal(driver)
        if mode == "Unnormal":
            o = open(self.dest + "Log.txt", "w", encoding="utf-8")
            o.close()

            for driver in self.drive_list:
                self.logWriter(driver)

    def normal(self, driver):
        chdir(driver)
        print("\n" + driver + "...")
        print("start: "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))

        for (dirpath, dirname, filenames) in walk('.'):
            for filename in filenames:
                main_location = sep.join([dirpath, filename])
                absulpathR = path.abspath(main_location)
                absulpath = absulpathR.replace(":", "")[:absulpathR.rfind(sep)] + sep
                try:
                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                    file = open(self.dest + absulpath + filename, "w", encoding="utf-8")
                    file.write("[Size]\n" + str(path.getsize(absulpathR) / 1024) + " KB" + "\n" + str(
                        path.getsize(absulpathR) / 1024 / 1024) + " MB" + "\n" + str(
                        path.getsize(absulpathR) / 1024 / 1024 / 1024) + " GB" +
                               "\n\n[Modified Date]\n" + str(ctime(path.getmtime(absulpathR))) +
                               "\n\n[Created Date]\n" + str(ctime(path.getctime(absulpathR))))
                    file.close()
                except FileNotFoundError:
                    self.problems.append(self.dest + absulpath + filename + "\n")
        print("end  : "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))

    # region unNormal
    def logWriter(self, driver):
        chdir(driver)
        print("\n" + driver + "...")
        print("start: "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))

        for (dirpath, dirnames, filenames) in walk('.'):
            for filename in filenames:
                absulpathR = path.abspath(sep.join([dirpath, filename]))
                absulpath = absulpathR.replace(":", "")[:absulpathR.rfind(sep)] + sep

                try:
                    details = "[Size]" + str(path.getsize(absulpathR)) + " B" + "[MD]" + str(
                        path.getmtime(absulpathR)) + "[CD]" + str(path.getctime(absulpathR))

                    self.keep.append(absulpath + filename + "{" + details + "}" + "\n")
                except FileNotFoundError:
                    self.keep.append(str(FileNotFoundError) + absulpath + filename)
                except OSError:
                    self.keep.append(str(OSError) + absulpath + filename)

        file = open(self.dest + "Log.txt", "a", encoding="utf-8")
        for keep in self.keep:
            try:
                file.write(keep)
            except UnicodeEncodeError:
                self.problems.append(str(UnicodeEncodeError) + " for a file in " + keep[:keep.rfind(sep)])
        file.close()

        print("end  : "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))

    def logReader(self):
        print("start: "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))
        try:
            reader = open(self.dest + "Log.txt", "r", encoding="utf-8")
            lister = reader.readlines()
        except FileNotFoundError:
            input("====\nThe [Log.txt] couldn't be found in " + self.dest + "\nCopy it there and re-open the program.\n====")
            self.timer()
            exit()

        for item in lister:
            item = item.replace("\n", "")
            absulpath = item[:item.rfind(sep)]
            details = item[item.rfind("{"):item.rfind("}")].replace("{", "").replace("}", "")
            filename = item.replace(absulpath, "").replace(sep, "").replace("{" + details + "}", "")

            try:
                # region RIHGT_STRUCTURE
                cd = ctime(float(details[details.rfind("[CD]"):].replace("\n", "").replace("[CD]", "")))
                md = ctime(float(details[details.rfind("[MD]"):details.rfind("[CD]")].replace("[MD]", "")))
                sizeR = float(
                    details[details.rfind("[Size]"):details.rfind(" B")].replace(" B", "").replace("[Size]", ""))
                size = str(sizeR / 1024) + " KB\n" + str(sizeR / 1024 / 1024) + " MB\n" + str(
                    sizeR / 1024 / 1024 / 1024) + " GB"

                toprint = "[Size]\n" + size + "\n\n[Modified Date]\n" + str(md) + "\n\n[Created Date]\n" + str(cd)
                # endregion

                makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                with open(self.dest + absulpath + filename, "w", encoding="utf-8") as file:
                    file.write(toprint)
            except:
                self.problems.append(self.dest + absulpath + filename)
        print("end  : "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))

    # endregion


class MainLinux:
    def __init__(self):
        self.username = getuser()
        self.keep = []
        self.problems = []
        self.counter = 5

    def usb_finder(self):
#region root checker
        if getuid() != 0:
            print("====\nTry to run the script with root user unless it may not work\n====\n")
        else:
            self.username = input("====\nEnter your non-root username > ").lower()
            print("====\n")
# endregion

        chdir("/media/" + self.username + "/")
        self.usb_list = listdir('.')

        self.dest = ""

        if self.usb_list.__len__() == 0:
            print("No USB Connected!!!\n")
            self.timer()
            # system("clear")
            exit()

        favorite = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"

        for usb in self.usb_list:
            chdir("/media/" + self.username + sep + usb)
            if favorite in listdir('.'):
                self.dest = "/media/" + self.username + "/" + usb + sep + favorite + sep
                file = open(self.dest + "Problems.txt", "w", encoding="utf-8")
                file.write("#####No problem found#####")
                file.close()
                self.FUSB = usb
        if self.dest == "":
            print("No F-USB!!!\n")
            self.timer()
            exit()

    def timer(self):
        if self.counter >= 0:
            stdout.write('\r' + str("Exiting in " + str(self.counter)))
            t = threading.Timer(1, self.timer)
            t.start()
            self.counter -= 1

    def drives(self, mode,OS):
        self.home_list = []
        self.drive_list = []

         ## region NOT OS:
        if OS == "no":
            self.drive_list = ["/home", "/mnt"]
            for directory in listdir("/media" + sep + self.username + sep):
                if directory != self.FUSB:
                    self.home_list.append(directory)
        ## endregion

        else:
            if getuid() != 0:
                print("====\nTry to run the script with root user unless it may not work.\n====")

            chdir("/")
            for directory in listdir("."):
                 if isdir(directory) == True:
                    self.drive_list.append(directory)

            x = 0
            while x < len(self.drive_list):
                self.drive_list[x] = "/"+self.drive_list[x]
                x +=1

            if "/media" in self.drive_list :
                self.drive_list.remove("/media")

            for directory in listdir("/media" + sep + self.username + sep):
                if directory != self.FUSB:
                    self.home_list.append(directory)

        # # region AutoMinimize
        # import ctypes
        # ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
        # # endregion

        if mode == "normal":
            for driver in self.drive_list:
                if driver.replace(sep, "") in listdir("/"):
                    self.normal(driver)
            if len(self.home_list) != 0:
                for driver in self.home_list:
                    if driver in listdir("/media" + sep + self.username + sep):
                        self.normal("/media" + sep + self.username + sep + driver)

        if mode == "Unnormal":
            o = open(self.dest + "Log.txt", "w", encoding="utf-8")
            o.close()

            for driver in self.drive_list:
                if driver.replace(sep, "") in listdir("/"):
                    self.logWriter(driver)
            if len(self.home_list) != 0 :
                for driver in self.home_list :
                    if driver in listdir("/media"+sep+self.username+sep):
                        self.logWriter("/media"+sep+self.username+sep+driver)

    def normal(self, driver):
        chdir(driver)
        print("\n" + driver + "...")
        print("start: "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))

        for (dirpath, dirname, filenames) in walk('.'):
            for filename in filenames:
                main_location = sep.join([dirpath, filename])
                absulpathR = path.abspath(main_location)
                absulpath = absulpathR[:absulpathR.rfind(sep)] + sep
                try:
                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)

                    file = open(self.dest + absulpath + filename, "w", encoding="utf-8")
                    file.write("[Size]\n" + str(path.getsize(absulpathR) / 1024) + " KB" + "\n" + str(
                        path.getsize(absulpathR) / 1024 / 1024) + " MB" + "\n" + str(
                        path.getsize(absulpathR) / 1024 / 1024 / 1024) + " GB" +
                               "\n\n[Modified Date]\n" + str(ctime(path.getmtime(absulpathR))) +
                               "\n\n[Created Date]\n" + str(ctime(path.getctime(absulpathR))))
                    file.close()
                except FileNotFoundError:
                    self.problems.append(self.dest + absulpath + filename + "\n")
                except OSError:
                    self.problems.append(self.dest + absulpath+"\n")
        print("end  : "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))

    # region unNormal
    def logWriter(self, driver):
        chdir(driver)
        print("\n" + driver + "...")
        print("start: "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))

        for (dirpath, dirnames, filenames) in walk('.'):
            for filename in filenames:
                absulpathR = path.abspath(sep.join([dirpath, filename]))
                absulpath = absulpathR[:absulpathR.rfind(sep)] + sep

                try:
                    details = "[Size]" + str(path.getsize(absulpathR)) + " B" + "[MD]" + str(
                        path.getmtime(absulpathR)) + "[CD]" + str(path.getctime(absulpathR))

                    self.keep.append(absulpath + filename + "{" + details + "}" + "\n")
                except FileNotFoundError:
                    self.keep.append(str(FileNotFoundError) + absulpath + filename)
                except OSError:
                    self.keep.append(str(OSError) + absulpath + filename)

        file = open(self.dest + "Log.txt", "a", encoding="utf-8")
        for keep in self.keep:
            try:
                file.write(keep)
            except UnicodeEncodeError:
                self.problems.append(str(UnicodeEncodeError) + " for a file in " + keep[:keep.rfind(sep)])
        file.close()

        print("end  : "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))

    def logReader(self):
        print("start: "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))
        try:
            reader = open(self.dest + "Log.txt", "r", encoding="utf-8")
            lister = reader.readlines()
        except FileNotFoundError:
            input("====\nThe [Log.txt] couldn't be found in "+self.dest+"\nCopy it there and re-open the program.\n====")
            self.timer()
            exit()
        # localtime().tm_min)

        for item in lister:
            item = item.replace("\n", "")
            absulpath = item[:item.rfind(sep)]
            details = item[item.rfind("{"):item.rfind("}")].replace("{", "").replace("}", "")
            filename = item.replace(absulpath, "").replace(sep, "").replace("{" + details + "}", "")

            try:
                # region RIHGT_STRUCTURE
                cd = ctime(float(details[details.rfind("[CD]"):].replace("\n", "").replace("[CD]", "")))
                md = ctime(float(details[details.rfind("[MD]"):details.rfind("[CD]")].replace("[MD]", "")))
                sizeR = float(
                    details[details.rfind("[Size]"):details.rfind(" B")].replace(" B", "").replace("[Size]", ""))
                size = str(sizeR / 1024) + " KB\n" + str(sizeR / 1024 / 1024) + " MB\n" + str(
                    sizeR / 1024 / 1024 / 1024) + " GB"

                toprint = "[Size]\n" + size + "\n\n[Modified Date]\n" + str(md) + "\n\n[Created Date]\n" + str(cd)
                # endregion

                makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                with open(self.dest + absulpath + filename, "w", encoding="utf-8") as file:
                    file.write(toprint)
            except:
                self.problems.append(self.dest + absulpath + filename)
        print("end  : "+ str(localtime().tm_min)+":"+str(localtime().tm_sec))

    # endregion


if __name__ == "__main__":
    if syst() == "Windows":
        # region libs
        from os import environ
        from win32api import GetLogicalDrives
        from win32file import GetDriveType, DRIVE_FIXED, DRIVE_REMOVABLE
        #endregion

        M = MainWindows()
        M.usb_finder()
        mode = input(
            "WHAT WOULD YOU LOVE TO DO?\n1)COPY Structure\n2)SAVE structure to Log\n3)LOAD structure from Log\n > ")

        if mode == "1" or mode == "2":
            OS = input("\n====\nDo you want to search OS drive\directories ?(yes\\no)\n >").lower()
            print("====")

        if mode == "1":
            M.drives("normal",OS)
            if len(M.problems) > 0:
                file = open(M.dest + "Problems.txt", "a", encoding="utf-8")
                file.write("Problems found in coping structure: \n\n")
                file.writelines(M.problems)
                file.close()

        elif mode == "2":
            M.drives("Unnormal",OS)
        elif mode == "3":
            M.logReader()
        else:
            print("\nDidn't get it!!! What do you want to do?\nre-run the program if you were sure.")


    if syst() == "Linux":
        # region libs
        from getpass import getuser
        from os import getuid
        #endregion

        M = MainLinux()
        M.usb_finder()
        mode = input(
            "WHAT WOULD YOU LOVE TO DO?\n1)COPY Structure\n2)SAVE structure to Log\n3)LOAD structure from Log\n > ")

        if mode == "1" or mode == "2":
            OS = input("\n====\nDo you want to search OS drive\directories ?(yes\\no)\n >").lower()
            print("====")

        if mode == "1":
            M.drives("normal",OS)
            if len(M.problems) > 0:
                file = open(M.dest + "Problems.txt", "a", encoding="utf-8")
                file.write("Problems found in coping structure: \n\n")
                file.writelines(M.problems)
                file.close()

        elif mode == "2":
            M.drives("Unnormal",OS)
        elif mode == "3":
            M.logReader()
        else:
            print("\nDidn't get it!!! What do you want to do?\nre-run the program if you were sure.")

