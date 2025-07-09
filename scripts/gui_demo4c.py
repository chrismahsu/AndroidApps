import sys
import PySimpleGUI as sg
import codecs
import os

# this version tries to read from files dynamically
# two files for app name and app creator instead of one because of the splitting issue

f_al = ''
f_anl = ''
f_apl = ''
f_acl = ''

permission_list = []
category_list = []
output_file = ''
# except permission list and category list, we may consider reading the records line by line instead of storing the
# whole file into the list to save space, and it is really not necessary to do so

appLink = ''
appVersion = ''
desc = ''
descLine = ''
descLength = 0
readNext = False


# function to real general input
def read_general_input(str1, the_list):
    fi1 = open(str1, 'r')
    line1 = fi1.readline()
    line1 = fi1.readline()
    while len(line1) > 0:
        the_list.append(line1.split(",", 2))
        line1 = fi1.readline()
    fi1.close()


# function to read app description
def read_app_desc_file(fi1):
    global appLink
    global appVersion
    global desc
    global descLine
    global readNext
    global descLength

    descContinue = False

    appLink = ''
    appVersion = ''
    # use encoding to read non-ACSII descriptions
    if readNext is False:
        descLine = fi1.readline()
        if len(descLine) <= 0:
            sys.exit()
    else:
        readNext = False

    # read the description from the csv file
    # complication due to the newline character in the description
    if len(descLine) > 0:
        if len(descLine.split(",", 3)) > 3:
            descIndex = 3
            appLink = descLine.split(",", 3)[0]
            appVersion = descLine.split(",", 3)[1]
            # print(appLink)
            # app version can also contain ',', need to concatenate until reaching the number field representing
            # the length of description
            while not descLine.split(",", descIndex)[descIndex - 1].isdigit():
                appVersion += "," + descLine.split(",", descIndex)[descIndex - 1]
                descIndex += 1
                # print("error here")
            descLength = int(descLine.split(",", descIndex)[descIndex - 1])

            # if (appLink == "abhitech.com.currentaffairsdost"):
            #    print("here")

            descLineExt = descLine.split(",", descIndex)[descIndex]
            if (descLength > len(descLineExt)):
                # print(appLink, ": multi-line desc to be continued")

                descContinue = True
                descLength -= len(descLineExt) - 1
                # print(descLength)
                desc = descLine.split(",", 3)[3].lstrip('"')
            else:
                # print(appLink, ": single-line desc")

                if len(descLineExt) == descLength + 3:
                    desc = descLine.split(",", 3)[3].lstrip('"').rstrip('"\n')
                else:
                    desc = descLine.split(",", 3)[3].rstrip('\n')

        # use the length of the description to check if ending is reached
        # still have issue because emoji seeems not correctly counted
        # - under-count happens and read also the next line!
        while descContinue:
            descLine = fi1.readline()

            # check if the real end of description is reached
            if (descLength > len(descLine)):
                descLength -= len(descLine)
                desc += descLine
            else:
                descLength -= len(descLine)
                descContinue = False
                if descLength > -3:
                    desc = desc + descLine.rstrip('"\n')
                else:
                    desc = desc.rstrip('"\n')
                    readNext = True


layout = [[sg.T("")],
          [sg.Text("App details file: ", size=(20, 1)), sg.Input(), sg.FileBrowse(key="-IN1-")],
          [sg.Text("App name file: ", size=(20, 1)), sg.Input(), sg.FileBrowse(key="-IN2-")],
          [sg.Text("App creator file: ", size=(20, 1)), sg.Input(), sg.FileBrowse(key="-IN3-")],
          [sg.Text("App category file: ", size=(20, 1)), sg.Input(), sg.FileBrowse(key="-IN4-")],
          [sg.Text("Category description file: ", size=(20, 1)), sg.Input(), sg.FileBrowse(key="-IN5-")],
          [sg.Text("App permission file: ", size=(20, 1)), sg.Input(), sg.FileBrowse(key="-IN6-")],
          [sg.Text("Permission description file: ", size=(20, 1)), sg.Input(), sg.FileBrowse(key="-IN7-")],
          [sg.Text("Output file: ", size=(20, 1)), sg.Input(), sg.FileBrowse(key="-IN8-")],
          [sg.T("")],
          [sg.Button("OK", size=(10, 1)), sg.Button("Hard-code", size=(10, 1))]]

