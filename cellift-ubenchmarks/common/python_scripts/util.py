import json
import os

SUPPORTED_IFT_FLAVORS = ["cellift", "cellift_p", "rtlift"]
DEFAULT_WIDTH_BOUNDS = [1, 64, 3] # Min, max, step.

# Auxiliary function, do not use externally
# @return the sub-dict corresponding to the given cellify type.
# @param cell_abspath: example: something/cellift-ubenchmarks/add
def get_json_content(cell_abspath):
    # Get the current type from the parameter
    curr_cell_type = os.path.basename(cell_abspath)
    # Read targets.json
    with open("../../targets.json", "r") as f:
        targets_content = json.load(f)
    # Get the list of IFT flavors from the target
    if not curr_cell_type in targets_content:
        raise ValueError("Cell type not found in targets.json: {} (basename of path {}).".format(curr_cell_type, cell_abspath))
    return targets_content[curr_cell_type]


# @param cell_abspath: example: something/cellift-ubenchmarks/add
def get_ift_flavors(cell_abspath):
    subdict = get_json_content(cell_abspath)
    ret_list = list(subdict.keys())
    # Ensure the list is valid, and then return
    if not ret_list:
        raise ValueError("IFT flavor list is empty for cell type {}.".format(curr_cell_type))
    for elem in ret_list:
        if elem not in SUPPORTED_IFT_FLAVORS:
            raise ValueError("IFT flavor not supported: {}".format(elem))
    return ret_list 

# @param cell_abspath: example: something/cellift-ubenchmarks/add
# @param ift_flavor: example: cellift
# @return a list [min, max, step]
def get_data_widths(cell_abspath, ift_flavor):
    subdict = get_json_content(cell_abspath)
    if not ift_flavor in subdict:
        raise ValueError("No data width bounds for {} for {}".format(ift_flavor, cell_abspath))
        # return DEFAULT_WIDTH_BOUNDS
    return list(range(*subdict[ift_flavor])) 
