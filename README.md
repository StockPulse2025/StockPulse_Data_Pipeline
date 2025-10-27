# 📈 StockPulse Data Pipeline

> 주식 뉴스 데이터 수집 및 AI 분석을 위한 자동화 데이터 파이프라인

<p align="center">
  <img src="https://img.shields.io/badge/Apache%20Airflow-2.9.3-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-24.0+-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-13-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS%20S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white" />
</p>

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [시스템 아키텍처](#-시스템-아키텍처)
- [기술 스택](#-기술-스택)
- [DAG 구성](#-dag-구성)
- [설치 및 실행](#-설치-및-실행)
- [환경 변수 설정](#-환경-변수-설정)
- [프로젝트 구조](#-프로젝트-구조)
- [개발 로드맵](#-개발-로드맵)

## 🎯 프로젝트 소개

**StockPulse Data Pipeline**은 국내 주요 80개 종목의 뉴스 데이터를 실시간으로 수집하고, AI 모델을 통해 주가 영향도를 예측하는 자동화된 데이터 파이프라인

- **자동화된 데이터 수집**: Apache Airflow를 통한 스케줄 기반 데이터 수집
- **클라우드 스토리지**: AWS S3를 통한 안정적인 데이터 저장

## ✨ 주요 기능

### 1. 뉴스 데이터 수집 (News Crawling)
- 네이버 금융에서 국내 주요 80개 종목의 뉴스 수집
- 뉴스 제목, 본문, 이미지, 발행일, 언론사 정보 추출
- 페이지네이션을 통한 대량 데이터 수집

### 2. 데이터 전처리 (Data Processing)
- 중복 제거 및 데이터 정제
- 날짜/시간 표준화 (Asia/Seoul 타임존)
- S3 버킷에 CSV 형식으로 저장

### 3. AI 모델 예측 (ML Inference)
- PyTorch 기반 DeBERTa 모델 사용
- 뉴스 본문 분석을 통한 주가 영향도 예측
- 실시간 배치 추론

### 4. API 연동 (Data Integration)
- 분석 결과를 백엔드 API로 자동 전송
- RESTful API 통신
- JSON 포맷 페이로드 전송

## 🏗 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                      Apache Airflow Scheduler                    │
│                     (Docker Container 기반)                      │
└────────────────┬───────────────────────────┬────────────────────┘
                 │                           │
                 ▼                           ▼
    ┌────────────────────────┐  ┌────────────────────────┐
    │   DAG 1: News List     │  │  DAG 2: News Detail    │
    │   뉴스 목록 수집         │  │  뉴스 상세 정보 수집     │
    └───────────┬────────────┘  └───────────┬────────────┘
                │                           │
                └───────────┬───────────────┘
                            ▼
                ┌────────────────────────┐
                │    AWS S3 Storage      │
                │   (데이터 레이크)        │
                └───────────┬────────────┘
                            │
                ┌───────────▼────────────┐
                │  DAG 3: AI Prediction  │
                │  (DeBERTa 모델)        │
                └───────────┬────────────┘
                            │
                ┌───────────▼────────────┐
                │   Backend API Server   │
                │  (결과 데이터 전송)      │
                └────────────────────────┘
```

## 🛠 기술 스택

### Workflow Management
- **Apache Airflow 2.9.3**: 데이터 파이프라인 오케스트레이션
- **LocalExecutor**: 로컬 환경에서의 태스크 실행

### Data Collection
- **BeautifulSoup4 4.12.3**: HTML 파싱 및 데이터 추출
- **Requests 2.31.0**: HTTP 통신
- **lxml 5.1.0**: XML/HTML 파서

### Data Processing
- **Pandas 2.1.4**: 데이터프레임 기반 데이터 처리
- **NumPy 1.26.3**: 수치 연산

### Machine Learning
- **PyTorch 2.1.2**: 딥러닝 프레임워크
- **Transformers 4.36.2**: Hugging Face 트랜스포머 모델
- **scikit-learn 1.4.0**: 머신러닝 유틸리티
- **KoreanFinancialBERT/DeBERTa**: 금융 도메인 특화 모델

### Infrastructure
- **Docker & Docker Compose**: 컨테이너 오케스트레이션
- **PostgreSQL 13**: Airflow 메타데이터 저장
- **Redis**: 메시지 큐 및 캐싱
- **AWS S3**: 클라우드 스토리지

### Additional Tools
- **pytz**: 타임존 처리
- **OpenAI API**: GPT 기반 추가 분석 (선택적)

## 📊 DAG 구성

### 배치 개수: **3개**

### DAG 1: `crawl_news_list`
**목적**: 종목별 뉴스 목록 수집

| 항목 | 내용 |
|------|------|
| **파일명** | `crawl_news_list.py` |
| **실행 주기** | 매일 00:00 (KST) |
| **작업 내용** | - 80개 종목의 뉴스 목록 페이지 크롤링<br>- 뉴스 제목, 링크, 날짜, 언론사 수집<br>- S3에 `news-list/{날짜}.csv` 저장 |
| **데이터 소스** | 네이버 금융 (finance.naver.com) |
| **출력 형식** | CSV (S3 버킷) |

**수집 종목 (80개)**:
삼성전자, SK하이닉스, LG에너지솔루션, 삼성바이오로직스, 현대차, 한화에어로스페이스, HD현대중공업, KB금융, 기아, 두산에너빌리티, 셀트리온, NAVER, 한화오션, 신한지주, 삼성물산, 현대모비스, 카카오, HD한국조선해양, 삼성생명, POSCO홀딩스, 하나금융지주, HMM, 한국전력, LG화학, 현대로템, 삼성화재, 메리츠금융지주, SK스퀘어, 우리금융지주, HD현대일렉트릭, 삼성중공업, KT&G, 삼성SDI, SK이노베이션, 고려아연, 기업은행, 크래프톤, SK, KT, LIG넥스원, LG전자, 카카오뱅크, LG, SK텔레콤, 삼성에스디에스, 미래에셋증권, 두산, 한화시스템, 현대글로비스, 삼성전기, 삼양식품, 포스코퓨처엠, 하이브, HD현대, 유한양행, 한국항공우주, LS ELECTRIC, DB손해보험, HD현대마린솔루션, 대한항공, 포스코인터내셔널, 한미반도체, 아모레퍼시픽, 카카오페이, 한국금융지주, HD현대미포, 한화, 코웨이, 현대건설, SK바이오팜, 한진칼, S-Oil, LG씨엔에스, 에이피알, NH투자증권, LG유플러스, 삼성증권, 삼성카드, 한국타이어앤테크놀로지, LG디스플레이

---

### DAG 2: `crawl_news_detail`
**목적**: 뉴스 본문 및 상세 정보 수집

| 항목 | 내용 |
|------|------|
| **파일명** | `dags/crawl_news_detail.py` |
| **실행 주기** | DAG 1 완료 후 자동 실행 (의존성) |
| **작업 내용** | - S3에서 뉴스 목록 CSV 읽기<br>- 각 뉴스 링크 접속하여 본문 추출<br>- 뉴스 대표 이미지(og:image) 추출<br>- S3에 `news/{날짜}.csv` 저장 |
| **데이터 소스** | 네이버 뉴스 (news.naver.com) |
| **출력 형식** | CSV (S3 버킷) |
| **Rate Limiting** | 0.3초 딜레이 (과도한 요청 방지) |

**주요 함수**:
- `collect_daily_news(interval_start_date)`: 뉴스 목록 수집
- `collect_daily_news_detail(interval_start_date)`: 뉴스 본문 수집
- `get_article_content(url)`: 본문 추출 (리다이렉트 처리 포함)
- `extract_news_image(soup)`: OG 이미지 추출

---

### DAG 3: `predict_and_upload`
**목적**: AI 모델 예측 및 결과 업로드

| 항목 | 내용 |
|------|------|
| **파일명** | `dags/predict_model.py` (히스토리에서 제거됨) |
| **실행 주기** | DAG 2 완료 후 자동 실행 (의존성) |
| **작업 내용** | - S3에서 뉴스 데이터 로드<br>- DeBERTa 모델로 주가 영향도 예측<br>- 예측 결과를 S3에 저장<br>- 백엔드 API로 결과 전송 |
| **모델 파일** | `dags/model_head.pt` (743MB) |
| **Scaler 파일** | `dags/label_scaler.joblib` |
| **API 엔드포인트** | `https://stockpulse.p-e.kr/api/v1/news/pipeline/batch` |

**주요 함수**:
- `upload_daily_news_result(interval_start_date)`: 예측 결과 업로드
- `df_to_news_payload(df)`: 데이터프레임을 API 페이로드로 변환

**페이로드 구조**:
```json
{
  "newsDataList": [
    {
      "newsTitle": "뉴스 제목",
      "newsUrl": "뉴스 링크",
      "newsImage": "이미지 URL",
      "press": "언론사",
      "content": "본문 내용",
      "reason": "분석 근거",
      "publishedDate": "2025-10-27T09:00:00",
      "relatedStocks": [
        {
          "stockName": "삼성전자",
          "symbol": "005930",
          "influenceScore": 0.85
        }
      ]
    }
  ]
}
```

---

## 🚀 설치 및 실행

### Prerequisites
- Docker 24.0 이상
- Docker Compose 2.0 이상
- 최소 4GB RAM
- 최소 2 CPU 코어
- 10GB 이상의 디스크 공간

### 1. 저장소 클론

```bash
git clone https://github.com/StockPulse2025/StockPulse_Data_Pipeline.git
cd StockPulse_Data_Pipeline
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 필요한 환경 변수를 설정합니다:

```bash
# AWS 자격 증명
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# Airflow 설정
AIRFLOW_UID=50000
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow

# OpenAI API (선택사항)
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Docker Compose 실행

```bash
# 백그라운드에서 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 4. Airflow 웹 UI 접속

브라우저에서 `http://localhost:8080` 접속

- **Username**: `airflow` (기본값)
- **Password**: `airflow` (기본값)

### 5. DAG 활성화

Airflow UI에서 각 DAG를 활성화하고 실행합니다.

### 서비스 중지

```bash
docker-compose down
```

### 전체 데이터 삭제 (초기화)

```bash
docker-compose down -v
```

---

## 🔐 환경 변수 설정

### 필수 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `AWS_ACCESS_KEY_ID` | AWS 액세스 키 | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS 시크릿 키 | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `AIRFLOW_UID` | Airflow 사용자 UID | `50000` |

### 선택 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `OPENAI_API_KEY` | OpenAI API 키 (GPT 사용 시) | `sk-proj-...` |
| `_AIRFLOW_WWW_USER_USERNAME` | Airflow 관리자 계정 | `admin` |
| `_AIRFLOW_WWW_USER_PASSWORD` | Airflow 관리자 비밀번호 | `secure_password` |

---

## 📁 프로젝트 구조

```
StockPulse_Data_Pipeline/
├── dags/                           # Airflow DAG 파일들
│   ├── crawl_news_detail.py       # 뉴스 상세 정보 수집 DAG
│   ├── model_head.pt              # PyTorch 모델 파일 (743MB)
│   └── label_scaler.joblib        # 스케일러 파일
├── inference/                      # 추론 관련 모듈
│   └── api_keys.py                # API 키 관리 (환경변수 권장)
├── models/                         # 모델 관련 파일
├── config/                         # Airflow 설정 파일
│   └── airflow.cfg                # Airflow 구성 파일
├── logs/                           # Airflow 로그 (생성됨)
├── plugins/                        # Airflow 플러그인 (선택)
├── docker-compose.yaml            # Docker Compose 설정
├── requirements.txt               # Python 패키지 의존성
├── .env                           # 환경 변수 (git ignore)
├── .gitignore                     # Git 제외 파일 목록
└── README.md                      # 프로젝트 문서 (본 파일)
```

---

## 📈 데이터 플로우

```
1. 뉴스 목록 수집
   └─> S3: stockplus-datalake/news-list/{date}.csv
        ├─ title: 뉴스 제목
        ├─ link: 뉴스 링크
        ├─ info: 언론사
        ├─ date: 발행일
        ├─ stock_code: 종목코드
        ├─ stock_name: 종목명
        └─ sector: 섹터

2. 뉴스 상세 정보 수집
   └─> S3: stockplus-datalake/news/{date}.csv
        ├─ (위 필드 전부 포함)
        ├─ content: 본문 내용
        └─ newsImage: 대표 이미지 URL

3. AI 모델 예측
   └─> S3: stockplus-datalake/news-result/{date}.csv
        ├─ (위 필드 전부 포함)
        ├─ prediction: 주가 영향도 예측값
        └─ description: 예측 근거

4. 백엔드 API 전송
   └─> POST https://stockpulse.p-e.kr/api/v1/news/pipeline/batch
        └─ JSON 페이로드 전송
```

---

## 🔧 개발 가이드

### 로컬 개발 환경 설정

1. **Python 가상 환경 생성**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **패키지 설치**
```bash
pip install -r requirements.txt
```

3. **Airflow 초기화**
```bash
export AIRFLOW_HOME=$(pwd)
airflow db init
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

4. **Airflow 실행 (로컬)**
```bash
airflow webserver --port 8080  # Terminal 1
airflow scheduler               # Terminal 2
```

### DAG 개발 팁

- DAG 파일은 `dags/` 디렉토리에 저장
- `@dag` 데코레이터 또는 `DAG()` 클래스 사용
- `schedule_interval`로 실행 주기 설정
- 의존성은 `>>` 또는 `.set_downstream()` 사용

---

## 🐛 트러블슈팅

### Docker 메모리 부족
```bash
# Docker Desktop에서 최소 4GB RAM 할당 필요
# Settings > Resources > Memory 에서 조정
```

### S3 연결 오류
```bash
# AWS 자격 증명 확인
aws configure list

# S3 버킷 접근 권한 확인
aws s3 ls s3://stockplus-datalake/
```

### Airflow 스케줄러 응답 없음
```bash
# 스케줄러 재시작
docker-compose restart airflow-scheduler

# 로그 확인
docker-compose logs airflow-scheduler
```


---


## 🔗 관련 링크

- [Apache Airflow 공식 문서](https://airflow.apache.org/docs/)
- [BeautifulSoup 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [AWS S3 Python SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3.html)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)

