# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [options.proto](#options.proto)
    - [FaceDetectorOptions](#.FaceDetectorOptions)
    - [HaarCascadeModel](#.HaarCascadeModel)
  
  
  
  




<a name="options.proto"></a>
<p align="right"><a href="#top">Top</a></p>

## options.proto



<a name=".FaceDetectorOptions"></a>

### FaceDetectorOptions
Service Configuration


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| broker_uri | [string](#string) |  |  |
| zipkin_host | [string](#string) |  |  |
| zipkin_port | [uint32](#uint32) |  |  |
| zipkin_batch_size | [uint32](#uint32) |  |  |
| model | [HaarCascadeModel](#HaarCascadeModel) |  | Configurations of the HaarCascade model |






<a name=".HaarCascadeModel"></a>

### HaarCascadeModel



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| model_file | [string](#string) |  | Path of the model |
| scale_factor | [float](#float) |  | The value indicates how much the image size is reduced at each image scale |
| min_neighbors | [uint32](#uint32) |  | How many “neighbors” each candidate rectangle should have |
| min_size | [google.protobuf.ListValue](#google.protobuf.ListValue) |  | The minimum object size |





 

 

 

 



