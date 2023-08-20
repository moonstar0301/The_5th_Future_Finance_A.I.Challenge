# KB 국민은행 The 5th Future Finance A.I.Challenge - 챗봇

이 프로젝트는 KB 국민은행 The 5th Future Finance A.I.Challenge 공모전에 출품된 작품으로, AI 전문위원에게 물어보고 관련 답을 얻을 수 있는 챗봇 서비스입니다.

## 주제

「현직자 Pick」AI 전문위원에게 물어보고 관련 답을 얻을 수 있는 금융 콘텐츠 솔루션

## 시작하기 전에

프로젝트를 실행하기 전에 아래 단계를 따라주세요:

1. 필요한 패키지를 설치하기 위해 터미널에서 다음 명령어를 실행하세요: `pip install -r requirements.txt`
2. KB 자산관리 전문가 칼럼([링크](https://omoney.kbstar.com/quics?page=C042014))에서 최신 칼럼을 크롤링하기 위해 아래 명령어를 실행하세요: `python main.py`

## 시작하기

프로젝트를 실행하려면 다음 단계를 따라주세요:

1. Flask 애플리케이션을 실행하기 위해 터미널에서 `flask run` 명령을 실행하세요.
2. 웹 브라우저에서 다음 URL로 이동하여 프로젝트를 사용하세요: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## 기능

이 프로젝트는 다음과 같은 주요 기능을 제공합니다:

1. KB 전문가 칼럼을 크롤링한 데이터를 Large Language Model (LLM)에 학습시켜 세법, 부동산, 재테크 등과 관련된 궁금증에 전문적인 지식으로 답변할 수 있습니다.
2. 질문을 처음 묻는 사용자를 위해 추천 질문 목록을 제공하여 도움을 줍니다.
3. 마인드맵을 제공하여 답변의 근거를 시각적으로 확인할 수 있습니다.

![마인드맵 예시](마인드맵_이미지_링크)

## 사용 화면

![사용 화면 예시 1](https://github.com/moonstar0301/The_5th_Future_Finance_A.I.Challenge/assets/129285999/a4f2853a-99a1-44aa-a9a0-1748dbf25051)
![사용 화면 예시 2](https://github.com/moonstar0301/The_5th_Future_Finance_A.I.Challenge/assets/129285999/10a4a169-99cb-4a2f-8dcf-dd6a2e632192)
![사용 화면 예시 3](https://github.com/moonstar0301/The_5th_Future_Finance_A.I.Challenge/assets/129285999/fd487b70-0d95-4ad5-b146-d57431e1ddf7)
![사용 화면 예시 4](https://github.com/moonstar0301/The_5th_Future_Finance_A.I.Challenge/assets/129285999/35835487-6392-43dd-b40b-4c9db6c87025)

> Team. DART


### :rainbow: Contributors
| [moonstar0301](https://github.com/moonstar0301) | [dong-yxxn](https://github.com/dong-yxxn) | [hyeyeong02](https://github.com/hyeyeong02) |
