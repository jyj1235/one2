
# AI 주식 타이밍 알리미

## 기능
- 실시간 한국주식 데이터
- 삼성전자 / SK하이닉스 분석 가능
- 이동평균 분석
- RSI 과열/과매도 분석
- 거래량 증가 감지
- 매수/매도 위험 점수 표시

## 실행 방법

### 1. Python 설치

https://www.python.org/downloads/

### 2. 라이브러리 설치

pip install streamlit pandas numpy yfinance

### 3. 실행

streamlit run app.py

## 종목 코드 예시
- 삼성전자: 005930.KS
- SK하이닉스: 000660.KS
- NAVER: 035420.KS

## 추가 개발 가능 기능
- 텔레그램 알림
- 카카오톡 알림
- AI 예측 모델
- 자동매매 연동
- 뉴스 분석
