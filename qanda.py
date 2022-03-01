import requests
from io import BytesIO
import cv2
from urllib import parse
import json

def url2stream(url):
    return BytesIO(requests.get(url).content)

def removeSymbol(detail):
    token = "$|{\\}"
    for i in token:
        detail = detail.replace(i, '')
    return detail.replace("text","")

def search(input): #미완성 코드
    readStream = None

    if str(input).startswith("http"):
        try:
            readstream = url2stream(input)
        except Exception as e:
            return {
                "해당 경로를 찾을 수 없습니다.",
                e
            }
    else:
        try:
            readStream = cv2.imread(input)
        except Exception as e:
            return {
                "해당 경로를 찾을 수 없습니다.",
                e
            }
    requests.get(
        "https://api-gateway.qanda.ai/api/v2/aws/fileserver/key/?ext=jpg",
        headers = {
            "Authorization": "Token 78e41643473b64388bfaa664485ec0a50069d994",
            "Accept-Language": "ko",
            "X-Service-Locale": "ko_KR",
            "X-Jarvis-Config": "prod",
            "Content-Type": "charset=utf-8",
            "X-AP-MAC": "7085C2809FCE",
            "X-Android-DeviceID": "a805ea1bcafe6595",
            "X-IP-ADDRESS": "172.16.61.2",
            "X-Android-DeviceOS": "5.1.1",
            "X-Android-DeviceName": "SM-G965N",
            "X-Android-Version": "4307",
            "X-App-ID": "com.mathpresso.qanda",
            "User-Agent": "QandaStudent/4307 (com.mathpresso.qanda; OS:22)",
            "Connection": "Keep-Alive",
        }
    )

def calc(exp):
    try:
        formula = requests.post(
                url="https://api-gateway.qanda.ai/api/v3/question/input_formula/?version=2&editor_version=2",
                headers = {
                    "Authorization": "Token 78e41643473b64388bfaa664485ec0a50069d994",
                    "Accept-Language": "ko",
                    "X-Service-Locale": "ko_KR",
                    "X-Jarvis-Config": "prod",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-AP-MAC": "7085C2809FCE",
                    "X-Android-DeviceID": "a805ea1bcafe6595",
                    "X-IP-ADDRESS": "172.16.61.2",
                    "X-Android-DeviceOS": "5.1.1",
                    "X-Android-DeviceName": "SM-G965N",
                    "X-Android-Version": "4307",
                    "X-App-ID": "com.mathpresso.qanda",
                    "User-Agent": "QandaStudent/4307 (com.mathpresso.qanda; OS:22)",
                    "Connection": "Keep-Alive"
                },
                data=f"formula={parse.quote(exp)}"
            )
    except:
        return "검색하지 못했습니다."

    id = json.loads(formula.text)["id"]

    calc = requests.get(
            url=f"https://api-gateway.qanda.ai/api/v3/question/input_formula/{id}/?version=2&editor_version=2",
            headers = {
                "Authorization": "Token 78e41643473b64388bfaa664485ec0a50069d994",
                "Accept-Language": "ko",
                "X-Service-Locale": "ko_KR",
                "X-Jarvis-Config": "prod",
                "Content-Type": "charset=utf-8",
                "X-AP-MAC": "7085C2809FCE",
                "X-Android-DeviceID": "a805ea1bcafe6595",
                "X-IP-ADDRESS": "172.16.61.2",
                "X-Android-DeviceOS": "5.1.1",
                "X-Android-DeviceName": "SM-G965N",
                "X-Android-Version": "4307",
                "X-App-ID": "com.mathpresso.qanda",
                "User-Agent": "QandaStudent/4307 (com.mathpresso.qanda; OS:22)",
                "Connection": "Keep-Alive"
            }
        )

    info = json.loads(calc.text)

    if info["results"] == None:
        return "결과가 없습니다."

    info = info["results"][0]["actions"][0]
    result = {}

    try:
        result["title"] = info["action_data"]["prob_title"]
        result["problem"]= removeSymbol(info["action_data"]["problem"]);
        result["solution"] = removeSymbol(info["action_data"]["solutions"][0]["answer"]);

        steps = []

        for i in info["action_data"]["solutions"][0]["steps"]:
            steps.append(removeSymbol(i["description"]["detail"]))
            result["steps"] = steps
    except:
        return "계산도중 실패하였습니다."

    return result
        
