"""[事件监测模块]
负责人:李佳恩
功能:调用openpose识别动作，目前可以识别举手动作包含左右手
"""
from PyQt5.QtCore import QThread, pyqtSignal, Qt
#  openpose依赖
from PyQt5.QtGui import QImage


class CameraThread(QThread):
    changePixmap = pyqtSignal(QImage)
    close_camera = pyqtSignal()
    raise_hand = pyqtSignal(str)

    flag = True
    # opencv camera
    # def run(self):
    #     cap = cv2.VideoCapture(0)
    #     while True:
    #         ret, frame = cap.read()
    #         if ret:
    #             rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #             convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
    #             p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
    #             self.changePixmap.emit(p)

    def __del__(self):
        self.flag = False

    def run(self):
        import cv2
        from tf_pose.estimator import TfPoseEstimator
        from tf_pose.networks import get_graph_path, model_wh

        print('creating camera thread...')
        w, h = model_wh("432x368")
        e = TfPoseEstimator(get_graph_path("mobilenet_thin"), target_size=(432, 368))
        #   logger.debug('cam read+')
        cam = cv2.VideoCapture(0)
        ret_val, image = cam.read()
        #   logger.info('cam image=%dx%d' % (image.shape[1], image.shape[0]))
        print(self.flag)
        while self.flag:
            ret_val, image = cam.read()
            if ret_val:
                # logger.debug('image process+')
                humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=(4.0))
                # logger.debug('postprocess+')
                image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

                for human in humans:
                    # draw point
                    # 18=common.CocoPart.Background.value
                    for i in range(18):
                        if i not in human.body_parts.keys():
                            continue

                        body_part = human.body_parts[i]

                        # i=2 右肩膀
                        if i == 2:
                            tmp_right_y = body_part.y
                        # i=5 左肩膀
                        if i == 5:
                            tmp_left_y = body_part.y

                        if i == 4:
                            if tmp_right_y > body_part.y:
                                print("举右手", body_part.x, body_part.y)
                                self.raise_hand.emit("右手")
                            # print("右手",body_part.x, body_part.y)
                            # cv2.putText(npimg, '右手腕', (int(body_part.x), int(body_part.y)),cv2.FONT_HERSHEY_COMPLEX, 6, (0, 0, 255), 25)

                        if i == 7:
                            if tmp_left_y > body_part.y:
                                print("举左手", body_part.x, body_part.y)
                                self.raise_hand.emit("左手")
                            # print("左手",body_part.x, body_part.y)
                            # cv2.putText(npimg, '左手腕', (int(body_part.x), int(body_part.y)), cv2.FONT_HERSHEY_COMPLEX, 6,(0, 0, 255), 25)

                # logger.debug('show+')
                # cv2.putText(image,
                #             "FPS: %f" % (1.0 / (time.time() - 0)),
                #             (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                #             (0, 255, 0), 2)
                # cv2.imshow('tf-pose-estimation result', image)
                rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                self.sleep(0.5)
            # logger.debug('finished+')

        cam.release()

        print("relase open-cv camera ...")
        self.close_camera.emit()
