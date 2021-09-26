# Song-screenshot-to-Spotify-playlist
This program converts an image containing song names and artists names to a Spotify playlist.

Installation:
	Requirements:
      •	Pytesseract must be installed on your machine, follow the instructions to install here: https://medium.com/@marioruizgonzalez.mx/how-install-tesseract-orc-and-               pytesseract-on-windows-68f011ad8b9b 
      •	The location of the tesseract.exe file must be as follows: C:\Program Files\Tesseract-OCR\tesseract.exe
      •	Client ID and Secret Key obtained through: https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app 
      •	Image containing a list of songs and their respective artist names (an example is provided)
      
      Copy code into IDE

Usage:
Open your python IDE of choice (I used pycharm). 
Open code in the IDE.
After obtaining the Spotify client id and Spotify secret key, put them in the variables named “SPOTIFY_CLIENT_ID” and “SPOTIFY_SECRET_KEY” on lines 8 and 9.
Run.
Follow on screen instructions.

Where to find playlist id:
After naming it, go to the Spotify client and find your new playlist. Click on share and copy the link and paste it in a text editor. The link should look something like this: https://open.spotify.com/playlist/1aXVp4IMjnVOpuWnRqdDSS?si=554a0dc2e7b84f5b 
The playlist id is 1aXVp4IMjnVOpuWnRqdDSS from the above link. It is always between the slash and question mark.

Where to find username:
On Spotify client click your profile then click on account. In account overview you should see your username.
 

Known issues:
Due to the OCR not always being able to recognise the text, sometimes it will crash if the text is converted incorrectly. 
To mitigate this issue I created a word document, used a large font size, wrote down the song and artist one at a time and problem was solved.

Shortcomings:
Due to the design of this program, one can only enter a screenshot with the following format:
Song name
Artist name



Example:
 
