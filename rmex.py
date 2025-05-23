#!/usr/bin/env python3

# Author: Richard Lopez Corbalan
# GitHub: github.com/richardloopez
# Citation: If you use this code, please cite Lopez-Corbalan, R

import os
import shutil
import sys


#Initialize lists
cwd = None  #current working directory
total_user_input_list = []  #input list of the user, with both (rd and rf) if the user has put them
user_input_list = [] #input list of the user, without both (rd and rf)
items_all = [] #all the items (both folders and documents) in the cwd
deletable_items = [] #items in the cwd not included in the user_input_list: The script is gonna try to delete them. "try" because the program wont delete them if the flags (rd and rf) dont permit the action





#################################################################
#WORK IN THE TEST DIR!!

#os.chdir(r"C:\Users\richa\OneDrive\Desktop\pruebas_rmex")
#################################################################

#F0. Explanation
def explanation():
    print("""Looks like you need help, so the way this code works is: 
    
    --------------------------------    rmex("-rd -rf folders and documents")     ------------------------------------------------------------------------
    
    Here you have some examples:

    1. rmex("-rd alonso.txt") -> destroy all documents [except alonso.txt] (folders remain untouched)
    2. rmex("-rd -rf schumacher.txt") -> destroy all documents [except schumacher.txt] and all folders
    3. rmex("-rf hamilton.txt") -> destroy all folders (documents remain untouched). Yeah, it makes no sense adding "hamilton.txt" because no "rd" was added...

    4. rmex("-rf renault)-> destroy all folders [except renault] (documents remain untouched)
    5. rmex("-rd -rf ferrari") -> destroy all documents and all folders [except ferrari.txt]
    6. rmex("-rd mercedes") -> destroy all documents (folders remain untouched). Yeah, it makes no sense adding "mercedes" because no "rf" was added...

    7. rmex("-rd -rf alonso.txt renault") -> MAXIMUN POWER!! destroy all documents [except alonso.txt] and all folders [except renault]
    
    """)

#F1. Creating a list with all both documents and folders
def all_items_obtainer(cwd, items_all):
    for item in os.listdir(cwd):
        item_path = os.path.join(cwd, item)
        items_all.append(item_path)
    return items_all
        
#F2. Creating the whole route for the deletable elements
def whole_deletable_routes_obtainer(total_user_input_list, items_all, deletable_items, cwd):
    deletable_items = items_all[:]
    for inpuut in total_user_input_list:
        inpuut_path = os.path.join(cwd, inpuut)
        try:
            deletable_items.remove(inpuut_path)
        except ValueError as e:
            print(f"ITEM {inpuut_path} not found in current working directory")
            sys.exit()
    return deletable_items

#F3. "Are you sure?" statement (PART 1) 
def are_you_sure_mate_part1(deletable_items, cwd, rd=False, rf=False):
    print("Following items will be DESTROYED:")
    for item in deletable_items:
        item_cleaned_path = item.replace(cwd + os.sep, "")
        try:
            if os.path.isfile(item) and rd == True:
                print(f"- {item_cleaned_path}")
            elif os.path.isfile(item) and rd == False:
                pass

            if os.path.isdir(item) and rf == True:
                print(f"- {item_cleaned_path}")
            elif os.path.isdir(item) and rf == False:
                pass
        except ValueError as e:
            print(f"ITEM {item_cleaned_path} is not considered a folder or a document neither? ... ARE YOU KIDDING ME?!")


#F4. "Are you sure?" statemente (PART 2)    
def are_you_sure_mate_part2():
    you_sure = input ("mate, are you completely sure? yes/no: ")
    if you_sure.lower() == "yes":
        pass
    else:
        print("Operation cancelled, you were NOT sure bro :(")
        sys.exit()

#F4. Deleting items
def rmex_function (deletable_items, rd=False, rf=False):
    for deletable in deletable_items:
        if (os.path.isfile(deletable)) and (rd):
            os.remove(deletable)
        elif (os.path.isdir(deletable)) and (rf):
            shutil.rmtree(deletable)
    print("Destroyable items have been DESTROYED...")
    print("How many time have you save? Yeah, breathe...")


#########################################################################################################################

#P1. Principal function 1

def whole_process_without_input_module (cwd, total_user_input_list, items_all, deletable_items, rd=False, rf=False):
    cwd = str(os.getcwd())
    items_all = all_items_obtainer(cwd, items_all)
    deletable_items = whole_deletable_routes_obtainer(total_user_input_list, items_all, deletable_items, cwd)
    are_you_sure_mate_part1(deletable_items, cwd, rd=rd, rf=rf)
    are_you_sure_mate_part2()
    rmex_function (deletable_items, rd=rd, rf=rf)

#P2. Principal function 2

def rmex_real (total_user_input_list, rd=False, rf=False):
    whole_process_without_input_module (cwd, total_user_input_list, items_all, deletable_items, rd=rd, rf=rf)

##########################################################################################################################
#MAIN




def rmex(total_user_input):
    total_user_input_list = str(total_user_input).split()

    if len(total_user_input_list) < 2:
        explanation()
    else:
        pass

    rd = False
    rf = False

    if total_user_input_list[0] == "-rd":
        rd = True
    if total_user_input_list[1] == "-rd":
        rd = True
    if total_user_input_list[0] == "-rf":
        rf = True
    if total_user_input_list[1] == "-rf":
        rf = True

    if rd == True:
        total_user_input_list.remove("-rd")
    if rf == True:
        total_user_input_list.remove("-rf")



    try:
            rmex_real (total_user_input_list, rd=rd, rf=rf)
    except ValueError as e:
        print("Main function error, probably, rd or rf wrong")
    
    
        
if __name__ == "__main__":
    import sys
    total_user_input = " ".join(sys.argv[1:])
    rmex(total_user_input)


