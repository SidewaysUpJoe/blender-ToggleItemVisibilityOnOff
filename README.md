# HowTo/Tutorial Video 
https://youtu.be/68HoJy1cmM8


# Hide Items (Viewport and Render) based on TXT file
Install the add-on, head to 3D View and look through your Pannel TAB's for 'Cycle Items Visibility' (image below). Here you can specify the Start and End frame along with an Intervolt at which you want to hide your Objects or Collections along with the 'LOAD ITEMS FILE' button. When pressing the LOAD OBJECTS FILE button you can selet a text file with a list of Objects or Collection that you want to hide. The order of you list will be the order they are displyed (un-hidden). You can use a pipe ( | just above of enter key of your keyboard) to specify an Intervolt for that item. If you use the prefix [COL] before an item, that will specify the item is a Collection.


Text File Example:  
Plane|18  
Cube  
Cone|31  
Torus  
[COL]Test|20  


With that example; the Plane will be shown for 18 frames, the Cube (with out a | and Intervolt) will be show for what ever default value you have enteted into the pannel, the Cone for 31 frames, the Torus for default Intervolt and [COL]Test is a Collection which will be shown for 20 Intervolts.  


As of now this addon is NOT layer spcific, it will effects items in all layers.  


## Know Issue(s):
If you select a Collection to be hidden, you can NOT select any Items(s) with-in that Collection to be also hidden. When the script hides the collection it also hides everything in it, hence all objects including any you specify in your TXT file. Being this script runs during rendering, i do not see any effectnet way around this.
So, you can hide any Object and hide any Collection, but you can not hide a Collection and also hide an Object in that Collection.


# TODO
Add an option to the text file to incorate a frame span  
EXAMPLE:  
Plane|{15-32}

Panel Tab  
![Panel Tab Image](https://i.imgur.com/j1R1A0Z.png)
