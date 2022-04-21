from django.http import HttpResponse
from django.shortcuts import render

from .forms import WebcamPicForm
from .models import WebcamPic

from django.views.decorators import gzip
from django.http import StreamingHttpResponse

import cv2
import threading

import cv2
from FacialDetectionDots import detect_face_pos


# Create your views here.

#button to capture SS
    #needs to have if camera valid

def homepage_view (request,*args, **kwargs):
    form = WebcamPicForm(request.POST or None)

    print(request.GET)
    print(request.POST)
    my_new_title = request.POST.get('title_of_posted_info')

    if request.POST:
        cam = VideoCamera()
        user_pic = cam.get_pic()
        # currently has to write pic and then run ML
        # update to just run ML on incoming pic
        cv2.imwrite('color_img03.jpg', user_pic)
        result = detect_face_pos('color_img03.jpg')
        print("Got the result", result)
        #context = {'result': result}
        print('type :',type(result))
        context = {}
        context["rec_dic"] = result
    else:
        context = {}

    print("my_new_title:",my_new_title)
    # if form.is_valid():
    #     form.save()
    #     form = WebcamPicForm()

    return render(request, "home.html", context)

def screenshot_view (request,*args, **kwargs):
    #create an obj with the posted screenshot
    #render with context pulled from obj
    return render(request, "screenshot.html", {})

@gzip.gzip_page
def webcam_feed(request,*args, **kwargs):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        #return to a failed webpage
        pass



class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(2)
        (self.grabbed, self.frame) = self.video.read(2)
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image=self.frame
        _, jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

    def get_pic(self):
        image = self.frame
        # _, jpeg = cv2.imencode('.jpg', image)
        # return jpeg
        return image

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
