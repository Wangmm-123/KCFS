import json
import requests
import simplejson
import base64
import os
import cv2


def find_face(imagpath):
    print("finding")
    ## 旷世（face++） api接口实现人脸识别
    http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    data = {"api_key": 'qShtXyD3sjzPx0VMuE5L4cHGEJ0WneW2',
            "api_secret": 'gq7zDzeXzPjC5pkUc8fvIDgKPtCnjkiX',
            'image_url':imagpath, "return_landmark":1
            }
    files = {'image_file':open(imagpath,'rb')}
    response = requests.post(http_url,data=data,files= files)
    req_con = response.content.decode('utf-8')
    
    this_json = simplejson.loads(req_con)
    faces = this_json['faces']
    list0 = faces[0]
    rectangle = list0['face_rectangle'] # 脸部位置
   
    return rectangle # 返回的是字典 {top,...}

def merge_face(image_url1,image_url2,image_url_new,merge_rate): #merge rate： 清晰度
    ff1 = find_face(image_url1)
    ff2 = find_face(image_url2)

    f1 = open(image_url1,'rb')
    f1_64 = base64.b64encode(f1.read())
    f1.close()

    f2 = open(image_url2,'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()

    
    fc1 = []
    fc2 = []

    for key in ff1:
        fc1.append(str(ff1[key]))
    for key in ff2:
        fc2.append(str(ff2[key]))
    
    fc1 = ",".join(fc1)
    fc2 = ','.join(fc2)

    api_url = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"
    data = {"api_key": 'qShtXyD3sjzPx0VMuE5L4cHGEJ0WneW2',"api_secret": 'gq7zDzeXzPjC5pkUc8fvIDgKPtCnjkiX',
            "template_base64": f1_64, "template_rectangle":fc1,
            "merge_base64": f2_64, "merge_rectangle":fc2, "merge_rate":merge_rate
           }

    response1 = requests.post(api_url,data=data)
    req_con1 = response1.content.decode('utf-8')
    
    req_dict = json.JSONDecoder().decode(req_con1)

    result = req_dict['result']
    imgdata = base64.b64decode(result)
    dir_path = os.path.dirname(image_url_new)
    # dir_path = os.path.dirname(args.out)
    # # if not os.path.isdir(dir_path):
    # #     os.makedirs(dir_path)
    # #
    # # cv2.imwrite(image_url_new, imgdata)
    #
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    file = open(image_url_new,'wb')
    file.write(imgdata)
    # file.close()
    # print("新图片已合成！")
    #

if __name__ =='__main__':

    file = open('train.txt', 'r')  # 打开文件
    # datapath = "F:\CelebA\Img\img_align_celeba"
    datapath = "E:/lfw"
    outpath = './faceswap_results2'
    data = file.readlines()  # 读取所有行
    i = 1
    for line in data:
        tmp_list = line.split(' ')

        file_name1 = tmp_list[2].strip()
        file_name2 = tmp_list[0]
        img1 = os.path.join(datapath + '/' + file_name1)
        img2 = os.path.join(datapath + '/' + file_name2)
        img3_new = outpath + '/faceswap_' + str(i) + '.jpeg'
        i = i + 1
        merge_face(img1,img2,img3_new,100)

