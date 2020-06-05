from platform import system as syst
from os import chdir, makedirs, walk, sep, path, listdir
from time import ctime, sleep, localtime

class MainWindows:
    def __init__(self):
        self.keep = []
        self.problems = []

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
            print("No USB Connected!!!")
            sleep(4)
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
            print("No F-USB!!!")
            sleep(4)
            exit()

    def drives(self, mode):
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

        # region OS
        for i in self.drive_list:
            if i == win:
                self.drive_list.remove(i)
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
        print("I'm in " + driver + " ...")
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

    # region unNormal
    def logWriter(self, driver):
        chdir(driver)
        print("I'm in " + driver + " ...")

        print(str(localtime().tm_min))
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

        print(str(localtime().tm_min))

    def logReader(self):
        reader = open(self.dest + "Log.txt", "r", encoding="utf-8")
        lister = reader.readlines()

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
        # print(str(localtime().tm_min))

    # endregion



class MainLinux:
    def __init__(self):
        self.username = getuser()
        self.keep = []
        self.problems = []

    def usb_finder(self):
        if getuid() != 0:
            print("Try to run the script with root user unless may not work")
            # sleep(4)
            # exit()
        else:
            self.username = input("enter your non-root username: ").lower()


        self.dest = ""
        chdir("/media/" + self.username + "/")
        self.usb_list = listdir('.')

        if self.usb_list.__len__() == 0:
            print("No USB Connected!!!")
            sleep(4)
            exit()

        favorite = ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}"

        for usb in self.usb_list:
            chdir(usb)
            if favorite in listdir('.'):
                self.dest = "/media/" + self.username + "/" + usb + sep + favorite + sep
                file = open(self.dest + "Problems.txt", "w", encoding="utf-8")
                file.write("#####No problem found#####")
                file.close()
                self.FUSB = usb
        if self.dest == "":
            print("No F-USB!!!")
            sleep(4)
            exit()

    def drives(self, mode):
        self.home_list = []
        self.drive_list = ["/home", "/mnt"]
        for directory in listdir("/media"+sep+self.username+sep):
            if directory != self.FUSB :
                self.home_list.append(directory)

        # # region AutoMinimize
        # import ctypes
        # ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
        # # endregion

        if mode == "normal":
            for driver in self.drive_list:
                self.normal(driver)
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
        print("I'm in " + driver + " ...")
        for (dirpath, dirname, filenames) in walk('.'):
            for filename in filenames:
                main_location = sep.join([dirpath, filename])
                absulpathR = path.abspath(main_location)
                absulpath = absulpathR[:absulpathR.rfind(sep)] + sep
                try:
                    # junks = ["@",":","{","}","!","="]
                    # for junk in junks:
                    #     filename = filename.replace(junk,"")
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

    # region unNormal
    def logWriter(self, driver):
        chdir(driver)
        print("I'm in " + driver + " ...")

        print(str(localtime().tm_min))
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

        print(str(localtime().tm_min))

    def logReader(self):
        reader = open(self.dest + "Log.txt", "r", encoding="utf-8")
        lister = reader.readlines()

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
        # print(str(localtime().tm_min))

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

        if mode == "1":
            M.drives("normal")
            if len(M.problems) > 0:
                file = open(M.dest + "Problems.txt", "w", encoding="utf-8")
                file.write("Problems found in coping structure: \n\n")
                file.writelines(M.problems)
                file.close()

        elif mode == "2":
            M.drives("Unnormal")
        elif mode == "3":
            M.logReader()
        else:
            print("Didn't get it!!! What do you want to do?\nre-run the program if you were sure.")


    if syst() == "Linux":
        # region libs
        from getpass import getuser
        from os import getuid
        #endregion

        M = MainLinux()
        M.usb_finder()
        mode = input("WHAT WOULD YOU LOVE TO DO?\n1)COPY Structure\n2)SAVE structure to Log\n3)LOAD structure from Log\n > ")

        if mode == "1":
            M.drives("normal")
            if len(M.problems) > 0:
                file = open(M.dest + "Problems.txt", "w", encoding="utf-8")
                file.write("Problems found in coping structure: \n\n")
                file.writelines(M.problems)
                file.close()

        elif mode == "2":
            M.drives("Unnormal")
        elif mode == "3":
            M.logReader()
        else:
            print("Didn't get it!!! What do you want to do?\nre-run the program if you were sure.")

