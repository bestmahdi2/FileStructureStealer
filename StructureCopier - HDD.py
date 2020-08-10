import datetime
import threading
from math import floor
from os.path import isdir
from platform import system as syst
from os import chdir, makedirs, walk, sep, path, listdir
from sys import stdout,exit
from time import ctime, localtime


class MainWindows:
    def __init__(self):
        self.keep = []
        self.problems = []
        self.counter = 5
        self.log = "Log - " + str(datetime.date.today()) + ".txt"

    def opendir(self):
        file_path = ""
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_path = filedialog.askdirectory(initialdir=".", title="Select Directory")
        return file_path.replace("/",sep).replace("\\",sep)

    def timer(self):
        if self.counter >= 0:
            stdout.write('\r' + str("Exiting in " + str(self.counter)))
            t = threading.Timer(1, self.timer)
            t.start()
            self.counter -= 1

    def drives(self, mode):
            input("Click [Enter] to choose the directory you want to be copied...")
            driver = self.opendir() + sep
            print("=======\nSource Directory : " + "\"" + driver + "\"" + "\n=======\n")

            input("Click [Enter] to choose the directory you want to save files or log...")
            self.dest = self.opendir() + sep
            print("=======\nDestination Directory : " + "\"" + self.dest + "\"" + "\n=======\n")

            # # region AutoMinimize
            # import ctypes
            # ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
            # # endregion

            if mode == "normal":
                self.normal(driver)
            if mode == "Unnormal":
                o = open(self.dest + self.log, "w", encoding="utf-8")
                o.close()
                self.logWriter(driver)

    def normal(self, driver):
        chdir(driver)
        print("\n" + driver + "...")
        print("start: "+ str(localtime().tm_min)+"\':"+str(localtime().tm_sec)+"\"")

        for (dirpath, dirname, filenames) in walk('.'):
            for filename in filenames:
                main_location = sep.join([dirpath, filename])
                absulpathR = path.abspath(main_location)
                absulpath = absulpathR.replace(":", "")[:absulpathR.rfind(sep)] + sep
                try:
                    makedirs(path.dirname(self.dest + absulpath), exist_ok=True)

                    file = open(self.dest + absulpath + filename, "w", encoding="utf-8")
                    sizeR = path.getsize(absulpathR)

                    if floor(sizeR / 1024 / 1024 / 1024) != 0:
                        size = str(round(sizeR / 1024 / 1024 / 1024, 2)) + " GB"
                    else:
                        if floor(sizeR / 1024 / 1024) != 0:
                            size = str(round(sizeR / 1024 / 1024, 1)) + " MB"
                        else:
                            size = str(round(sizeR / 1024)) + " KB"

                    file.write("[Size]\n" + size +
                               "\n\n[Modified Date]\n" + str(ctime(path.getmtime(absulpathR))) +
                               "\n\n[Created Date]\n" + str(ctime(path.getctime(absulpathR))))
                    file.close()
                except FileNotFoundError:
                    self.problems.append(self.dest + absulpath + filename + "\n")
        print("end  : "+ str(localtime().tm_min)+"\':"+str(localtime().tm_sec)+"\"")

    # region unNormal
    def logWriter(self, driver):
        chdir(driver)
        print("\n" + driver + "...")
        timeS = str(localtime().tm_min)+"\':"+str(localtime().tm_sec)+"\""
        print("start: "+ timeS)

        self.file_count = 0
        for (dirpath, dirnames, filenames) in walk('.'):
            for filename in filenames:
                self.file_count += 1
                absulpathR = path.abspath(sep.join([dirpath, filename]))
                absulpath = absulpathR.replace(":", "")[:absulpathR.rfind(sep)] + sep

                try:
                    details = "[S]" + str(path.getsize(absulpathR)) + " B" + "[MD]" + str(
                        path.getmtime(absulpathR)) + "[CD]" + str(path.getctime(absulpathR))

                    self.keep.append(absulpath + filename + "{" + details + "}" + "\n")
                except FileNotFoundError:
                    self.keep.append(str(FileNotFoundError) + absulpath + filename)
                except OSError:
                    self.keep.append(str(OSError) + absulpath + filename)

        file = open(self.dest + self.log, "a", encoding="utf-8")
        for keep in self.keep:
            try:
                file.write(keep)
            except UnicodeEncodeError:
                self.problems.append(str(UnicodeEncodeError) + " for a file in " + keep[:keep.rfind(sep)])

        timeE = str(localtime().tm_min)+"\':"+str(localtime().tm_sec)+"\""
        print("end  : "+ timeE)

        toprint = ("\n===============\n" +
                        "[Source] > " + driver + "\n" +
                        "[Destination] > "  + self.dest + "\n" +
                        "[Date] > " + str(datetime.date.today()) + "\n" +
                        "[Start] > "+ timeS + "\n" +
                        "[End] > " + timeE + "\n" +
                        "[Files] > " + str(self.file_count) +
                         "\n===============")

        file.write(toprint)
        file.close()

    def openfile(self):
        file_path = ""
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(initialdir=".", title="Select file",filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        self.address = file_path.replace("/",sep).replace("\\",sep)
        return file_path

    def logReader(self):
        try:
            reader = open("."+ sep + self.log, "r", encoding="utf-8")
            lister = reader.readlines()
        except FileNotFoundError:
        # region ask open file
            input("\nThe [Log.txt] couldn't be found in this directory "+ "\nClick [Enter] to select the file manually.\n")
            if self.openfile() == "":
                input("You didn't choose a file, select again[Enter]\n")
                if self.openfile() == "":
                    print("Time out!!!")
                    self.timer()
                    exit()
                else:
                    reader = open(self.address, "r", encoding="utf-8")
                    lister = reader.readlines()
            else:
                reader = open(self.address, "r", encoding="utf-8")
                lister = reader.readlines()

            print("====\n")
           # endregion


        input("Click [Enter] to choose the directory you want to extract files...")
        self.dest = self.opendir() + sep
        print("=======\nDestination Directory : " + "\"" + self.dest + "\"" + "\n=======\n")


        print("start: "+ str(localtime().tm_min)+"\':"+str(localtime().tm_sec)+"\"")

        # Remove the info
        for item in lister:
            if "===============" in item:
                lister.remove(lister[lister.index(item)])
            if "[Source]" in item :
                lister.remove(lister[lister.index(item)])
            if "[Destination]" in item :
                lister.remove(lister[lister.index(item)])
            if "[Date]" in item :
                lister.remove(lister[lister.index(item)])
            if "[Start]" in item :
                lister.remove(lister[lister.index(item)])
            if "[End]" in item :
                lister.remove(lister[lister.index(item)])
            if "[Files]" in item :
                lister.remove(lister[lister.index(item)])

        for item in lister:
            item = item.replace("\n", "")
            absulpath = item[:item.rfind(sep)]
            details = item[item.rfind("{"):item.rfind("}")].replace("{", "").replace("}", "")
            filename = item.replace(absulpath, "").replace(sep, "").replace("{" + details + "}", "")

            try:
                # region RIHGT_STRUCTURE
                cd = ctime(float(details[details.rfind("[CD]"):].replace("\n", "").replace("[CD]", "")))
                md = ctime(float(details[details.rfind("[MD]"):details.rfind("[CD]")].replace("[MD]", "")))
                sizeR = float(details[details.rfind("[S]"):details.rfind(" B")].replace(" B", "").replace("[S]", ""))

                if floor(sizeR / 1024 / 1024 / 1024) != 0:
                    size = str(round(sizeR / 1024 / 1024 / 1024, 2)) + " GB"
                else:
                    if floor(sizeR / 1024 / 1024) != 0:
                        size = str(round(sizeR / 1024 / 1024, 1)) + " MB"
                    else:
                        size = str(round(sizeR / 1024)) + " KB"

                toprint = "[Size]\n" + size + "\n\n[Modified Date]\n" + str(md) + "\n\n[Created Date]\n" + str(cd)
                # endregion

                makedirs(path.dirname(self.dest + absulpath), exist_ok=True)
                with open(self.dest + absulpath + filename, "w", encoding="utf-8") as file:
                    file.write(toprint)
            except:
                self.problems.append(self.dest + absulpath + filename)
        print("end  : "+ str(localtime().tm_min)+"\':"+str(localtime().tm_sec)+"\"")

    # endregion




if __name__ == "__main__":
    def rerun():
        answer = input("\nWould you like to continue?(yes/no)\n > ")
        if answer == "yes":
            main()
        else:
            print("Ok , Bye !!! ...")

    def main():
        if syst() == "Windows":

            M = MainWindows()
            mode = input(
                "\n WHAT WOULD YOU LOVE TO DO?\n\t1)COPY Structure\n\t2)SAVE structure to Log\n\t3)LOAD structure from Log\n\t =>  ")
            print("\n")

            if mode == "1":
                M.drives("normal")
                if len(M.problems) > 0:
                    file = open(M.dest + "Problems.txt", "w", encoding="utf-8")
                    file.write("Problems found in coping structure: \n\n")
                    file.writelines(M.problems)
                    file.close()
                input("\n=======Done=======\n")
                rerun()
            elif mode == "2":
                M.drives("Unnormal")
                input("\n=======Done=======\n")
                rerun()
            elif mode == "3":
                # M.drives("load")
                M.logReader()
                input("\n=======Done=======\n")
                rerun()
            else:
                print("\nDidn't get it!!! What do you want to do?\nre-run the program if you were sure.")

    main()
