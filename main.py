import threading
import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0
face_match = False
reference_img_path = "reference.jpg"  # Path to the reference image

thread_lock=threading.Lock()

def check_face(frame):
    global face_match
    try:
        result=DeepFace.verify(img1_path=frame,img2_path=reference_img_path,model_name="OpenFace",enforce_detection=False)
        with thread_lock:
            face_match=result["verified"]
    except Exception as e:
        with thread_lock:
            face_match=False


while True:
    ret, frame = cap.read()
    if ret:
        if counter % 30 == 0:  # Check face every 1 second (30 frames per second)

                threading.Thread(target=check_face,args=(frame.copy(),)).start()


        counter += 1

        # Display match status on the video frame
        if face_match:
            cv2.putText(frame, "MATCH", (20, 450), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH", (20, 450), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("video", frame)

    if cv2.waitKey(1)&0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
