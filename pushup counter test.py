import cv2
import mediapipe as mp
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils


def calculate_angle(a, b, c):
    """
    Calculates the angle between three points (a, b, c).
    """
    a = np.array(a)  # Point A
    b = np.array(b)  # Point B
    c = np.array(c)  # Point C

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

def classify_exercise(landmarks):
    """
    Classifies the current exercise based on landmark positions and angles.
    """
    # Get key points
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

    # Calculate angles
    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    hip_angle = calculate_angle(shoulder, hip, knee)
    knee_angle = calculate_angle(hip, knee, ankle)

    # Classify based on thresholds
    if elbow_angle > 160 and hip_angle > 160:  # Push-up
        return "pushup", elbow_angle
    elif hip_angle > 160 and knee_angle > 160:  # Squat
        return "squat", knee_angle
    elif hip_angle < 90:  # Sit-up (lower body curl detected)
        return "situp", hip_angle
    else:
        return "unknown", None



# Start video capture
cap = cv2.VideoCapture(1)

# Initialize counters for exercises
counters = {"pushup": 0, "situp": 0, "squat": 0}
stages = {"pushup": None, "situp": None, "squat": None}

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting.")
        break

    # Flip and process the frame
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Classify exercise
        exercise, angle = classify_exercise(landmarks)

        if exercise in counters:
            if angle and exercise == "pushup" and angle > 160:
                stages["pushup"] = "up"
            if angle and exercise == "pushup" and angle < 90 and stages["pushup"] == "up":
                counters["pushup"] += 1
                stages["pushup"] = "down"

            if angle and exercise == "squat" and angle > 160:
                stages["squat"] = "up"
            if angle and exercise == "squat" and angle < 90 and stages["squat"] == "up":
                counters["squat"] += 1
                stages["squat"] = "down"

            if angle and exercise == "situp" and angle < 90:
                stages["situp"] = "up"
            if angle and exercise == "situp" and angle > 160 and stages["situp"] == "up":
                counters["situp"] += 1
                stages["situp"] = "down"

        # Display exercise count
        cv2.putText(frame, f'Pushups: {counters["pushup"]}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Squats: {counters["squat"]}', (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Situps: {counters["situp"]}', (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Draw landmarks
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Show frame
    cv2.imshow('Exercise Counter', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
