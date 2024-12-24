from typing import Dict, List, Tuple

class Rules:
    def __init__(self):
        self.rules = {}

    def add(self, rule: str):
        parts = rule.split("|")
        prev, next = int(parts[0]), int(parts[1])
        rule = self.rules.get(prev, [])

        rule.append(next)
        self.rules[prev] = rule

    def valid_page(self, page: List[int]) -> bool:
        # print("Rules:", self.rules)
        seen = []
        for p in page:
            intersect = [s for s in seen if s in self.rules.get(p, [])]
            # print("intersect", intersect)
            if len(intersect) > 0:
                # print("Found intersection:", seen, intersect, p)
                return False

            seen.append(p)

        return True

    def fix_page(self, page: List[int]) -> List[int]:
        # print("Rules:", self.rules)
        new_page = []
        for p in page:
            intersect = [s for s in new_page if s in self.rules.get(p, [])]
            # print("intersect", intersect)
            if len(intersect) > 0:
                # print("Found intersection:", seen, intersect, p)
                index = new_page.index(intersect[0])
                new_page.insert(index, p)
            else:
                new_page.append(p)

        return new_page

def parse_lines_rules_pages(filepath: str) -> Tuple[Rules, List[List[int]]]:
    with open(filepath) as file:
        lines = [line.rstrip() for line in file]

    rules = Rules()
    pages = []

    part_2_parse = False
    for line in lines:
        if line == "":
            part_2_parse = True
            continue

        if not part_2_parse:
            rules.add(line)
        else:
            page = list(map(lambda x: int(x),line.split(",")))
            pages.append(page)

    return (rules, pages)

def part_01(args: List[str], options: Dict[str, any]):
    print("Running part 01", args, options)
    rules, pages = parse_lines_rules_pages(options.get("filepath", args[0]))

    total = 0
    for page in pages:
        if rules.valid_page(page):
            mid = int(len(page) / 2)
            total += page[mid]
            # print(page, page[mid])

    print("Total:", total)

def part_02(args: List[str], options: Dict[str, any]):
    print("Running part 02", args, options)
    rules, pages = parse_lines_rules_pages(options.get("filepath", args[0]))

    total = 0
    for page in pages:
        if not rules.valid_page(page):
            new_page = rules.fix_page(page)
            mid = int(len(new_page) / 2)
            total += new_page[mid]
            # print(new_page, new_page[mid])

    print("Total:", total)