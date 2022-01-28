import os
CHROME_PROFILE_PATH = f"user-data-dir=C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Wtsp"

# Windows 7, 8.1, and 10: C:\\Users\\{os.getlogin()\\AppData\\Local\\Google\\Chrome\\User Data\\Default
# Mac OS X El Capitan: Users/{os.getlogin()/Library/Application Support/Google/Chrome/Default
# Linux: /home/{os.getlogin()/.config/google-chrome/default