# Create the window
window = sg.Window("Data Labeling System - Files Setup", layout)
canProceed = False

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        window.close()
        sys.exit()
    if event == "OK":
        if len(values["-IN1-"]) > 0 and len(values["-IN2-"]) > 0 and len(values["-IN3-"]) > 0 and \
                len(values["-IN4-"]) > 0 and len(values["-IN5-"]) > 0 and len(values["-IN6-"]) > 0 and \
                len(values["-IN7-"]) > 0 and len(values["-IN8-"]) > 0:
            canProceed = True
            print(values["-IN1-"])
            print(values["-IN2-"])
            print(values["-IN3-"])
            print(values["-IN5-"])

            # file for app link, version, and description
            f_al = codecs.open(values["-IN1-"], encoding='utf-8')
            f_al.readline()
            # file for app name and creator
            f_anl = open(values["-IN2-"])
            f_anl.readline()
            # file for app name and creator
            f_anl2 = open(values["-IN3-"])
            f_anl2.readline()
            # file for app category
            f_acl = open(values["-IN4-"])
            f_acl.readline()
            # file for app permission requests
            f_apl = open(values["-IN6-"])
            f_apl.readline()

            read_general_input(values["-IN5-"], category_list)
            read_general_input(values["-IN7-"], permission_list)
            output_file = values["-IN8-"]
        else:
            print("Incomplete input!")
            sg.Popup('Select all the three files first')
        break
    elif event == "Hard-code":
        canProceed = True

        # file for app link, version, and description
        f_al = codecs.open("D:/fds/202021/app details ordered all apps 20230213 wcl.csv", encoding='utf-8')
        f_al.readline()
        # skipping the header line

        # file for app name
        f_anl = codecs.open("D:/fds/202021/app name table ordered all apps 20230213 v2.csv", encoding='utf-8')
        f_anl.readline()

        # file for app creator
        f_anl2 = codecs.open("D:/fds/202021/app creator table ordered all apps 20230213.csv", encoding='utf-8')
        f_anl2.readline()
        # skipping the header line

        # file for app category
        f_acl = codecs.open("D:/fds/202021/app category ordered all apps 20230213.csv", encoding='utf-8')
        f_acl.readline()
        # skipping the header line

        # file for app permission requests
        f_apl = codecs.open("D:/fds/202021/app permissions ordered all apps 20230213.csv", encoding='utf-8')
        f_apl.readline()
        # skipping the header line

        # files for the category descriptions and permission descriptions
        read_general_input("D:/fds/202021/category details ordered all apps 20230213.csv", category_list)
        read_general_input("D:/fds/202021/permission list ordered 317 20230213.csv", permission_list)

        # file for output of request decisions
        output_file = "D:/fds/202021/output4.txt"
        # output_file = "D:/fds/202021/output3.txt"
        break
window.close()

# prepare to show the first app with requested permission
faplList = [None, None, None]
lastLineList = [None, None, None, None]

