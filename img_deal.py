import cv2
from PIL import Image


def get_contours():
    """获取图像轮廓 """
    img = r'E:\Programme\GIT\Python\Hotchpotch\Itchat2Api\Ico\cangshu.png'
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 获取灰度图
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 利用阈值自动选择的方法获取二值图像
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 检测轮廓
    print(len(contours))
    cv2.drawContours(img, contours, 28, (0, 255, 0), 3)  # 画出轮廓
    cv2.imshow('gray', binary)
    cv2.imshow('res', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_pixel(file,mode='row'):
    """
    获取需要的图片像素点和值
    :return: mode['RGB'|'RGBA'|*],size[w,h],data[x,y,v1,v2,v3,[v4]]
    """

    # 修改分辨率
    # im = cv2.imread(file)
    # im = cv2.resize(im,(1920,1920))
    # cv2.imwrite('cs.png',im)
    # return

    img = Image.open(file,'r')

    # 旋转
    # img.rotate(90)

    # 存储值
    new_datas = []
    # 遍历读取像素值， PIL的坐标是x,y的形式

    # 按行读取
    if mode == 'row':
        for y in range(img.height):
            current = []
            temp = []
            flg = 0
            for x in range(img.width):
                # 获取像元
                pixel = img.getpixel((x,y))

                if img.mode == 'RGBA':
                    if pixel != (0, 0, 0,0): # ======== 修改区域 =========
                        flg = 1
                    elif flg == 1: flg = 2

                    if flg == 1:
                        if temp:
                            current.extend(temp)
                            temp.clear()
                        current.append([x,y, pixel[0], pixel[1], pixel[2], pixel[3]])

                    elif flg == 2: temp.append([x,y, pixel[0], pixel[1], pixel[2], pixel[3]])

                else:
                    # 限定范围修改
                    if 420 < y < 485:
                        if pixel[0] < 249 and pixel[1] < 249 and pixel[2] < 249: # ======== 修改区域 =========
                            flg = 1
                        elif flg == 1: flg = 2
                    else:
                        if pixel[2] < 234: # ======== 修改区域 =========
                            flg = 1
                        elif flg == 1: flg = 2

                    if flg == 1:
                        if temp:
                            current.extend(temp)
                            temp.clear()
                        current.append([x,y, pixel[0], pixel[1], pixel[2]])

                    elif flg == 2: temp.append([x,y, pixel[0], pixel[1], pixel[2]])

            if current: new_datas.append(current)

    # 按列读取
    else:
        for x in range(img.width):
            current = []
            temp = []
            flg = 0
            for y in range(img.height):
                # 获取像元
                pixel = img.getpixel((x, y))

                if img.mode == 'RGBA':
                    if pixel != (0, 0, 0, 0): # ======== 修改区域 =========
                        flg = 1
                    elif flg == 1:
                        flg = 2

                    if flg == 1:
                        if temp:
                            current.extend(temp)
                            temp.clear()
                        current.append([x, y, pixel[0], pixel[1], pixel[2], pixel[3]])

                    elif flg == 2:
                        temp.append([x, y, pixel[0], pixel[1], pixel[2], pixel[3]])

                else:
                    # if pixel[0] < 250 and pixel[1] < 250 and pixel[2] < 250: # ======== 修改区域 =========
                    # 过滤白色，但是获取蓝色
                    if pixel[0] < 240 and pixel[1] < 240: # ======== 修改区域 =========
                        flg = 1
                    elif flg == 1:
                        flg = 2

                    if flg == 1:
                        if temp:
                            current.extend(temp)
                            temp.clear()
                        current.append([x, y, pixel[0], pixel[1], pixel[2]])

                    elif flg == 2:
                        temp.append([x, y, pixel[0], pixel[1], pixel[2]])

            if current: new_datas.append(current)

    print('像素值获取完成')

    return img.mode, img.size, new_datas

def new_img(mode, size,datas=None,path=None, mat=None,flg=None):
    """
    创建新图像
    :param mat: 图片格式
    :param mode:
    :param size:
    :param path: 保存路径
    :param datas:
    :return:
    """
    if not path:  path = './Ico/imgrec2.png'

    if not mat: mat = 'PNG'

    # 创建新图像
    img = Image.new(mode, size, (0,255,0))
    # new_img.show()
    if datas:
        for index,line in enumerate(datas):
            for x in line:
                if mode == "RGBA":
                    # ======== 修改区域 =========
                    if index > len(datas)-20:
                        img.putpixel((x[0], x[1]), (0,0,0,0))
                        continue
                    if x[2] == 0: img.putpixel((x[0], x[1]), (26, 250, 41, 1))  # 26,250,41
                    else: img.putpixel((x[0], x[1]), (x[2], x[3], x[4], x[5])) # 26,250,41

                else:
                    # ======== 修改区域 =========
                    if flg:
                        if index > len(datas)-23 or index < 80:
                            img.putpixel((x[0], x[1]), (0,255,0))
                            continue
                        if index == len(datas)-23:
                            img.putpixel((x[0], x[1]), (0,0,255))
                            continue

                    img.putpixel((x[0], x[1]), (x[2], x[3], x[4]))  # 26,250,41

    img.save(path, mat)
    print('图像创建完成')
    img.show()
    return img,path


def get_canny(file=None,path=None):
    """获取图像边缘轮廓"""
    if not file: file = r'E:\Programme\GIT\Python\Hotchpotch\Itchat2Api\Ico\imgrec.png'

    if not path: path = './canny.png'

    img = cv2.imread(file)
    img_canny = cv2.Canny(img,60,200)
    cv2.imshow('img',img)
    cv2.imshow('img_canny',img_canny)
    cv2.imwrite(path,img_canny)
    print('边缘获取完成')
    cv2.waitKey(0)

def img_evenness(file):
    img = cv2.imread(file)
    res = cv2.GaussianBlur(img,(21,21),1,1,1)
    cv2.imshow('res',res)
    cv2.waitKey(0)



if __name__ == '__main__':
    # file = r'E:\Programme\GIT\Python\Hotchpotch\Itchat2Api\Ico\imgrec.png'
    _file = r'E:\Programme\GIT\Python\Hotchpotch\Itchat2Api\Ico\cangshu.png'
    data = get_pixel(_file,'row')
    data = new_img(data[0],data[1],data[2],flg=True)
    data = get_pixel(data[1],'col')
    data = new_img(data[0], data[1], data[2])
