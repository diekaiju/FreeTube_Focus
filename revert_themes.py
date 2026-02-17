
import re

file_path = 'src/renderer/themes.css'

with open(file_path, 'r') as f:
    content = f.read()

# Define mapping for specific themes
# Format: class_name: (icon, text)
theme_map = {
    'nordic': ('iconNordicLightSmall.svg', 'textNordicLightSmall.svg'),
    'hotPink': ('iconWhiteSmall.svg', 'textWhiteSmall.svg'),
    'pastelPink': ('iconBlackSmall.svg', 'textBlackSmall.svg'),
    'catppuccinMocha': ('iconCatppuccinMochaLightSmall.svg', 'textCatppuccinMochaLightSmall.svg'),
    'dracula': ('iconDraculaLightSmall.svg', 'textDraculaLightSmall.svg'),
    'solarizedDark': ('iconSolarizedLightSmall.svg', 'textSolarizedLightSmall.svg'),
    'solarizedLight': ('iconSolarizedDarkSmall.svg', 'textSolarizedDarkSmall.svg'),
    'gruvboxDark': ('iconGruvboxLightSmall.svg', 'textGruvboxLightSmall.svg'),
    'gruvboxLight': ('iconGruvboxDarkSmall.svg', 'textGruvboxDarkSmall.svg'),
    'catppuccinFrappe': ('iconCatppuccinFrappeLightSmall.svg', 'textCatppuccinFrappeLightSmall.svg'),
    'everforestDarkHard': ('iconEverforestLightHardSmall.svg', 'textEverforestLightHardSmall.svg'),
    'everforestDarkMedium': ('iconEverforestLightMediumSmall.svg', 'textEverforestLightMediumSmall.svg'),
    'everforestDarkLow': ('iconEverforestLightLowSmall.svg', 'textEverforestLightLowSmall.svg'),
    'everforestLightHard': ('iconEverforestDarkHardSmall.svg', 'textEverforestDarkHardSmall.svg'),
    'everforestLightMedium': ('iconEverforestDarkMediumSmall.svg', 'textEverforestDarkMediumSmall.svg'),
    'everforestLightLow': ('iconEverforestDarkLowSmall.svg', 'textEverforestDarkLowSmall.svg'),
    'catppuccinLatte': ('iconCatppuccinLatteDarkSmall.svg', 'textCatppuccinLatteDarkSmall.svg'),
}

# Mapping for primary color blocks
# These usually inherit or set specific ones.
# .mainRed etc set --logo-icon/text-bar-color usually, but let's check if they set the main logo vars.
# Based on the file content I saw, they modify --logo-icon-bar-color, not --logo-icon.
# But I modified ALL occurrences of --logo-icon: ...
# Let's check the bottom of the file where .mainRed is defined.

# Revert the main default block (Light/Dark/Black together)
# Lines 72-74 in the provided file view.
# It matches .system... .light ... .dark ... .black
default_block_pattern = r'(\.system\[data-system-theme\*=\'light\'\],\s*\.light,\s*\.system\[data-system-theme\*=\'dark\'\],\s*\.dark,\s*\.black\s*\{[^}]*?)(--logo-icon:\s*none;)(\s*--logo-text:\s*url\(\'../../_icons/logoColor.png\'\);)(\s*--logo-icon-display:\s*none;)'

def default_replacer(match):
    prefix = match.group(1)
    return f"{prefix}--logo-icon: url('../../_icons/iconColorSmall.svg');\n  --logo-text: url('../../_icons/textColorSmall.svg');"

content = re.sub(default_block_pattern, default_replacer, content, flags=re.DOTALL)


# Function to replace for specific themes
for theme, (icon, text) in theme_map.items():
    # Pattern to match the theme block and the modified logo lines inside it
    # We look for the class name, then correct brace opening, then find the logo definitions
    pattern = r'(\.' + theme + r'\s*\{[^}]*?)(--logo-icon:\s*none;)(\s*--logo-text:\s*url\(\'../../_icons/logoColor.png\'\);)(\s*--logo-icon-display:\s*none;)'

    def replacer(match, ico=icon, txt=text):
        prefix = match.group(1)
        return f"{prefix}--logo-icon: url('../../_icons/{ico}');\n  --logo-text: url('../../_icons/{txt}');"

    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

