# imports

import cv2 # type: ignore
import mediapipe as mp # type: ignore
from pynput.keyboard import Key, Controller  # type: ignore
import time
import math

keyboard = Controller() 
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Configure MediaPipe 
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1, 
    min_detection_confidence=0.3, 
    min_tracking_confidence=0.3
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

pTime = 0
active_action = "Idle"

# Gesture States
gesture_state = {
    'move_left': False,
    'move_right': False,
    'jump': False,
    'duck': False
}

# Lane Boundaries 
LEFT_LANE_BOUND = 0.33
RIGHT_LANE_BOUND = 0.63

# Indices for the tips 
FINGER_TIPS = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP, 
               mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, 
               mp_hands.HandLandmark.PINKY_TIP]

#  Pynput Key Press
def press_and_release(key_code):
    keyboard.press(key_code)
    keyboard.release(key_code)

# check fingers
def count_extended_fingers(landmarks):
    extended_fingers = [False] * 5
    
    if landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y:
        extended_fingers[0] = True
        
    for i in range(1, 5): 
        tip_id = FINGER_TIPS[i].value
        pip_id = tip_id - 2 
        
        if landmarks.landmark[tip_id].y < landmarks.landmark[pip_id].y:
            extended_fingers[i] = True
            
    return extended_fingers

# Main Loop
while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)

    h, w, c = image.shape 
    image.flags.writeable = False
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    image.flags.writeable = True

    current_action = {
        'move_left': False,
        'move_right': False,
        'jump': False,
        'duck': False
    }

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        
        center_x = (thumb_tip.x + index_tip.x) / 2
        
        extended = count_extended_fingers(hand_landmarks)
        
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        

        # Check lane

        if center_x > RIGHT_LANE_BOUND:
            current_action['move_right'] = True
        elif center_x < LEFT_LANE_BOUND:
            current_action['move_left'] = True
        
        
        # Check jump / duck

        if all(extended):
            current_action['jump'] = True

        elif extended[0] and extended[4] and not extended[1] and not extended[2] and not extended[3]:
            current_action['duck'] = True
            
    
    # MOVE RIGHT
    if current_action['move_right'] and not gesture_state['move_right']:
        press_and_release(Key.right)
        gesture_state['move_right'] = True
        active_action = "Move RIGHT (Press)"
    elif not current_action['move_right'] and gesture_state['move_right']:
        gesture_state['move_right'] = False
        
    # MOVE LEFT
    elif current_action['move_left'] and not gesture_state['move_left']:
        press_and_release(Key.left)
        gesture_state['move_left'] = True
        active_action = "Move LEFT (Press)"
    elif not current_action['move_left'] and gesture_state['move_left']:
        gesture_state['move_left'] = False

    # JUMP (Open Palm)
    elif current_action['jump'] and not gesture_state['jump']:
        press_and_release(Key.up)
        gesture_state['jump'] = True
        active_action = "JUMP (Press)"
    elif not current_action['jump'] and gesture_state['jump']:
        gesture_state['jump'] = False

    # DUCK (Hang Loose)
    elif current_action['duck'] and not gesture_state['duck']:
        press_and_release(Key.down)
        gesture_state['duck'] = True
        active_action = "DUCK (Press)"
    elif not current_action['duck'] and gesture_state['duck']:
        gesture_state['duck'] = False

        
    elif any(gesture_state.values()):
        for action, is_active in gesture_state.items():
            if is_active:
                active_action = f"{action.upper().replace('_', ' ')} (Held)"
                break
    else:
        active_action = "Idle (Middle Lane)"

    
    # --- Display FPS and Status ---
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    cv2.putText(image, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.putText(image, f'Action: {active_action}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Subway Surfers Gesture Control', image)
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()