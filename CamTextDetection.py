import cv2
import keyboard
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

cap = cv2.VideoCapture(0)

frameSpeed = 1

def check_frame(img):
    hImg , wImg , channel = img.shape
    boxes = pytesseract.image_to_data(img)
    for x,b in enumerate(boxes.splitlines()):
        if x != 0 :
            b = b.split()
            print(b)
            if len(b) == 12 : 
                x , y , w , h = int(b[6]) , int(b[7]) , int(b[8]) , int(b[9])
                cv2.rectangle(img , (x , y), (w+x , y+h) , (255,0,0) , 3 )
                cv2.putText(img , b[11] , (x,y) ,  cv2.FONT_HERSHEY_COMPLEX , 1 ,  (255,0,0)  , 2)


while cap.isOpened():
    suc , img = cap.read()

    if frameSpeed == 0 : 
        check_frame(img)
    else : 
        cv2.putText(img , "Press Space to Run !" , (10,40) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255,0,255))

    cv2.imshow('results' , img)
    k = cv2.waitKey(frameSpeed)

    if k == 27 : break
    elif k == 32 : 
        if not frameSpeed : frameSpeed = 1
        else : frameSpeed = 0

cap.release()
cv2.destroyAllWindows()