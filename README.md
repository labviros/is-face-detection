# Protocol Documentation
<a name="top"/>

## Table of Contents

- [conf/options.proto](#conf/options.proto)
    - [FaceDetectorOptions](#.FaceDetectorOptions)
    - [HaarCascadeModel](#.HaarCascadeModel)
  
  
  
  

- [Scalar Value Types](#scalar-value-types)



<a name="conf/options.proto"/>
<p align="right"><a href="#top">Top</a></p>

## conf/options.proto



<a name=".FaceDetectorOptions"/>

### FaceDetectorOptions
All options


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| broker_uri | [string](#string) |  | Uri of the broker |
| model | [HaarCascadeModel](#HaarCascadeModel) |  | Haarcascade Model |






<a name=".HaarCascadeModel"/>

### HaarCascadeModel
Options of the HaarCascade model


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| model_file | [string](#string) |  | Path of the model |
| scale_factor | [float](#float) |  | The value indicates how much the image size is reduced at each image scale |
| min_neighbors | [uint32](#uint32) |  | How many “neighbors” each candidate rectangle should have |
| min_size | [google.protobuf.ListValue](#google.protobuf.ListValue) |  | The minimum object size |





 

 

 

 



