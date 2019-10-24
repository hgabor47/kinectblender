bl_info = {
    "name": "Kinect Data Import Addon",
    "author": "Michal Polcer",
    "version": (1, 0),
    "blender": (2, 6, 3),
    "api": 35622,
    "location": "Toolbar > Kinect Data Import",
    "description": "",
    "category": "Animation",
    'wiki_url': '',
    'tracker_url': ''
    }

import bpy
from bpy import data as bpy_data
from bpy.types import Scene as bpy_types_Scene
from bpy.props import *
import socket
import math

def returnObjectByName (passedName= ""):
    r = None
    obs = bpy_data.objects
    for ob in obs:
        if ob.name == passedName:
            r = ob
    return r

obs = bpy.data.objects

def setData(objects, bone_name, quat):
    if bone_name in objects.keys():
        if bone_name == "HipCenter":
            objects[bone_name].location = (float(quat[0]*1),float(-quat[2]*1),float(quat[1]*1)+bpy.context.scene.ki_rootheight)
            objects[bone_name].keyframe_insert(data_path="location")
            
        if bone_name == "Head" :
            objects[bone_name].rotation_quaternion = (float(quat[3]),float(quat[4]),float(-quat[6]),float(-quat[5]))
            objects[bone_name].keyframe_insert(data_path="rotation_quaternion")
        elif bone_name =="ElbowLeft" or bone_name =="WristLeft" or bone_name =="HandLeft" or bone_name == "ElbowRight" or bone_name == "WristRight" or bone_name=="HandRight" or bone_name == "KneeLeft" or bone_name =="AnkleLeft" or bone_name =="FootLeft" or bone_name == "KneeRight" or bone_name =="AnkleRight" or bone_name =="FootRight":
            objects[bone_name].rotation_quaternion = (float(quat[3]),float(quat[4]),float(-quat[6]),float(quat[5]))
            objects[bone_name].keyframe_insert(data_path="rotation_quaternion")
        elif bone_name == "HipLeft" or bone_name== "HipRight":
            objects[bone_name].rotation_quaternion = (0,0,0,0)
            objects[bone_name].keyframe_insert(data_path="rotation_quaternion")
        else:
            objects[bone_name].rotation_quaternion = (float(quat[3]),float(quat[4]),float(-quat[6]),float(quat[5]))
            objects[bone_name].keyframe_insert(data_path="rotation_quaternion")
            
            
class UDPserver():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        self.sock.bind(("127.0.0.1", 10124))
        print("Start receiving on UDP port 10124")

    def __del__(self):
        self.sock.close()
        print("Stop receiving on UDP port 10124")


    def receive(self, objects,setdata):
        dict = {}

        try:
            data = self.sock.recv(2048)
        except:
            return{'PASS_THROUGH'}
        temp = data
        while(True):
            data = temp
            list = str(data).split(';')
            for item in list:
                bone = item.split()
                if bone[0]=="b'HipCenter":
                    bone_name = "HipCenter"
                else:    
                    bone_name=bone[0]
                quat=(float(bone[1]),float(bone[2]),float(bone[3]),float(bone[4]),float(bone[5]),float(bone[6]),float(bone[7]))
                dict[bone_name] = quat
                
            try:
                temp = self.sock.recv(1024)
            except:
                break

        for key,value in dict.items():
            setdata(objects,key,value)
            

bpy.types.Scene.ki_arms = BoolProperty(
    name = "Arms", 
    description = "Arms are connected?")
bpy.types.Scene.ki_neck = BoolProperty(
    name = "Neck", 
    description = "Neck are connected?")
bpy.types.Scene.ki_armaturename= StringProperty(
    name = "Armature name", 
    default = "woman2",
    description = "Which armature will connect?")    
bpy.types.Scene.ki_hands = BoolProperty(
    name = "Hands", 
    description = "Hands are connected?")
bpy.types.Scene.ki_influence = FloatProperty(
    name = "Influence", 
    default = 1.0,
    min = 0, max = 1.0,
    description = "Connections power?")
bpy.types.Scene.ki_rootheight = FloatProperty(
    name = "Root Height", 
    default = 0.86,
    min = 0, max = 2.0,
    description = "Root Height?")
bpy.types.Scene.ki_transform = BoolProperty(
    name = "Transform", 
    description = "Is transform several bones?")

