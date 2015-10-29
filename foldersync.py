#!/usr/bin/env python

import sys
import os
from os import listdir
from os.path import isfile, join

"""

foldersync.py - A script that given two input directories, will delete files that are in one folder but not the other.
The script will sync the two folders only by deleting, and will not add. It will delete empty folders as well.

Usage - python foldersync.py [path_to_directory1] [path_to_directory2]

Ex - 

python foldersync.py ~/Music ~/external/phone/music

"""


def set_of_files(directory):
    x = []
    for root, subFolders, files in os.walk(directory):
        x += map(lambda x: join(root, x).replace(directory + "/", ""), files)
    return set(x)

def get_difference(dir1, dir2):
    dir1_files = set_of_files(dir1)
    dir2_files = set_of_files(dir2)
    difference = dir1_files - dir2_files
    return map(lambda x: join(dir1, x), difference)

def get_bidirectional_difference(dir1, dir2):
    return get_difference(dir1, dir2) + get_difference(dir2, dir1)

def delete_files(files):
    map(lambda f: os.remove(f), files)

def remove_empty_folders(path, removeroot=True):
    if not os.path.isdir(path):
        return
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)
    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and removeroot:
        print "Removing empty folder:", path
        os.rmdir(path)

if __name__ == "__main__":
    if not len(sys.argv) >= 3:
        print "Not enough inputs, please specify 2 directories to sync."
        sys.exit(0)
    dir1, dir2 = sys.argv[1], sys.argv[2]
    files = get_bidirectional_difference(dir1, dir2)

    if not files:
        print "Both directories are already synced! Party time."
        sys.exit(0)

    print "Files to delete:"
    print "==============="
    for f in files:
        print f
    print "==============="

    confirm = raw_input("Continue? y/n: ")
    if confirm.lower() == "y":
        delete_files(files)
        remove_empty_folders(dir1)
        remove_empty_folders(dir2)
    else:
        print "No confirmation. Exiting."

