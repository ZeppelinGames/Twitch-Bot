# Twitch Bot
 A simple GUI Twitch bot made in Python 3.8 with IntelliJ

**How to use**
**Connecting to your stream**
Launch the program using Python
Enter your authentification token (not password, can get from https://twitchapps.com/tmi/)
Enter in your stream's channel name
Press 'Update Info'
Press 'Connect'

**Editing bot data**
Locate the 'botData.json' file
To change the command prefix edit the string after the "command-prefix" tag.

**To add commands:**
Find the "commands" tag
Add your new command keyword in quotation marks followed by a colon.
Add your response to the keyword on the same line in qutoes 
*(Format "command" : "response")*

**To add blacklisted words:**
Find the "banned-words" tag.
Add words into the square brackets in quotes



**Features**
Simple to use GUI
Editable command prefix
Easy to edit/add commands
Easy to edit/add words to blacklist