scn = 0
        
class KDI_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Kinect Data Import"
   
    def draw(self, context):
        scn = context.scene
        layout = self.layout
        row = layout.row()
        col = layout.column()
        col.enabled = not KDI_start_operator.enabled
      
        if (KDI_start_operator.enabled):
            layout.operator("wm.kinect_data_import_stop", text="Stop")
        else:
            layout.operator("wm.kinect_data_import_start", text="Start")
        layout.prop(scn, 'ki_armaturename')      
        layout.prop(scn, 'ki_rootheight')      
        layout.operator("wm.kinect_data_import_setup", text="Setup Skeleton")
        layout.prop(scn, 'ki_arms')      
        layout.prop(scn, 'ki_hands')      
        layout.prop(scn, 'ki_neck')      
        layout.prop(scn, 'ki_transform')      
        layout.prop(scn, 'ki_influence')      
        layout.split()
        layout.operator("wm.kinect_data_import_clear", text="Clear Skeleton")

class CustomDrawOperator(bpy.types.Operator):
    bl_idname = "object.custom_draw"
    bl_label = "Simple Modal Operator"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    my_float = bpy.props.FloatProperty(name="Float")
    my_bool = bpy.props.BoolProperty(name="Toggle Option")
    my_string = bpy.props.StringProperty(name="String Value")

    def execute(self, context):
        print()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Custom Interface!")

        row = col.row()
        row.prop(self, "my_float")
        row.prop(self, "my_bool")

        col.prop(self, "my_string")

bpy.utils.register_class(CustomDrawOperator)
bpy.ops.object.custom_draw('INVOKE_DEFAULT')


def removeConstraints(pBase):
    obs = pBase.constraints
    for ob in obs:
        if ((ob.name=="Copy_Rotation_Kinect") or (ob.name=="Copy_Location_Kinect")):
            obs.remove(ob)

def removeConstraintsRotation(amt,sFrom):
    pBase0 = amt.pose.bones[sFrom]
    removeConstraints(pBase0)
    
            
def addConstraintsRotation(amt,sFrom, sTo):
    pBase0 = amt.pose.bones[sFrom]
    removeConstraints(pBase0)
    cns3 = pBase0.constraints.new('COPY_ROTATION')
    cns3.name = 'Copy_Rotation_Kinect'
    cns3.target = bpy_data.objects[sTo] 
    cns3.subtarget = 'Bone'
    cns3.owner_space = 'WORLD'
    cns3.target_space = 'WORLD'
    cns3.influence = bpy.context.scene.ki_influence
    
def addConstraintsLocation(amt,sFrom, sTo):
    pBase0 = amt.pose.bones[sFrom]
    #removeConstraints(pBase0)
    cns3 = pBase0.constraints.new('COPY_LOCATION')
    cns3.name = 'Copy_Location_Kinect'
    cns3.target = bpy_data.objects[sTo] 
    cns3.subtarget = ''
    cns3.owner_space = 'WORLD'
    cns3.target_space = 'WORLD'
    cns3.influence = bpy.context.scene.ki_influence

