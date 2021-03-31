# 提交代码模块
import requests
import json
import re
import time
from urllib.parse import urlencode

url = 'https://pintia.cn/api/exams/1204048399886860288/submissions'
# 此处cookies为用户登录后的cookies，若使用我的cookies，代码会提交到我的账号，可贴上自己的cookies进行测试
Cookies = '******'
headers = {
    'Accept': 'application/json;charset=UTF-8',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': Cookies,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.63',
}


def get_page(url, code):
    # problemType 参数指定题目类型
    # problemSetProblemId 参数指定要提交的题目，题目对应的id可从爬取的数据中查看
    # compiler指定编译器
    # 后续可优化为完整功能段
    data = {
        "problemType": "CODE_COMPLETION",
        "details": [{"problemId": "0", "problemSetProblemId": "735",
                     "codeCompletionSubmissionDetail": {"program": code, "compiler": "GCC"}}]}

    data = json.dumps(data)    # 格式要转换为json
    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.headers, response.json()
        return None
    except requests.ConnectionError:
        return None


def get_problem_judge(param):
    base_url = 'https://pintia.cn/api/submissions/'
    urls = base_url + param + '?preview_submission=false'
    # print(url)

    #  重点，如果不加time.sleep,返回的响应的测评状态都显示judging，原因是太快返回响应，此时，oj还在测评中
    #  必须加上time.sleep来控制时间，使得返回的是测评后的结果，而不是judging即正在测评中
    time.sleep(1)
    response = requests.get(urls, headers=headers)
    print(response.status_code)
    return response.json()


def main():

    # 此处第二个参数传入要提交的代码，后续可优化为完整功能段，暂且先这样测试
    header, page = get_page(url, "#include<stdio.h>\r\n\r\nint Sum ( int List[], int N )\r\n{\r\n    int total = "
                                 "0;\r\n    int n = 0;\r\n\r\n    while(n<N){\r\n        total += List[n];\r\n        "
                                 "n++;\r\n    }\r\n    \r\n    return total;\r\n}\r\n")
    print(page)
    # 通过观察可知，submission后会返回一个submissionId字段
    # 得到测评结果的url需要用该字段的数据构造
    p = page.get('submissionId')
    print(p)
    # head = header.get('Set-Cookie')
    # head = re.sub('; Path=/; Secure; HttpOnly', '', head)
    # print(head)
    # Cookies = cookie_copy + str(head)
    r = get_problem_judge(p)
    print(r)


if __name__ == '__main__':
    main()