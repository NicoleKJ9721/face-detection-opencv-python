import cv2
import datetime
import os

def capture_camera():
    # 创建保存图片的目录
    save_dir = "captured_images"
    os.makedirs(save_dir, exist_ok=True)

    # 加载Haar级联分类器用于人脸检测
    # 直接指定Haar级联文件的名称，假设它与脚本在同一目录下
    # 或者你可以提供文件的绝对路径
    cascade_filename = 'haarcascade_frontalface_default.xml'
    
    # 获取脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cascade_path = os.path.join(script_dir, cascade_filename)

    if not os.path.exists(cascade_path):
        print(f"错误：找不到Haar级联文件: {cascade_path}")
        print(f"请确保 '{cascade_filename}' 文件与脚本在同一目录下，")
        print("或者修改脚本中的 'cascade_filename' 为文件的正确路径。")
        print("你可以从以下地址下载该文件：")
        print("https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml")
        return
        
    face_cascade = cv2.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        print(f"错误：无法加载Haar级联分类器，即使文件存在于: {cascade_path}")
        print("这可能意味着文件已损坏或不是有效的级联文件。")
        return
    
    # 初始化摄像头（0-内置摄像头，1-外接摄像头）
    cap = cv2.VideoCapture(0) # 在Mac上，有时需要尝试不同的索引，如 -1 或 1
    
    if not cap.isOpened():
        print("错误：无法访问摄像头。请检查摄像头是否被其他应用占用，或尝试更改 VideoCapture 的索引 (例如 0, 1, -1)。")
        return
    
    # 设置摄像头参数（可选）
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 宽度
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 高度
    cap.set(cv2.CAP_PROP_FPS, 30)            # 帧率
    
    window_name = "MacBook Camera - Press 's' to Save, 'q' to Quit"
    
    while True:
        # 读取摄像头帧
        ret, frame = cap.read()
        if not ret:
            print("错误：无法获取视频帧")
            break
        
        # 针对图像带有角度的问题：
        # 如果图像是旋转的（例如90度），你可能需要在这里添加旋转操作。
        # 请取消注释并选择适合你的旋转方式：
        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE) # 逆时针旋转90度
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)     # 顺时针旋转90度
        # frame = cv2.rotate(frame, cv2.ROTATE_180)              # 旋转180度

        # 镜像显示（更符合自拍习惯），如果进行了旋转，这步应该在旋转之后
        frame = cv2.flip(frame, 1)
        
        # 转换为灰度图像用于人脸检测
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 检测人脸
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # 在检测到的人脸周围绘制矩形
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) # 蓝色矩形
            
        # 添加时间戳
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # 显示画面
        cv2.imshow(window_name, frame)
        
        # 键盘操作
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # 保存图片
            safe_timestamp = timestamp.replace(' ', '_').replace(':', '-')
            filename = f"{save_dir}/capture_{safe_timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"已保存图片到：{filename}")
        elif key == ord('q'):  # 退出程序
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("OpenCV版本：", cv2.__version__)
    
    # 在Apple Silicon (如M1, M2, M4)上，OpenCV可以通过OpenCL利用Metal进行加速
    # 你的输出显示 "OpenCL 不可用"，这可能是因为你的OpenCV构建版本不支持，或者缺少必要的依赖
    # 这通常不影响基本功能，但会缺少GPU加速。
    if cv2.ocl.haveOpenCL():
        cv2.ocl.setUseOpenCL(True)
        if cv2.ocl.useOpenCL():
            print("OpenCL (Metal) 加速已成功启用。")
        else:
            print("OpenCL (Metal) 可用但未能成功启用。")
    else:
        print("OpenCL 不可用，无法启用GPU加速。") # 你的终端输出与此一致
    
    capture_camera()