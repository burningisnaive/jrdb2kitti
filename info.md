# INFO  
date: 2021/6/12  
author: blli  
email: blli@hust.edu.cn  
If you find any bugs or better implementation, please share with me. <br> <br/> 

# Reference 
## Website of JRDB
https://jrdb.stanford.edu/

## JRDB Paper
https://arxiv.org/pdf/1910.11792.pdf

## Sensor Setup 
(You can also find information about coordinates in JRDB sensor setup from this PDF)
http://download.cs.stanford.edu/downloads/jrdb/Sensor_setup_JRDB.pdf

## File Structure
https://drive.google.com/file/d/1DyfU_A0x5OzdDGUWPPPWuW-epupIyvT7/view?usp=sharing

# Maybe helpful
You can find development kits at 
https://jrdb.stanford.edu/benchmark/preparing

## Some comments about convert_dataset_to_KITTI.py in Detection Development Kit
1. download from https://jrdb.stanford.edu/static/assets/detection_eval.zip

2. Converted points are located in rgb coordinate
<img src=imgs/loadpointcloud.png>

3. Labels in 3D Point Clouds (folder 3D)  
The coordinates of these annotations have axes which are oriented as above defined with respect to <font color = blue size=3> the reference frame of the upper Velodyne sensor but are centered on the RGB camera. </font> This means x forward, y left, z up.
(discribed in File Structure)

4. After convertion, the boxes are labeled in <font color = blue size=3> KITTI camera oritentation </font> 

x: right, y: down, z: forward
center of box is the bottom center: -cz + h/2 . 
For more details, refer to
http://www.cvlibs.net/datasets/kitti/index.php  
code snippet from convert_dataset_to_KITTI.py:
<img src=imgs/box_label.png width=70%>

5. Combine 2 and 3, converted 3d boxes are located w.r.t camera coordinate, which is <font color = blue size=3> x: right, y: down, z: forward and centered on the RGB camera </font>.
And you can conclude that
```
Tr_velo_to_cam = [[0, -1, 0, 0],
                  [0, 0, -1, 0],
                  [1, 0,  0, 0]]
```

## Some bugs about convert_dataset_to_KITTI.py
1. \u200b  
unzip the detection_eval.zip, and you may see this while reading convert_dataset_to_KITTI.py
<img src=imgs/u200b.png>
Maybe a short script could help.
I just replace '\u200b's with '' var VScode(Well done! Microsoft).
2. processed_labels/
In line 17-18 of convert_dataset_to_KITTI.py, you see something like IN_LABELS_3D = 'processed_labels/labels_3d/*.json'.
Howerver, there are only 'labels/label_2d' and 'labels/label_3d' in the unzipped files
<img src=imgs/labels.png width=50%>  
It seems that labels are also processed in convert_dataset_to_KITTI.py, so I don't execute convert_labels_to_KITTI.py.  

3. KeyError: ('bytes-cafe-2019-02-07_0', '000000')   
occurs in
<img src=imgs/key_error_1.png>  
because detection_2d is an empty dict.  
one way to fix it:   
```
# line 19: 
IN_DETECTIONS_2D = 'detections/\*.json'
# should be modified to
IN_DETECTIONS_2D = 'detections/detections_2d_stitched/\*.json'  
```

## bugs you might meet about evaluate_object.cpp
1. compiling the file, you may get
```
error: ‘>>’ should be ‘> >’ within a nested template argument list
```
```
error: no match for ‘operator+’ (operand types are ‘std::__cxx11::basic_string<char>’ and ‘const int’)
         result_path = result_dir + '/' + sequence + '/' + frame;
```         
try to compile evaluate_object.cpp with std c++ 11, I failed with std 5
```
g++ -std=c++11 file.cpp -o file
```
2. running the code with detection results organized in "Expected Directory Structure of 3D Detection Submissions"(https://jrdb.stanford.edu/benchmark/preparing) and marked in KITTI format, you may see only zeros  
<img src=imgs/all_zeros.png width=50%>  
The phenomenon can be explained with this code snippet:
<img src=imgs/num_points.png>  
Original code tries to read "num_points_3d" which is invalid in original KITTI format.
I write a modifed version, which has two main differences:
    + disable the check of N_N_TESTIMAGES to make the code works for different spliting
    + disable num_points_3d field in function loadDetection and loadGroundtruth