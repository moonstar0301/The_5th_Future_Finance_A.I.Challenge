from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def process_page(title, href, driver, c):
    # 게시글 방문
    driver.get(href)
    time.sleep(1)  # 페이지 로딩 대기

    # 등록일 정보 크롤링
    date_elements = driver.find_elements(By.CLASS_NAME, "date")
    date_text = ""
    for date_element in date_elements:
        em_element = date_element.find_element(By.TAG_NAME, "em")
        if em_element.text == "등록일":
            date_text = date_element.text.replace("등록일", "").strip()
            break

    # PDF 파일 작업
    font_size = 10  # 폰트 크기
    gap = font_size + 2  # 줄간격
    starting_point = 700  # 시작 위치
    y_position = 700  # 현위치
    x_position = 30 # 시작 위치
    max_words = 70 #최대 n자씩 표시
    c.setFont("Korean", 10)  # 폰트 크기를 10으로 설정
    c.drawString(x_position, y_position, f"Title: {title}")  # 타이틀 추가
    y_position -= gap
    c.drawString(x_position, y_position, f"등록일: {date_text}")  # 등록일 추가
    y_position -= gap
    view_cont = driver.find_element(By.ID, "view_cont").text
    lines = view_cont.split("\n")
    lines = [line for line in lines if line.strip() != '']
    for line in lines:
        while len(line) > 0:
            if y_position < 50:
                c.showPage()
                c.setFont("Korean", font_size)
                y_position = starting_point
            line_part = line[:max_words]
            c.drawString(x_position, y_position, line_part)
            y_position -= gap
            line = line[max_words:]
    y_position -= gap
    c.showPage()


def crawling(topic, url):
    print(f"{topic} progressing(0%)", end="\r")
    # 크롬 드라이버 자동 업데이트
    chrome_driver_path = ChromeDriverManager().install()

    # Selenium 웹 드라이버 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # 브라우저를 숨김
    chrome_options.add_argument("--disable-gpu")
    service = webdriver.chrome.service.Service(executable_path=chrome_driver_path)

    # PDF 파일 생성
    pdf_file_path = f"researches/{topic}.pdf"

    c = canvas.Canvas(pdf_file_path, pagesize=letter)

    # 한글 폰트 설정
    font_path = "./font/NanumGothic.ttf"
    pdfmetrics.registerFont(TTFont("Korean", font_path))

    # 1. url에 진입한다.
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(1)

    total_pages = 5  # 총 페이지 수
    page_progress_step = 100 // total_pages  # 한 페이지 진행시 증가할 단계

    # 1페이지부터 total_pages까지 반복
    for page_num in range(1, total_pages + 1):
        tbl_list = driver.find_element(By.CLASS_NAME, "tbl_list")
        links = tbl_list.find_elements(By.TAG_NAME, "a")
        titles = [link.text for link in links]
        hrefs = [link.get_attribute("href") for link in links]

        # 각 링크별로 페이지 처리
        for title, href in zip(titles, hrefs):
            process_page(title, href, driver, c)
        
        #현재 진행상황 출력
        progress_percentage = page_num * page_progress_step
        print(f"{topic} progressing({progress_percentage}%)", end="\r")
        
        # 초기 페이지로 가기
        driver.get(url)
        time.sleep(1)
        # 페이지 넘어가는 버튼 클릭 및 로딩 대기
        if page_num < 5:
            next_page_num = page_num + 1
            next_page_button = driver.find_element(By.XPATH, f'//*[@id="pageinput{next_page_num}"]/span/input')
            next_page_button.click()
            time.sleep(1)  # 페이지 로딩 대기
    print(f"{topic} progressing(100%)")  # 마지막에 100% 출력
    driver.quit()

    # 기존의 real_estate.pdf 파일 삭제
    if os.path.exists(pdf_file_path):
        os.remove(pdf_file_path)
    c.save()  # PDF 파일 저장

def real_estate_research_crawl():
    topic = "real_estate"
    url = "https://omoney.kbstar.com/quics?page=C042015&cc=b037806:b037806"
    crawling(topic, url)
    
def tax_research_crawl():
    topic = "tax"
    url = "https://omoney.kbstar.com/quics?page=C042014&cc=b037807:b037807"
    crawling(topic, url)

def investment_research_crawl():
    topic = "investment"
    url = "https://omoney.kbstar.com/quics?page=C042016&cc=b039708:b039708"
    crawling(topic, url)