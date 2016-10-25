#flcsv2tree.py

#import csv
from csv import DictReader
import os.path
from json import dump


def ospath_win2pos(ospath):
    if os.path.sep == '\\':
        ospath = ospath.replace('\\', '/')
    return ospath


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def csv_2_tree_path_dicts(file):
    path_ditc = {}
    with open(file) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            nod_path = ospath_win2pos(row['path'])
            row['path'] = nod_path
            path_ditc[nod_path] = row
    return path_ditc


def write_2_jsonfile(pydict, pathfile_name):
    with open(pathfile_name, 'w') as outfile:
        dump(dir_tree, outfile)


def root_str(candidate, test):
    min_idx = min(len(candidate), len(test))
    for i in range(min_idx):
        if candidate[i] != test[i]:
            return candidate[0: i]
    return candidate


def find_root_dir(tree_ditc):
    root_dir_candidate = tree_ditc.keys()[0]
    for test_path in tree_ditc.keys():
        root_dir_candidate = root_str(root_dir_candidate, test_path)
    root_dir_candidate = os.path.dirname(root_dir_candidate)
    return root_dir_candidate


def add_root(tree_ditc, root_path):
    tree_ditc[root_path] = {}
    tree_ditc[root_path]['root'] = True


def calc_children(tree_ditc):
    for each_dir_path, dir_info in tree_ditc.items():
        this_dir = os.path.split(each_dir_path)[-1]
        parent_dir = os.path.dirname(each_dir_path)
        #print '\n', 'this_dir',this_dir, 'parent_dir',parent_dir, 'each_dir_path',each_dir_path
        #print dir_info.keys()
        if parent_dir and not ('root' in dir_info.keys()):
            if 'children' in tree_ditc[parent_dir]:
                tree_ditc[parent_dir]['children'].append(this_dir)
            else:
                tree_ditc[parent_dir]['children'] = [this_dir]


def calc_root_totlas(tree_ditc, root_path):
    # TODO ??
    root_dir = root_path
    for child in tree_ditc[root_dir]['children']:
        child_key = root_dir + '/' + child
        for key in tree_ditc[child_key].keys():
            #print tree_ditc[child_key][key]
            if not isinstance(tree_ditc[child_key][key], list):  # not list
                if RepresentsInt(tree_ditc[child_key][key]):
                    #print key, int(tree_ditc[child_key][key])
                    col_value = int(tree_ditc[child_key][key])
                    if key in tree_ditc[root_dir]:
                        tree_ditc[root_dir][key] += col_value
                    else:
                        tree_ditc[root_dir][key] = col_value


def working_node_total(working_node, fl_type):
    total = 0
    # setup typ_suf as fun(fl_type)
    typ_suf = ''
    if '_' in fl_type:
        l = fl_type.split("_")
        typ_suf = "_"+l[-1]
    # calc total as fun(working_node, typ_suf)
    node = working_node['node']
    for key in node.keys():
        if not isinstance(node[key], list):  # not list
            if RepresentsInt(node[key]):  # only str represent ins
                if typ_suf == '':
                    if not ('_' in key):
                        total += int(node[key])
                else:
                    if typ_suf in key:
                        total += int(node[key])
    return total


def build_dir_tree(tree_ditc, working_node, fl_type, level, max_level):
    # TODO total, max_level
    build = {}
    level += 1
    name = working_node['name']
    build["name"] = name
    if 'children' in working_node['node'].keys() and level <= max_level:
        children = working_node['node']['children']
        build["children"] = []
        for child in children:
            #print 'name', name, 'child', child, 'level', level
            path_key = name + '/' + child 
            next_working_node = {'name': path_key, 'node': tree_ditc[path_key]}
            build["children"].append(
                build_dir_tree(tree_ditc, next_working_node, fl_type, level, max_level))
    else:
        if 'total' in fl_type:
            build["size"] = working_node_total(working_node, fl_type)
        else:
            build["size"] = working_node['node'][fl_type]
    level -= 1
    return build


#######################
print 'Start convert csv to flare json'
# lode data from csv file
tree_ditc = csv_2_tree_path_dicts('FSHistory_Dojo.csv')  # FSHistory_Dojo
# calculate commoun base path
root_path = find_root_dir(tree_ditc)
# add a root node
add_root(tree_ditc, root_path)
# calculate list of children for each node and add to each
calc_children(tree_ditc)
# calculate values totals for root by summing up child values
calc_root_totlas(tree_ditc, root_path)

# build d3 treemap comparable data structured
# stare with root node
working_node = {'name': root_path, 'node': tree_ditc[root_path]}
level = 0
dir_tree = build_dir_tree(tree_ditc, working_node, 'total', level, 4)

# out put dir_tree as json file


write_2_jsonfile(dir_tree, 'flare_data.json')
print 'Done convert csv to flare json'

'''
TODO:
    git
    oo 1
    unittest 1
    maim > convert_csv_2_flare(csv_in, json_out, root_path = null) 1.5
    readme.md 1.5
    github as website index.html... 2
    leve 3 shows ???
'''

