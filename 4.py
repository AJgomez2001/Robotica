import cv2
import numpy as np

def draw(mask, color):
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contornos:
        area = cv2.contourArea(c)
        
        if area > 5000:    
            M = cv2.moments(c)
            if M["m00"] == 0:
                M["m00"] = 1
                
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            
            newContorno = cv2.convexHull(c)
             
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv2.putText(frame, '{}, {}'.format(x, y), (x+10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.drawContours(frame, [newContorno], 0, color, 3)

cap = cv2.VideoCapture(0)

azulBajo = np.array([100, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)

amarilloBajo = np.array([15, 100, 20], np.uint8)
amarilloAlto = np.array([45, 255, 255], np.uint8)

rojoBajo1 = np.array([0, 100, 20], np.uint8)
rojoAlto1 = np.array([5, 255, 255], np.uint8)

rojoBajo2 = np.array([175, 100, 20], np.uint8)
rojoAlto2 = np.array([179, 255, 255], np.uint8)

Blanco_bajo = np.array([226, 218, 216], np.uint8)
Blanco_alto = np.array([255, 255, 255], np.uint8)

Negro_bajo = np.array([0, 0, 0], np.uint8)
Negro_alto = np.array([61, 13, 2], np.uint8)


while True:
    ret, frame = cap.read()

    if ret:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)
        maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)
        maskRojo1 = cv2.inRange(frameHSV, rojoBajo1, rojoAlto1)
        maskRojo2 = cv2.inRange(frameHSV, rojoBajo2, rojoAlto2)
        maskRojo = cv2.add(maskRojo1, maskRojo2)
        maskBlanco=cv2.inRange(frameHSV, Blanco_bajo, Blanco_alto)
        maskNegtro=cv2.inRange(frameHSV, Negro_bajo, Negro_alto)
        
        
        draw(maskAzul, (255, 0, 0))
        draw(maskAmarillo, (0, 255, 255))
        draw(maskRojo, (0, 0, 255))
        draw(maskBlanco, (255, 255, 255))
        draw(maskNegtro, (0, 0, 0))

        cv2.imshow('Captura de video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

cap.release()
cv2.destroyAllWindows()