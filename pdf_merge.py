import os
from PyPDF2 import PdfMerger

def pdf_merger():
    # 폴더 경로 설정
    folder_path = './researches'
    output_filename = 'total_research.pdf'

    # 합칠 PDF 파일 목록
    pdf_files = ['real_estate.pdf', 'tax.pdf', 'investment.pdf']

    # PdfMerger 객체 생성
    pdf_merger = PdfMerger()

    # PDF 파일 합치기
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        pdf_merger.append(pdf_path)

    # 결과 PDF 저장
    output_path = os.path.join(folder_path, output_filename)
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)
