"""
Convert Storagetats csv output to D3 Tree Map graphics flare.json format
StorageStats: Convert FileSystem Storage Statistics csv output to
a hierarchically embedded treee format used by mbostocks D3 treemap
referred to as flare.json see:
http://mbostock.github.io/d3/talk/20111018/treemap.html

python 2.7
Created on Oct 26, 2016
@author: jayventi
convert_csv_2_flare.py
"""

from csv import DictReader
import os.path
from json import dump


class ConvertCsv2Flare(object):
    """
    Package for convert_csv_2_flare utility
    ConvertCsv2Flare.main orchestrates main execution
    """

    def __init__(self):
        self.def_verbosity = 3
        self.def_json_out = 'flare_data.json'
        self.def_fl_type = 'total'

    def ospath_win2pos(self, ospath):
        if os.path.sep == '\\':
            ospath = ospath.replace('\\', '/')
        return ospath

    def RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def csv_2_tree_path_dicts(self, file):
        """
        opens storgstats csv file and setsup in path_dicts format
        opens csv output file from storgstats.py converge to a dictionary
        with the key is row['path'] and the value is row
        """
        path_ditc = {}
        with open(file) as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                nod_path = self.ospath_win2pos(row['path'])
                row['path'] = nod_path
                path_ditc[nod_path] = row
        return path_ditc

    def write_2_jsonfile(self, pydict, pathfile_name):
        with open(pathfile_name, 'w') as outfile:
            dump(pydict, outfile)

    def root_str(self, candidate, test):
        """
        finds shortest common prefix string
        """
        min_idx = min(len(candidate), len(test))
        for i in range(min_idx):
            if candidate[i] != test[i]:
                return candidate[0: i]
        return candidate

    def find_root_dir(self, tree_ditc):
        """
        finds common base path to all listed full paths
        finds shortest common prefix string which will
        be equivalent to root / base path
        """
        root_dir_candidate = tree_ditc.keys()[0]
        for test_path in tree_ditc.keys():
            root_dir_candidate = self.root_str(root_dir_candidate, test_path)
        root_dir_candidate = os.path.dirname(root_dir_candidate)
        return root_dir_candidate

    def add_root(self, tree_ditc, root_path):
        """
        ads a empty root directory, totals added later
        Storagetats does not output the root directory this routine remedies
        """
        tree_ditc[root_path] = {}
        tree_ditc[root_path]['root'] = True

    def calc_children(self, tree_ditc):
        """
        calculates list of sub directories for each and addeds
        """
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

    def calc_root_totlas(self, tree_ditc, root_path):
        """
        calculates totals for root directory
        only needs to sum up from immediate children since they
        contain all of their subtotals down to the leafs
        """
        # TODO ??
        root_dir = root_path
        for child in tree_ditc[root_dir]['children']:
            child_key = root_dir + '/' + child
            for key in tree_ditc[child_key].keys():
                #print tree_ditc[child_key][key]
                if not isinstance(tree_ditc[child_key][key], list):  # not list
                    if self.RepresentsInt(tree_ditc[child_key][key]):
                        #print key, int(tree_ditc[child_key][key])
                        col_value = int(tree_ditc[child_key][key])
                        if key in tree_ditc[root_dir]:
                            tree_ditc[root_dir][key] += col_value
                        else:
                            tree_ditc[root_dir][key] = col_value

    def working_node_total(self, working_node, fl_type):
        """
        calculates total directory file size or file count
        if '_' appears in fl_type total '_Cn' values
        otherwise total file size types
        """
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
                if self.RepresentsInt(node[key]):  # only str represent ins
                    if typ_suf == '':
                        if not ('_' in key):
                            total += int(node[key])
                    else:
                        if typ_suf in key:
                            total += int(node[key])
        return total

    def build_dir_tree(self, tree_ditc, working_node, fl_type, level, max_level):
        """
        Main algorithm for converting data structure to flare.json format
        recursively parses row-based dictionary tree_ditc producing embedded
        hierarchically tree representation of data.
        Takes row-based dir data from tree_ditc, works on the current
        working_node converts it into a directory format
        {'name':dir-path,"children":[list of children]} if no children replace
        children with "size": integer value.
        max_level: Describes the maximum depth returned
        fl_type: is intended to be a str name of one of the values totaled in
        Storagetats csv output. If 'total' in fl_type totals are calculated
        see working_node_total.
        """
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
                    self.build_dir_tree(tree_ditc, next_working_node, fl_type, level, max_level))
        else:
            if 'total' in fl_type:
                build["size"] = self.working_node_total(working_node, fl_type)
            else:
                build["size"] = working_node['node'][fl_type]
        level -= 1
        return build

    def main(self, csv_in, json_out, fl_type='total', max_level=3, root_path=None):
        print 'Start convert csv to flare json'
        print 'csv_in:', csv_in, 'json_out:', json_out, \
            'fl_type:', fl_type, 'root_path:', root_path
        # lode data from csv file
        tree_ditc = self.csv_2_tree_path_dicts(csv_in)
        if root_path is None:
            # calculate commoun base path
            root_path = self.find_root_dir(tree_ditc)
        # add a root node
        self.add_root(tree_ditc, root_path)
        # calculate list of children for each node and add to each
        self.calc_children(tree_ditc)
        # calculate values totals for root by summing up child values
        self.calc_root_totlas(tree_ditc, root_path)
        # build d3 treemap comparable data structured
        # stare with root node
        working_node = {'name': root_path, 'node': tree_ditc[root_path]}
        level = 0
        dir_tree = self.build_dir_tree(tree_ditc, working_node, fl_type, level, max_level)
        # out put dir_tree as json file
        self.write_2_jsonfile(dir_tree, json_out)
        print 'Done convert csv to flare json'

if __name__ == "__main__":
    converter = ConvertCsv2Flare()
    converter.main('FSHistory_Dojo.csv', 'flare_data.json')  # root_path="C:/work/Dojo"

'''
TODO:
    xx git
    xx add comments
    xx convert to a object ername main file convert_csv_2_flare.py
    unittest 1
    use system deftes
    xx maim > convert_csv_2_flare(csv_in, json_out, root_path = null) 1.5
        added main orchestration function convert_csv_2_flare
    xx exposed top level parameters to convert_csv_2_flare
    readme.md 1.5
    github as website index.html... 2
    D3 stuff leve 3 shows ???
'''
