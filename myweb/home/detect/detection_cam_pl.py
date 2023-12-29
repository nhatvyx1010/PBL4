import os
import cv2
import math
import numpy as np 
from skimage.filters import threshold_local
from ultralytics import YOLO
import time
from PIL import Image


def get_Frame(model_plates, model_charaters, ret, frame, cap, threshold):
    frame_count = 0
    
    prev_time = time.time()
    while ret:
        
        # Kiểm tra thời gian hiện tại
        current_time = time.time()
        if current_time - prev_time >= 2:
            results = model_plates(frame)[0]
            for result in results.boxes.data.tolist():

                x1, y1, x2, y2, score, class_id = result

                if score > threshold:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
                    cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                    frame_out = frame[int(y1):int(y2), int(x1):int(x2)]
                    frame_out = clean_noisy(frame_out)

                    # frame_out = xoay_Anh(cnts, frame_out)
                    frame_out = xoay_anh(frame_out, 1)

                    frame_out_2 = clean_noisy_2(frame_out)

                    line_box = line_detection(frame_out_2)
                    if len(line_box) >= 7 and len(line_box) <= 9:
                        for _ in line_box:
                            x, y, w, h = _
                            cv2.rectangle(frame_out, (x, y), (x + w, y + h), (0, 255, 0), 1)  # Vẽ hình chữ nhật bao quanh contour

                        new_img = cut_and_paste(line_box, frame_out)
                        
                        get_Characters(model_charaters, new_img)

                        frame_out = resize(frame_out)
                        new_img = resize(new_img)

                        image_filename = f'frame_1_{frame_count:04d}.jpg'
                        cv2.imwrite(image_filename, frame_out)
                        image_filename2 = f'frame_2_{frame_count:04d}.jpg'
                        cv2.imwrite(image_filename2, new_img)

                        frame_count+=1
            # Cập nhật thời gian cuối cùng
            prev_time = current_time

        # Hiển thị video trên màn hình
        cv2.imshow('Video', frame)

        # Đợi một khoảng thời gian ngắn (ví dụ: 30ms) và kiểm tra xem người dùng có nhấn phím 'q' để thoát không
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break   

        ret, frame = cap.read()

def resize(image):

    new_width = 400

    # Tính toán tỷ lệ giữa chiều rộng mới và chiều rộng ban đầu
    r = new_width / image.shape[1]
    new_height = int(image.shape[0] * r)
    dim = (new_width, new_height)

    # Sử dụng hàm resize để thay đổi kích thước hình ảnh về giá trị cố định
    resized_img = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return resized_img

