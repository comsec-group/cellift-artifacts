import re
import sys

# sys.argv[1]: source Verilog file
# sys.argv[2]: target Verilog file

FIND_REGEX = r"\b(assign\s+\w+\s*= [^&]*&\s*)\{([^\n]+)\};"
MAX_TERMS_IN_BRACKET = 1000 # After processing
TYPE = "logic"
SUFFIX = "inst"
VAR_BASE_NAME = "compress_concat_right"

num_brackets_treated = 0

def reduce_bracket(match):
    global num_brackets_treated

    assignment_start = match.group(1)
    bracket_content = match.group(2)
    splitted = list(map(lambda x: x.strip(), bracket_content.split(',')))
    tot_num_elems = len(splitted)

    var_name = "{}_{}".format(VAR_BASE_NAME, num_brackets_treated)
    var_name_with_suffix = "{}_{}".format(var_name, SUFFIX)

    if tot_num_elems < MAX_TERMS_IN_BRACKET:
        return match.group(0)

    num_macroterms_floor = tot_num_elems // MAX_TERMS_IN_BRACKET
    is_there_remainder = bool(tot_num_elems % MAX_TERMS_IN_BRACKET)

    ret_groups = []

    # Declare the intermediate wires

    ret_groups.append("  {} [{}-1:0] {};".format(TYPE, tot_num_elems, var_name))

    for macroterm_id in range(num_macroterms_floor):
        # If this is the last and there is no remainder
        if macroterm_id == num_macroterms_floor-1 and not is_there_remainder:
            ret_groups.append("  {} [{}-1:0] {}_{};".format(TYPE, MAX_TERMS_IN_BRACKET, var_name_with_suffix, macroterm_id))
            break
        ret_groups.append("  {} [{}-1:0] {}_{};".format(TYPE, MAX_TERMS_IN_BRACKET+1, var_name_with_suffix, macroterm_id))


    if is_there_remainder:
        ret_groups.append("  {} [{}-1:0] {}_{};".format(TYPE, tot_num_elems % MAX_TERMS_IN_BRACKET, var_name_with_suffix, num_macroterms_floor))

    ret_groups.append("  assign {} = {}_0;".format(var_name, var_name_with_suffix))

    for macroterm_id in range(num_macroterms_floor):
        macrobracket_content = ' , '.join(splitted[macroterm_id*MAX_TERMS_IN_BRACKET:(macroterm_id+1)*MAX_TERMS_IN_BRACKET])
        if macroterm_id < num_macroterms_floor-1 or is_there_remainder:
            ret_groups.append("  assign {}_{} = ".format(var_name_with_suffix, macroterm_id) + "{ " + macrobracket_content + ", {}_{}".format(var_name_with_suffix, macroterm_id+1) + " };")
        else:
            ret_groups.append("  assign {}_{} = ".format(var_name_with_suffix, macroterm_id) + "{ " + macrobracket_content + " };")

    if is_there_remainder:
        remaining_terms = splitted[num_macroterms_floor*MAX_TERMS_IN_BRACKET:]
        macrobracket_content = ' , '.join(remaining_terms)
        ret_groups.append("  assign {}_{} = ".format(var_name_with_suffix, num_macroterms_floor) + "{ " + macrobracket_content + " };")

    ret_groups.append("  {}{};".format(assignment_start, var_name))

    num_brackets_treated += 1
    return '\n'.join(ret_groups)

if __name__ == "__main__":
    src_filename = sys.argv[1]
    tgt_filename = sys.argv[2]

    with open(src_filename, "r") as f:
        content = f.read()

    content = re.sub(FIND_REGEX, reduce_bracket, content)

    with open(tgt_filename, "w") as f:
        f.write(content)
