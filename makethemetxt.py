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
	font = "Unknown Regular 16"
	color = "white"
}

"""

template = """
+ boot_menu {{
	left = 50%-600
	top = 32%
	width = 50%+600
	height = 68%

	item_font = "DoomShade Regular shade{0} {2}"
	item_color = "{0}, 0, 0"
	selected_item_color = "{1}, 0, 0"
	item_height = {3}
	item_padding = 0
	item_spacing = {4}
	
	icon_width = 0
	item_icon_space = {5}
	
	selected_item_pixmap_style = "icon{2}_*.png"
}}
"""

darker = 40

graustufen = 8
posterization_range = 256 // graustufen

pxsize: int = 5
font_size = 17*pxsize
item_height = 19*pxsize
item_spacing = item_height - 16 * pxsize
item_icon_space = 12 * pxsize

# inverse direction
for i in range(graustufen)[::-1]:
    val = posterization_range//2 + i * posterization_range
    val_selected = (val-darker) if val >= darker else 0
    theme += template.format(val, val_selected, font_size, item_height, item_spacing, item_icon_space)
    pass

print(theme)

with open("./doomgrub_theme/theme.txt", "w") as f:

    f.write(theme)


