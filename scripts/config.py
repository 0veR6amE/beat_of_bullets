import configparser
from os import path

from pygame.locals import *

from scripts import CONST


class Config:
    def __init__(self):
        self.writer = configparser.ConfigParser()
        if path.exists(CONST.currentDirectory + "/BoBConf.ini"):
            self.writer.read(CONST.currentDirectory + "/BoBConf.ini")
            self.config = self.writer["BoB Config"]
        else:
            self.writer["BoB Config"] = {}
            self.config = self.writer["BoB Config"]
            self.config["volume"] = "float://" + str(1)
            self.config["blue1"] = "int://" + str(K_d)
            self.config["blue2"] = "int://" + str(str(K_f))
            self.config["red1"] = "int://" + str(str(K_j))
            self.config["red2"] = "int://" + str(str(K_k))
            self.Save()

    def getValue(self, key: str):
        try:
            value = self.config[key]
            type, value = value.split("://")
            if type == "float":
                return float(value)
            if type == "int":
                return int(value)
            if type == "str":
                return str(value)
            else:
                return value
        except:
            CONST.Logger.error("Tried to read nonexistent value ({}) "
                               "in BoBConf.ini".format(key))
            return

    def setValue(self, key, value, type):
        if type == "float":
            ftype = float
        if type == "str":
            ftype = str
        if type == "int":
            ftype = int
        else:
            ftype = str
        self.config[key] = type + "://" + ftype(value)
        self.Save()

    def __getitem__(self, item):
        return self.getValue(item)

    def Save(self):
        with open(CONST.currentDirectory + "/BoBConf.ini", "w") as f:
            self.writer.write(f)
