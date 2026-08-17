import cv2
import mediapipe as mp
import math
import pygame

# 1. Initialize Pygame's audio mixer
pygame.mixer.init()

# --- SETTINGS ---
# Make sure this exactly matches the name of your mp3 file in the folder
ALARM_FILE = "wakeup.mp3" 

EAR_THRESHOLD = 0.25       # How closed the eye needs to be (lower = more closed)
CLOSED_FRAMES_LIMIT = 20   # How many frames the eye must stay closed before the alarm sounds
# ----------------

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE_POINTS = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_POINTS = [33, 160, 158, 133, 153, 144]

closed_frames_count = 0

def euclidean_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def calculate_ear(eye_points, landmarks, frame_width, frame_height):
    coords = []
    for point_idx in eye_points:
        landmark = landmarks.landmark[point_idx]
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        coords.append((x, y))
    
    v1 = euclidean_distance(coords[1], coords[5])
    v2 = euclidean_distance(coords[2], coords[4])
    h = euclidean_distance(coords[0], coords[3])
    
    # Prevent division by zero just in case
    if h == 0:
        return 0.0
    
    return (v1 + v2) / (2.0 * h)

# 2. Start the webcam
cap = cv2.VideoCapture(0)

print("Starting Sleep Detector... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = face_mesh.process(rgb_frame)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            
            left_ear = calculate_ear(LEFT_EYE_POINTS, face_landmarks, frame_width, frame_height)
            right_ear = calculate_ear(RIGHT_EYE_POINTS, face_landmarks, frame_width, frame_height)
            avg_ear = (left_ear + right_ear) / 2.0
            
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            # 3. Check if eyes are closed
            if avg_ear < EAR_THRESHOLD:
                closed_frames_count += 1
                
                # 4. Trigger the alarm if closed for too long
                if closed_frames_count >= CLOSED_FRAMES_LIMIT:
                    cv2.putText(frame, "WAKE UP!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
                    
                    # Check if the music is already playing so it doesn't stutter/restart every frame
                    if not pygame.mixer.music.get_busy():
                        try:
                            pygame.mixer.music.load(ALARM_FILE)
                            pygame.mixer.music.play()
                        except Exception as e:
                            print(f"Error loading audio: {e}. Check your file name!")
            else:
                # Eyes are open, reset the counter
                closed_frames_count = 0
                
                # Stop the alarm if it is currently playing
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                
    cv2.imshow("Drowsiness Detector", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
