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
