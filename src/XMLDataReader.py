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
                self.key = str(elem.get('name'))
                self.students[self.key] = []
                for subelem in elem:
                    subj = subelem.get('name')
                    score = subelem.text
                    self.students[self.key].append(
                        (subj.strip() if subj is not None else "",
                         int(score.strip() if score is not None else "")))
        return self.students
