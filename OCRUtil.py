import base64
import urllib

import pytesseract
from PIL import Image
import requests
from imageai.Detection import ObjectDetection

API_KEY = "cDFraFkMf7txng3M5Zd2nurN"
SECRET_KEY = "7Sjnr6fPioy0ExahU2p6ggwlWOe0A9L2"


def object_detection():
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath("model/resnet50_imagenet_tf.2.0.h5")
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image="doc/pic.png", output_image_path="doc/picnew.jpg", minimum_percentage_probability=30)
    for eachObject in detections:
        print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])


def get_object(path):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/multi_object_detect?access_token=" + get_access_token()

    # image 可以通过 get_file_content_as_base64("C:\fakepath\objects.jpeg",True) 方法获取
    payload = 'image=' + get_file_content_as_base64(path=path, urlencoded=True)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


count_dict = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4
}


def ocr(img_path):
    # 打开图像文件
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img, lang='chi_sim')
    start_index = text.find("的") + 1
    end_index = text.find("后")
    result = text[start_index:end_index]
    result = result.replace(" ", "")
    split_result = result.split("个")
    return count_dict[split_result[0]], split_result[1]


def save_base64_image_to_file(base64_string, file_path):
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_string))


base64_image = "data:image/jpeg;base64,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"
base64_image = base64_image.split("data:image/jpeg;base64,")[1]
file_path = "doc/pic.png"  # 保存的文件路径和名称
if __name__ == '__main__':
    # save_base64_image_to_file(base64_image, file_path)
    # get_object("doc/pic.png")
    print(object_detection())