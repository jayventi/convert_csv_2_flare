##convert_csv_2_flare and Treemap example##

##[D3 Zoomable Treemap of Directory Space Usage](https://jayventi.github.io/convert_csv_2_flare/index.html)##

### Description ###
This is a tool to produce a D3 zoomable treemap visualization of directory space utilization and a data file conversion utility to support the D3 graphics. The general idea is to ultimately build a utility which monitors ongoing space utilization from a flat file data store systems. convert_csv_2_flare is part of a two-part project the first part [storagestats](https://github.com/jayventi/storagestats) calculates space usage on a per file type basis which is configurable, and produce a CSV output file containing usage statistics. This utility converts the CSV to a flare json format which is consumed by the D3 treemap. The D3 treemap graphic index.html is based on Mike Bostock's original [D3 zoomable treemap graph](http://mbostock.github.io/d3/talk/20111018/treemap.html).

These are building blocks which are intended to be used in a dashboard setting where the storagestats utility would run in a Cron script generate updated CSV data files which would be consumed by a dynamic site to produce the D3 graphics. 

The example graphic shows the space utilization for the open source phpmyadmin4.1.14 project.

###Overview Of Workflow###

The workflow starts with the generation of the CSV storage statistics datafile. This file is produced by the command line utility storagestats.py which resides in the [storagestats](https://github.com/jayventi/storagestats) repository. See the project's readme file for command line parameters.

The convert_csv_2_flare.py program fully converts the CSV to the D3 flare json file form. This utility consumes the CSV and produces a flair json file. The utility is configurable by setting the parameters in the main() method see below for details.

The D3 treemap graphic is produced by the [index.html](https://jayventi.github.io/convert_csv_2_flare/index.html) file. 

####Converting CSV Data File to Treemap Flare Json format####
Conversion is performed by the single file utility convert_csv_2_flare.py. convert_csv_2_flare.py consists of a single object with a main() method which orchestrates conversion configurable by five main parameters. It is executed the command line as:
```Shell
    python convert_csv_2_flare.py 
```
##### Main Procedure Parameters #####
Prototype for the main method is
```Python
    main(self, csv_in, json_out, fl_type='total', max_level=5, root_path=None)
```
All files are assumed to be in the same directory as the convert_csv_2_flare.py file.

csv_in : is the name of the input data CSV file. 

json_out: name of output flair json five used by the D3 treemap.

fl_type: file summation specifier, specifies values to be some there are two classes direct space counts in bits, and file count in number of files. Further files may be summed in total or by any of several types specified in the CSV data file. Summations the occur for any given file specifier. For instance all .log files may be summed up the new structure independent of other file types. Type 'other' and total is always present. The treemap only displays one particular file in the indices at a time. Examples of allowable, specifiers are ['total', 'total_Cn', 'other_Cn', 'other_Cn', 'log', 'log_Cn'] etc. log or anything besides total and other are dependent on the configuration parameters used to generate the CSV datafile from the storagestats utility.

 max_level: gives the number of subdirectories to output into the flair file, default set to five. If the depth given is less than total depth available space and file count is provided for the last directories appearing which will be treated as a 'leaf' directories. The tree is shorter in any given branch than the level count provided no harm will occur in all directories, and those branches will be output.
 
root_path: the root directory may in itself along given from the filesystem root if the time the path is known to the common root and may be given if not it will be calculated. The point of this parameter is the same overhead of calculating the roof which for deep paths could be nontrivial.

### Bill of Material ###
First three utilities generate files used by later steps

FS_*.csv: 
these are the space usage data files output by storagestats. it is the responsibility of the developer to see to it that these files are located in the directory where the convert_csv_2_flare.py utility resides.
```
convert_csv_2_flare.py:

```
actual file utility.
```
test_convert_csv_2_flare.py:

```
unit test fixture for convert_csv_2_flare.py

FSHistory_test.csv: required csv test file.

flare_*.json: flare json output files consumable by D3 treemap graphics.

index.html: html and JavaScript contains D3 JavaScript produces zoomable Treemap

generate_e_one_digit_at_a_time.py
Generates e one digit at a time, found code see header for source. Generates files of the form e_digit_{size}.txt
```
prime_file_list_2_dict.py:

```
Helper file not strictly necessary converts the lists of prime numbers founded in primes_sieve_{size}.json into a dictionary format for fast lookup. Files generated are in a form primes_sieve_ditc_{size}.json
###Unittest Support##
Unit test support is provided by test_convert_csv_2_flare.py which is built on the unittest framework. It requires a test input data file FSHistory_test.csv which is provided.


###D3 Example Treemap visualization###
To switch example flare json files edit in index.html the line:
```JavaScript
    var fileName = "flare_data_phpmyadmin.json";
```
Replace flare_data_phpmyadmin.json with one of the other example flare json files.

###TODO###
1) Add hover over feature to give statistics on a given directory.

2) Expose parameters as external command line utility parameters

3) Place in a dynamic node server,uUse data factories capable of calling the convert_csv_2_flare.py using the exposed parameters to request different file type summations, presented choices in treemap webpage.
