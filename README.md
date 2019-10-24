# kinectblender
Blender kinect data importer

Kinect szenzorral felépített 3D környezet.

Alapanyagok: 

Kinect 360 XBOX + windows tápegység
Kinect SDK 1.5
Blender python script javított verziója
Blender alap fájl

Blender3D
MakeHuman

Fontos: A Blender fileban levő python script nem a legutolsó verzió, azt mindig töltsük le innen!

Telepítés:

1. Az MS SDK feltelpítése után a szenzor működik (újraindítás kell)
2. A Kinect - Blender softwer telepítése után elindítható és a kinect képét mutatja.
3. A Kinect-Blender UDP Start gombal kezdi sugározni a kinect adatokat a 127.0.0.1 portra, melyet a python scrypt fogad
4. Blender elindítása után a mellékelt (nem a csomagban levő!) alapot beolvassuk. KinectArmature_OK5… fájl. Ebben a fájlban megtalálható a Kinect-Blender softwerhez adaptált eredeti skeleton (utolsó előtti rétegen) Illetve az ezt működtető objektumhalmaz (utolsó rétegen) Ezekkel nincs teendőnk, mivel erről veszi le az adatokat a javyított python script és teszi rá a makehuman karakterünkre. Tehát a két réteg nem törlendő :)
5. Az 1-3 rétegeken található a MakeHuman karakter, melyet össze kell kötnünk a működtető réteggen lévő skeletonnal (utolsó előtti layer) 
6. A Script screen tartalmazza a python scriptet, melyet el kell indítanunk, hogy legyen a TOOLS Panelen egy Kinect panel. Ez kell a használathoz. A python scríypt egyébként mellékelve és beolvasható és úgy is elindítható. 
7. A panelen be kell állítani a csatlakoztatni kívánt MakeHuman karakter skeletont. Alapesetben woman2 de ha új karaktert hozunk be és ezt töröljük, akkor annak nevét kell beírni. A setup skeleton után a karakterünk összekötve a működtető skeletonnal.
8. Start megnyomására a Kinec-Blender softwerrel sugárzott adatokat a működtető skeletonra (az pedig a mi makehuman karakterünkre) kerül a 3D adat. Azaz a modellünk mozog, ha a kinect mozgó alakot talál.
9. Influence a karaktermozgatási adatok milyen erősségben kerüljenek felhasználásra.
10. Transform csak abban az esetben, ha a makeHuman ból kimentett karakter nem tartalmaz rotation limitet. 

A scrípt kétféle makehuman karaktert képes kezelni. 

hibák:
Ha a karakterünk rosszul mozogna, akkor 180 fokkal forgassuk el az alaját. 