class KDI_clear_operator(bpy.types.Operator):
    bl_label = "Kinect Data Import Start Operator"
    bl_idname = "wm.kinect_data_import_clear"
    
    def execute(self, context):

        amt = bpy_data.objects[bpy.context.scene.ki_armaturename]
        try:
            removeConstraintsRotation(amt,'RightArm')
            removeConstraintsRotation(amt,'RightForeArm')
            removeConstraintsRotation(amt,'RightHand')
            removeConstraintsRotation(amt,'RightUpLeg')
            removeConstraintsRotation(amt,'RightLeg')
            removeConstraintsRotation(amt,'RightFoot')

            removeConstraintsRotation(amt,'LeftArm')
            removeConstraintsRotation(amt,'LeftForeArm')
            removeConstraintsRotation(amt,'LeftHand')
            removeConstraintsRotation(amt,'LeftUpLeg')
            removeConstraintsRotation(amt,'LeftLeg')
            removeConstraintsRotation(amt,'LeftFoot')
            
            removeConstraintsRotation(amt,'Hips')
            removeConstraintsRotation(amt,'Spine')
            removeConstraintsRotation(amt,'Neck')
            arm = bpy_data.armatures[bpy.context.scene.ki_armaturename]
            try:
                arm.edit_bones['RightUpLeg'].roll = 10 * (math.pi*2 / 360)
            except:
                pass
            try:
                arm.edit_bones['RightLeg'].roll = 10 * (math.pi*2 / 360)
            except:
                pass
            try:
                arm.edit_bones['LeftUpLeg'].roll = -10 * (math.pi*2 / 360)
            except:
                pass
            try:
                arm.edit_bones['LeftLeg'].roll = -10 * (math.pi*2 / 360)
            except:
                pass
            try:
                arm.edit_bones['Neck'].roll = 0 * (math.pi*2 / 360)
            except:
                pass
        except:
            pass

        #anoher skeleton mekahuman
        try:
            removeConstraintsRotation(amt,'upper_arm.fk.R')
            removeConstraintsRotation(amt,'forearm.fk.R')
            removeConstraintsRotation(amt,'upper_arm.fk.L')
            removeConstraintsRotation(amt,'forearm.fk.L')

            
            removeConstraintsRotation(amt,'hand.fk.R',)
            removeConstraintsRotation(amt,'hand.fk.L',)

            removeConstraintsRotation(amt,'thigh.fk.R')
            removeConstraintsRotation(amt,'shin.fk.R')
            removeConstraintsRotation(amt,'foot.fk.R')
            removeConstraintsRotation(amt,'thigh.fk.L')
            removeConstraintsRotation(amt,'shin.fk.L')
            removeConstraintsRotation(amt,'foot.fk.L')
            removeConstraintsRotation(amt,'root')
            removeConstraintsRotation(amt,'chest')
            removeConstraintsRotation(amt,'neck')

            arm = bpy_data.armatures[bpy.context.scene.ki_armaturename]
            try:
                arm.edit_bones['thigh.fk.R'].roll = 9.18 * (math.pi*2 / 360)
            except:
                pass
            try:
                arm.edit_bones['shin.fk.R'].roll = 8.75 * (math.pi*2 / 360)
            except:
                pass
            try:
                arm.edit_bones['thigh.fk.L'].roll = -9.18 * (math.pi*2 / 360)
            except:
                pass
            try:
                arm.edit_bones['shin.fk.L'].roll = -8.75 * (math.pi*2 / 360)
            except:
                pass
            try:
                arm.edit_bones['neck'].roll = 0 * (math.pi*2 / 360)
            except:
                pass
        except:
            pass


        return {'RUNNING_MODAL'}
        

