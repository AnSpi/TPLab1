from Types import DataType
from DataReader import DataReader
import xml.etree.ElementTree as ET


class XMLDataReader(DataReader):

    def __init__(self) -> None:
        self.key: str = ""
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        with open(path, encoding='utf-8') as file:
            tree = ET.parse(file)
            root = tree.getroot()
            for elem in root:
                self.key = elem.tag.replace("_"," ")
                self.students[self.key] = []
                for subelem in elem:
                    subj = subelem.tag
                    score = subelem.text
                    self.students[self.key].append(
                        (subj.strip(), int(score.strip())))
        return self.students
