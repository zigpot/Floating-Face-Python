import cv2
import numpy as np
from imutils import face_utils
import dlib
 
import argparse
 
 
# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("filename")
parser.add_argument("-o", "--Output", help = "output name, default: output.mp4")
 
# Read arguments from command line
args = parser.parse_args()
 
output_filename = "output.mp4"
if args.Output:
   output_filename = args.Output + ".mp4"

# Videoplay

cap = cv2.VideoCapture(args.filename)
SHAPE_PREDICTOR = "shape_predictor.dat"
faces = []
xpos_arr = []
ypos_arr = []
w_arr = []
h_arr = []
framecount_relative = []
if (cap.isOpened()== False): # Check if video opened successfully
  print("Error opening video  file")
  quit()
   
frame_rate = cap.get(cv2.CAP_PROP_FPS)

print("Frame rate:", frame_rate, "fps")

framecount = 0
keyframe = []
orientation = []
keyframe_relative = 50

facecount = 0

while(cap.isOpened()):
  ret, frame = cap.read()

  if ret == True:
    cv2.imshow('Frame', frame)
    framecount = framecount + 1
    key = cv2.waitKey(25)
    if key == -1:
      continue
    elif key == ord('q'):
      quit()
    elif key == 13: # ENTER
      break
    elif key >= ord('1') and key <= ord('8') and framecount >= keyframe_relative:
      orientation.append(key - 48)
      keyframe.append(framecount)
      #cv2.imwrite('face_frame.png', frame)
      print('Keyframe at', framecount)
      #face extraction
      image = frame
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      
      out_face = np.zeros_like(image)
      
      detector = dlib.get_frontal_face_detector()
      predictor = dlib.shape_predictor(SHAPE_PREDICTOR)
      
      rects = detector(gray, 1)
      
      for (i, rect) in enumerate(rects):
         shape = predictor(gray, rect)
         shape = face_utils.shape_to_np(shape)
      
         remapped_shape = np.zeros_like(shape) 
         feature_mask = np.zeros((image.shape[0], image.shape[1]))   
      
         remapped_shape = cv2.convexHull(shape)
                                  
         cv2.fillConvexPoly(feature_mask, remapped_shape[0:27], 1)
         feature_mask = feature_mask.astype(np.bool)
         feature_mask = feature_mask * np.uint8(255)
      
         new_img = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
         new_img[:, :, 3] = feature_mask
         contours = cv2.findContours(feature_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
         contours = contours[0] if len(contours) == 2 else contours[1]
         cntr = contours[0]
         xpos,ypos,w,h = cv2.boundingRect(cntr)
         xpos_arr.append(xpos)
         ypos_arr.append(ypos)
         w_arr.append(w)
         h_arr.append(h)
      
         crop = new_img[ypos:ypos+h, xpos:xpos+w]
      
      print('xpos',xpos,'ypos',ypos,'w',w,'h',h)
      face_height, face_width, _ = crop.shape
      faces.append(crop)
      framecount_relative.append(0)
      #break
  else:
    break
cv2.destroyAllWindows()

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
  
out = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc('M','J','P','G'), frame_rate, (frame_width,frame_height))

#Add faces to video
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

if(not cap.isOpened()):
  print("Error opening video file")
  quit()

framecount = 0
while(cap.isOpened()):
  
  ret, frame = cap.read()

  facecount = 0
  while(facecount < len(faces)):
    xpos_ = xpos_arr[facecount]
    ypos_ = ypos_arr[facecount]
    if(orientation[facecount] == 1 or orientation[facecount] == 8 or orientation[facecount] == 7): x = int(xpos_*framecount_relative[facecount]/keyframe_relative) # leftmost
    elif(orientation[facecount] == 3 or orientation[facecount] == 4 or orientation[facecount] == 5):  x = int(xpos_ + (frame_width - xpos_ - w_arr[facecount]) * (1 - framecount_relative[facecount]/keyframe_relative)) # rightmost
    else: x = xpos_
  
    if(orientation[facecount] == 1 or orientation[facecount] == 2 or orientation[facecount] == 3): y = int(ypos_*framecount_relative[facecount]/keyframe_relative) # most top
    elif(orientation[facecount] == 7 or orientation[facecount] == 6 or orientation[facecount] == 5): y = int(ypos_ + (frame_height - ypos_ - h_arr[facecount]) * (1 - framecount_relative[facecount]/keyframe_relative)) # most bottom
    else: y = ypos_
  
    if framecount <= keyframe[facecount] and framecount > keyframe[facecount]-50:
      framecount_relative[facecount] = framecount_relative[facecount] + 1
      x_ = x + faces[facecount].shape[1]
      y_ = y + faces[facecount].shape[0]
      alpha_face = faces[facecount][:, :, 3]/255.0
      alpha_frame = 1.0 - alpha_face
      for c in range(0,3):
        frame[y:y_, x:x_, c] = (alpha_face * faces[facecount][:, :, c] + alpha_frame *frame[y:y_, x:x_, c])
    facecount = facecount + 1

  if (ret):
    framecount = framecount + 1
    out.write(frame)
  else:
    break

out.release()
cap.release()
cv2.destroyAllWindows()
print(framecount)

