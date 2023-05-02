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


non_cap_words = ["the", "an", "a", "at", "by", "to", "and", "but", "for", "and", "as", "as" "," "as", "at", "but", "by", "if", "for", "from", "if", "in", "into", "like", "near", "now", "nor", "of", "off", "on", "once", "onto", "or", "of", "over", "past", "so", "so", "than", "that", "till", "to", "up", "upon", "with", "when", "yet"] # TODO(cheryl): Add and handle multi-words
def filename_to_title(string):
	# TODO(cheryl): handle hyphens and capitalization
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
	subdir_files = [x for x in dir.iterdir() if x.is_file()]

	# Build!!!
	# ==============

	# Make output directory
	output_dir = Path("./output")
	output_dir.mkdir(parents=True, exist_ok=True)

	# Create generic navbar - we'll highlight later
	navbar_string = "<div id=navbar>\n"
	navbar_string += "<ol>\n"
	navbar_string += "	<li class=navbar_title>Aidan Foley<span style=color:#aaa;> | PLACEHOLDER TITLE</span></li>\n"
	for file in subdir_files:
		navbar_string += "	<li class=navbar_item><a href='./" + file.name +"'>"+filename_to_title(file.name)+"</a></li>"
		navbar_string += "\n"

	navbar_string += "<button id='toggle_dark_mode_button' class='emoji_button' onclick='toggle_dark_mode()'>🌞</button>"
	navbar_string += "</ol>"
	navbar_string += "</div>\n"
	navbar_string += "<div id=navbar_shadow>"
	navbar_string += "</div>"

	for file in subdir_files:
		#navbar_string_copy = navbar_string
		#navbar_string_copy = navbar_string.replace(">"+filename_to_title(file.name), " class='selected'>"+filename_to_title(file.name))
		navbar_string_copy = navbar_string.replace("<a href='./" + file.name + "'>" + filename_to_title(file.name) + "</a>", "<span>"+filename_to_title(file.name) + "</span>")
		navbar_string_copy = navbar_string_copy.replace("PLACEHOLDER TITLE", filename_to_title(file.name))
		navbar_string_copy = navbar_string_copy.replace("Index", "About Me")
		navbar_string_copy = navbar_string_copy.replace("Resume", "Résumé")

		file_path = "pages/" + file.name
		file_title = filename_to_title(file.name)
		# Copy file to output
		file_str = ""
		with Path(file_path).open('r') as f:
			for line in f:
				file_str += line

		output_file_path = "output/" + file.name
		Path(output_file_path).touch()
		with Path(output_file_path).open('w') as f:
			header_str = ""
			with Path("./header.html").open('r') as header:
				for line in header:
					header_str += line
			f.write(header_str)

			f.write(navbar_string_copy)
			f.write('<div id="main">\n')

			f.write(file_str)

			footer_str = ""
			with Path("./footer.html").open('r') as footer:
				for line in footer: 
					footer_str += line
			f.write(footer_str)

				#f.write('<!doctype html>\n<html>\n\n<head>\n<link rel="stylesheet" href="style.css">\n<meta charset="utf-8"/>\n</head>\n\n<body>')
				#f.write("\n")

				#f.write("\n<script>")
				##f.write("div.classList.remove('dark_mode');")
				#f.write("function myFunction() {\n")
				#f.write("var element = document.body;\n")
				#f.write("element.classList.toggle('dark-mode');\n")
				##f.write("document.cookie = 'dark_mode=true'")
				#f.write("}\n")
				#f.write("</script>\n\n")


				#f.write(navbar_string_copy)
				#f.write("\n")
				#f.write('<div id="main">\n')
				#f.write("\n")
				#f.write(file_str)
				#f.write("\n")
				#f.write('</div>\n</body>\n</html>\n')
		#}
	#}
#}

def build_main_page():
	print("Building main page")





print("Hi!")
print("I'm now making the site...")

main_dirs = [x for x in pages_dir.iterdir() if x.is_dir()]
build_main_dir(pages_dir)

print("And it's been made! Thank you for your service!")

# NOTES
# Main -> Art -> Painting -> Rene
# Basically main folders have subfolders which only have files
# Main index lists main folders
# main folders have lists of their sub-folders and the files inside those
