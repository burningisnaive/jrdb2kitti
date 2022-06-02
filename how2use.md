# Convert JRDB format to KITTI format

## download JRDB dataset
download and unzip 
you get:
```
train_dataset
    |---calibration           
    |---detections
    |---images
    |---labels
    |---pointclouds
    |---rosbags
    |---timestamps
    
test_dataset
    |---calibration           
    |---detections
    |---images
    |---pointclouds
    |---rosbags
    |---timestamps
```

## convert training set 
1.  convert file structure. 
    type 
    ```
    python convert2KITTI.py -o jrdb_KITTI/object/training -i jrdb/train_dataset
    ```
    and you will get
    ```
    jrdb_KITTI/object/training
        |---calib
        |---image_2          
        |---velodyne
        |---label_2
        |---detection
        |---filelist.txt
    ```
    filelist.txt records the order of "scene frame" of JRDB, its content looks like
    ```
    bytes-cafe-2019-02-07_0 000000
    bytes-cafe-2019-02-07_0 000001
    bytes-cafe-2019-02-07_0 000002
    bytes-cafe-2019-02-07_0 000003
    bytes-cafe-2019-02-07_0 000004
    bytes-cafe-2019-02-07_0 000005
    bytes-cafe-2019-02-07_0 000006
    bytes-cafe-2019-02-07_0 000007
    ...
    ```
2.  generate calibrations
    type 
    ```
    python build_kitti_calib.py -o jrdb_KITTI/object/training -n 27947
    # there are 27947 frames in convert training set
    ```  

## convert testing set 
1.  convert file structure. 
    type 
    ```
    python convert_testset_to_KITTI.py -o jrdb_KITTI/object/testing -i jrdb/test_dataset
    ```
    and you will get
    ```
    jrdb_KITTI/object/testing
        |---calib
        |---image_2          
        |---velodyne
        |---detection
        |---filelist.txt
    ```
2.  generate calibrations
    type 
    ```
    python build_kitti_calib.py -o jrdb_KITTI/object/training -n 27661
    # there are 27661 frames in convert testing set
    ```  
## split the dataset
type
```
python build_split_txt.py -o jrdb_KITTI --filelist jrdb_KITTI/object/training/filelist.txt --test_num 27661
```
you will get
```
jrdb_KITTI/ImageSets
    |---test.txt
    |---train.txt
    |---trainval.txt
    |---val.txt
```
note that authors of JRDB provide a suggested validation split which can be find in detection_eval/README.md.  
```
clark-center-2019-02-28_1
gates-ai-lab-2019-02-08_0
huang-2-2019-01-25_0
meyer-green-2019-03-16_0
nvidia-aud-2019-04-18_0
tressider-2019-03-16_1
tressider-2019-04-26_2 
```

## if you want clean labels 
JRDB 3d detection benckmark ignore a object if one of these is met
+ has less than 10 points
+ is more than 25m away from original point on bev-view 

For convenience, convert_cleanlabel.py remove labels which 
+ has less than 10 points
+ is fully occluded on stitched images
type 
```
python convert_cleanlabel.py -o jrdb_KITTI/object/training -i jrdb/train_dataset
```
only jrdb_KITTI/object/training/label_2 will be overwritten

## prepare submission to JRDB website
to convert KITTI-format detection result for 3d detection submission  
```
python convert2JRDB.py -d directory/for/output -l KITTI-format/label -f jrdb_KITTI/object/testing/filelist.txt
```
you will get
```
directory/for/output
    |---cubberly-auditorium-2019-04-22_1
    |---discovery-walk-2019-02-28_0
    |---discovery-walk-2019-02-28_1
    |---food-trucks-2019-02-12_0
    |---gates-ai-lab-2019-04-17_0
    |---gates-basement-elevators-2019-01-17_0
    |---gates-foyer-2019-01-17_0
    |---gates-to-clark-2019-02-28_0
    |---hewlett-class-2019-01-23_0
    ...
```
zip and submit the archive