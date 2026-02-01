import pandas as pd
import io

def load_csv(uploaded_file):
    try:
        # 한글 인코딩 대응 (EUC-KR 또는 UTF-8)
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except:
            df = pd.read_csv(uploaded_file, encoding='cp949')
            
        # 날짜 컬럼 자동 탐색 및 변환
        date_col = next((col for col in df.columns if '날짜' in col or 'Date' in col), df.columns[0])
        df[date_col] = pd.to_datetime(df[date_col])
        return df, date_col
    except Exception as e:
        return None, str(e)

def generate_sample_csv():
    """사용자가 다운로드할 수 있는 샘플 CSV 데이터 생성"""
    data = {
        '날짜': ['2026-01-01', '2026-01-02', '2026-01-05', '2026-01-10', '2026-01-15'],
        '내역': ['스타벅스 커피', '택시비', '쿠팡 장보기', '식당 점심', '넷플릭스 구독'],
        '금액': [5500, 12000, 45000, 9000, 17000]
    }
    df_sample = pd.DataFrame(data)
    # CSV를 스트링 버퍼에 저장
    csv_buffer = io.StringIO()
    df_sample.to_csv(csv_buffer, index=False, encoding='utf-8-sig') # Excel 한글 깨짐 방지용 sig
    return csv_buffer.getvalue()