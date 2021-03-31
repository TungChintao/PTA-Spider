# 该部分实现爬出pta题目以及将爬取的题目存入MySQL的功能
import requests
from urllib.parse import urlencode
import pymysql

headers = {
    'Accept': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.63',
}           # 请求头中需要有Accept参数，否则爬取的数据会乱码


def get_page(url):                          # 爬取url对应的网页的内容
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()          # 返回json格式数据，便于后期处理
        return None
    except requests.ConnectionError:
        return None


def get_problem_list(pro_type):             # 得到题目列表
    params = {
        'problem_type': pro_type,
        'page': 0,
        'limit': 100
    }
    base_url = 'https://pintia.cn/api/problem-sets/14/problem-list?'
    url = base_url + urlencode(params)
    # print(url)
    return get_page(url)


def get_problem_url(json_item):             # 得到每个题目的url
    base_url = 'https://pintia.cn/api/problem-sets/14/problems/'
    if json_item:
        items = json_item.get('problemSetProblems')
        for item in items:
            url = base_url + item.get('id')
            yield url


def get_problem(problem):                  # 得到所需题目
    if problem:
        item = problem.get('problemSetProblem')
        prob = {}
        prob['id'] = item.get('id')
        prob['label'] = item.get('label')
        prob['title'] = item.get('title')
        prob['content'] = item.get('content')
        yield prob


def create_database(data_name):            # 创建数据库以及表格
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306)
    cursor = db.cursor()
    sql = 'CREATE DATABASE IF NOT EXISTS ' + data_name
    cursor.execute(sql)
    cursor.execute('use %s' % data_name)
    sql2 = 'CREATE TABLE IF NOT EXISTS problems (id VARCHAR(6) , label VARCHAR(5) , title VARCHAR(15) , content VARCHAR(1500))'
    cursor.execute(sql2)
    db.close()


def trans_to_mysql(data, data_name):        # 向表单插入爬取的数据
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db=data_name)
    cursor = db.cursor()
    sql3 = 'INSERT INTO problems(id, label, title, content) values(%s, %s, %s, %s)'
    try:
        cursor.execute(sql3, (data['id'], data['label'], data['title'], data['content']))
        db.commit()
    except:
        db.rollback()

    db.close()


def main():
    create_database('pta_data2')
    problem_types = ['CODE_COMPLETION', 'PROGRAMMING']
    for p_type in problem_types:
        json_item = get_problem_list(p_type)
        print(json_item)
        results = get_problem_url(json_item)
        for result in results:
            # print(result)
            problem = get_page(result)
            # print(problem)
            prob = get_problem(problem)
            for i in prob:
                trans_to_mysql(i, 'pta_data2')
                print(i)
                # print(i['label'], i['title'])
                # print(i['content'])


if __name__ == '__main__':
    main()
