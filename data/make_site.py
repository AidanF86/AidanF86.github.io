import os
from pathlib import Path
from dataclasses import dataclass
import shutil

pages_dir = Path('./pages')
navbar_file = Path('./pages/navbar.html')
style_file = Path('./pages/style.css')

@dataclass
class MainDir:
	name: str
	files: list

	def print(self):
		print(filename_to_title(self.name) + " | " + self.name)
		for file in self.files:
			file_path = file.name
			file_title = filename_to_title(file.name)
			print("	" + file_title + " | " + file_path)


non_cap_words = ["the", "an", "a", "at", "by", "to", "and", "but", "for", "and", "as", "as" "," "as", "at", "but", "by", "if", "for", "from", "if", "in", "into", "like", "near", "now", "nor", "of", "off", "on", "once", "onto", "or", "of", "over", "past", "so", "so", "than", "that", "till", "to", "up", "upon", "with", "when", "yet"] # TODO(aidan): Add and handle multi-words
def filename_to_title(string):
	# TODO(aidan): handle hyphens and capitalization
	words = os.path.splitext(string)[0].split('_')
	title = ""
	for word in words:
		if not word in non_cap_words:
			word = word.capitalize()
		title = title + word + " "
	title = title.strip()
	#print("Filename changed to title: \"" + string + "\" -> \"" + title + "\"")
	return title


# dir should be a path
def build_main_dir(dir):
	print("\033[96mBuilding directory: \033[00m" + str(dir))
	# Make a list of directories with their files
	subdirs = []
	for subdir in [x for x in dir.iterdir() if x.is_dir()]: 
		subdir_files = [x for x in subdir.iterdir() if x.is_file()]
		subdirs.append(MainDir(subdir.name, subdir_files))

	# Build!!!
	# ==============

	# Make output directory
	output_dir = Path("./output/" + dir.name)
	output_dir.mkdir(parents=True, exist_ok=True)

	# Create generic navbar - we'll highlight later
	navbar_string = "<div id=side_navbar>\n"
	navbar_string += "<a href='../../index.html'>Back to Homepage</a>"
	navbar_string += "<h1>" + filename_to_title(dir.name) + "</h1>\n"
	navbar_string += "<hr/>\n"
	for subdir in subdirs:
		#navbar_string += "<div class=section>\n"
		#navbar_string += "	<h4><a class='section_title'>"+filename_to_title(subdir.name)+"</a></h4>\n"
		navbar_string += "	<h4>"+filename_to_title(subdir.name)+"</h4>\n"
		navbar_string += "<ul>"
		for file in subdir.files:
			navbar_string += "\n"
			#navbar_string += "<hr/>"
			#navbar_string += "\n"
			navbar_string += "	<li><a href='../" + subdir.name + "/" + file.name +"'>"+filename_to_title(file.name)+"</a></li>"
			navbar_string += "\n"
		#navbar_string += "</div\n>"
		navbar_string += "</ul>"

	navbar_string += "</div>\n"


	for subdir in subdirs:
		subdir.print()
		# Make output directory
		output_subdir = Path("./output/" + dir.name + "/" + subdir.name)
		output_subdir.mkdir(parents=True, exist_ok=True)

		# Copy stylesheet file
		shutil.copy(os.getcwd() + "/pages/style.css", os.getcwd() + "/output/" + dir.name + "/" + subdir.name)

		for file in subdir.files:
			#navbar_string_copy = navbar_string
			# TODO(aidan): set the right link as selected
			navbar_string_copy = navbar_string.replace(">"+filename_to_title(file.name), " class='selected'>"+filename_to_title(file.name))
#			for line in iter(navbar_string_copy.splitlines()):
#				if file.name in line:
#					line = "<h1>AAAAAA</h1>"

			file_path = "pages/" + dir.name + "/" + file.parent.name + "/" + file.name
			file_title = filename_to_title(file.name)
			# Copy file to output
			file_str = ""
			with Path(file_path).open('r') as f:
				for line in f:
					file_str += line

			output_file_path = "output/" + dir.name + "/" + file.parent.name + "/" + file.name
			Path(output_file_path).touch()
			with Path(output_file_path).open('w') as f:
				f.write('<!doctype html>\n<html>\n\n<head>\n<link rel="stylesheet" href="style.css">\n<meta charset="utf-8"/>\n</head>\n\n<body>')
				f.write("\n")
				f.write(navbar_string_copy)
				f.write("\n")
				f.write('<div id="main">\n')
				f.write("\n")
				f.write(file_str)
				f.write("\n")
				f.write('</div>\n</body>\n</html>\n')
			#}
		#}
	#}

def build_main_page():
	print("Building main page")





print("Hi!")
print("I'm now making the site...")

main_dirs = [x for x in pages_dir.iterdir() if x.is_dir()]
for dir in main_dirs:
	build_main_dir(dir)

print("And it's been made! Thank you for your service!")

# NOTES
# Main -> Art -> Painting -> Rene
# Basically main folders have subfolders which only have files
# Main index lists main folders
# main folders have lists of their sub-folders and the files inside those
