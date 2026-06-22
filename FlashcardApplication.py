import FreeSimpleGUI as sg
import json
import random
import os

# The dictionary that will hold all flashcard values
deck_information = {}
flashcard_faces = []
display_card = ""

# A function that updates the deck's displayed info when cards are created or deleted
def update_deck_info():
	global flashcard_faces
	flashcard_faces = list(deck_information.keys())
	display_information = ""
	for face, back in deck_information.items():
		display_information += face + ": " + back + "\n"
	window["-DECK_INFORMATION-"].update(display_information)
	update_practice_info()

def update_practice_info():
	global display_card
	if flashcard_faces == []:
		return
	display_card = random.choice(flashcard_faces)
	window["-FACE_TEXT-"].update(display_card)
	window["-USER_ANSWER-"].update("")

if __name__ == "__main__":
	if os.path.exists("flashcards.json"):
		try:
			with open("flashcards.json", "r") as file:
				deck_information = json.load(file)
				flashcard_faces = list(deck_information.keys())
		except Exception as e:
			sg.popup("Unable to find save file, starting a new file")
			deck_information = {}
	else:
		deck_information = {}

	sg.theme("DefaultNoMoreNagging")

	layout1 = [
		[sg.Text("Create and practice with flashcards.", font=("Helvetica", 14))],
		[sg.Text("Create a new flashcard: ")],
		[sg.Text("Flashcard face: "), sg.Input(key="-FLASHCARD_FACE-", size=(50, 1))],
		[sg.Text("Flashcard back: "), sg.Input(key="-FLASHCARD_BACK-", size=(50, 1))],
		[sg.Button("Create flashcard")],
		[sg.Text("Delete a flashcard: "), sg.Input(key="-DELETE_FLASHCARD-", size=(50, 1))],
		[sg.Button("Delete flashcard")],
		[sg.Text("Created flashcards:")],
		[sg.Text(key="-DECK_INFORMATION-")]
	]

	layout2 = [
		[sg.Text("Practice with your flashcards"), sg.Button("Next card")],
		[sg.Text(key="-FACE_TEXT-"), sg.Input(key="-USER_ANSWER-")],
		[sg.Button("Submit")],
		[sg.Text(key="-CORRECT_ANSWER-")]
	]

	layout = [
		[sg.TabGroup([[sg.Tab("Deck Information", layout1), sg.Tab("Practice", layout2)]
	])]
	]
	
	window = sg.Window("Flashcard App", layout, finalize=True)
	update_deck_info()
# This loop runs continuously, waiting for the user to click buttons or type.
	while True:
		event, values = window.read() # Pauses and waits for user action
		if event == sg.WINDOW_CLOSED:
			with open("flashcards.json", "w") as file:
				json.dump(deck_information, file, indent=4)
			break

		if event == "Create flashcard":
			deck_information[values["-FLASHCARD_FACE-"]] = values["-FLASHCARD_BACK-"]
			window["-FLASHCARD_FACE-"].update("")
			window["-FLASHCARD_BACK-"].update("")
			update_deck_info()

		if event == "Delete flashcard":
			deck_information = {face: back for face, back in deck_information.items() if face != values["-DELETE_FLASHCARD-"]}
			window["-DELETE_FLASHCARD-"].update("")
			update_deck_info()

		if event == "Next card":
			update_practice_info()

		if event == "Submit":
			update_practice_info()
			if values["-USER_ANSWER-"].strip().lower() == deck_information[display_card]:
				window["-CORRECT_ANSWER-"].update("Correct")
			else:
				window["-CORRECT_ANSWER-"].update(f"Incorrect, the correct answer is: {deck_information[display_card]}")

	window.close()
