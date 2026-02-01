import pandas as pd
import io

def load_csv(uploaded_file):
    """CSV 파일을 안전하게 읽고 날짜 형식을 변환합니다."""
    try:
        # 파일 포인터를 처음으로 되돌림 (중복 읽기 오류 방지)
        uploaded_file.seek(0)
        
        # 1. 인코딩 시도 (utf-8-sig는 엑셀 생성 파일 대응에 좋습니다)
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        except:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='cp949')
            
        # 2. 데이터 유무 확인
        if df.empty or len(df.columns) < 2:
            return None, "파일에 유효한 데이터가 없거나 형식이 잘못되었습니다."

        # 3. 날짜 컬럼 탐색 및 변환
        # '날짜'나 'Date'를 포함하는 컬럼을 찾고, 없으면 첫 번째 컬럼 사용
        date_col = next((col for col in df.columns if '날짜' in col or 'Date' in col), df.columns[0])
        
        # 날짜 변환 (에러 발생 시 NaT로 처리 후 행 삭제)
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col])
        
        return df, date_col
        
    except Exception as e:
        return None, f"파일 처리 중 오류 발생: {str(e)}"

def generate_sample_csv():
    """사용자가 다운로드할 수 있는 샘플 CSV 데이터 생성"""
    data = {
        '날짜': ['2026-01-01', '2026-01-02', '2026-01-05', '2026-01-10', '2026-01-15'],
        '내역': ['스타벅스 커피', '택시비', '쿠팡 장보기', '식당 점심', '넷플릭스 구독'],
        '금액': [5500, 12000, 45000, 9000, 17000]
    }
    df_sample = pd.DataFrame(data)
    
    # 엑셀 한글 깨짐 방지를 위해 utf-8-sig 사용
    csv_buffer = io.StringIO()
    df_sample.to_csv(csv_buffer, index=False, encoding='utf-8-sig') 
    
    return csv_buffer.getvalue()
