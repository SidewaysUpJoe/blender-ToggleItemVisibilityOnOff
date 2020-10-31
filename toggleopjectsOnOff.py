import bpy
from bpy import context

from bpy.app.handlers import persistent
#from bpy.app import handlers

from bpy.props import BoolProperty, StringProperty, PointerProperty, FloatProperty
from bpy.types import (Panel,
					   Operator,
					   PropertyGroup,
					   )
from bpy.utils import register_class, unregister_class

import os
import re
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator


class CycleObjectVisibilitySettings(PropertyGroup):	
	bl_idname = __package__
	
	cov_enabled_bool: BoolProperty(
		name="ENABLE",
		description="On / Off",
		default = False,
		)
	
	cov_sFrame: StringProperty(
		name="START FRAME",
		description="Frame to start Visibility Cycle",
		default = '10',
		)
		
	cov_eFrame: StringProperty(
		name="END FRAME",
		description="Frame to end Visibility Cycle",
		default = '200',
		)
		
	cov_iFrame: StringProperty(
		name="INTERVOLT FRAMES",
		description="Intervolt of frame to toggle",
		default = "25",
		)
		
		
class CycleObjectVisibility_Panel(Panel):
	bl_idname = "OBJECT_PT_cycle_object_panel"
	bl_label = "Cycle Item Visibility" # lable shown with TAB clicked
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Cycle Item Visibility" # name displayed in TAB
	
	@classmethod 
	def poll(self,context):
		return True
	
	def draw(self, context):
		
		layout = self.layout
		scene = context.scene
		CycleObjectVisibilityPanel = scene.COV_Tool
		
		layout.prop(CycleObjectVisibilityPanel, "cov_enabled_bool")
		layout.prop(CycleObjectVisibilityPanel, "cov_sFrame")
		layout.prop(CycleObjectVisibilityPanel, "cov_eFrame")
		layout.prop(CycleObjectVisibilityPanel, "cov_iFrame")
		
		layout.operator("cov.open_filebrowser", text="LOAD ITEMS FILE", icon='OBJECT_DATA')


class OBJECTS_SELECTED_PANEL(bpy.types.Panel):
	bl_idname = "OBJECT_PT_objectsselected"
	bl_label = "ITEMS SELECTED"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Cycle Item Visibility" # name displayed in TAB
	#bl_options = {"DEFAULT_CLOSED"}

	def draw(self, context):
		layout = self.layout
		
		for obj_toggle in cov_varSettings.objToggles:
			layout.label(text=obj_toggle[0] + ' (' + str(obj_toggle[3]) + ') ' + str(obj_toggle[1]))
		
		return {'FINISHED'}
			
 
# https://sinestesia.co/blog/tutorials/using-blenders-filebrowser-with-python/  
class OT_OpenFilebrowser(Operator, ImportHelper):

	bl_idname = "cov.open_filebrowser"
	bl_label = "Load Object File"
	
	filter_glob: StringProperty(
		default='*.txt',
		options={'HIDDEN'}
	)
	
	#some_boolean: BoolProperty(
		#name='Do a thing',
		#description='Do a thing with the file you\'ve selected',
		#default=True,
	#)

	def execute(self, context):
		#filename, extension = os.path.splitext(self.filepath)
		cov_fillObjList(self.filepath)
		return {'FINISHED'}
		



def cov_fillObjList(fPath):
	cov = cov_varSettings
	
	f = open(fPath, 'r') 
	Lines = f.readlines() 
	f.close()
	
	cov_clear()
	badNameList = ''
	
	for line in Lines:
		l = line.strip()
		l = l.strip()
		
		lArr = l.split('|')
		name = lArr[0].strip()
		typeIs = '' # obj/col
		interType = '' # span/single
		
		
		# check if array has two elements indicating a frame intervolt was set
		if  len(lArr) == 1: 
			intervolt = 0
		else:
			intervolt = lArr[1].strip()
		
		
		if name != '':
			
			# Cone|{25-50}
			regexp = re.compile('(\{*-*\})')
			if re.search(regexp, str(intervolt)):
				interType = 'span'
				intervolt = 0 # TODO : frame span not finshed
			else:
				interType = 'single'
			
			
			if name[0:5] == "[COL]":
				typeIs = 'col'
			else:
				typeIs = 'obj'
			
			name = name.replace('[COL]', '')
			name = name.strip()
			
			intervolt = int(intervolt) # TODO : frame span not finshed
			
			colFound = False
			for col in bpy.data.collections:
				if name == col.name:
					cov.objToggles.append([name, typeIs, interType, intervolt])# add
					colFound = True
					break
				
			if colFound:
				continue
				
			# check to make sure object is found in scene	
			if not bpy.context.scene.objects.get(name):
				badNameList = badNameList + '\n - ' + name 
			else:
				cov.objToggles.append([name, typeIs, interType, intervolt])# add
	
	# call sub panel to list off found objects
	OBJECTS_SELECTED_PANEL
	
	# send msbox for non-found objects
	if badNameList != "":
		ShowMessageBox("You have Name(s) in your TXT file that could not be found in your scene:" + badNameList + "\nItems found will be added to your 'OBJECTS SELECTED' List")
	
	return {'FINISHED'}



def ShowMessageBox(message = "", title = "Ooooh Noooo...", icon = 'ERROR'):
	
	def draw(self, context):
		lines = message.split('\n')
		for l in lines:
			self.layout.label(text=l)

	bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


class cov_varSettings():
	interVolt_new = 0
	interVolt_ChangeAt = 0
	interVolt_index = 0
	interVolt_DefaultLoop = False
	objToggles = []


