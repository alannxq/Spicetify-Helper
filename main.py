import PySimpleGUI as sg
import os


def update_last_path(path):
	with open("PreviousDirectory.txt", "w") as f:
		f.write(path)

def read_last_path():
	with open("PreviousDirectory.txt", "r") as f:
		path = f.read()
	return path

def get_folders(path):
	try:
		all_items = os.listdir(path)
	except FileNotFoundError:
		print("ERROR: Directory not found")
		return

	folders = ["Select a Theme"]
	for item in all_items:
		if "." in item:
			continue
		folders.append(item)

	return folders

def load_themes(path):
	folders = get_folders(path)
	update_last_path(path)
	window["-FOLDER-"].update(f"Directory: {path}")
	window['-THEMES-'].update(value=folders[0], values=folders)

def apply_theme(theme):
	os.system(f"spicetify config current_theme {theme}")
	os.system("spicetify apply")

def load_previous_config():
	global start_folders, directory
	path = read_last_path()
	if path != "NONE" and path != "":
		directory = path
		start_folders = get_folders(path)

start_folders = ["Select a Theme"]
directory = "NONE"

load_previous_config()

sg.theme('DarkGrey12')

layout = [  [sg.Text('Spicetify Helper', font = ("Arial, 15"), pad=(20, 25))],
			[sg.Text('1. Select Spicetify Directory', font = ("Arial, 12"), pad=(5, 10))],
			[sg.Text(f"Directory: {directory}", key='-FOLDER-')],
            [sg.FolderBrowse(), sg.Button('Load Themes', pad = (5, 10))],
            [sg.Text("")],
			[sg.Text('2. Select Spicetify Theme', font = ("Arial, 12"), pad=(5, 10))],
            [sg.Combo(values = start_folders, key="-THEMES-"), sg.Button('Apply Theme', pad = (5, 10))]]

window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break

    if event == "Load Themes":
    	path = values["Browse"]
    	load_themes(path)

    if event == "Apply Theme":
    	apply_theme(values["-THEMES-"])

window.close()
