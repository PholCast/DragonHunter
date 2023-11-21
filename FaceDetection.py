import cv2
import mediapipe as mp
import numpy as np
import math

import mediapipe.python.solutions.face_detection
import mediapipe.python.solutions.face_mesh
import mediapipe.python.solutions.face_mesh_connections


class FaceDetection:
    playerAction = None
    
    @staticmethod
    def detect(cap):

        mpDibujo = mp.solutions.drawing_utils

        confDibu = mpDibujo.DrawingSpec(thickness=1,circle_radius = 1)
        mp_face_mesh = mp.solutions.face_mesh
        #face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
        #cap = cv2.VideoCapture(0)

        while FaceDetection.playerAction== None:
            success, image = cap.read()

            # Flip the image horizontally for a later selfie-view display
            # Also convert the color space from BGR to RGB
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # To improve performance
            image.flags.writeable = False
            
            # Get the result
            results = face_mesh.process(image)
            
            # To improve performance
            image.flags.writeable = True
            
            # Convert the color space from RGB to BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            img_h, img_w, img_c = image.shape
            face_3d = []
            face_2d = []
            lista = []

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mpDibujo.draw_landmarks(image,face_landmarks,mp_face_mesh.FACEMESH_TESSELATION,confDibu,confDibu)
                    for idx, lm in enumerate(face_landmarks.landmark):
                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D Coordinates
                        face_2d.append([x, y])

                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])  

                        lista.append([idx, x, y])  
    
                    # Convert it to the NumPy array
                    face_2d = np.array(face_2d, dtype=np.float64)

                    # Convert it to the NumPy array
                    face_3d = np.array(face_3d, dtype=np.float64)

                    # The camera matrix
                    focal_length = 1 * img_w

                    cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                            [0, focal_length, img_w / 2],
                                            [0, 0, 1]])

                    # The Distance Matrix
                    dist_matrix = np.zeros((4, 1), dtype=np.float64)

                    # Solve PnP
                    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                    # Get rotational matrix
                    rmat, jac = cv2.Rodrigues(rot_vec)

                    # Get angles
                    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                    # Get the y rotation degree
                    x = angles[0] * 360
                    y = angles[1] * 360

                    #Boca Extremos
                    x1, y1 = lista[78][1:]
                    x2, y2 = lista[308][1:]
                    #cx1, cy1 = (x1 + x2) // 2, (y1 + y2) // 2
                    longitud1 = math.hypot(x2 - x1, y2 - y1)

                    #Boca Abertura
                    x3, y3 = lista[13][1:]
                    x4, y4 = lista[14][1:]
                    #cx2, cy2 = (x3 + x4) // 2, (y3 + y4) // 2
                    longitud2 = math.hypot(x4 - x3, y4 - y3)

                    #Ceja Derecha
                    x5, y5 = lista[65][1:]
                    x6, y6 = lista[158][1:]
                    #cx3, cy3 = (x5 + x6) // 2, (y5 + y6) // 2
                    longitud3 = math.hypot(x6 - x5, y6 - y5)

                    #Ceja Izquierda
                    x7, y7 = lista[295][1:]
                    x8, y8 = lista[385][1:]
                    #cx3, cy3 = (x7 + x8) // 2, (y7 + y8) // 2
                    longitud4 = math.hypot(x8 - x7, y8 - y7)

                    #Ojo izquierdo
                    x9,y9 = lista [385][1:]
                    x10,y10 = lista[374][1:]

                    longitudOjoI = math.hypot(x10 - x9, y10 - y9)


                    #Ojo derecho
                    x11,y11 = lista [159][1:]
                    x12,y12 = lista[145][1:]

                    longitudOjoD = math.hypot(x12 - x11, y12 - y11)



                    # print(y)

                    # See where the user's head tilting
                    if y < -10:
                        cv2.putText(image, "Izquierda", (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        FaceDetection.playerAction = "left"
                        
                        #return "left"

                    elif y > 15:
                        cv2.putText(image, "Derecha", (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        FaceDetection.playerAction = "right"
                    
                    elif x < -10:
                        cv2.putText(image, "Abajo", (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        FaceDetection.playerAction = "down"
                    
                    elif x > 10:
                        cv2.putText(image, "Arriba", (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        FaceDetection.playerAction = "up"
                    
                    elif longitud1 < 90 and longitud2 > 20:
                        cv2.putText(image, "Boca abierta", (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        FaceDetection.playerAction = "open mouth"

                    elif longitud3 > 22.1 and longitud4 > 22.1 and -5<x<-2 and longitudOjoI > 13:
                        cv2.putText(image, "Cejas arribas", (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        
                        FaceDetection.playerAction = "eyebrows"
                    
                    elif longitud1 > 62:
                        cv2.putText(image, "Sonriendo", (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                        FaceDetection.playerAction = "smile"

                    # elif longitud3 < 19 and longitud4 < 19 and -5<x<-2:
                    #     cv2.putText(image, "Cerrar los ojos", (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    #     FaceDetection.playerAction = "eyebrows"

                    elif longitudOjoI < 9 and longitudOjoD <  9 and -5<x<-2:
                        cv2.putText(image, "Cerrar los ojos", (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (33, 229, 205), 3)
                        FaceDetection.playerAction = "closed eyes"
                    else:
                        cv2.putText(image, "Mirada Adelante", (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (253, 203, 0), 3)
                        text = "Forward"

                    # Display the nose direction
                    #nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

                    #p1 = (int(nose_2d[0]), int(nose_2d[1]))
                    #p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
                    
                    #cv2.line(image, p1, p2, (255, 0, 0), 2)

                    # Add the text on the image
                    #cv2.putText(image, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('Head Pose Estimation', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

        #cap.release()
