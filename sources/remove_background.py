import cv2
from PIL import Image, ImageFile
from rembg import remove

print("####### Test: remove background from image #######")

ImageFile.LOAD_TRUNCATED_IMAGES = True
print(">> Input and output as a PIL image")

input_path = "../resources/dog.jpeg"

print("-----------------------------")
print(">> Input and output as bytes")

output_path = "../output/dog_1.png"

inp = Image.open(input_path)
output = remove(inp)
output.save(output_path)

print("-----------------------------")
print(">> Input and output as bytes")

output_path2 = "../output/dog_2.png"

with open(input_path, "rb") as i:
    with open(output_path2, "wb") as o:
        input2 = i.read()
        output2 = remove(input2)
        o.write(output2)

print("-----------------------------")
print(">> Input and output as a numpy array")

output_path3 = "../output/dog_3.png"

input3 = cv2.imread(input_path)
output3 = remove(input3)
cv2.imwrite(output_path3, output3)

# TODO check bugs
