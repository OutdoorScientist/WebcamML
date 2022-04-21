#source: https://machinelearningmastery.com/how-to-perform-face-detection-with-classical-and-deep-learning-methods-in-python-with-keras/
# face detection with mtcnn on a photograph

from matplotlib import pyplot
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from mtcnn.mtcnn import MTCNN

import cv2
from numpy import asarray
## for brightness
import math
from PIL import Image, ImageStat
##

# draw an image with detected objects
def draw_image_with_boxes(filename, result_list):
    # load the image
    data = pyplot.imread(filename)
    # plot the image
    pyplot.imshow(data)
    # get the context for drawing boxes
    ax = pyplot.gca()
    # plot each box
    for result in result_list:
        # get coordinates
        x, y, width, height = result['box']
        # create the shape
        rect = Rectangle((x, y), width, height, fill=False, color='red')
        # draw the box
        ax.add_patch(rect)
        # draw the dots
        for key, value in result['keypoints'].items():
            # create and draw dot
            dot = Circle(value, radius=2, color='red')
            ax.add_patch(dot)
    # show the plot
    pyplot.show()

# filename = 'color_img02.JPG'

def detect_face_pos(filename,context_dic):
    pixels = pyplot.imread(filename)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    faces = detector.detect_faces(pixels)

    if len(faces)==0:
        #no face detected
        print('legnth of bbboxes is 0', len(faces))
        context_dic["noface"] = "No faces detected; Check your camera feed and camera view"
        #return ('No faces detected; Check your camera feed and camera view')
        return context_dic
    elif(len(faces) >1):
        #more than one face
        print("too many faces in scene")
        context_dic["faces"] = "Detecting more than one face"
        #return("Detecting more than one face")
        return context_dic
    else:
        # display faces on the original image
        print("faces[0]['box']",faces[0]['box'])
        print("faces[0]['box'][0]",faces[0]['box'][0])

        image01 = cv2.imread(filename)

        # dimensions = image01.shape
        # print('dimensions',dimensions)

        #current bug in which x&y dimensions flipped
        x_safe_zone_pieces = image01.shape[1]/4
        y_safe_zone_pieces = image01.shape[0]/4

        face_left_pos_hor = faces[0]['box'][0]
        face_right_pos_hor = faces[0]['box'][0] + faces[0]['box'][2]

        face_top_pos_ver = faces[0]['box'][1]
        face_bottom_pos_ver = faces[0]['box'][1] + faces[0]['box'][3]

        print('type of face_bottom_pos_ver',(type(face_bottom_pos_ver)))
        if face_right_pos_hor > (x_safe_zone_pieces*3):
            # print('image01.shape[0]',image01.shape)
            # print('face_right_pos_hor:',face_right_pos_hor)
            # print('x_safe_zone_pieces*7:',x_safe_zone_pieces*7)
            print('Move camera left')
            context_dic["left"]= "Recommendation - Move camera left"
            #return ('Recommendation - Move camera left')

        if face_left_pos_hor < (x_safe_zone_pieces*1):
            print('Move camera Right')
            context_dic["right"]= "Recommendation - Move camera right"
            #return('Recommendation - Move camera right')
        if face_top_pos_ver < (y_safe_zone_pieces*1):
            print('Move camera up')
            context_dic["up"] = "Recommendation - Move camera up"
            #return('Recommendation - Move camera up')
        if face_bottom_pos_ver > (y_safe_zone_pieces*3):
            print('Move camera down')
            context_dic["down"]= "Recommendation - Move camera down"
            #return ('Recommendation - Move camera down')

        context_dic = camera_rotation(faces,context_dic)

        return context_dic
        # draw_image_with_boxes(filename, faces)
        # quit()
    print("Got to far Nathaniel **Check this")

def brightness( im_file , context_dic):
    im = Image.open(im_file)
    stat = ImageStat.Stat(im)
    r,g,b = stat.mean
    brightness = math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))
    print("brightness:",brightness)
    if int(brightness) > 130:
        context_dic["brightness"] = "Recommendation - Make Environment Darker"
    if int(brightness) < 60:
        print("int brightness:",int(brightness))
        print("been determined its to dark")
        context_dic["brightness"] = "Recommendation - Make Environment Brighter"
    else:
        pass
    return context_dic

def camera_rotation(faces,context_dic):

    l_x = faces[0]['keypoints']['left_eye'][0]
    l_y = faces[0]['keypoints']['left_eye'][1]
    r_x = faces[0]['keypoints']['right_eye'][0]
    r_y = faces[0]['keypoints']['right_eye'][1]

    degree_of_rotation = math.degrees(math.atan(abs((r_y - l_y)) / (r_x - l_x)))
    print("degree_of_rotation",degree_of_rotation)
    # if abs((l_y - r_y)) > 30:
    if degree_of_rotation > 25:
        if (r_y > l_y):
            print("degree_of_rotation", degree_of_rotation)
            print("counter clockwise")
            context_dic["rotate"] = "Recommendation - Rotate your camera clockwise"
        if (l_y > r_y):
            print("degree_of_rotation", degree_of_rotation)
            print("rotate clockwise")
            context_dic["rotate"] = "Recommendation - Rotate your camera counter-clockwise"

    return context_dic

def analyzePhoto(file):
    context_dic = {}
    context_dic = detect_face_pos(file,context_dic)
    print("context_dic:",context_dic)
    if "noface" in context_dic:
        return context_dic
    elif "faces" in context_dic:
        return context_dic
    else:
        brightness(file, context_dic)

    if len(context_dic) == 0:
        print("picture good")
        context_dic["good"] = "Good"
    return context_dic

# to do
#     - need to get detected more than one face
#       - great camera feed.
