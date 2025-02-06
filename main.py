import face_recognition
import cv2
import os
import glob
import numpy as np
import pickle
from threading import Thread

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Yüzleri yükleyip encode eder ve dosyaya kaydeder
        """
        if os.path.exists("encodings.pkl"):
            with open("encodings.pkl", "rb") as f:
                self.known_face_encodings, self.known_face_names = pickle.load(f)
            print("Yüz verileri dosyadan yüklendi.")
            return

        images_path = glob.glob(os.path.join(images_path, "*.*"))
        print("{} yüz görüntüsü bulundu.".format(len(images_path)))

        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)

            face_encodings = face_recognition.face_encodings(rgb_img)
            if face_encodings:
                img_encoding = face_encodings[0]
                self.known_face_encodings.append(img_encoding)
                self.known_face_names.append(filename)
            else:
                print(f"⚠️ Uyarı: '{filename}' içinde yüz bulunamadı!")

        with open("encodings.pkl", "wb") as f:
            pickle.dump((self.known_face_encodings, self.known_face_names), f)
        print("Yüz verileri yüklendi ve dosyaya kaydedildi.")

    def detect_known_faces(self, frame):
        """
        Kameradaki yüzleri tanımlar
        """
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=1, model='hog')
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
            face_names.append(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names

# 📷 KAMERA BAĞLANTISI VE FPS ARTTIRMA
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 350)
cap.set(cv2.CAP_PROP_FPS, 30)

# Yüzleri yükleyelim
sfr = SimpleFacerec()
sfr.load_encoding_images("C:/Users/anil6/Desktop/pythonGoruntuIsleme/AnlikYuzTanima/person_images/")

def process_frame(frame):
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
    return frame

frame_counter = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_counter += 1
    if frame_counter % 1 == 0:  # Her 5 karede bir yüz tanıma işlemi yap
        frame = process_frame(frame)

    cv2.imshow("Face Recognition", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC tuşuna basınca çık
        break

cap.release()
cv2.destroyAllWindows()