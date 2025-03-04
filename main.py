import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random
import os


# Directory to store the screenshots
screenshot_folder = "Dataset"

# Create the directory if it doesn't exist
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Set hand detector to only take one hand max
detector = HandDetector(maxHands=1)

timer = 0
stateResult = False 
startGame = False
screenshotTaken = False

# One score for AI & one score for Player
scores = [0, 0]

while True:
    imgBG = cv2.imread("Images/background.png")
    success, img = cap.read()
    
    if not success:
        print("Failed to capture image")
        break

    # Saving an original raw frame
    imgOriginal = img.copy()

    # Resize the webcam frame
    imgScaled = cv2.resize(img, (400, 420))

    # Locate hands and draw default hand info (by cvzone, this might show left/right)
    hands, imgScaled = detector.findHands(imgScaled)

    # If a hand is detected, determine the gesture and overlay its name
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        # Determine the gesture based on finger positions
        if fingers == [0, 0, 0, 0, 0]:
            gesture = "Rock"
        elif fingers == [1, 1, 1, 1, 1]:
            gesture = "Paper"
        elif fingers == [0, 1, 1, 0, 0]:
            gesture = "Scissors"
        else:
            gesture = "Unknown"
        # Extract the hand's bounding box to position the text
        x, y, w, h = hand['bbox']
        cv2.putText(imgScaled, gesture, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if startGame:
        if stateResult is False:
            # Initialize and display the timer on the background
            timer = time.time() - intialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            # Stop timer at 3 seconds and process the move
            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # Rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # Paper
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # Scissors

                    # AI randomly picks a move
                    options = ['rock.png', 'paper.png', 'scissor.png']
                    randomHandSignal = random.choice(options)
                    imgAI = cv2.imread(f'Images/{randomHandSignal}', cv2.IMREAD_UNCHANGED)
                    
                    if imgAI is None:
                        print(f"Failed to load image: {randomHandSignal}")
                        break

                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
                    
                    # Determine the round result and update scores
                    # Player Wins
                    if (playerMove == 1 and randomHandSignal == 'scissor.png') or (playerMove == 2 and randomHandSignal == 'rock.png') or (playerMove == 3 and randomHandSignal == 'paper.png'):
                        scores[1] += 1
                    
                    # AI Wins
                    if (playerMove == 2 and randomHandSignal == 'scissor.png') or (playerMove == 3 and randomHandSignal == 'rock.png') or (playerMove == 1 and randomHandSignal == 'paper.png'):
                        scores[0] += 1
                  
                    # After scoring, capture a screenshot of the player
                    if stateResult:
                        timestamp = int(time.time())
                        screenshot_filename = os.path.join(screenshot_folder, f'player_{timestamp}.png')
                        cv2.imwrite(screenshot_filename, imgOriginal) #change this original to scaled
                        print(f"Screenshot saved as {screenshot_filename}")
                   

    # Place the resized webcam frame (with gesture text) onto the background image
    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
    
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        intialTime = time.time()
        stateResult = False

    if key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
