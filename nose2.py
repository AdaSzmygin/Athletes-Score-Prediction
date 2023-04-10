import cv2
import math
import matplotlib
#from PIL import Image
kol_odl_list = []
kolor_hex = []
kolor_rgb = []
for s in range(len(df)):
        if df['zdj'][s] == 'None':
            kol_odl_list.append('brak zdj')
            kolor_hex.append('brak zdj')
            kolor_rgb.append('brak zdj')
        else:
            img_data = requests.get(df['zdj'][s]).content

            image = cv2.imdecode(np.frombuffer(img_data, np.uint8), -1)
            face_classiffier = cv2.CascadeClassifier(r'C:\studia\informatyka_stosowana\semestr2\face.xml')
            face_box = face_classiffier.detectMultiScale(image)

            if len(face_box) == 0:  # warunek, gdy nie wykruje zadnej twarzy
                kol_odl_list.append('nie wykryto twarzy')
                kolor_hex.append('nie wykryto twarzy')
                kolor_rgb.append('nie wykryto twarzy')
            else:

                face_area = 0
                best = 0

                # czasami wykrywa sie kilka twarzy, dlatego biore z najwiekszym polem
                # nie jest to idealnie rozwiazanie, ale dziala, mozna to jakos udoskonalic
                for j in range(len(face_box)):
                    w, h = face_box[j][2:]
                    area = w * h
                    if area > face_area:
                        face_area = area
                        best = j  # wybiera j-ta twarz dla danego zawodnika

                # rysujemy prostokat z twarza na zdjeciu
                x, y, w, h = face_box[best]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 5)

                # mozna to odkomentowac zeby zobaczyc jak wyglada prostokat zaznaczonej twarzy na zdjeciu
                # cv2.imshow('face detection', image)
                # cv2.waitKey(0)

                # wycinam obraz do samej twarzy
                twarz = image[y:y + h, x:x + w]

                # na twarzy szukam nosa, dzieki temu pozbywam sie potencjalnych nosow spoza twarzy
                # znowu jakis gotowy xml z internetu
                nose_classiffier = cv2.CascadeClassifier(
                    r'C:\studia\informatyka_stosowana\semestr2\haarcascade_mcs_nose.xml')
                nose_box = nose_classiffier.detectMultiScale(twarz)

                # okreslam srodek obrazu (twarzy), kolejne zalozenie, ze szukany nos ma srodek najblizej srodka twarzy
                srodek = (twarz.shape[1] / 2, twarz.shape[0] / 2)
                odl = twarz.shape[0]  # maks odl od srodkow moze wynosic wymiar obrazu twarzy
                best2 = 0

                if len(nose_box) == 0:  # warunek, gdy nie wykruje zadnej twarzy
                    kol_odl_list.append('nie wykryto nosa')
                    kolor_hex.append('nie wykryto nosa')
                    kolor_rgb.append('nie wykryto nosa')
                else:
                    for k in range(len(nose_box)):
                        x2, y2, w2, h2 = nose_box[k]
                        sr = (x2 + 0.5 * w2, y2 + 0.5 * h2)
                        od = math.sqrt(math.pow(srodek[0] - sr[0], 2) + math.pow(srodek[1] - sr[1],
                                                                                 2))  # obliczam odl od srodka twarzy do k-tych srodkow nosa
                        if od < odl:
                            odl = od
                            best2 = k  # wybieram najlepszy nos

                    x3, y3, w3, h3 = nose_box[best2]

                    # rysunek nosa na twarzy
                    cv2.rectangle(twarz, (x3, y3), (x3 + w3, y3 + h3), (0, 0, 255), 5)
                    # cv2.imshow('nose', twarz)
                    # cv2.waitKey(0)

                    print(s)

                    if len(twarz.shape) < 3:  # ogarnac dlaczego tak sie dzieje???
                        kol_odl_list.append('zly wymiar')
                        kolor_hex.append('zly wymiar')
                        kolor_rgb.append('zly wymiar')

                    else:
                        # kolor nosa
                        r = 0
                        g = 0
                        b = 0
                        for l in range(h3):  # przejscie po calej dlugosci
                            for m in range(w3):  # po szerokosci
                                r = r + twarz[int(y3 + l)][int(x3 + m)][2]  # suma wartosci koloru z danych pikseli
                                g = g + twarz[int(y3 + l)][int(x3 + m)][1]
                                b = b + twarz[int(y3 + l)][int(x3 + m)][0]

                        wym = h3 * w3  # wymiar (pole)

                        # odl koloru na kwadracie rgb, ta kol_odl ma okreslic jak daleko jest od bialego
                        # teoretycznie im jasniejszy zawodnik to kol_odl mniejsza
                        # w miare dziala, ale nie idealnie - moze to byc spowodowane cieniami, dziurkami w nosie itp
                        kol_odl = round(math.sqrt(
                            math.pow(255 - b / wym, 2) + math.pow(255 - g / wym, 2) + math.pow(255 - r / wym, 2)), 2)
                        # print(matplotlib.colors.to_hex([r/wym/255, g/wym/255, b/wym/255]))
                        # print(int(r / wym), int(g / wym), int(b / wym), kol_odl)  # srednia = suma/ pole
                        kol_odl_list.append(kol_odl)
                        kolor_hex.append(matplotlib.colors.to_hex([r / wym / 255, g / wym / 255, b / wym / 255]))
                        kolor_rgb.append([int(r / wym), int(g / wym), int(b / wym)])
    #return kol_odl_list, kolor_hex, kolor_rgb