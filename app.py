import streamlit as st
import pandas as pd
from utils.file_loader import load_csv, generate_sample_csv
from utils.category_mapper import apply_categories

st.set_page_config(page_title="지출 분석 대시보드", layout="wide")

st.title("💸 개인 지출 분석 및 미리보기")

# --- 사이드바: 파일 관리 ---
with st.sidebar:
    st.header("1. 데이터 준비")
    
    # 샘플 파일 다운로드 버튼
    sample_csv = generate_sample_csv()
    st.download_button(
        label="📥 샘플 CSV 양식 다운로드",
        data=sample_csv,
        file_name="expense_sample.csv",
        mime="text/csv"
    )
    
    st.divider()
    
    st.header("2. 파일 업로드")
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

# --- 메인 화면: 데이터 처리 및 미리보기 ---
if uploaded_file:
    df, date_col = load_csv(uploaded_file)
    
    if isinstance(df, pd.DataFrame):
        # 카테고리 분류 적용
        desc_col = next((col for col in df.columns if '내역' in col or '적요' in col or 'Description' in col), df.columns[1])
        df = apply_categories(df, desc_col)
        
        # 탭을 사용하여 화면 구성 분리
        tab1, tab2 = st.tabs(["🔍 데이터 미리보기", "📊 분석 결과"])
        
        with tab1:
            st.subheader("데이터 확인")
            st.info(f"✅ 날짜 컬럼 **'{date_col}'**을(를) datetime 형식으로 변환 완료했습니다.")
            
            # 요약 정보 표시
            col1, col2, col3 = st.columns(3)
            col1.metric("총 데이터 건수", f"{len(df)}건")
            
            amt_col = next((col for col in df.columns if '금액' in col or 'Amount' in col), None)
            if amt_col:
                col2.metric("총 지출액", f"{df[amt_col].sum():,}원")
                col3.metric("평균 지출액", f"{int(df[amt_col].mean()):,}원")

            st.markdown("---")
            st.write("**불러온 데이터 리스트 (최신순)**")
            # 미리보기 (최신순 정렬)
            st.dataframe(df.sort_values(by=date_col, ascending=False), use_container_width=True)
            
        with tab2:
            st.write("이곳에 차트와 월별 분석 내용을 추가할 수 있습니다.")
            # (이전 단계의 차트 코드 삽입 가능)

    else:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {date_col}")
else:
    st.warning("먼저 왼쪽 사이드바에서 샘플 양식을 확인하거나 CSV 파일을 업로드해주세요.")