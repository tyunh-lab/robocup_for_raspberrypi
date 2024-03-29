import cv2 
import numpy as np

def blue_goal_ditect(frame,hsv_image):
    # 青色のHSV範囲を指定
    lower_blue = np.array([100, 100, 100])  # 下限値
    upper_blue = np.array([200, 255, 255])  # 上限値

    # 指定した範囲内のピクセルを抽出
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(frame,frame, mask= blue_mask)

    # 輪郭抽出
    gray = cv2.cvtColor(res_blue, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def yellow_goal_ditect(frame,hsv_image):
    # 黄色のHSV範囲を指定
    lower_yellow = np.array([15, 80, 80])  # 下限値
    upper_yellow = np.array([35, 255, 255])  # 上限値

    # 指定した範囲内のピクセルを抽出
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    res_yellow = cv2.bitwise_and(frame,frame, mask= yellow_mask)

    # 輪郭抽出
    gray = cv2.cvtColor(res_yellow, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours




########デバッグ用##########
def blue(cap, withGUI=False):
    while (cap.isOpened()):
    # 1フレーム毎　読込み
        ret, frame = cap.read()

        # フレームがない場合終了
        if (frame is None):
            break

        # ブラー処理
        frame = cv2.GaussianBlur(frame, (33,33), 0) # <-奇数にしないといけないらしい

        # 画像をHSVに変換
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 青色のHSV範囲を指定
        # lower_blue = np.array([100, 100, 80])  # 下限値
        # upper_blue = np.array([200, 255, 255])  # 上限値
        
        lower_blue = np.array([100, 80, 60])  # 下限値
        upper_blue = np.array([200, 255, 255])  # 上限値

        # 指定した範囲内のピクセルを抽出
        blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
        res_blue = cv2.bitwise_and(frame,frame, mask= blue_mask)

        # 輪郭抽出
        gray = cv2.cvtColor(res_blue, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #　小さいのは省く
        contours = list(filter(lambda x: cv2.contourArea(x) > 300, contours))

        # 各輪郭に対して処理
        for contour in contours:
            # 輪郭を囲む長方形を取得
            # x, y, w, h = cv2.boundingRect(contour)

            #####改良版#####
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            center = (int(rect[0][0]), int(rect[0][1]))

            if withGUI:
                # ゴールの枠を表示
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                frame = cv2.drawContours(frame,[box],0,(0,255,255),2) #<-改良版
                # ゴールの中心を表示
                frame = cv2.circle(frame,center,5,(0,0,255),-1)
                # 中心から線を表示
                frame = cv2.line(frame, (int(frame.shape[1]/2),int(frame.shape[0]/2)), center, (255,0,0), 2)


        if withGUI:
            # 画像の中心を表示
            frame = cv2.circle(frame,(int(frame.shape[1]/2),int(frame.shape[0]/2)),5,(0,0,255),-1)
            # GUIに表示
            cv2.imshow("Camera", frame)
            #マスク画像を表示
            # cv2.imshow("Mask", blue_mask)

        # qキーが押されたら途中終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 終了処理
    cap.release()
    cv2.destroyAllWindows()

def yellow(cap, withGUI=False):
    while (cap.isOpened()):
    # 1フレーム毎　読込み
        ret, frame = cap.read()

        # フレームがない場合終了
        if (frame is None):
            break

        # ブラー処理
        frame = cv2.GaussianBlur(frame, (33,33), 0) # <-奇数にしないといけないらしい

        # 画像をHSVに変換
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 黄色のHSV範囲を指定
        lower_yellow = np.array([20, 100, 100])  # 下限値
        upper_yellow = np.array([40, 255, 255])  # 上限値

        # 指定した範囲内のピクセルを抽出
        yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        res_yellow = cv2.bitwise_and(frame,frame, mask= yellow_mask)

        # 輪郭抽出
        gray = cv2.cvtColor(res_yellow, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #　小さいのは省く
        contours = list(filter(lambda x: cv2.contourArea(x) > 300, contours))

        # 各輪郭に対して処理
        for contour in contours:
            # 輪郭を囲む長方形を取得
            # x, y, w, h = cv2.boundingRect(contour)

            #####改良版#####
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            center = (int(rect[0][0]), int(rect[0][1]))

            if withGUI:
                # ゴールの枠を表示
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                frame = cv2.drawContours(frame,[box],0,(0,255,255),2) #<-改良版
                # ゴールの中心を表示
                frame = cv2.circle(frame,center,5,(0,0,255),-1)
                # 中心から線を表示
                frame = cv2.line(frame, (int(frame.shape[1]/2),int(frame.shape[0]/2)), center, (255,0,0), 2)

        if withGUI:
            # 画像の中心を表示
            frame = cv2.circle(frame,(int(frame.shape[1]/2),int(frame.shape[0]/2)),5,(0,0,255),-1)
            # GUIに表示
            cv2.imshow("Camera", frame)
            #マスク画像を表示
            # cv2.imshow("Mask", yellow_mask)

        # qキーが押されたら途中終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 終了処理
    cap.release()
    cv2.destroyAllWindows()