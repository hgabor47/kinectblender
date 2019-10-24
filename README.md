# kinectblender
Blender kinect data importer
Broken project for study only!!!

Kinect sensor with 3D environment

--Needs:

Kinect 360 XBOX + windows power supply
Kinect SDK 1.5
Kinect - blender software (http://blender.vsb.cz/index.php/en/kinect-blender)
Blender python script new version
Blender base file

Blender3D (about 2.5)
MakeHuman

Important: You need refresh the script in the A Blender file. Download the latest version from here.

--Install:

1. The MS SDK install. Sensor is working (reboot neded)
2. The Kinect - Blender software intall and run. You can see the kinect picture.
3. The Kinect-Blender broadcats the UDP data with click Start button. (to 127.0.0.1 and the receiver the python script )
4. Start Blender and load the KinectArmature_OK5… file. In the blender you found the original Kinect-Blender sofware adapted skeleton (before last layer). Working data in last layer. You don't need change it. Don't clear these layers.
5. The makehuman character is in the 1-3 layers, need connect to before last layers skeleton. 
6. The Script screens contains the python script. Need to start, and this create a Kinect panel in the TOOLS panel. This need it for use. This python script can open from file too. 
7. In this panel you need to setup the connected Makehuman skeleton. Originally woman2. After this tep the skeleton is working.
8. Click Start button. The Kinec-Blender boadcasted data recevied to the working skeleton (and transferred via connection to my makehuman skeleton) So in this case the skeleton will moving if kinect found a moving character. 
9: Influence
10. Transform if the makeHuman imported character not contains rotation limit. 

The scrípt can use tow kind of makehuman character. 

Errors:
Lot of.. :)))
and if the character moving bad, then try to turn the base platform with 180 degree. 


(Thanks to Michal Polcer for idea)

