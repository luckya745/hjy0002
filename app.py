import streamlit as st
import pandas as pd
import os
# 이미지 인식을 돕기 위한 라이브러리 (필요시)
from utils.file_loader import load_csv, generate_sample_csv
from utils.category_mapper import apply_categories

# 페이지 설정
st.set_page_config(page_title="지출 분석 대시보드", layout="wide", page_icon="💸")

st.title("💸 개인 지출 분석 및 미리보기")

# --- 사이드바: 파일 관리 ---
with st.sidebar:
    st.header("1. 데이터 준비")
    
    # 샘플 파일 다운로드 버튼
    try:
        sample_csv = generate_sample_csv()
        st.download_button(
            label="📥 샘플 CSV 양식 다운로드",
            data=sample_csv,
            file_name="expense_sample.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"샘플 생성 중 오류: {e}")
    
    st.divider()
    
    st.header("2. 파일 업로드")
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

# --- 메인 화면: 데이터 처리 및 미리보기 ---
if uploaded_file:
    # utils/file_loader.py의 load_csv 함수 호출
    df, date_info = load_csv(uploaded_file)
    
    if df is not None:
        # 1. 컬럼 자동 탐색 (오류 방지를 위한 안전장치 추가)
        all_cols = df.columns.tolist()
        
        # 내역/적요 컬럼 탐색
        desc_col = next((col for col in all_cols if any(k in col for k in ['내역', '적요', 'Description', '항목'])), None)
        # 금액 컬럼 탐색
        amt_col = next((col for col in all_cols if any(k in col for k in ['금액', 'Amount', '가격'])), None)
        # 날짜 컬럼 탐색
        date_col = next((col for col in all_cols if any(k in col for k in ['날짜', 'Date'])), all_cols[0])

        if desc_col:
            df = apply_categories(df, desc_col)
        
        # 탭 구성
        tab1, tab2 = st.tabs(["🔍 데이터 미리보기", "📊 분석 결과"])
        
        with tab1:
            st.subheader("데이터 확인")
            st.success(f"✅ 날짜 컬럼 **'{date_col}'** 인식 및 변환 완료")
            
            # 요약 정보 표시
            col1, col2, col3 = st.columns(3)
            col1.metric("총 데이터 건수", f"{len(df)}건")
            
            if amt_col:
                # 금액 데이터 숫자형 변환 (쉼표 등 제거)
                if df[amt_col].dtype == 'object':
                    df[amt_col] = df[amt_col].replace({',': ''}, regex=True).astype(float)
                
                total_amt = df[amt_col].sum()
                avg_amt = df[amt_col].mean()
                col2.metric("총 지출액", f"{int(total_amt):,}원")
                col3.metric("평균 지출액", f"{int(avg_amt):,}원")

            st.markdown("---")
            st.write("**불러온 데이터 리스트 (최신순)**")
            # 데이터프레임 출력
            st.dataframe(df.sort_values(by=date_col, ascending=False), use_container_width=True)
            
        with tab2:
            if amt_col:
                import plotly.express as px
                st.subheader("카테고리별 지출 비율")
                fig = px.pie(df, values=amt_col, names='카테고리', hole=0.3)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("금액 컬럼을 찾을 수 없어 차트를 표시할 수 없습니다.")

    else:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {date_info}")
else:
    st.info("💡 시작하려면 왼쪽 사이드바에서 샘플 양식을 다운로드하거나 CSV 파일을 업로드하세요.")
