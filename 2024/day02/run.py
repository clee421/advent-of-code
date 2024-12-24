from typing import Dict, List

def parse_lines_reports(filepath: str) ->List[List[int]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    reports = []
    for line in lines:
        report = list(map(lambda x: int(x),line.split(" ")))
        reports.append(report)

    return reports

def is_safe(report: List[int]) -> bool:
    increasing = report[0] < report[1]
    for i in range(1, len(report)):
        if (report[i-1] < report[i]) != increasing:
            return False

        diff = abs(report[i-1] - report[i])
        if diff < 1 or diff > 3:
            return False

    return True

def is_safe_with_dampener(report: List[int]) -> bool:
    for i in range(len(report)):
        copied = report.copy()
        del copied[i]
        if is_safe(copied):
            return True

    return False

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    reports = parse_lines_reports(options.get("filepath", args[0]))

    safe_count = 0
    for report in reports:
        if is_safe(report):
            safe_count += 1

    print("Safe reports:", safe_count)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    reports = parse_lines_reports(options.get("filepath", args[0]))

    safe_count = 0
    for report in reports:
        if is_safe_with_dampener(report):
            safe_count += 1

    print("Safe reports:", safe_count)