import cv2
import socket

# 待bind的ip/port
ip_port = ('172.20.10.2', 5000) #自己的ip地址与端口号
# 建立socket
s = socket.socket()
# 绑定ip/port
s.bind(ip_port)
# 监听连接
s.listen()
conn, addr = s.accept()


cv2.namedWindow("Image")  # 创建窗口
# 抓取摄像头视频图像
cap = cv2.VideoCapture(0)  # 创建内置摄像头变量
face_cascade = cv2.CascadeClassifier(r'.\haarcascade_frontalface_default.xml')

while (cap.isOpened()):  # isOpened()  检测摄像头是否处于打开状态

    ret, img = cap.read()  # 把摄像头获取的图像信息保存之img变量

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.15,
    minNeighbors=5,
    minSize=(5, 5),
    flags=cv2.CASCADE_SCALE_IMAGE
    )


    if ret == True:  # 如果摄像头读取图像成功
        print "发现{0}个人脸!".format(len(faces))
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + w), (0, 255, 0), 2)
            conn.send(bytes(str(len(faces)), encoding='utf-8'))
        cv2.imshow('Image', img)


        k = cv2.waitKey(10)

        if k == ord('a') or k == ord('A'):
            #cv2.imwrite('test.jpg', img)
            break

conn.close()
cap.release()  # 关闭摄像头
cv2.waitKey(0)
cv2.destroyAllWindows()