# in case we processed before, we continue from where we quited
# *** assuming we use the same set of files
if os.stat(output_file).st_size > 0:
    with open(output_file, 'rb') as f1:
        try:  # catch OSError in case of a one line file
            f1.seek(-2, os.SEEK_END)
            while f1.read(1) != b'\n':
                f1.seek(-2, os.SEEK_CUR)
        except OSError:
            f1.seek(0)
        last_line = f1.readline().decode()

    j = last_line.count(",")
    if j > 3:
        lastLineRightPart = last_line.split(",", 1)[1]
        lastLineList[0] = last_line.split(",", 1)[0]
        lastLineList[1] = lastLineRightPart.rsplit(",", 2)[0]
        lastLineList[2] = lastLineRightPart.rsplit(",", 2)[1]
        lastLineList[3] = lastLineRightPart.rsplit(",", 2)[2]
    else:
        lastLineList = last_line.split(",", 3)

    # read from the app permission request file
    faplLine = f_apl.readline()
    if len(faplLine) > 0:
        j = faplLine.count(",")
        if j > 2:
            faplRightPart = faplLine.split(",", 1)[1]
            faplList[0] = faplLine.split(",", 1)[0]
            faplList[1] = faplRightPart.rsplit(",", 1)[0]
            faplList[2] = faplRightPart.rsplit(",", 1)[1]
        else:
            faplList = faplLine.split(",", 2)
    else:
        sys.exit()

    while True:

        if (faplList[0] != lastLineList[0] or
                faplList[1] != lastLineList[1] or
                faplList[2].rstrip('"\n') != lastLineList[2]):
            # [0]: app_link; [1]: app version; [2]: permission id
            # not yet reaching where we left, read next record in app permission request file
            faplLine = f_apl.readline()
            faplList = [None, None, None]
            if len(faplLine) > 0:
                j = faplLine.count(",")
                if j > 2:
                    faplRightPart = faplLine.split(",", 1)[1]
                    faplList[0] = faplLine.split(",", 1)[0]
                    faplList[1] = faplRightPart.rsplit(",", 1)[0]
                    faplList[2] = faplRightPart.rsplit(",", 1)[1]
                else:
                    faplList = faplLine.split(",", 2)
            else:
                sys.exit()
        else:
            break

# reached where we left or at the very beginning, now read the next unprocessed app permission request
faplLine = f_apl.readline()
if len(faplLine) > 0:
    j = faplLine.count(",")
    if j > 2:
        faplRightPart = faplLine.split(",", 1)[1]
        faplList[0] = faplLine.split(",", 1)[0]
        faplList[1] = faplRightPart.rsplit(",", 1)[0]
        faplList[2] = faplRightPart.rsplit(",", 1)[1]
    else:
        faplList = faplLine.split(",", 2)
else:
    sys.exit()

# now proceed to the app description list (file)
# read until we reach the currently processing one
read_app_desc_file(f_al)
while faplList[0] != appLink:
    read_app_desc_file(f_al)

# now proceed to the app name list (file)
# read until we reach the currently processing one
fanlLine = f_anl.readline()
if len(fanlLine) > 0:
    fanlList = fanlLine.split(",", 1)
else:
    sys.exit()
while faplList[0] != fanlList[0]:
    fanlLine = f_anl.readline()
    if len(fanlLine) > 0:
        fanlList = fanlLine.split(",", 1)
    else:
        sys.exit()

# now proceed to the app creator list (file)
# read until we reach the currently processing one
fanl2Line = f_anl2.readline()
if len(fanl2Line) > 0:
    fanl2List = fanl2Line.split(",", 1)
else:
    sys.exit()
while faplList[0] != fanl2List[0]:
    fanl2Line = f_anl2.readline()
    if len(fanl2Line) > 0:
        fanl2List = fanl2Line.split(",", 1)
    else:
        sys.exit()

# now proceed to the app category list (file)
# read until we reach the currently processing one
faclLine = f_acl.readline()
if len(faclLine) > 0:
    faclList = faclLine.split(",", 2)
else:
    sys.exit()
while faplList[0] != faclList[0]:
    faclLine = f_acl.readline()
    if len(faclLine) > 0:
        faclList = faclLine.split(",", 2)
    else:
        sys.exit()