class KDI_setup_operator(bpy.types.Operator):
    bl_label = "Kinect Data Import Start Operator"
    bl_idname = "wm.kinect_data_import_setup"
    
    def execute(self, context):
        amt = bpy_data.objects[bpy.context.scene.ki_armaturename]
        
        try:
            if bpy.context.scene.ki_arms:
                addConstraintsRotation(amt,'RightArm',     'Armature.009')
                addConstraintsRotation(amt,'RightForeArm', 'Armature.010')
                addConstraintsRotation(amt,'LeftArm',      'Armature.005')
                addConstraintsRotation(amt,'LeftForeArm',  'Armature.006')

            if bpy.context.scene.ki_hands:
                addConstraintsRotation(amt,'RightHand',    'Armature.011')
                addConstraintsRotation(amt,'LeftHand',     'Armature.007')

            addConstraintsRotation(amt,'RightUpLeg',   'Armature.013')
            addConstraintsRotation(amt,'RightLeg',     'Armature.014')
            addConstraintsRotation(amt,'RightFoot',    'Armature.015')
            addConstraintsRotation(amt,'LeftUpLeg',    'Armature.017')
            addConstraintsRotation(amt,'LeftLeg',      'Armature.018')
            addConstraintsRotation(amt,'LeftFoot',     'Armature.019')
            addConstraintsRotation(amt,'Hips',     'HipCenter')
            addConstraintsLocation(amt,'Hips',     'HipCenter')
            addConstraintsRotation(amt,'Spine',     'Armature.002')
            
            if bpy.context.scene.ki_neck:
                addConstraintsRotation(amt,'Neck',     'Armature.003')


            
            if bpy.context.scene.ki_transform:
                arm = bpy_data.armatures[bpy.context.scene.ki_armaturename]
                try:
                    arm.edit_bones['RightUpLeg'].roll = 191 * (math.pi*2 / 360)
                except:
                    pass
                try:
                    arm.edit_bones['RightLeg'].roll = 191 * (math.pi*2 / 360)
                except:
                    pass
                try:
                    arm.edit_bones['LeftUpLeg'].roll = -191 * (math.pi*2 / 360)
                except:
                    pass
                try:
                    arm.edit_bones['LeftLeg'].roll = -191 * (math.pi*2 / 360)
                except:
                    pass
                try:
                    arm.edit_bones['Neck'].roll = 180 * (math.pi*2 / 360)
                except:
                    pass
        except:
            pass

        #SKELETON TYPE 2
        try:
            if bpy.context.scene.ki_arms:
                addConstraintsRotation(amt,'upper_arm.fk.R',     'Armature.009')
                addConstraintsRotation(amt,'forearm.fk.R', 'Armature.010')
                addConstraintsRotation(amt,'upper_arm.fk.L',      'Armature.005')
                addConstraintsRotation(amt,'forearm.fk.L',  'Armature.006')

            if bpy.context.scene.ki_hands:
                addConstraintsRotation(amt,'hand.fk.R',    'Armature.011')
                addConstraintsRotation(amt,'hand.fk.L',     'Armature.007')

            addConstraintsRotation(amt,'thigh.fk.R',   'Armature.013')
            addConstraintsRotation(amt,'shin.fk.R',     'Armature.014')
            addConstraintsRotation(amt,'foot.fk.R',    'Armature.015')
            addConstraintsRotation(amt,'thigh.fk.L',    'Armature.017')
            addConstraintsRotation(amt,'shin.fk.L',      'Armature.018')
            addConstraintsRotation(amt,'foot.fk.L',     'Armature.019')

            addConstraintsRotation(amt,'chest',     'Armature.002')
            if bpy.context.scene.ki_neck:
                addConstraintsRotation(amt,'neck',     'Armature.003')
                
            addConstraintsRotation(amt,'root',     'HipCenter')
            addConstraintsLocation(amt,'root',     'HipCenter') #csak a rotation után lehet mert az töröl is! így jó



            if bpy.context.scene.ki_transform:
                arm = bpy_data.armatures[bpy.context.scene.ki_armaturename]
                try:
                    arm.edit_bones['thigh.fk.R'].roll = 191 * (math.pi*2 / 360)
                except:
                    pass
                try:
                    arm.edit_bones['shin.fk.R'].roll = 191 * (math.pi*2 / 360)
                except:
                    pass
                try:
                    arm.edit_bones['thigh.fk.L'].roll = -191 * (math.pi*2 / 360)
                except:
                    pass
                try:
                    arm.edit_bones['shin.fk.L'].roll = -191 * (math.pi*2 / 360)
                except:
                    pass
                try:
                    arm.edit_bones['neck'].roll = 180 * (math.pi*2 / 360)
                except:
                    pass
        except:
            pass



        return {'RUNNING_MODAL'}



class KDI_start_operator(bpy.types.Operator):
    bl_label = "Kinect Data Import Start Operator"
    bl_idname = "wm.kinect_data_import_start"
    
    enabled = False
    receiver = None
    timer = None
	
    def modal(self, context, event):
        if (event.type == 'ESC' or not __class__.enabled):
            return self.cancel(context)
        if event.type == 'TIMER':
	        self.receiver.receive(bpy.data.objects, setData)

        return {'PASS_THROUGH'}

    def execute(self, context):
	    __class__.enabled = True
	    self.receiver = UDPserver()
	    
	    context.window_manager.modal_handler_add(self)
	    self.timer = context.window_manager.event_timer_add(1/context.scene.render.fps, context.window)
	    return {'RUNNING_MODAL'}
	
    def cancel(self, context):
	    __class__.enabled = False
	    context.window_manager.event_timer_remove(self.timer)
	    
	    del self.receiver
	    
	    return {'CANCELLED'}
	
    @classmethod
    def disable(cls):
	    if cls.enabled:
	        cls.enabled = False

                
class KDI_stop_operator(bpy.types.Operator):
    bl_label = "Kinect Data Import Stop Operator"
    bl_idname = "wm.kinect_data_import_stop"

    def execute(self, context):
        KDI_start_operator.disable()
        return{"FINISHED"}


def register():
    bpy.utils.register_module(__name__)

def unregister():        
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()








