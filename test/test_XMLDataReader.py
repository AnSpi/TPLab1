import pytest
from typing import Tuple
from Types import DataType
from XMLDataReader import XMLDataReader


class TestTextDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> Tuple[str, DataType]:
        text = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>" + \
            "<root>" + \
            "<Иванов_Константин_Дмитриевич>\n" + \
            "<математика>91</математика>\n" + \
            "<химия>100</химия>\n" + \
            "</Иванов_Константин_ Дмитриевич>\n" + \
            "<Петров_Петр_ Семенович>\n" + \
            "<русский язык>87</русский язык>\n" + \
            "<литература>78</литература>\n" + \
            "</Петров_Петр_Семенович>\n" + \
            "</root>"

        data = {
            "Иванов Константин Дмитриевич": [
                ("математика", 91), ("химия", 100)
            ],
            "Петров Петр Семенович": [
                ("русский язык", 87), ("литература", 78)
            ]
        }
        return text, data

    @pytest.fixture()
    def filepath_and_data(self,
                          file_and_data_content: Tuple[str,
                                                       DataType],
                          tmpdir) -> Tuple[str,
                                           DataType]:
        p = tmpdir.mkdir("datadir").join("my_data.txt")
        p.write_text(file_and_data_content[0])
        return str(p), file_and_data_content[1]

    def test_read(self, filepath_and_data:
                  Tuple[str, DataType]) -> None:
        file_content = XMLDataReader().read(filepath_and_data[0])
        assert file_content == filepath_and_data[1]
