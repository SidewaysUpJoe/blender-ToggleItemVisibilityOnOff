

from . import toggleopjectsOnOff


bl_info = {
    "name": "Cycle Item Visibility on/off",
    "author": "SidewaysUp Joe",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View - Right Panel - 'N' button",
    "description": "Load a list of Objects (and Collections) from a text file and have there Visibility toggled on/off during timeline play",
    "warning": "",
    "wiki_url": "https://github.com/SidewaysUpJoe/blender-ToggleItemVisibilityOnOff/wiki",
    "tracker_url": "https://github.com/SidewaysUpJoe/blender-ToggleItemVisibilityOnOff/issues",
    'support': 'COMMUNITY',
    "category": "3D VIEW",
}  

def register(): 
    toggleopjectsOnOff.register()    
    #print("registered init")
    

def unregister():
    toggleopjectsOnOff.unregister()
    #print("unregistered init")
    
     
if __name__ == "__main__":
    register()
