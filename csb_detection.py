from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import pylab
import datetime
from PIL import Image
import os

# the path of caffe & the path of python in caffe
import sys,getopt
sys.path.append('/home/bystu/caffe-ssd/python')
import caffe
caffe_root = '/home/nvidia/caffe-ssd/'

#caffe.set_mode_cpu()
caffe.set_mode_gpu()
caffe.set_device(0)

from google.protobuf import text_format
from caffe.proto import caffe_pb2
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

model_def = 'models/deploy.prototxt'
model_weights = 'models/VGG_217_wave_SSD_512x512_iter_40000.caffemodel'
labelmap_file = 'models/labelmap_voc.prototxt'

#get parameter
def GetJPGName(InputImagePath):
    jpg_names = []
    jpgs = os.listdir(InputImagePath)
    for one_jpg in jpgs:
        if (os.path.splitext(one_jpg)[1] == '.jpg') or (os.path.splitext(one_jpg)[1] == '.bmp'):
            jpg_names.append(one_jpg)
    return jpg_names

def WrongInput():
    print("Usage: python slope_detection.py -i InputImagePath -o OutputImagePath -s score -l OutputCSVFileName")
    sys.exit(1)

def GetPara():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:s:l:")
    except getopt.GetoptError:
        WrongInput()
    #get options into dictionary
    option=[]
    value=[]
    for opt,val in opts:
        option.append(opt)
        value.append(val)
    parameter = dict(zip(option,value))
    
    #check para
    if len(parameter.keys()) != 4:
        WrongInput()
    return parameter['-i'],parameter['-o'], parameter['-s'], parameter['-l']    

#about result.csv
def InitCSV(OutputCSVFileName):
    WriteCSVFile = open(OutputCSVFileName, 'w')
    WriteCSVFile.write( ",".join(['0','1','2','3','4','5','6']) + "\n" )
    WriteCSVFile.write( ",".join(['image_name','x1','y1','x2','y2','label','score']) + "\n" )
    WriteCSVFile.close()

def WriteinCSV(OutputCSVFileName,image_name,xmin,ymin,xmax,ymax,label_name,score):
    WriteCSVFile = open(OutputCSVFileName, 'a')
    one_line_data = [image_name,xmin,ymin,xmax,ymax,label_name,score]
    WriteCSVFile.write( ",".join(one_line_data) + "\n" )
    WriteCSVFile.close()

def RunDetection(InputImagePath, OutputImagePath, jpg_names, score_threshold):
    net = caffe.Net(model_def, model_weights, caffe.TEST)
    for one_jpg in jpg_names:
        load_path = os.path.join( InputImagePath + '/' + one_jpg )
        save_path = os.path.join( OutputImagePath + '/' + one_jpg )
        image = caffe.io.load_image(load_path)

        # net = caffe.Net(model_def, model_weights, caffe.TEST)
        transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
        transformer.set_transpose('data', (2, 0, 1))
        transformer.set_mean('data', np.array([104, 117, 123]))  # mean pixel
        transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
        transformer.set_channel_swap('data',(2, 1, 0))  # the reference model has channels in BGR order instead of RGB
        image_resize = 512
        net.blobs['data'].reshape(1, 3, image_resize, image_resize)
        transformed_image = transformer.preprocess('data', image)

        # transformed_image = detection_init(labelmap_file, net, image)
        net.blobs['data'].data[...] = transformed_image
        detections = net.forward()['detection_out']

        # Parse the outputs.
        det_label = detections[0, 0, :, 1]
        det_conf = detections[0, 0, :, 2]
        det_xmin = detections[0, 0, :, 3]
        det_ymin = detections[0, 0, :, 4]
        det_xmax = detections[0, 0, :, 5]
        det_ymax = detections[0, 0, :, 6]

        # Get detections with confidence higher than 0.6.
        top_indices = [i for i, conf in enumerate(det_conf) if conf >= score_threshold]
        top_conf = det_conf[top_indices]
        top_label_indices = det_label[top_indices].tolist()

        # get_lablename_fcn
        file = open(labelmap_file, 'r')
        labelmap = caffe_pb2.LabelMap()
        text_format.Merge(str(file.read()), labelmap)
        num_labels = len(labelmap.item)
        labelnames = []
    
        for label in top_label_indices:
            found = False
            for i in range(0, num_labels):
                if label == labelmap.item[i].label:
                    found = True
                    labelnames.append(labelmap.item[i].display_name)
                    break
            assert found == True

        top_labels = labelnames
        top_xmin = det_xmin[top_indices]
        top_ymin = det_ymin[top_indices]
        top_xmax = det_xmax[top_indices]
        top_ymax = det_ymax[top_indices]
        # Plot the boxes in test picture

        colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()
        plt.switch_backend('agg')
        currentAxis = plt.gca()

        for i in range(top_conf.shape[0]):
            # bbox value
            xmin = int(round(top_xmin[i] * image.shape[1]))
            ymin = int(round(top_ymin[i] * image.shape[0]))
            xmax = int(round(top_xmax[i] * image.shape[1]))
            ymax = int(round(top_ymax[i] * image.shape[0]))
            # score
            score = top_conf[i]
            # label
            label = int(top_label_indices[i])
            label_name = top_labels[i]
            # display info2: label score xmin ymin xmax ymax
            #display_txt = ''
            #display_txt = '%s: %.2f xmin=%d ymin=%d xmax=%d ymax=%d' % (label_name, score, xmin, ymin,xmax, ymax)
            #write in CSV
            WriteinCSV("1.csv", one_jpg, str(xmin), str(ymin), str(xmax), str(ymax) ,label_name, str(score) )
	    # display info1: label score
            #coords = (xmin, ymin), xmax - xmin + 1, ymax - ymin + 1
            #color = colors[label]
            #currentAxis.add_patch( plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2) )
            #currentAxis.text( xmin, ymin, display_txt, bbox={'facecolor': color,'alpha': 0.5} )
        #plt.imshow(image)
        #plt.axis('off')
        #plt.savefig(save_path,bbox_inches='tight')
        #label_set = set(top_labels)

if __name__ == '__main__':
    InputImagePath,OutputImagePath,score_threshold,OutputCSVFileName = GetPara()
    InitCSV(OutputCSVFileName)
    jpg_names = GetJPGName(InputImagePath)
    RunDetection(InputImagePath, OutputImagePath, jpg_names, float(score_threshold) )
    for i in os.listdir(InputImagePath):
        ri = os.path.join(InputImagePath,i)
        #print(ri)
        os.remove(ri)
