#source: https://machinelearningmastery.com/how-to-perform-face-detection-with-classical-and-deep-learning-methods-in-python-with-keras/
# face detection with mtcnn on a photograph
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from mtcnn.mtcnn import MTCNN

import cv2
from numpy import asarray
from PIL import Image

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

def detect_face_pos(filename):
    pixels = pyplot.imread(filename)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    faces = detector.detect_faces(pixels)
    context_dic ={}

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
        if len(context_dic) ==0:
            print("picture good")
            context_dic["good"] = "Good"
            #return('Good')
        return context_dic
        # draw_image_with_boxes(filename, faces)
        # quit()
    print("Got to far Nathaniel **Check this")
# to do
# - Check for orientation of head
# - Check for center of head in camera view
# - chek for brightness