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

If using scripts - reboot

## Piping stderr to file
```sh
$ command 2> output.txt
```

## Disabling Jetson GUI 
Saving ~800MB for Unity/GNOME, ~250MB for LXDE

```sh 
$ sudo init 3 # Network and multitasking, no GUI
$ sudo init 5 # Network, multitasking and GUI
```

## Training issues
- ONNX does not support [SSD ResNet50 V1 FPN 640x640 (RetinaNet50)](http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8.tar.gz) (`eager operation StridedSlice: attribute new_axis_mask not supported`)

- [CenterNet MobileNetV2 FPN 512x512](http://download.tensorflow.org/models/object_detection/tf2/20210210/centernet_mobilenetv2fpn_512x512_coco17_od.tar.gz) implementation is broken:

     ```
     tensorflow.python.framework.errors_impl.InvalidArgumentError: Attempting to add a duplicate function with name: Dataset_map_TfExampleDecoder.decode_9975 where the previous and current definitions differ
     ```