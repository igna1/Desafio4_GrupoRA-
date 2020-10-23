from src.editor import Editor
import sys, os


if __name__ == "__main__":
	if len(sys.argv) == 1:
		print ("Uso python3 world_editor.py filename.json")
	elif len(sys.argv) == 2:
		filename = sys.argv[1]
		if filename.endswith(".json"):
			if os.path.exists(filename):
				editor = Editor(filename,True)
			else:
				editor = Editor(filename,False)
			editor.run()
		else:
			print ("el nombre del archivo debe terminar en .json")
