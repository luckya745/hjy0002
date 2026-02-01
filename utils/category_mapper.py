def classify_category(description):
    # 키워드 기반 카테고리 사전
    category_map = {
        '식비': ['식당', '카페', '편의점', '마트', '배달'],
        '교통': ['택시', '버스', '지하철', '주유', '하이패스'],
        '쇼핑': ['쿠팡', '네이버쇼핑', '백화점', '의류'],
        '생활': ['관리비', '통신비', '보험료', '구독']
    }
    
    for category, keywords in category_map.items():
        if any(keyword in description for keyword in keywords):
            return category
    return '기타'

def apply_categories(df, desc_col):
    df['카테고리'] = df[desc_col].apply(classify_category)
    return df