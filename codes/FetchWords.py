import re

import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'
}


def merge_dict(x, y):
    for k, v in x.items():
        if k in y.keys():
            y[k] += v
        else:
            y[k] = v


def get_html(url):  # 爬取主页
    try:
        html = requests.get(url, headers=header)  # 使用requests库爬取
        if html.status_code == 200:  # 如果状态码是200，则表示爬取成功
            print(url + '获取成功')
            return html.text  # 返回H5代码
        else:  # 否则返回空
            print('获取失败')
            return None
    except:  # 发生异常返回空
        print('获取失败')
        return None


def get_url(html):  # 解析首页得到所有的网页和课程id
    class_list = []  # 定义存放class_id的列表
    class_info = BeautifulSoup(html, "html.parser")
    class_div = class_info.find('div', {'class': 'main_l'})  # 找到存放class_id的div
    class_li = class_div.find('ul', {'class': 'cl'}).find_all('li')  # 找到div下的ul标签内的所有li
    for class_id in class_li:
        class_list.append(class_id.get('class_id'))  # 得到class_id
    return class_list


def get_info(word_html, type_name):  # 爬取所有的单词、发音、翻译
    word_all = {}  # 字典，存放词汇所有相关内容
    word_info = BeautifulSoup(word_html, "html.parser")
    word_div = word_info.find_all('div', class_="word_main_list_w")  # 单词div内容
    pronunce_div = word_info.find_all('div', {'class': 'word_main_list_y'})  # 发音div内容
    trans_div = word_info.find_all('div', {'class': 'word_main_list_s'})  # 翻译div内容
    for i in range(1, len(word_div)):
        key = word_div[i].span.get('title')  # 获取单词
        pronunce = pronunce_div[i].strong.string.split()  # 获取发音
        characteristic = trans_div[i].span.get('title').split(".")[0]
        trans = trans_div[i].span.get('title').split(".")[-1]  # 获取翻译

        if len(pronunce) < 1:  # 无发音则跳过本次循环
            continue
        word_all[key] = [pronunce[0], characteristic+".", trans, type_name]  # 字典结构:字典名={'key': ['value_1','value2_',....,'value_n'],}

    print('创建数据成功')
    return word_all


def main():
    base_url = 'http://word.iciba.com/'  # 主页网址
    base_html = get_html(base_url)  # 得到首页的H5代码
    class_id = get_url(base_html)  # 得到所有class_id值
    # print(class_id)
    print('爬取主页')
    All_Words = dict()
    for id in class_id:  # word_all为class_id所有可能的取值
        # print(id)

        if id == '13':  # 考研词汇class_id
            class_url = 'http://word.iciba.com/?action=courses&classid=' + str(id)  # 利用字符串拼接起来，得到URL网址
            html = get_html(class_url)
            class_info = BeautifulSoup(html, "html.parser")  # 课程信息

            # 获取课程中所有课时，其中li的长度就是课时的数量
            course_li = class_info.find('ul', {'class': 'study-speed-m cl'}).find_all('li')
            name_info = class_info.find('div', {'class': 'word_h2'})  # 得到显示单词类型的div内容
            # print(name)
            r = re.compile(".*?</div>(.*?)</div>")  # 从div中匹配单词类型
            name = re.findall(r, str(name_info))  # 得到单词类型：六级必备词汇, 并存入name列表
            name = name[0]  # 由于列表的值都相同，所以取第一个就好啦
            print('开始爬取' + name)

            # 课时的数量即li标签的数量，就是course的值，考研词汇为1到274
            for course_id in range(1, len(course_li) + 1):
                # 拼接单词的URL
                course_url = 'http://word.iciba.com/?action=words&class=' + str(id) + '&course=' + str(course_id)
                word_html = get_html(course_url)
                print('开始爬取数据')
                word_dict = get_info(word_html, name)  # 得到数据字典
                print('开始存储数据')
                # print(word_dict)
                merge_dict(word_dict, All_Words)
            print(All_Words)
            print(len(All_Words))
            with open("words.txt", "w", encoding="utf-8") as file:
                for k, v in All_Words.items():
                    file.write(k + "\t")
                    for s in v[:-1]:
                        file.write(s + "\t")
                    file.write("\n")


if __name__ == '__main__':
    main()
