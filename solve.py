import rules
import test_cases

# a dictionary mapping rule functions to strings. used for output
rules_ = {"QED":"QED",
          "Rule 1":"Rule 1",
          rules.RULES[0]:"Rule 2a",
          rules.RULES[1]:"Rule 2b",
          rules.RULES[2]:"Rule 3a",
          rules.RULES[3]:"Rule 3b",
          rules.RULES[4]:"Rule 4a",
          rules.RULES[5]:"Rule 4b",
          rules.RULES[6]:"Rule 5a",
          rules.RULES[7]:"Rule 5b",
          rules.RULES[8]:"Rule 6a",
          rules.RULES[9]:"Rule 6b"}

# a global list of steps(Step) that keeps track of the proof 
steps_ = []

# a global boolean ensuring none of the sequents produces during splits don't hold
valid = True

# a class for representing each step of the proof
class Step:

        def __init__(self, sequent, rule):
            '''
            Constructor
            Parameters:
            sequent(Sequent): the sequent used in the step
            rule(<function>): the rule method applied to the afformentioned sequent
            '''
            self.sequent = sequent
            self.rule = rule
            self.applied_to = []

        def __repr__(self):
            return "{seq}	{rule}".format(seq=self.sequent,rule=rules_[self.rule])

def solve_help(sequent):
    '''
    Method for recursively applying rules to sequents 
    Halts if a sequent holds or doesn't hold and populates 
    the steps_ global list

    Parameters:
    sequent(Sequent): the inputted sequent
    '''
    global steps
    global valid
    if sequent.rule_one_check():
        steps_.append(Step(sequent,"Rule 1"))
        return
    else:
        proceed = False
        for i in range(len(rules.RULES)):
            if proceed == True:
                break
            next_step = rules.RULES[i](sequent)
            if next_step[0]:
                proceed = True
                new_step = Step(sequent, rules.RULES[i])
                steps_.append(new_step)
                for s in next_step[1]:
                    new_step.applied_to.append(s)
                    solve_help(s)
        if not proceed:
            valid = proceed
            return
    return

def solve(sequent):
    '''
    Solves the given sequent and produces beautiful output
    Parameters:
    sequent(Sequent): the inputted sequent
    '''
    solve_help(sequent)
    print("-----------------------------------------------------")
    print("Input: {seq}".format(seq=sequent))
    if not valid:
        print("-----------------------------------------------------")
        print("SEQUENT DOES NOT HOLD")
        print("-----------------------------------------------------")
        return
    print("-----------------------------------------------------")
    line = 0
    lines = []
    sequents = []
    rules_out = []
    applied_to_out = []
    for step in reversed(steps_):
        line += 1	
        step.sequent.line = line
        lines.append(str(line)+". ")
        sequents.append(str(step.sequent))
        rules_out.append(rules_[step.rule])
        if len(step.applied_to) > 0:
            if len(step.applied_to) == 1:
                applied_to_out.append("applied to line " + " and ".join([str(apto.line) for apto in reversed(step.applied_to)]))
            else:
                applied_to_out.append("applied to lines " + " and ".join([str(apto.line) for apto in reversed(step.applied_to)]))
        else:
            applied_to_out.append("")
    output = [lines, sequents, rules_out, applied_to_out]
    transposed = list(map(list, zip(*output)))
    col_widths = [max(len(word) for word in col)+1 for col in output] 
    for row in transposed:
        print("".join(word.ljust(col_widths[i]) for i, word in zip(range(4), row)))
    if valid:
        print("QED")
    print("-----------------------------------------------------")	
    return
