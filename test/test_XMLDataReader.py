import pytest
from typing import Tuple
from Types import DataType
from XMLDataReader import XMLDataReader


class TestTextDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> Tuple[str, DataType]:
        text = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" + \
            "<root>\n" + \
            "<person name=\"Иванов Константин Дмитриевич\">\n" + \
            "<subject name=\"математика\">91</subject>\n" + \
            "<subject name=\"химия\">100</subject>\n" + \
            "</person>\n" + \
            "<person name=\"Петров Петр Семенович\">\n" + \
            "<subject name=\"русский язык\">87</subject>\n" + \
            "<subject name=\"литература\">78</subject>\n" + \
            "</person>\n" + \
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
        p.write_text(file_and_data_content[0], encoding='utf-8')
        return str(p), file_and_data_content[1]

    def test_read(self, filepath_and_data:
                  Tuple[str, DataType]) -> None:
        file_content = XMLDataReader().read(filepath_and_data[0])
        assert file_content == filepath_and_data[1]
