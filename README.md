# 摄像头人脸检测与图像捕捉项目

## 项目介绍

本项目是一个使用 Python 和 OpenCV 实现的简单应用程序，它能够通过计算机的内置或外接摄像头实时捕捉视频流，检测视频中的人脸，并在人脸周围绘制矩形框。用户可以按 's'键保存当前帧（包含人脸检测框和时间戳）为图片，按 'q' 键退出程序。图片将保存在项目根目录下的 `captured_images` 文件夹中。

## 运行环境

- **操作系统**: macOS (已在MacBook上测试)
- **Python版本**: Python 3.6+ (由于使用了f-string等特性)
- **OpenCV版本**: 脚本运行时会打印OpenCV版本，请确保已安装与脚本兼容的版本。

## 依赖包

主要依赖以下 Python 包：

- `opencv-python`: 用于图像处理和摄像头访问。
- `datetime` (Python标准库): 用于生成时间戳。
- `os` (Python标准库): 用于文件和目录操作。

你还需要 `haarcascade_frontalface_default.xml` 文件，这是一个预训练的Haar级联分类器，用于人脸检测。此文件应与 `test.py` 脚本位于同一目录下。

### 安装依赖

你可以使用 pip 安装 OpenCV：

```bash
pip install opencv-python
```

## 如何运行

1.  **确保依赖完整**：
    *   安装 `opencv-python`。
    *   确保 `haarcascade_frontalface_default.xml` 文件与 `test.py` 在同一个目录下。如果找不到，脚本会提示下载地址。
2.  **运行脚本**：
    在项目根目录下打开终端，执行以下命令：
    ```bash
    python test.py
    ```
3.  **操作**：
    *   程序启动后，会打开一个显示摄像头画面的窗口。
    *   窗口标题为 "MacBook Camera - Press 's' to Save, 'q' to Quit"。
    *   按下键盘上的 `s` 键可以保存当前画面到 `captured_images` 文件夹。
    *   按下键盘上的 `q` 键可以关闭程序。

## 文件结构

```
.
├── captured_images/      # 保存捕捉到的图片
├── haarcascade_frontalface_default.xml # Haar级联分类器文件
├── test.py               # 主程序脚本
└── README.md             # 本说明文件
```

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 注意事项

-   如果摄像头无法打开，请检查摄像头是否被其他应用占用，或者尝试修改 `test.py` 文件中 `cv2.VideoCapture()` 的参数（例如 `0`, `1`, `-1`）。
-   脚本默认会进行画面镜像翻转，以符合自拍习惯。如果不需要，可以注释掉 `frame = cv2.flip(frame, 1)` 这一行。
-   如果捕捉到的图像有旋转问题，可以取消注释 `test.py` 文件中 `cv2.rotate()` 相关的行，并选择合适的旋转角度。
-   在Apple Silicon设备上，OpenCV可能尝试使用OpenCL (Metal)进行GPU加速。如果脚本输出 "OpenCL 不可用"，这通常不影响基本功能，但会缺少GPU加速。