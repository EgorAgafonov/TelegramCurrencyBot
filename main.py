import requests
import lxml.html
from lxml import etree
from bs4 import BeautifulSoup
import easyocr
import sys
import segno



# 1 -
# - ?????? ???????? ??????????? HTML-???????? (??????? ??????????? ? ???????? ????? ???????) ? ??????? ????????? lxml:

# html = requests.get("https://www.python.org/").content
# tree = lxml.html.document_fromstring(html)
# title = tree.xpath("//*[@id='dive-into-python']/ul[2]/li[1]/div[2]/p/text()")
# print(title)
#
# # ???????? ?????? ElementTree. ?? ???????????? ???????? parse()
# tree = etree.parse('Welcome to Python.org.html', lxml.html.HTMLParser())  # ?????????? ???????? ??? ???? ? ???????
# # HTML-???????. ??? HTML ? ??? ??, ??? ?? ??????? ? ????????? ? ????? ?? ????????.
#
# ul = tree.findall('/body/div/div[3]/div/section/div[2]/div[1]/div/ul/li')  # ???????? ? ???????? ?????? findall
# # ????????????? xpath. ????? ?? ??????? ??? ???????? ?????? ????????.
#
# for li in ul:
#     a = li.find('a')    # ? ?????? ???????? ???????, ??? ???????? ????????? ???????. ? ??? ??? ??? <a>. ?.?.
#                         # ???????????, ?? ??????? ????? ??????, ????? ??????? ?? ???????? ? ????????. ??????????? ?
#                         # HTML ? ??? ?????? ??? <a>.
#     print(a.text)  # ?? ????? ???? ???????? ????? ? ??? ? ????? ????? ?????????


# 2 -
# - ?????? ???????? ??????????? HTML-???????? (??????? ??????????? ? ???????? ????? ???????) ? ??????? ??????????
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

# def text_recognition(file_path):
#     reader = easyocr.Reader(['ru', "en"])
#     result = reader.readtext(file_path, detail=0, paragraph=True)
#     return result
#
#
# def main():
#     file_object = os.path.split("\\chat_images\\test.png")
#     recognized_text = text_recognition(file_path=file_object)
#     print(recognized_text)
#
#     # 1 - ??????? ??????????? ?????? ??????????? OCR
#     recognized_string = '\n'.join(recognized_text)
#     print(recognized_string)
#
#     # 2 - ??????? ??????????? ?????? ??????????? OCR
#     for key in recognized_text:
#         print(key)


# if __name__ == "__main__":
#     main()


qrcode_1 = segno.make_qr("https://github.com/EgorAgafonov/TelegramCurrencyBot.git")
qrcode_1.save("qrcode_1.png")
qrcode_1.show()

