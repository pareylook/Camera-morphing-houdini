import hou
fetches = []
nodes = hou.selectedNodes()
# print nodes
# Create chopnet
obj = hou.node("/obj")
new_cam = obj.createNode("cam", "camera_morphing")
new_cam.moveToGoodPosition()
ch = obj.createNode("chopnet", "camera_morphing")
ch.moveToGoodPosition()
target = obj.createNode("null", "camera_target")
target.moveToGoodPosition()
interp_node = ch.createNode("interp")

# create fetches
for i in nodes:
    if i.type().name() == "cam":
        # print "cam"
        fnode = ch.createNode("fetch", i.type().name())
        fetches.append(fnode)
        fnode.moveToGoodPosition()
        fnode.parm('nodepath').set(i.path())
        fnode.parm('path').set("tx ty tz rx ry rz focal")

# create interpolate
interp_node.moveToGoodPosition()
for f in fetches:
    interp_node.setNextInput(f)
interp_node.parm("overlap").set(0)

# create extend1
extend1 = interp_node.createOutputNode("extend")
extend1.parm("left").set(2)
extend1.parm("right").set(2)

filter1 = extend1.createOutputNode("filter")

# create extend1
extend2 = filter1.createOutputNode("extend")
extend2.parm("left").set(1)
extend2.parm("right").set(1)

# create lookat
lookat1 = extend2.createOutputNode("constraintlookat")
lookat1.parm("lookatx").set(hou.parm("/obj/camera_target/tx"))
lookat1.parm("lookaty").set(hou.parm("/obj/camera_target/ty"))
lookat1.parm("lookatz").set(hou.parm("/obj/camera_target/tz"))

out = lookat1.createOutputNode("null", "out")
out.parm("export").set(new_cam.path())
out.setExportFlag(1)
out.setDisplayFlag(1)