def objsDefault():
	cov = cov_varSettings
	
	# do a check, no need to keep looping and un-hiding when not needed
	if cov.interVolt_DefaultLoop == False:
		return {'FINISHED'}
		
	#print("objsDefault")
	cov.interVolt_new = 0
	cov.interVolt_ChangeAt = 0
	cov.interVolt_index = 0
	
	for col_toggle in cov.objToggles:
		if col_toggle[1] == 'obj':
			bpy.data.objects[col_toggle[0]].hide_viewport = False
			bpy.data.objects[col_toggle[0]].hide_render = False
		else:
			bpy.data.collections[col_toggle[0]].hide_viewport = False
			bpy.data.collections[col_toggle[0]].hide_render = False
	
	cov.interVolt_DefaultLoop = False
	return {'FINISHED'}
	
			
			
def cov_clear():
	
	cov = cov_varSettings
	cov.interVolt_DefaultLoop = True

	objsDefault()

	cov.interVolt_new = 0
	cov.interVolt_ChangeAt = 0
	cov.interVolt_index = 0
	cov.objToggles.clear()
	#print(" CLEAR COV")

	return {'FINISHED'}
	
			   
@persistent
def monitorSceneTimelinePost(scene):
	test = bpy.context.window.screen.is_animation_playing
	
	if test == False :
		#print("ANIMATION STOPPED")
		cov_varSettings.interVolt_DefaultLoop = True
		objsDefault()
	
	
	
@persistent
def monitorSceneTimeline(scene):
	
	# check to see if Enabled
	CycleObjectVisibilityPanel = scene.COV_Tool
	changeOn = CycleObjectVisibilityPanel.cov_enabled_bool
	if changeOn == False :
		return {'FINISHED'}
		
	# if array list empty, no need to go any farther
	if len(cov_varSettings.objToggles) <= 0:
		return {'FINISHED'}
	
	cov = cov_varSettings # class name shortened
	
	currentFrame = int(bpy.data.scenes['Scene'].frame_current)
	sFrame = int(CycleObjectVisibilityPanel.cov_sFrame)
	eFrame = int(CycleObjectVisibilityPanel.cov_eFrame)
	iFrame = int(CycleObjectVisibilityPanel.cov_iFrame)
	
	
	if currentFrame >= sFrame and currentFrame <= eFrame:
		cov.interVolt_DefaultLoop = True
		
		# Double Check, when time line first starts some COV settings need alittle help
		if cov.interVolt_ChangeAt == 0:
			cov.interVolt_ChangeAt = int(iFrame + currentFrame)
			cov.interVolt_index = -1
			
		
		#print("interVolt_index " + str(cov.interVolt_index))
		#print(cov.objToggles[cov.interVolt_index][0] + ' currentFrame = ' + str(currentFrame) + ' interVolt_ChangeAt = ' + str(cov.interVolt_ChangeAt) + ' New = ' + str(cov.interVolt_new))
		
		if currentFrame >= cov.interVolt_ChangeAt:
			#print("CHANGED")
			
			cov.interVolt_index = (cov.interVolt_index + 1)
			
			# check that the Index do not excede array list size
			# if so, reset to first item
			if cov.interVolt_index >= len(cov.objToggles):
				cov.interVolt_index = 0
			
			
			cov.interVolt_new = iFrame
			
			# check and see if obj has its own Intervolt
			if cov.objToggles[cov.interVolt_index][3] > 0:
				cov.interVolt_new = cov.objToggles[cov.interVolt_index][3]
			
			
			cov.interVolt_ChangeAt = int(cov.interVolt_new + currentFrame)			
			
			# LOOP THROUGH LIST AND HIDE EVERYTHING
			for obj_toggle in cov.objToggles:
				if obj_toggle[1] == 'obj':
					bpy.data.objects[obj_toggle[0]].hide_viewport = True
					bpy.data.objects[obj_toggle[0]].hide_render = True
				else:
					bpy.data.collections[obj_toggle[0]].hide_viewport = True
					bpy.data.collections[obj_toggle[0]].hide_render = True
					
			
			
			# unHide current index
			if cov.objToggles[cov.interVolt_index][1] == 'obj':
				bpy.data.objects[cov.objToggles[cov.interVolt_index][0]] .hide_viewport = False
				bpy.data.objects[cov.objToggles[cov.interVolt_index][0]] .hide_render = False
			else:
				bpy.data.collections[cov.objToggles[cov.interVolt_index][0]].hide_viewport = False
				bpy.data.collections[cov.objToggles[cov.interVolt_index][0]].hide_render = False
			

	
	else:
		objsDefault()
	
		
classes = (
	CycleObjectVisibilitySettings, 
	CycleObjectVisibility_Panel,
	OT_OpenFilebrowser, 
	OBJECTS_SELECTED_PANEL
)

			
def register():
	for cls in classes:
		register_class(cls)
	bpy.types.Scene.COV_Tool = bpy.props.PointerProperty(type=CycleObjectVisibilitySettings)
	
	cov_clear()
	
	bpy.app.handlers.frame_change_pre.clear()
	bpy.app.handlers.frame_change_post.clear()
	
	bpy.app.handlers.frame_change_pre.append(monitorSceneTimeline)
	bpy.app.handlers.frame_change_post.append(monitorSceneTimelinePost)
	
	#print(" Registered Worker")
	

def unregister():
	for cls in classes:
		unregister_class(cls)
		
	del bpy.types.Scene.COV_Tool
	
	cov_clear()
	#print("unregistered worker")


if __name__ == "__main__":
	register()




