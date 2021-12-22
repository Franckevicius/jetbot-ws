## Pipeline
1. Train with TF2(`model_main_tf2.py`)/PyTorch() on machine/cloud
2. Export to saved model TF2(`exporter_main_v2.py`)/Pytorch()
3. Convert to ONNX with `tf2onnx`/`torchonnx`
4. Load ONNX into TensorRT 
5. Deploy on JetBot

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

## Jetson Stats
[jetson stats docs](https://pypi.org/project/jetson-stats/)

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
- Add `stats.py` to run on startup and display stats on OLED display. Alternatively, use `jtop` API with `stats.py` to route CPU/GPU util, battery percentage to OLED display.

    Currently `stats.py ` since `torch` is paired with `CUDA 10.0`, we have `CUDA 10.2.3` 
    Disabled `/usr/local/lib/python3.6/dist-packages/jetbot-0.4.0-py3.6.egg/jetbot/__init__.py` import `from .object_detection import ObjectDetector`

    `jetbot_stats.service` daemon fails on after a few seconds.

- Jupyter Lab try launch with `0.0.0.0`, otherwise find start for localhost


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

