[![Build Status](https://app.travis-ci.com/AnSpi/TPLab1.svg?branch=main)](https://app.travis-ci.com/AnSpi/TPLab1)
# Лабораторная 1 по дисциплине "Технологии программирования"
Знакомство с системой контроля версий Git и инструментом CI/CD Travis CI
## Цели работы
1. Познакомиться c распределенной системой контроля версий кода Git и ее функциями;
2. Познакомиться с понятиями «непрерывная интеграция» (CI) и «непрерывное развертывание»
(CD), определить их место в современной разработке программного обеспечения;
3. Получить навыки разработки ООП-программ и написания модульных тестов к ним на
современных языках программирования;
4. Получить навыки работы с системой Git для хранения и управления версиями ПО;
5. Получить навыки управления автоматизированным тестированием программного обеспечения,
расположенного в системе Git, с помощью инструмента Travis CI.
# Ход работы
## Для выполнения индивидуального задания согласно 10 варианту создадим файл формата XML, класс XMLDataReader как наследник класса DataReader, тест этого класса и изменим файл main для работы с новым класом. Для этого откроем ветку XMLReader проекта.
### Представленный в файле src/XMLDataReader.py класс реализует чтение данных из  файлов формата .xml
```python
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
```
### Тестирование класса XMLDataReader осуществляется с помощью класса, реализованного в файле test/test_XMLDataReader.py:
```python
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

```
### main.py:
```python
# from TextDataReader import TextDataReader
from XMLDataReader import XMLDataReader
from CalcRating import CalcRating
import argparse
import sys


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main():
    path = get_path_from_arguments(sys.argv[1:])
    reader = XMLDataReader()
    students = reader.read(path)
    print("Students: ", students)
    rating = CalcRating(students).calc()
    print("Rating: ", rating)


if __name__ == "__main__":
    main()
```
###Добавим в проект класс StudentsInDebt, реализующий расчет и вывод на экран количество студентов, имеющих академические задолженности (имеющих балл < 61) ровно по двум предметам.
```python
from Types import DataType


class StudentsInDebt:
    def __init__(self, data: DataType) -> None:
        self.data: DataType = data
        self.doubtCount = 0
        self.count = 0

    def calc(self) -> int:
        for key in self.data:
            self.doubtCount = 0
            for subject in self.data[key]:
                if subject[1] < 61:
                    self.doubtCount += 1
            if self.doubtCount == 2:
                self.count += 1
        return self.count

```
### Тестирование класса StudentsInDebt осуществляется с помощью класса, реализованного в файле test/test_StudentsInDebt.py:
```python
from typing import Tuple
from Types import DataType
from StudentsInDebt import StudentsInDebt
import pytest


class TestStudentsInDebt():
    @pytest.fixture()
    def input_data(self) -> Tuple[DataType, int]:
        data: DataType = {
            "Абрамов Петр Сергеевич":
            [
                ("математика", 80),
                ("русский язык", 76),
                ("программирование", 100)
            ],
            "Петров Игорь Владимирович":
            [
                ("математика", 50),
                ("русский язык", 40),
                ("программирование", 78),
                ("литература", 97)
            ]
        }

        students_with_two_debt = 1

        return data, students_with_two_debt

    def test_init_calc_debt(self, input_data:
                            Tuple[DataType, int]) -> None:

        calc_debt = StudentsInDebt(input_data[0])
        assert input_data[0] == calc_debt.data

    def test_calc(self, input_data:
                  Tuple[DataType, int]) -> None:
        count = StudentsInDebt(input_data[0]).calc()
        assert count == input_data[1]
```
### main.py:
```python
# from TextDataReader import TextDataReader
from XMLDataReader import XMLDataReader
from CalcRating import CalcRating
from StudentsInDebt import StudentsInDebt
import argparse
import sys


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main():
    path = get_path_from_arguments(sys.argv[1:])
    reader = XMLDataReader()
    students = reader.read(path)
    print("Students: ", students)
    rating = CalcRating(students).calc()
    print("Rating: ", rating)
    death_list = StudentsInDebt(students).calc()
    print("Students with 2 debts:", death_list)


if __name__ == "__main__":
    main()

```
### Работа кода ветки XMLReader
![program_result](/images/program_result.png)
### Проверка кода прошла успешно
![test](/images/test_result.png)
### Структура файлов проекта
![structure](/images/structure.png)
### UML-диаграмма
![UML-diagram](/images/UMLdiagram.png)
### Пакеты:
- pytest - тестирование
- mypy - корректность работы с типами
- pycodestyle - соответствие кода стандарту РЕР-8
- XMLDataReader - модуль для работы с xml

# Выводы
1. Закреплено представление о распределенной системе контроля версий кода Git и ее функциях;
2. Закреплены понятия «непрерывная интеграция» (CI) и «непрерывное развертывание»
(CD), определено их место в современной разработке программного обеспечения;
3. Получены навыки разработки ООП-программ и написания модульных тестов к ним на
современных языках программирования;
4. Получены навыки работы с системой Git для хранения и управления версиями ПО;
5. Получены навыки управления автоматизированным тестированием программного обеспечения, расположенного в системе Git, с помощью инструмента Travis CI.