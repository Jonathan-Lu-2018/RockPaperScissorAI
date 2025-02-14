import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Set hand detector to only take one hand max
detector = HandDetector(maxHands=1)

timer = 0
stateResult = False 
startGame = False

# One score for AI & one score for Player
scores = [0, 0]

while True:
    imgBG = cv2.imread("Images/background.png")
    success, img = cap.read()
    
    if not success:
        print("Failed to capture image")
        break

    '''
    OG code
    # imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)
    # imgScaled = imgScaled[:, 80:480]
    # imgBG[234:654,795:1195] = imgScaled
    '''
    # Resize the webcam frame
    imgScaled = cv2.resize(img, (400, 420))

    # Locate hands
    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:

            # Initalizes the timer & displays it on the screen
            timer = time.time() - intialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN,6,(255,0,255), 4)

            # Stops timer at 3 seconds
            if timer > 3:
                stateResult = True
                timer = 0

                # Determines the hand signal
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 0, 0, 0, 0]:      # Rock
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:      # Paper
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:      # Scissor 
                        playerMove = 3

                    # AI agent to pick a random hand signal
                    options = ['rock.png', 'paper.png', 'scissor.png']
                    randomHandSignal = random.choice(options)
                    imgAI = cv2.imread(f'Images/{randomHandSignal}', cv2.IMREAD_UNCHANGED)
                    
                    if imgAI is None:
                        print(f"Failed to load image: {randomHandSignal}")
                        break

                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
                    
                    # Player Wins
                    if (playerMove == 1 and randomHandSignal == 'scissor.png') or (playerMove == 2 and randomHandSignal == 'rock.png') or (playerMove == 3 and randomHandSignal == 'paper.png'):
                        scores[1] += 1
                    
                    # AI Wins
                    if (playerMove == 2 and randomHandSignal == 'scissor.png') or (playerMove == 3 and randomHandSignal == 'rock.png') or (playerMove == 1 and randomHandSignal == 'paper.png'):
                        scores[0] += 1
                  
                    #print(playerMove)

    # Place the resized frame onto the background image
    imgBG[234:654,795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
    
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # Capture frame
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break
    
    # Display frame
    cv2.imshow("BG", imgBG)
    #cv2.imshow("Scaled", imgScaled)

    # Start the game with 's' key
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        intialTime = time.time()
        stateResult = False

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()