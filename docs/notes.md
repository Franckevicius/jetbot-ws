## x11vnc headless resolution setup with xrandr
`xrandr --fb 1920x1080 -display :0`

## Connecting bluetooth device 
```sh
sudo echo 1 > /sys/module/bluetooth/parameters/disable_ertm # Default is N
bluetoothctl
scan on
pair MAC_ADDR 
connect MAC_ADDR
```

## TF2 pipeline without detectnet
1. Train with TF2(`model_main_tf2.py`)
2. Export to saved model TF2(`exporter_main_v2.py`)
3. Convert to ONNX with `tf2onnx`
4. Load ONNX into TensorRT
5. Deploy on JetBot

## Training 
```sh
cd jetson-inference/python/training/detection/ssd/
python3 train_ssd.py --dataset-type=voc --data=data/data-12-31 --epochs=100
python3 onnx_export.py --model-dir=./models/ --labels=./models/labels.txt 
```

## Inference
```sh
cd ~/jetbot/jetbot-ws/course-navigation/training-ws
detectnet --model=onnx-exported-models/ssd1-can.onnx --labels=onnx-exported-models/can-labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes csi://0
```

## Traitlet links, controller observe
Must `unlink()`/`unobserve()` after establish `link()`/`observe()` relationship. Observe binds to function object which does not get overwritten - use `unobserve_all()`.

## Camera refuses to connect after `unlink()` 
If using notebooks - kill and restart kernels

## Piping stderr to file
```sh
$ call 2> output.txt
```

## Disabling Jetson GUI 
Saving ~800MB for Unity/GNOME, ~250MB for LXDE

```sh 
$ sudo init 3 # Network and multitasking, no GUI
$ sudo init 5 # Network, multitasking and GUI
```

## ONNX 
[ONNX to TF2 mappings](https://github.com/onnx/tensorflow-onnx/blob/master/support_status.md)

[TensorRT ONNX support](https://github.com/onnx/onnx-tensorrt/blob/master/docs/operators.md):

`TensorRT 8.2 supports operators up to Opset 13`

Check TensorRT 8.0 (JetBot version) operator support 

## Training / Inference
- [int8 will not be supported](https://docs.nvidia.com/deeplearning/tensorrt/support-matrix/index.html#hardware-precision-matrix) (Jetson Nano CUDA arch 5.3, no tensor cores)

    CUDA compute capability = CUDA arch version

- ONNX with [SSD ResNet50 V1 FPN 640x640 (RetinaNet50)](http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8.tar.gz) (`eager operation StridedSlice: attribute new_axis_mask not supported`). 

    Fix - use flags `--opset 11 --fold_const`

- TF2 [CenterNet MobileNetV2 FPN 512x512](http://download.tensorflow.org/models/object_detection/tf2/20210210/centernet_mobilenetv2fpn_512x512_coco17_od.tar.gz) implementation is broken:
     ```
     tensorflow.python.framework.errors_impl.InvalidArgumentError: Attempting to add a duplicate function with name: Dataset_map_TfExampleDecoder.decode_9975 where the previous and current definitions differ
     ```

## Upgrading to Jetpack 4.6
- Try use `jtop` API with `stats.py` to route CPU/GPU util, battery percentage to OLED display.

    Disabled `/usr/local/lib/python3.6/dist-packages/jetbot-0.4.0-py3.6.egg/jetbot/__init__.py` import `from .object_detection import ObjectDetector`

[Script for OPENCV CUDA compilation](https://github.com/AastaNV/JEP/blob/master/script/install_opencv4.5.0_Jetson.sh)  - upgraded to OPENCV-4.5.0

Currently:
```sh
$ jetson_release
 - NVIDIA Jetson Nano (Developer Kit Version)
   * Jetpack 4.6 [L4T 32.6.1]
   * NV Power Mode: MAXN - Type: 0
   * jetson_stats.service: active
 - Libraries:
   * CUDA: 10.2.300
   * cuDNN: 8.2.1.32
   * TensorRT: 8.0.1.6
   * Visionworks: 1.6.0.501
   * OpenCV: 4.5.0 compiled CUDA: YES
   * VPI: ii libnvvpi1 1.1.12 arm64 NVIDIA Vision Programming Interface library
   * Vulkan: 1.2.70
```

## Doc links
[Nvidia VPI 1.1](https://docs.nvidia.com/vpi/index.html)

[TensorRT 8.0.1](https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt-801/index.html)

[CUDA 10.2](https://docs.nvidia.com/cuda/archive/10.2/)

[cuDNN 8.2.1](https://docs.nvidia.com/deeplearning/cudnn/archives/cudnn-821/index.html)

[OPENCV 4.5.0](https://docs.opencv.org/4.5.0/)

[jetson_stats](https://github.com/rbonghi/jetson_stats)

[Jetson Zoo](https://elinux.org/Jetson_Zoo)

[TAO Toolkit](https://docs.nvidia.com/tao/tao-toolkit/index.html)

[GStreamer](https://docs.nvidia.com/jetson/l4t/index.html#page/Tegra%20Linux%20Driver%20Package%20Development%20Guide/accelerated_gstreamer.html#)

[NVBuffer manager](https://docs.nvidia.com/jetson/l4t-multimedia/group__ee__nvbuffering__group.html)