def clean_noisy(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img_blur = cv2.bilateralFilter(img_gray, 11, 17, 17) 

    return img_blur

def clean_noisy_2(image):

    V = image
    # Adaptive threshold
    T = threshold_local(V, 35, offset=5, method="gaussian")
    thresh = (V > T).astype("uint8") * 255

    # Đảo ngược mask
    thresh = cv2.bitwise_not(thresh)

    # Connected component labeling
    _, labels = cv2.connectedComponents(thresh)

    # Tạo mask cuối cùng
    mask = np.zeros(thresh.shape, dtype="uint8")
    total_pixels = thresh.shape[0] * thresh.shape[1]
    lower = total_pixels // 120
    upper = total_pixels // 20

    for label in np.unique(labels):
        if label == 0:
            continue
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        if numPixels > lower and numPixels < upper:
            mask = cv2.add(mask, labelMask)
    return mask


# license plate type classification helper function
def linear_equation(x1, y1, x2, y2):
    b = y1 - (y2 - y1) * x1 / (x2 - x1)
    a = (y1 - b) / x1
    return a, b

def check_point_linear(x, y, x1, y1, x2, y2):
    a, b = linear_equation(x1, y1, x2, y2)
    y_pred = a*x+b
    return(math.isclose(y_pred, y, abs_tol = 20))

# detect character and number in license plate
def read_plate(bb_list):
    LD_type = "1"
    center_list = []
    y_mean = 0
    y_sum = 0
    for bb in bb_list:
        x_c = (bb[0]+bb[2])/2
        y_c = (bb[1]+bb[3])/2
        y_sum += y_c
        center_list.append([x_c,y_c,bb[-1]])

    # find 2 point to draw line
    l_point = center_list[0]
    r_point = center_list[0]
    for cp in center_list:
        if cp[0] < l_point[0]:
            l_point = cp
        if cp[0] > r_point[0]:
            r_point = cp
    for ct in center_list:
        if l_point[0] != r_point[0]:
            if (check_point_linear(ct[0], ct[1], l_point[0], l_point[1], r_point[0], r_point[1]) == False):
                LD_type = "2"

    return LD_type

def line_detection(image):

    cnts, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    
    line_box = []
    
    for i, (x, y, w, h) in enumerate(boundingBoxes):
        boundingBoxes[i] = (x - 2, y - 2, w + 4, h + 4)
    arr = np.array(boundingBoxes)

    LD_type = read_plate(arr)
    print('line type = ', LD_type)
    
    # trung bình cộng của w và h
    mean_w = np.mean(arr[:, 2])
    mean_h = np.mean(arr[:, 3])
    # Tính ngưỡng dựa trên trung bình cộng của w và h
    threshold_w = mean_w * 1.3
    threshold_h = mean_h * 1.3
    new_arr = arr[(arr[:, 2] < threshold_w) & (arr[:, 3] < threshold_h) & ((arr[:, 2]) < (0.8 * arr[:, 3]))]

    line1 = []
    line2 = []
    mean_y = np.mean(arr[:, 1])

    if LD_type == "2":
        for box in new_arr:
            x, y, w, h = box
            if y > mean_y:
                line2.append(box)
            else:
                line1.append(box)

        line1 = sorted(line1, key=lambda box: box[0])
        line2 = sorted(line2, key=lambda box: box[0])

        for _ in line1:
            line_box.append(_)
        for _ in line2:
            line_box.append(_)
    else:
        for box in new_arr:
            x, y, w, h = box
            line_box.append(box)

        line_box = sorted(line_box, key=lambda box: box[0])
    # Trả về line1 và line2 hoặc bất kỳ giá trị bạn cần
    return line_box

# Hàm cắt và gán các box vào một hình ảnh mới
def cut_and_paste(line_box, image):
    # Tính toán kích thước của ảnh mới dựa trên kích thước của các box
    max_width = sum(box[2] for box in line_box) + 3 * (len(line_box) - 1)
    max_height = max(box[3] for box in line_box)
    new_img = np.zeros((max_height, max_width, 3), dtype=np.uint8)

    # Gán từng box vào ảnh mới
    x_offset = 0
    for box in line_box:
        x, y, w, h = box
        box_img = image[y:y+h, x:x+w]
        if len(box_img.shape) < 3:
            box_img = cv2.cvtColor(box_img, cv2.COLOR_GRAY2RGB)

        new_img[0:h, x_offset:x_offset+w] = cv2.resize(box_img, (w, h))
        x_offset += w + 3  # Khoảng cách giữa các box là 3

    return new_img

def find_Contours(gray_img):

    edged = cv2.Canny(gray_img, 30, 200)  

    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    return cnts

# xoay_anh_2
def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result   

def compute_skew(src_img, center_thres):
    if len(src_img.shape) == 3:
        h, w, _ = src_img.shape
    elif len(src_img.shape) == 2:
        h, w = src_img.shape
    else:
        print('upsupported image type')
    img = cv2.medianBlur(src_img, 3)
    edges = cv2.Canny(img,  threshold1 = 30,  threshold2 = 100, apertureSize = 3, L2gradient = True)
    lines = cv2.HoughLinesP(edges, 1, math.pi/180, 30, minLineLength=w / 1.5, maxLineGap=h/3.0) 
                            # ( , độ phân giải, radian, ngưỡng, độ dài tối thiểu của đoạn thẳng, khoảng cách tối đa giữa các điểm trên một đường thẳng)
    if lines is None:
        return 1

    min_line = 100
    min_line_pos = 0
    for i in range (len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            center_point = [((x1+x2)/2), ((y1+y2)/2)]
            if center_thres == 1:
                if center_point[1] < 7:
                    continue
            if center_point[1] < min_line:
                min_line = center_point[1]
                min_line_pos = i

    angle = 0.0
    nlines = lines.size
    cnt = 0
    for x1, y1, x2, y2 in lines[min_line_pos]:
        ang = np.arctan2(y2 - y1, x2 - x1)
        if math.fabs(ang) <= 30: # excluding extreme rotations
            angle += ang
            cnt += 1
    if cnt == 0:
        return 0.0
    return (angle / cnt)*180/math.pi

def xoay_anh(image, center_thres):
    angle = compute_skew(image, center_thres)
    print('goc lech:', angle)
    return rotate_image(image, angle)
     

def get_Characters(model_charaters, new_img):
    result_char = model_charaters(new_img)[0]
    
    result_char_data = sorted(result_char.boxes.data.tolist(), key=lambda box: box[0])

    characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 
                  'L', 'M', 'N', 'P', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    value = ''
    for result_char in result_char_data:
        value += characters[int(result_char[5])]
        
    print("Result: ", value)

def main():

    #video_path = os.path.join('.','video', 'oto_3.mp4')
    #cap = readVideo(video_path)
    #   Web Cam
    cap = cv2.VideoCapture("http://192.168.1.12:81/stream")
    # cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    H, W, _ = frame.shape

    model_plates_path = os.path.join('best_plates.pt')
    model_charaters_path = os.path.join('best_characters.pt')
    # Load a model
    model_plates_path = YOLO(model_plates_path)  # load a plates model
    model_charaters_path = YOLO(model_charaters_path) # load a charaters model
    threshold = 0.5

    get_Frame(model_plates_path, model_charaters_path, ret, frame, cap, threshold)


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()