# prepare the layout for display
# some entries contain \n, need to be stripped for better display
layout2 = [[sg.T("")],
           [sg.Text("Link: ", size=(9, 1)), sg.Text(appLink, key="-INLK-")],
           [sg.Text("Name: ", size=(9, 1)), sg.Text(fanlList[1].rstrip('\n'), key="-INNM-")],
           [sg.Text("Creator: ", size=(9, 1)), sg.Text(fanl2List[1].rstrip('\n'), key="-INCR-")],
           [sg.Text("Category: ", size=(9, 1)),
            sg.Text(category_list[int(faclList[1].rstrip('\n')) - 1][1].rstrip('\n'), key="-INCA-")],
           [sg.Text("Version: ", size=(9, 1)), sg.Text(appVersion, key="-INVR-")],
           [sg.T("")],
           [sg.Multiline(desc.replace('\n', '\n\n'), key="-INML-", size=(100, 10))],
           [sg.T("")],
           [sg.Text("Type: ", size=(9, 1)), sg.Text(permission_list[int(faplList[2].rstrip('\n'))][1], key="-INTY-")],
           [sg.Text("Details: ", size=(9, 1)),
            sg.Text(permission_list[int(faplList[2].rstrip('\n'))][2].rstrip('\n'), key="-INDE-")],
           [sg.Button("OK", size=(6, 1)), sg.Button("Not OK", size=(6, 1))]]

# Create the window to display
if canProceed:
    window = sg.Window("Data Labeling System", layout2)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break
        if event == "OK":
            # permission request justified, write '1'
            # updated the following on 21/03/2023 to correct the output error
            f1 = open(output_file, 'a', encoding="utf_8_sig")
            f1.write(faplList[0] + ',' + faplList[1] + ',' + faplList[2].rstrip('\n') + ',1\n')
            f1.close()
        elif event == "Not OK":
            # permission request not justified, write '0'
            # updated the following on 21/03/2023 to correct the output error
            f1 = open(output_file, 'a', encoding="utf_8_sig")
            f1.write(faplList[0] + ',' + faplList[1] + ',' + faplList[2].rstrip('\n') + ',0\n')
            f1.close()

        # read the next permission request and update various fields on the layout
        faplLine = f_apl.readline()
        if len(faplLine) > 0:
            j = faplLine.count(",")
            if j > 2:
                faplRightPart = faplLine.split(",", 1)[1]
                faplList[0] = faplLine.split(",", 1)[0]
                faplList[1] = faplRightPart.rsplit(",", 1)[0]
                faplList[2] = faplRightPart.rsplit(",", 1)[1]
            else:
                faplList = faplLine.split(",", 2)
        else:
            window.close()
            sys.exit()

        # if the next permission does not belong to the current app, read the next app description
        while faplList[0] != appLink:
            read_app_desc_file(f_al)
            window["-INML-"].update(desc.replace('\n', '\n\n'))
            window["-INLK-"].update(appLink)
            window["-INVR-"].update(appVersion)

        # if the next permission does not belong to the current app, read the next app name and creator
        while faplList[0] != fanlList[0]:
            fanlLine = f_anl.readline()
            fanl2Line = f_anl2.readline()
            if len(fanlLine) > 0:
                fanlList = fanlLine.split(",", 1)
                fanl2List = fanl2Line.split(",", 1)
            else:
                window.close()
                sys.exit()
            window["-INNM-"].update(fanlList[1].rstrip('\n'))
            window["-INCR-"].update(fanl2List[1].rstrip('\n'))

        # if the next permission does not belong to the current app, read the next app category
        while faplList[0] != faclList[0]:
            faclLine = f_acl.readline()
            if len(faclLine) > 0:
                faclList = faclLine.split(",", 2)
            else:
                window.close()
                sys.exit()
            window["-INCA-"].update(category_list[int(faclList[1].rstrip('\n')) - 1][1].rstrip('\n'))

        window["-INTY-"].update(permission_list[int(faplList[2].rstrip('\n'))][1])
        window["-INDE-"].update(permission_list[int(faplList[2].rstrip('\n'))][2].rstrip('\n'))
    window.close()
