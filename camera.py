from picamera import PiCamera

def take_pic(db, user, day):
    with PiCamera() as camera:
        camera.start_preview()
        camera.capture('/home/pi/Desktop/day{}.jpg'.format(day))
        camera.stop_preview()
    with open("/home/pi/Desktop/day{}.jpg".format(day), "rb") as imageFile:
        imgbytes = base64.b64encode(imageFile.read())
        imgstr = imgbytes.decode('utf-8')
        db.child("Camera").child("day " + str(day)).set(imgstr, user['idToken'])
    return
