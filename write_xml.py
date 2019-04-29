"""
根据txt，生成xml格式文件。
"""
from xml.dom import minidom
import os
import cv2
import sys


"""
根据txt文件，写xml
"""
def W_xml(D,F_name,F_path,F_img,F_object):
    """
    :param D: tytd
    :param F_name:图片名字
    :param F_path: 图片路径
    :param F_object: 坐标框
    :param F_img:图片大小
    :return: tree(一个annotation)
    """
    #创建DOM树对象
    dom = minidom.Document()
    #创建根节点
    Annotation = dom.createElement('Annotation')
    #用DOM对象添加根节点
    dom.appendChild(Annotation)

    #创建子节点
    folder =dom.createElement('folder')
    #添加子节点内容
    folder_text = dom.createTextNode(str(D))
    #将本文节点插入到<folder_text>下
    folder.appendChild(folder_text)
    #将foler插入到Annotation节点下
    Annotation.appendChild(folder)

    #创建图片名节点
    filename = dom.createElement('filename')
    filename_text = dom.createTextNode(str(F_name))
    filename.appendChild(filename_text)
    Annotation.appendChild(filename)

    #创建path节点
    filepath = dom.createElement('filepath')
    filepath_text = dom.createTextNode(str(F_path))
    filepath.appendChild(filepath_text)
    Annotation.appendChild(filepath)

    #创建source节点
    source = dom.createElement('source')
    database = dom.createElement('database')
    database_text = dom.createTextNode(str('Unknow'))
    database.appendChild(database_text)
    source.appendChild(database)
    Annotation.appendChild(source)

    #创建size节点,image_w/h/d 表示图片的长、宽、深度
    size = dom.createElement('size')
    width = dom.createElement('width')
    height = dom.createElement('height')
    depth = dom.createElement('depth')
    width_text = dom.createTextNode(str(F_img[0]))
    height_text = dom.createTextNode(str(F_img[1]))
    depth_text = dom.createTextNode(str(F_img[2]))
    size.appendChild(width)
    width.appendChild(width_text)
    size.appendChild(height)
    height.appendChild(height_text)
    size.appendChild(depth)
    depth.appendChild(depth_text)
    Annotation.appendChild(size)

    #创建segmented
    segmented = dom.createElement('segmented')
    segmented_text = dom.createTextNode('0')
    segmented.appendChild(segmented_text)
    Annotation.appendChild(segmented)

    #创建object
    for i in F_object:
        object = dom.createElement('object')
        Annotation.appendChild(object)

        name = dom.createElement('name')
        object.appendChild(name)

        name_txt = dom.createTextNode(str(i.split(',')[4].split('\n')[0]))
        name.appendChild(name_txt)

        pose = dom.createElement('pose')
        pose_txt = dom.createTextNode('Unspecified')
        pose.appendChild(pose_txt)
        object.appendChild(pose)

        truncated = dom.createElement('truncated')
        truncated_txt = dom.createTextNode('0')
        truncated.appendChild(truncated_txt)
        object.appendChild(truncated)

        difficult = dom.createElement('difficult')
        difficult_txt = dom.createTextNode('0')
        difficult.appendChild(difficult_txt)
        object.appendChild(difficult)

        bndbox = dom.createElement('bndbox')

        xmin = dom.createElement('xmin')
        xmin_txt = dom.createTextNode(str(i.split(',')[0]))
        xmin.appendChild(xmin_txt)
        bndbox.appendChild(xmin)

        ymin = dom.createElement('ymin')
        ymin_txt = dom.createTextNode(str(i.split(',')[1]))
        ymin.appendChild(ymin_txt)
        bndbox.appendChild(ymin)

        xmax = dom.createElement('xmax')
        xmax_txt = dom.createTextNode(str(i.split(',')[2]))
        xmax.appendChild(xmax_txt)
        bndbox.appendChild(xmax)

        ymax = dom.createElement('ymax')
        ymax_txt = dom.createTextNode(str(i.split(',')[3]))
        ymax.appendChild(ymax_txt)
        bndbox.appendChild(ymax)

        object.appendChild(bndbox)

    return Annotation

"""
读txt,返回坐标、类别
"""
def R_txt(txt_path):
    with open(txt_path,'r') as f:
        data = f.readlines()
    return data

"""
读图片，获取size、depth
"""
def R_img(img_path):
    img = cv2.imread(img_path)
    return img.shape

if __name__ == '__main__':
    txt_path = sys.argv[1]  #txt路径
    img_path = sys.argv[2]  #图片路径
    annotation_path = sys.argv[3]   #xml保存路径
    for i in os.listdir(txt_path):
        txt_i = R_txt(os.path.join(txt_path,i))
        print(os.path.join(img_path,'{}.jpg'.format(i.split('.')[0])))
        img_i = R_img(os.path.join(img_path,'{}.jpg'.format(i.split('.')[0])))
        with open(os.path.join(annotation_path,'{}.xml'.format(i.split('.')[0])), 'w') as f:
            W_xml('tytd',
                  i.split('.')[0],
                  os.path.join(img_path,'{}.jpg'.format(i.split('.')[0])),
                 img_i,txt_i ).writexml(f,addindent='\t',newl='\n')