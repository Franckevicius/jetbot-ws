import jetson.inference
import jetson.utils
from robot import Robot

robot = Robot()

net = jetson.inference.detectNet(argv=["--model=../training-ws/onnx-exported-models/ssd-mobilenet.onnx", 
                                       "--labels=../training-ws/metadata/labels.txt",
                                       '--input-blob=input_0',
                                       '--output-cvg=scores',
                                       '--output-bbox=boxes'],
                                 threshold=0.4)
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

def rotate():
    robot.left_motor.value = 0.1
    robot.right_motor.value = 0

def go():
    robot.left_motor.value = 0.1
    robot.right_motor.value = 0.1

def stop():
    robot.left_motor.value = 0.0
    robot.right_motor.value = 0.0

def is_centered(obj, maxX, maxY):
    return obj.Center[0] > maxX * (1/3) and obj.Center[0] < maxX * (2/3)

while display.IsStreaming():
    img = camera.Capture()
    detections = net.Detect(img)    
    closest_objects = sorted(detections, key = lambda o : o.Area, reverse=True)
    if len(closest_objects) != 0:
        go()
    else:
        rotate()

    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))