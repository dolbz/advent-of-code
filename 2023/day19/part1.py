class Workflow:
    def __init__(self, conditions, default_workflow):
        self.conditions = conditions
        self.default_workflow = default_workflow

    def evaluateForRatedPart(self, part_rating):
        for condition in self.conditions:
            result = condition.evaluateForRatedPart(part_rating)
            if result != "":
                return result

        return self.default_workflow


class ConditionEvaluator:
    def __init__(self, condition_str):
        condition, true_workflow = condition_str.split(":")

        self.true_workflow = true_workflow

        if len(condition.split("<")) == 2:
            self.less_than = True
            self.target_category, self.condition_value = condition.split("<")
        else:
            self.less_than = False
            self.target_category, self.condition_value = condition.split(">")

        self.condition_value = int(self.condition_value)

    def evaluateForRatedPart(self, part_rating):
        category_rating = part_rating[self.target_category]

        if self.less_than:
            if category_rating < self.condition_value:
                return self.true_workflow
        else:
            if category_rating > self.condition_value:
                return self.true_workflow

        return ""


def parse_workflows(workflow_lines):
    workflows = dict()

    for line in workflow_lines:
        workflow_name, conditions = line[:-1].split("{")

        conditions = conditions.split(",")
        default_workflow = conditions[-1]
        conditions = conditions[:-1]

        parsed_conditions = []
        for condition in conditions:
            parsed_conditions.append(ConditionEvaluator(condition))

        workflows[workflow_name] = Workflow(parsed_conditions, default_workflow)

    return workflows


def parse_part_ratings(part_rating_lines):
    part_ratings = []

    for line in part_rating_lines:
        category_ratings = line[1:-1].split(",")

        part_rating = dict()
        for rating in category_ratings:
            category, value = rating.split("=")
            part_rating[category] = int(value)

        part_ratings.append(part_rating)

    return part_ratings


def parseInput():
    file = open("input.txt", "r")
    lines = file.read().splitlines()

    workflow_lines = []
    part_rating_lines = []
    blank_line_passed = False

    for line in lines:
        if line == "":
            blank_line_passed = True
            continue

        if blank_line_passed:
            part_rating_lines.append(line)
        else:
            workflow_lines.append(line)

    workflows = parse_workflows(workflow_lines)
    part_ratings = parse_part_ratings(part_rating_lines)

    return (workflows, part_ratings)


workflows, part_ratings = parseInput()

accepted = []

for part_rating in part_ratings:
    next_workflow = "in"
    while next_workflow != "A" and next_workflow != "R":
        next_workflow = workflows[next_workflow].evaluateForRatedPart(part_rating)

    if next_workflow == "A":
        accepted.append(part_rating)

print(sum([sum(x.values()) for x in accepted]))