# Also handle the primary theme color definitions if they were modified.
# The `sed` command modified "--logo-icon-bar-color".
# "s|--logo-icon-bar-color: url('../../_icons/icon.*.svg');|--logo-icon-bar-color: none;|g"
# "s|--logo-text-bar-color: url('../../_icons/text.*.svg');|--logo-text-bar-color: url('../../_icons/logoColor.png');|g"

# Reverting these:
# Map .mainRed, etc to iconWhiteSmall/textWhiteSmall
dark_bg_pattern = r'(\.mainRed,|\.mainPink,|\.mainPurple,|\.mainDeepPurple,|\.mainIndigo,|\.mainBlue,|\.mainLightBlue,|\.mainCyan,|\.mainTeal,|\.mainGreen\s*\{[^}]*?)(--logo-icon-bar-color:\s*none;)'
def dark_bg_repl(match):
    return f"{match.group(1)}--logo-icon-bar-color: url('../../_icons/iconWhiteSmall.svg');"
content = re.sub(dark_bg_pattern, dark_bg_repl, content, flags=re.DOTALL)

dark_bg_text_pattern = r'(\.mainRed,|\.mainPink,|\.mainPurple,|\.mainDeepPurple,|\.mainIndigo,|\.mainBlue,|\.mainLightBlue,|\.mainCyan,|\.mainTeal,|\.mainGreen\s*\{[^}]*?)(--logo-text-bar-color:\s*url\(\'../../_icons/logoColor.png\'\);)'
def dark_bg_text_repl(match):
    return f"{match.group(1)}--logo-text-bar-color: url('../../_icons/textWhiteSmall.svg');"
content = re.sub(dark_bg_text_pattern, dark_bg_text_repl, content, flags=re.DOTALL)

# Map light bg colors (.mainLightGreen, etc) to iconBlackSmall/textBlackSmall
light_bg_pattern = r'(\.mainLightGreen,|\.mainLime,|\.mainYellow,|\.mainAmber,|\.mainOrange,|\.mainDeepOrange\s*\{[^}]*?)(--logo-icon-bar-color:\s*none;)'
def light_bg_repl(match):
    return f"{match.group(1)}--logo-icon-bar-color: url('../../_icons/iconBlackSmall.svg');"
content = re.sub(light_bg_pattern, light_bg_repl, content, flags=re.DOTALL)

light_bg_text_pattern = r'(\.mainLightGreen,|\.mainLime,|\.mainYellow,|\.mainAmber,|\.mainOrange,|\.mainDeepOrange\s*\{[^}]*?)(--logo-text-bar-color:\s*url\(\'../../_icons/logoColor.png\'\);)'
def light_bg_text_repl(match):
    return f"{match.group(1)}--logo-text-bar-color: url('../../_icons/textBlackSmall.svg');"
content = re.sub(light_bg_text_pattern, light_bg_text_repl, content, flags=re.DOTALL)


# Map Catppuccin Mocha colors
cat_pattern = r'(\.mainCatppuccinMochaRosewater,[\s\S]*?\.mainCatppuccinMochaLavender\s*\{[^}]*?)(--logo-icon-bar-color:\s*none;)'
def cat_repl(match):
    return f"{match.group(1)}--logo-icon-bar-color: url('../../_icons/iconCatppuccinMochaDarkSmall.svg');"
content = re.sub(cat_pattern, cat_repl, content, flags=re.DOTALL)

cat_text_pattern = r'(\.mainCatppuccinMochaRosewater,[\s\S]*?\.mainCatppuccinMochaLavender\s*\{[^}]*?)(--logo-text-bar-color:\s*url\(\'../../_icons/logoColor.png\'\);)'
def cat_text_repl(match):
    return f"{match.group(1)}--logo-text-bar-color: url('../../_icons/textCatppuccinMochaDarkSmall.svg');"
content = re.sub(cat_text_pattern, cat_text_repl, content, flags=re.DOTALL)


with open(file_path, 'w') as f:
    f.write(content)
