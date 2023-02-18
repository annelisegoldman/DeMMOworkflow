# This script checks for seqtk errors by comparing the number of sequence names in a .lst file to the number
# of sequences pulled out by seqtk in the genomeID_renamed.faa file.

import os
import os.path
import glob
import shutil
import re

lst_dir = "/Users/annelisegoldman/TCS_mining/seqtk_error_tests/lst_test_files/"
renamed_dir = "/Users/annelisegoldman/TCS_mining/seqtk_error_tests/faa_test_files/"
error_dir = "/Users/annelisegoldman/TCS_mining/seqtk_error_tests/seqtk_errors/"


def lst_counter(file):
    # counts the number of HK names listed in the .lst file
    # each HK name is identified by a "c" at the beginning
    # so just counting the number of "c"s
    with open(file, "rt") as lst_file:
        num_names = {}
        for line in lst_file:
            num = len([1 for line in open(file) if line.startswith("c")])
            num_names[(file)] = num
    return num_names


def prot_counter(file):
    # counts the number of HK protein sequences found in genomeID_renamed.faa
    # each HK sequence is identified by a ">" at the beginning
    # so just counting the number of ">"s in a file
    with open(file, "rt") as seq_file:
        num_prots = {}
        for line in seq_file:
            prot = len([1 for line in open(file) if line.startswith(">")])
            num_prots[(file)] = prot
    return num_prots


def ship_out(filename, current_dir, new_dir):
    # moves a file from its current directory to a new directory
    for f in filename:
        # command = "'mv %s %s' % (os.path.join(current_dir, filename), os.path.join(new_dir, filename))"
        res = os.system('mv %s %s' % (os.path.join(current_dir, filename), os.path.join(new_dir, filename)))
        # Testing checkpoint: print("Returned value: ", res)


def search(key, searchFor):
    # looks in either prot_count or lst_count dictionaries to identify the keys that correspond with each other
    # searchFor will either be the MAG_ID or the ID_match_lst variable
    for k in key:
        if searchFor in k:
            return k
    return None


def main():
    for file in glob.glob(renamed_dir + "*_renamed.faa", recursive=True):
        # Pull out the genome ID from the genomeID_renamed.faa file and save as
        # variable MAG_ID
        MAG_ID = re.split(r"[./_]", file)[11]
        # Testing checkpoint: print(MAG_ID)
        # Count the number of proteins in the .faa file and save as a variable prot_count
        prot_count = prot_counter(file)
        # Testing checkpoint: print(prot_count)
        # Check if matching lst file exists
        for lst_file in glob.glob(lst_dir + "FAA_ID%s.*.lst" % MAG_ID):
            if os.path.isfile(lst_file):
                # Count the number of HK names in the .lst file and save as a variable lst_count
                # Identify the matching lst file name
                ID_match_lst = re.split(r"/+", lst_file)[6]
                print("Found corresponding lst file %s" % ID_match_lst)
                lst_count = lst_counter(lst_file)
                # Testing checkpoint: print(lst_count)
                # Check if the prot_count == lst_count
                # If prot_count != lst_count, move the .lst file to the error folder seqtk_errors
                p = search(prot_count, MAG_ID)
                l = search(lst_count, MAG_ID)
                # Testing checkpoint: print(p, l)
                try:
                    if prot_count[p] == lst_count[l]:
                        print("seqtk pulled same number of HKs as lst file for %s" % MAG_ID)
                        continue
                except:
                    # Get the script to continue even when a key doesn't exist due to there not being any sequences
                    KeyError
                    print("Error with counting/no sequences counted, moving %s to error folder" % ID_match_lst)
                    ship_out(ID_match_lst, lst_dir, error_dir)
                # except:
                # KeyError and lst_count[l] is not None
                # print("seqtk pulled same number of HKs as lst file for %s" % MAG_ID)
                else:
                    print("Seqtk error, moving %s to error folder" % ID_match_lst)
                    ship_out(ID_match_lst, lst_dir, error_dir)
            # If matching lst file doesn't exist, say so
            else:
                print("Cannot find lst file %s" % MAG_ID)


# Run the whole script
if __name__ == "__main__":
    main()