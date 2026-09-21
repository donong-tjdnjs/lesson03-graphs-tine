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


# 3. 데이터 선택 및 필터 구역 (사이드바)
st.sidebar.header("🔍 데이터 필터")

# 전체 영화 목록 추출 (오름차순 정렬)
movie_list = sorted(data["영화명"].unique())

# 영화 선택 드롭다운 (Section 1용)
selected_movie = st.sidebar.selectbox("영화를 선택하세요:", movie_list)

# 선택한 영화의 데이터만 필터링
filtered_data = data[data["영화명"] == selected_movie].sort_values("날짜")


# 4. 그래프 구역 1: 개별 영화 일별 관객수 변화
st.header("📌 Section 1. 개별 영화 일별 관객수 변화")

if not filtered_data.empty:
    fig1 = px.line(
        filtered_data,
        x="날짜",
        y="일관객",
        title=f"[{selected_movie}] 날짜별 일관객수 추이",
        labels={"날짜": "날짜", "일관객": "일일 관객수 (명)"},
        markers=True,
    )

    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,.0f}명<extra></extra>"
    )

    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="일일 관객수 (명)",
        hovermode="x unified",
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 일별 관객수 흐름을 통해 개봉 초기 흥행 추세 및 관객수 감소 속도를 분석할 수 있습니다."
    )
else:
    st.warning("선택한 영화의 데이터가 존재하지 않습니다.")

st.markdown("---")


# 5. 그래프 구역 2: 누적 일관객 TOP 5 영화 비교
st.header("📌 Section 2. 누적 일관객 TOP 5 영화의 관객수 추이 비교")

# 해당 기간 일관객 합계 상위 5개 영화 추출
top5_movies = (
    data.groupby("영화명")["일관객"]
    .sum()
    .nlargest(5)
    .index.tolist()
)

# TOP 5 영화 데이터 필터링
top5_data = data[data["영화명"].isin(top5_movies)].sort_values("날짜")

# Plotly 선 그래프 생성 (color='영화명'으로 영화별 색상 구분)
fig2 = px.line(
    top5_data,
    x="날짜",
    y="일관객",
    color="영화명",
    title="기간 내 일관객 합계 TOP 5 영화 날짜별 비교",
    labels={"날짜": "날짜", "일관객": "일일 관객수 (명)", "영화명": "영화 제목"},
    markers=True,
)

# 호버 툴팁 포맷 설정
fig2.update_traces(
    hovertemplate="<b>영화명:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,.0f}명<extra></extra>"
)

# 레이아웃 설정 (범례 클릭 시 켜고 끌 수 있는 기능 기본 제공)
fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객수 (명)",
    legend_title="영화 목록 (클릭하여 토글)",
    hovermode="x unified",
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 해석 문구 자리
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 기간 내 흥행 Top 5 영화들의 개봉 시기별 관객 집중도와 경쟁 구도를 한눈에 비교할 수 있습니다."
)

st.markdown("---")


# 6. 추후 그래프 추가를 위한 구역 예시
st.header("📌 Section 3. (추가 예정 구역)")
st.caption("새로운 그래프가 추가될 위치입니다.")
st.info("💡 **이 그래프로 알 수 있는 것:** (추가 예정 설명 문구)")

st.markdown("---")
