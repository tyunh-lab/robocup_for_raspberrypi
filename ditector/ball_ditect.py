import cv2
import numpy as np

def ball_ditect(frame,hsv_image):
    # オレンジ色のHSV範囲を指定
    lower_orange = np.array([0, 100, 100])  # 下限値
    upper_orange = np.array([20, 255, 255])  # 上限値

    # 指定した範囲内のピクセルを抽出
    orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    res_orange = cv2.bitwise_and(frame,frame, mask= orange_mask)

    # 輪郭抽出
    gray = cv2.cvtColor(res_orange, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours




####デバッグ用#####
def ball(cap, withGUI=False):
    while (cap.isOpened()):
    # 1フレーム毎　読込み
        ret, frame = cap.read()

        # フレームがない場合終了
        if (frame is None):
            break

        # ブラー処理
        frame = cv2.GaussianBlur(frame, (33, 33), 0) # <-奇数にしないといけないらしい

        # 画像をHSVに変換
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        # オレンジ色のHSV範囲を指定
        # lower_orange = np.array([10, 80, 180])  # 下限値
        # upper_orange = np.array([20, 200, 255])  # 上限値

        lower_orange = np.array([0, 125, 200])  # 下限値
        upper_orange = np.array([20, 230, 255])  # 上限値


        # 指定した範囲内のピクセルを抽出
        orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
        res_orange = cv2.bitwise_and(frame,frame, mask= orange_mask)

        # 輪郭抽出
        gray = cv2.cvtColor(res_orange, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #　小さいのは省く
        contours = list(filter(lambda x: cv2.contourArea(x) > 300, contours))

        for i in range(len(contours)):
            (x,y), radius = cv2.minEnclosingCircle(contours[i])
            center = (int(x),int(y))
            # ボールの座標
            # print("x: ", f"{x:.2f}", "y: ", f"{y:.2f}", "radius: ", f"{radius:.2f}",)
            # 中心からのx,yの距離
            # print("x: ", f"{(x - frame.shape[1]/2):.2f}", "y: ", f"{(y - frame.shape[0]/2):.2f}", "radius: ", f"{radius:.2f}",)
            if withGUI:
                # ボールの中心を表示
                frame = cv2.circle(frame,center,5,(0,0,255),-1)

                # 画像の中心とボールの中心を結ぶ線を表示
                frame = cv2.line(frame, (int(frame.shape[1]/2),int(frame.shape[0]/2)), (int(x),int(y)), (255,0,0), 2)

                # 角度を表示
                angle = np.arctan2(y - frame.shape[0]/2, x - frame.shape[1]/2) * 180 / np.pi
                frame = cv2.putText(frame, f"{angle:.2f}", (int(x),int(y)), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2, cv2.LINE_4)
                #大きさを表示
                frame = cv2.putText(frame, f"{radius:.2f}", (int(x),int(y) + 20), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2, cv2.LINE_4)

                # ボールの円を表示
                radius = int(radius)
                frame = cv2.circle(frame,center,radius,(0,255,0),2)

        if withGUI:
            # 画像の中心を表示
            frame = cv2.circle(frame,(int(frame.shape[1]/2),int(frame.shape[0]/2)),5,(0,0,255),-1)
            # GUIに表示
            # cv2.imshow("Camera", frame)
            #マスク画像を表示
            cv2.imshow("Mask", orange_mask)

        # qキーが押されたら途中終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 終了処理
    cap.release()
    cv2.destroyAllWindows()