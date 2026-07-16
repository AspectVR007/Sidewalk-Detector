Personal Assistant:
This project is when you put in an image of a sidewalk it will detect if it is a sidewalk or not.



The Algorithm:
It scans the image and then confirms if it is a sidewalk or not. Just follow what I do in the video because the camera portion of it was never figured out but I will update it later.




Running this project:
You can download the code off of GitHub and use it in Vscode or anything python related. You run it, put an image in, and it will tell you if it is a sidewalk or not.
Nothing else needed




These are the certain commands you need for it:


This is the command for the sidewalk: python3 /opt/jetson-inference/python/examples/imagenet.py \
--model=models/sidewalk/resnet18.onnx \
--input_blob=input_0 --output_blob=output_0 \
--labels=data/sidewalks/labels.txt \
data/sidewalks/test/sidewalk/sidewalk_00034.jpg output.jpg 2>&1 | grep -i "class #"




This is the command for something that isnt a sidewalk: python3 /opt/jetson-inference/python/examples/imagenet.py \
--model=models/sidewalk/resnet18.onnx \
--input_blob=input_0 --output_blob=output_0 \
--labels=data/sidewalks/labels.txt \
data/sidewalks/test/not_sidewalk/not_sidewalk_00000.jpg output2.jpg 2>&1 | grep -i "class #"






This is the command for a random image. It shows a complete random image of either a sidewalk or a road.

IMG=$(find data/sidewalks/test -name "*.jpg" | shuf -n 1) && \
echo "Testing: $IMG" && \
python3 /opt/jetson-inference/python/examples/imagenet.py \
--model=models/sidewalk/resnet18.onnx \
--input_blob=input_0 --output_blob=output_0 \
--labels=data/sidewalks/labels.txt \
"$IMG" output.jpg 2>&1 | grep -iE "testing|class #"


