### NOTE - put all zone files (.zone extension) for checking into the same directory as this script - we'll detect them and through the menu select the appropriate file for the checks

import subprocess

def ls():
    process = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
    output = process.communicate()

    dir_objs = []

    #print(output[0])
    #print(str(output).split("\\n"))
    for dir_obj in str(output).split("\\n"):
        if dir_obj.__contains__(".zone"):
            dir_objs.append(dir_obj.replace("(b'",""))

    return dir_objs

def nslookup(domain):
    process = subprocess.Popen(["nslookup", domain], stdout=subprocess.PIPE)
    output = process.communicate()

    try:
        str(output).index('Non-authoritative answer:')
    except:
        print("record does not exist:")
        #print(output[0])
        #print("---------------------")
        #return str(output[0] + "not found")
        return("not found")

    else:
        return str(output).split('Non-authoritative answer:')[1]

def touch(filename):
    process = subprocess.Popen(["touch", filename], stdout=subprocess.PIPE)
    output = process.communicate()

dir_objects = ls()
#print(dir_objects)

print("~~~~~~~~~~~~~~~~~~~~~~")
print("~~ DNS CHECKER MENU ~~")
print("~~~~~~~~~~~~~~~~~~~~~~")

run_type = ""
while run_type != "pre" and run_type != "post":
    run_type = input("Are you running a pre-migration or post-migration check? (enter 'pre' or 'post')")

print("\n")
menu_counter = 1

print("The following zone files are available for your " + run_type + (" check:"))

for obj in dir_objects:
    print(str(menu_counter) + " - " + obj)
    menu_counter+=1

file_to_check = 0

print('\n')
if file_to_check == 0:
    file_to_check = input("Enter the number of the file you want to check: ")

    while int(file_to_check) == 0 or int(file_to_check) > len(dir_objects):
        print("invalid menu selection")
        file_to_check = input("Which file do you wish to check?")

print("Checking " + str(dir_objects[int(file_to_check) -1]))

sourcefile_name = str(dir_objects[int(file_to_check)-1])
checkfile_name = str(dir_objects[int(file_to_check)-1].replace(".zone","") + "_" + run_type + "-check.txt")

cnames = []

with open(sourcefile_name, 'r') as file:

    for line in file:
        if line.__contains__("CNAME"):
            #print(line.split()[0])
            cnames.append(line.split()[0])
    file.close()

touch(checkfile_name)

#with open(str(dir_objects[int(file_to_check)-1].replace(".zone","") + "_" + run_type + "-check.txt", mode="wt") as f:
with open(checkfile_name, mode="wt") as f:

    for cname in cnames:
        cn_record = (nslookup(cname))
        cn_record = cn_record.replace('\\t', '\\\t')
        cn_record = cn_record.replace('\\n', '\\\n')
        cn_record = cn_record.replace('\\', '')
        cn_record = cn_record.replace("', None)", '')

f.close()
