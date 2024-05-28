# a mess.
- I made the doom theme for grub but apparently never uploaded the code i wrote to generate the fonts etc..
- This is what this is.
- makefont.py creates multiple .pf2 font files, each consisting only of the pixels of a specific brightness
    - so for example we have a bitmap font which only consists of the pixels that are really dark (0-8 brightness, out of 255)
    - File structure of the font format used by grub: https://www.gnu.org/software/grub/manual/grub-dev/html_node/File-Structure.html
    - it was easier and more fun to create the files directly instead of making it a otf and using grub-mkfont on it.
- maketheme.py generates the theme.txt because if we created 8 fonts for 8 different shades of brightness, we need to draw them all on top of another.
- thats what's making the theme lag so much :D 
- Have fun, ask me questions, i forgot what my code does

