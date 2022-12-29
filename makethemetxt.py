import os, glob

theme = """
# Global
title-text: ""
desktop-image: "background.png"
terminal-font: "Unknown Regular 16"

+ label {
	id = "__timeout__"
	left = 30
	top = 90%
	height = 50
	width = 50%
	
	text = "Executing option in %d seconds"
	font = "Unifont Regular 16"
	color = "white"
}

"""

template = f"""
+ boot_menu {{
	left = 50%-600
	top = 200
	width = 1200
	height = 800

	item_font = "DoomShade Regular shade{0} {font_size}"
	item_color = "{0}, 0, 0"
	selected_item_color = "{1}, 0, 0"
	item_height = 108
	item_padding = 0
	item_spacing = 0
	
	icon_width = 120
	icon_height = 120
	item_icon_space = 72
}}
"""

darker = 40

graustufen = 16
posterization_range = 256 // graustufen

font_size = 102

# inverse direction
for i in range(graustufen)[::-1]:
    val = posterization_range//2 + i * posterization_range
    theme += template.format(val, (val-darker) if val >= darker else 0, font_size)
    pass

print(theme)

with open("./doomgrub_theme/theme.txt", "w") as f:

    f.write(theme)


