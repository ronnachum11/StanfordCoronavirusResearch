import cv2
import os
import numpy as np 

images = []
for i in ["7", "14", "21", "28"]:
    file = os.path.join("Graphs", "Analysis", f"ReopeningDataMedian-{i}.png")
    img = cv2.resize(cv2.imread(file), (580, 605))
    img = cv2.copyMakeBorder(img, 100, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    images.append(img)

final_image = np.concatenate((np.concatenate((images[0], images[1])), np.concatenate((images[2], images[3]))), axis=1)
cv2.imwrite(os.path.join("Graphs", "Analysis", "ReopeningDataMedians-All.png"), final_image)
while cv2.waitKey(0) != ord('q'):
    cv2.imshow("Image", final_image)