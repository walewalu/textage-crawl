from selenium.webdriver import Chrome, ChromeOptions
import csv

# Selenium 옵션 설정
options = ChromeOptions()
options.add_argument('-headless')
browser = Chrome(options=options)

# URL 리스트
baseurl = 'https://textage.cc/score/'
urls = []

# textage.cc 설정
# list_op | 0: 현행 버전, 1: 삭제곡+CS 포함, 2: INFINITAS, 5: CS 수록
single, double = '?s', '?d'
list_op = '0'
score_op = '0'
ttl = 'B000'

# 난이도 1부터 12까지 URL 설정
for i in range(1, 13):
    url = baseurl + single
    if i < 10:
        url = url + str(i)
    else:
        url = url + str(hex(i)).replace('0x', '').upper()
    url = url + list_op + score_op + ttl
    urls.append(url)

# 파일 생성
file = open('data.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)

# 헤더 입력
writer.writerow(['version', 'title', 'chart', 'level', 'bpm', 'notes'])


# 데이터 크롤 함수 작성
def data_crawl(url):
    browser.get(url)

    # tr 속성으로 곡별 정보가 담긴 HTML 요소에 접근, 11행부터 곡별 정보가 담짐
    rawdata = browser.find_elements_by_css_selector('tr')[10:]

    rows = []

    for temp in rawdata:
        data = temp.find_elements_by_css_selector('td')
        version = data[0].text \
            .replace('[', '') \
            .replace(']', '')
        chart = data[1].find_element_by_css_selector('img') \
            .get_attribute('src') \
            .replace('https://textage.cc/score/lv/', '') \
            .replace('.gif', '')
        level = chart[1:]

        if chart[0] == 'b':
            chart = 'BEGINNER'
        elif chart[0] == 'n':
            chart = 'NORMAL'
        elif chart[0] == 'h':
            chart = 'HYPER'
        elif chart[0] == 'a':
            chart = 'ANOTHER'
        elif chart[0] == 'x':
            chart = 'LEGGENDARIA'
        elif chart[0] == 'o':
            chart = 'OTHERS'

        title = data[3].text
        tempo = data[5].text
        notes = data[6].text

        try:
            rows.append([version, title, chart, level, tempo, notes])
            print(title + '(' + chart[0] + ') ok')
        except UnicodeEncodeError as e:
            print(title + ' (' + chart[0] + ') failed: ' + e.reason)

for u in urls:
    print(u + " start")
    data_crawl(u)
    print(u + " finish")

file.close()
browser.quit()
