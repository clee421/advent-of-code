from typing import List

import os
import shutil
import sys

ERR_CORRECT_DAY_FORMAT = "The correct day format is 01 - 25."

"""
HOW TO USE

1. Create a day
python main.py create <day>

Example:
python main.py create 01

* The day can be 01 to 25 since there are only 25 advent of code days

1. Run code
python main.py run <day> <part> <args>

Example:
python main.py run 01 2 /path/to/input

* The day can be 01 to 25 since there are only 25 advent of code days
* Only 1 or 2 is supported as the part since there are 2 parts to AoC
* args are the other arguments passed into the CLI

"""
def main():
    # 0 - main.py
    # 1 - next argument
    command = sys.argv[1]

    match command:
        case "create":
            day = sys.argv[2]
            create(day)
        case "run":
            day = sys.argv[2]
            part = sys.argv[3]
            run(day, part, sys.argv[4:])
        case _:
            print(f"The command {command} is not supported. Use either create or run")


def validate_day(day: str):
    if type(day) != str:
        raise Exception(ERR_CORRECT_DAY_FORMAT)
    if len(day) != 2:
        raise Exception(ERR_CORRECT_DAY_FORMAT)
    if int(day) < 1 or int(day) > 25:
        raise Exception(ERR_CORRECT_DAY_FORMAT)

def create(day: str):
    validate_day(day)

    if os.path.isdir(f"./day{day}"):
        raise Exception(f"The day already exists, run \"python main.py run {day} 1\"")

    os.makedirs(f"./day{day}")
    shutil.copyfile("./template/run.py", f"./day{day}/run.py")
    shutil.copyfile("./template/input.txt", f"./day{day}/input.txt")
    shutil.copyfile("./template/sample.txt", f"./day{day}/sample.txt")
    shutil.copyfile("./template/__init__.py", f"./day{day}/__init__.py")

def run(day: str, part: str, args: List[str]):
    validate_day(day)
    if part not in ["1", "2"]:
        raise Exception(f"The part {part} is not supported, run \"python main.py run {day} 1\"")

    print(f"Importing run.py from day{day}.run")
    day_run = __import__(f"day{day}.run")

    options = {
        "debug": False,
    }

    if "--debug" in args:
        options["debug"] = True
        args.remove("--debug")

    maybe_input_type = args[0]
    match maybe_input_type:
        case x if isinstance(x, str):
            options["filepath"] = f"./day{day}/{maybe_input_type}.txt"

    match part:
        case "1":
            day_run.part_01(args, options)
        case "2":
            day_run.part_02(args, options)
        case _:
            print("Not sure how we made it here")



if __name__ == "__main__":
    main()