import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정 및 제목
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("---")


# 2. 데이터 불러오기 및 전처리 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    # 날짜 열을 문자열(str) 형식으로 읽어옴
    df = pd.read_csv(url, dtype={"날짜": str})

    # 날짜 열을 YYYYMMDD 형식을 고려하여 datetime 객체로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")

    return df


# 데이터 로드
data = load_data()


# 3. 데이터 선택 및 필터 구역 (사이드바 또는 상단)
st.sidebar.header("🔍 데이터 필터")

# 전체 영화 목록 추출 (오름차순 정렬)
movie_list = sorted(data["영화명"].unique())

# 영화 선택 드롭다운
selected_movie = st.sidebar.selectbox("영화를 선택하세요:", movie_list)

# 선택한 영화의 데이터만 필터링
filtered_data = data[data["영화명"] == selected_movie].sort_values("날짜")


# 4. 그래프 구역 1: 시간 축 분석
st.header("📌 Section 1. 일별 관객수 변화 (시간 분석)")

if not filtered_data.empty:
    # Plotly 선 그래프 생성
    fig = px.line(
        filtered_data,
        x="날짜",
        y="일관객",
        title=f"[{selected_movie}] 날짜별 일관객수 추이",
        labels={"날짜": "날짜", "일관객": "일일 관객수 (명)"},
        markers=True,  # 각 데이터 포인트에 점 표시
    )

    # 마우스 오버(호버) 시 날짜 및 관객수 포맷 설정
    fig.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,.0f}명<extra></extra>"
    )

    # 그래프 축 및 레이아웃 다듬기
    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="일일 관객수 (명)",
        hovermode="x unified",
    )

    # Streamlit에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 그래프 해석 문구 자리 (자연스러운 디자인을 위해 info 상자 활용)
    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 일별 관객수 흐름을 통해 개봉 초기 흥행 및 관객수 감소 추세를 파악할 수 있습니다."
    )
else:
    st.warning("선택한 영화의 데이터가 존재하지 않습니다.")

st.markdown("---")


# 5. 추후 그래프 추가를 위한 구역 예시 (Section 2, 3...)
st.header("📌 Section 2. (추가 예정 구역)")
st.caption("새로운 그래프가 추가될 위치입니다.")
st.info("💡 **이 그래프로 알 수 있는 것:** (추가 예정 설명 문구)")

st.markdown("---")
