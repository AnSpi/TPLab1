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
