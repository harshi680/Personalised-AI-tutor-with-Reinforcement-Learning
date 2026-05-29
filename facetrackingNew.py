import cv2
import dlib
import time
from scipy.spatial import distance as dist
import winsound  # For beep sound on Windows

# Helper functions
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def get_head_turn(landmarks):
    left_chin = landmarks.part(0)
    right_chin = landmarks.part(16)
    nose = landmarks.part(30)
    left_dist = dist.euclidean((left_chin.x, left_chin.y), (nose.x, nose.y))
    right_dist = dist.euclidean((right_chin.x, right_chin.y), (nose.x, nose.y))
    ratio = right_dist / left_dist if left_dist else 0

    if ratio > 1.3:
        return "left"
    elif ratio < 0.7:
        return "right"
    else:
        return "straight"

def beep():
    duration = 500  # ms
    freq = 1500     # Hz
    winsound.Beep(freq, duration)

# Constants
EYE_AR_THRESH = 0.23
CLOSED_EYES_TIME_THRESH = 5  # seconds
HEAD_TURN_TIME_THRESH = 5   # seconds

# Load face detector and landmark predictor
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Eye landmark indices
(lStart, lEnd) = (42, 48)
(rStart, rEnd) = (36, 42)

cap = cv2.VideoCapture(0)
closed_eyes_start_time = None

# New variables for head turn duration tracking
head_turn_start_time = None
current_head_state = "straight"

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray, 0)

    for face in faces:
        landmarks = landmark_predictor(gray, face)
        leftEye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(lStart, lEnd)]
        rightEye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(rStart, rEnd)]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # Detect head direction
        head_turn = get_head_turn(landmarks)

        # Track duration of head turn
        if head_turn in ["left", "right"]:
            if current_head_state != head_turn:
                # Head just turned to a new direction
                current_head_state = head_turn
                head_turn_start_time = time.time()
            else:
                # Head remains turned in same direction
                elapsed = time.time() - head_turn_start_time
                if elapsed > HEAD_TURN_TIME_THRESH:
                    beep()
                    cv2.putText(frame, f"Head turned {head_turn} > {HEAD_TURN_TIME_THRESH}s!",
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            # Reset when head straightens
            current_head_state = "straight"
            head_turn_start_time = None

        # Eye closure detection (existing logic)
        if ear < EYE_AR_THRESH:
            if closed_eyes_start_time is None:
                closed_eyes_start_time = time.time()
            elif (time.time() - closed_eyes_start_time) > CLOSED_EYES_TIME_THRESH:
                beep()
                cv2.putText(frame, "CHEATING ALERT!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 0, 255), 2)
        else:
            closed_eyes_start_time = None

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
