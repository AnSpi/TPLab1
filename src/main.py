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
