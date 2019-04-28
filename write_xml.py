from xml.dom import minidom
import os


"""
根据txt文件，写xml
"""
def W_xml(D,F_name,F_path,F_object):
    """
    :param D: tytd
    :param F_name:图片名字
    :param F_path: 图片路径
    :param F_object: 坐标框
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
    width_text = dom.createTextNode('image_w')
    height_text = dom.createTextNode('image_h')
    depth_text = dom.createTextNode('image_d')
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
        name = dom.createElement('name')
        object.appendChild(name)
        pose = dom.createElement('pose')
        object.appendChild(pose)
        truncated = dom.createElement('truncated')
        object.appendChild(truncated)
        difficult = dom.createElement('difficult')
        object.appendChild(difficult)
        bndbox = dom.createElement('bndbox')
        object.appendChild(bndbox)
        xmin = dom.createElement('xmin')
        bndbox.appendChild(xmin)
        ymin = dom.createElement('ymin')
        bndbox.appendChild(ymin)
        xmax = dom.createElement('xmax')
        bndbox.appendChild(xmax)
        ymax = dom.createElement('ymax')
        bndbox.appendChild(ymax)
        Annotation.appendChild(object)

    return Annotation


if __name__ == '__main__':
    D = 'aaa'
    F_name = '17'
    F_path = 'a/a/a/'
    C = [1,2]
    with open('aa.xml', 'w') as f:
        W_xml(D,F_name,F_path,C).writexml(f,addindent='\t',newl='\n')
        #write:写入的对象，indent:每个tag前填充的字符，addindent：每个子节点的缩近字符，newl:每个tag后填充的字符

