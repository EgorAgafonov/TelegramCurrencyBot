import requests
import lxml.html
from lxml import etree
from bs4 import BeautifulSoup
import easyocr
import os


# 1 -
# - пример парсинга содержимого HTML-страницы (заранее сохраненной в корневой папке проекта) с помощью иблиотеки lxml:

# html = requests.get("https://www.python.org/").content
# tree = lxml.html.document_fromstring(html)
# title = tree.xpath("//*[@id='dive-into-python']/ul[2]/li[1]/div[2]/p/text()")
# print(title)
#
# # создадим объект ElementTree. Он возвращается функцией parse()
# tree = etree.parse('Welcome to Python.org.html', lxml.html.HTMLParser())  # попытаемся спарсить наш файл с помощью
# # HTML-парсера. Сам HTML — это то, что мы скачали и поместили в папку из браузера.
#
# ul = tree.findall('/body/div/div[3]/div/section/div[2]/div[1]/div/ul/li')  # помещаем в аргумент методу findall
# # скопированный xpath. Здесь мы получим все элементы списка новостей.
#
# for li in ul:
#     a = li.find('a')    # в каждом элементе находим, где хранится заголовок новости. У нас это тег <a>. Т.е.
#                         # гиперссылка, на которую нужно нажать, чтобы перейти на страницу с новостью. Гиперссылки в
#                         # HTML — это всегда тэг <a>.
#     print(a.text)  # из этого тега забираем текст — это и будет нашим названием


# 2 -
# - пример парсинга содержимого HTML-страницы (заранее сохраненной в корневой папке проекта) с помощью библиотеки
# bs4 import BeautifulSoup:

# base = 'https://ru.stackoverflow.com'
# html = requests.get(base).content
# soup = BeautifulSoup(html, 'lxml')
# div_container = soup.find('div', id='question-mini-list')
# a_tag = div_container.findAll('a', class_='s-link')
# file = 'lxml_lessons.txt'
# with open(file, 'w', encoding='windows-1251') as f:
#     for link in a_tag:
#         result = f"\n{link.getText()}\n" + f"\n{base + link.get('href')}\n"
#         f.write(result)
#         print(f"{link.getText()}\n" + f"{base + link.get('href')}\n")


def text_recognition(file_path):
    reader = easyocr.Reader(['ru', "en"])
    result = reader.readtext(file_path, detail=0, paragraph=True)
    return result


def main():
    file_object = os.path.abspath("C:\\Users\\agafo\\PycharmProjects\\TelegramCurrencyBot\\text_rec.jpg")
    recognized_text = text_recognition(file_path=file_object)
    print(recognized_text)

    # 1 - вариант построчного вывода результатов OCR
    recognized_string = '\n'.join(recognized_text)
    print(recognized_string)

    # 2 - вариант построчного вывода результатов OCR
    # for key in recognized_text:
    #     print(key)


if __name__ == "__main__":
    main()
