import os
import string
import json

# parsing information from game_ids.json. File taken from Renan's GRaca github with his permission from a similar project (https://github.com/RenanGreca/Switch-Screenshots/blob/master/game_ids.json) found after completing everything previous to converting ID to game name.
game_names = json.load(open(os.path.join(os.path.realpath(os.path.dirname(__file__)), "game_ids.json")))

#detect which drive contains the SD card based on the existence of the 'Nintendo' folder in the root
def detectDrive():
    for drive in string.ascii_uppercase:
        if os.path.exists("%s:\\Nintendo" % drive):
            path = "%s:\\nintendo" % drive
            return("%s:\\nintendo" % drive)
    return (None)

#obtain paths to all of the videos and images as well as the names as well as append them to the lists. Option if videos, images or both are included.
def getPaths(rootPath, option):
    images_paths = []
    videos_paths = []
    for root, dirs, files in os.walk(rootPath):
        for file_name in files:
            if "jpg" in file_name and (option == '1' or option == '3') :
                images_paths.append([os.path.join(root,file_name), file_name])
            if "mp4" in file_name and (option == '2' or  option == '3'):
                videos_paths.append([os.path.join(root,file_name), file_name])
    return ({ "images" : images_paths, "videos" : videos_paths})

# create folders for pictures/videos using current windows user's 'videos' and 'pictures' folders. 'option' will be 'pictures' or 'videos'
def createRootFolder(option):

    if not os.path.exists(os.path.join(os.path.expanduser("~"), "Pictures" ,"Nintendo Switch")) and (option == '1' or option == '3'):
        print("The folder ", os.path.join(os.path.expanduser("~"),"Pictures","Nintendo Switch"), "was created")
        os.mkdir(os.path.join(os.path.expanduser("~"),"Pictures" ,"Nintendo Switch"))
    if not os.path.exists(os.path.join(os.path.expanduser("~"), "Videos" ,"Nintendo Switch")) and (option == '2' or option == '3'):
        print("The folder ", os.path.join(os.path.expanduser("~"), "Videos" ,"Nintendo Switch"), "was created")
        os.mkdir(os.path.join(os.path.expanduser("~"), "Videos" ,"Nintendo Switch"))

# add the name of a game to the json file manually
def add_game_name(game, path):
    print('\a')
    print("The ID ", game, " is not recognized at this time. Please provide the name of the game: ")
    os.startfile(path)
    valid = False
    while valid == False:
        name = input()
        if len(name) > 0:
            valid = True
    # change invalid characters for '-'
    for char in name:
        if char in '<>:"/\|?*':
            name = name.replace(char, '-')
            print("Invalid character has been replaced")
    game_names[game] = name
    print("The name game :", name, " has been added for key ", game)
    with open(os.path.join(os.path.realpath(os.path.dirname(__file__)), "game_ids.json"), 'w') as outfile:
        json.dump(game_names, outfile)

# copy files based on their paths and names. These will be provided using a list of [path,name] lists. Returns list of game ids which are not in the json name list.
def copyFiles(paths, option):
    if option == '1':
        fileType = 'Pictures'
    elif option == '2':
        fileType = 'Videos'
    counter = 0
    if len(paths) > 0:
        print("A total of ", len(paths), " files were found")
        for file in paths:
            game = file[0].split('-')[1].split('.')[0]
            #change the game ID for its name if found in the game_ids.json file. If not found, saving it in a list in order to ask for the name at the end.
            if game in game_names:
                game = game_names[game]
            else:  
                # if name is not in the list, it will be requested manually. Then we change the ID for the name
                add_game_name(game, file[0])
                game = game_names[game]

            if not os.path.exists(os.path.join(os.path.expanduser("~"),fileType,"Nintendo Switch",game)):
                os.mkdir(os.path.join(os.path.expanduser("~"),fileType,"Nintendo Switch",game))
                print("Folder for ", game, " has been created")
                print("////////////////////////////////////////////////////////////////")
            if not os.path.exists(os.path.join(os.path.expanduser("~"),fileType,"Nintendo Switch",game,file[1])):
                new_f= open(os.path.join(os.path.expanduser("~"),fileType,"Nintendo Switch",game,file[1]), 'wb')
                original_f = open(file[0], "rb")
                new_f.write(original_f.read())
                new_f.close()
                original_f.close()
                print(file[1]," copied correctly")
                print("////////////////////////////////////////////////////////////////")
                counter += 1
        print("A total of ", counter, fileType," were copied!")
        

# Main script
rootPath = detectDrive()
if rootPath == None:
    print("No Valid SD card/location was detected. Make sure a valid SD was inserted or the 'Nintendo' folder was copied from the SD card to the root folder of a drive.")
else:
    print("\nThe files seem to be located at ", rootPath,".")
    # Don't want to take any risk when using this as any error could mess with the contents of the SD card.
    option = 0
    while option != '1' and option != '2' and option != '3':
        print("Do you want to copy only the pictures(1), videos(2) or both (3)?")
        option = input()
    print("Your option was ", option, "!")

    file_paths = getPaths(rootPath, option)
    createRootFolder(option)
    if option =='1':
        copyFiles(file_paths['images'], option)

    elif option == '2':
        copyFiles(file_paths['videos'], option)
    else:
        # use copyFiles function once for images and once for videos
        copyFiles(file_paths['images'], '1')
        copyFiles(file_paths['videos'], '2')

