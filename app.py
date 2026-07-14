"""
=====================================================
Casino Mines - Streamlit App

사용자 화면(UI)을 담당하는 파일

game.py:
    게임 로직

app.py:
    화면 / 버튼 / 입력 담당

=====================================================
"""


import streamlit as st

from game import Game

from config import (
    TITLE,
    ROWS,
    COLS,
    PAYOUTS,
    MIN_CASHOUT,
)



# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="Casino Mines",
    page_icon="🎰",
    layout="centered"
)



# =====================================================
# 카지노 스타일
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b0b0b;
    }


    h1 {
        color: gold;
        text-align: center;
        font-size: 45px;
    }


    h2, h3 {
        color: white;
    }


    p {
        color: white;
    }


    div.stButton > button {

        width: 100%;
        height: 55px;

        font-size: 25px;
        font-weight: bold;

        border-radius: 12px;

    }


    </style>

    """,
    unsafe_allow_html=True
)



# =====================================================
# Session State 초기화
# =====================================================


# 게임 객체 저장

if "game" not in st.session_state:

    st.session_state.game = Game()



# 이번 판 베팅 금액

if "bet_amount" not in st.session_state:

    st.session_state.bet_amount = 100




# =====================================================
# 제목
# =====================================================

st.title(TITLE)



# =====================================================
# 게임 상태
# =====================================================


game = st.session_state.game

status = game.get_status()



# =====================================================
# 상단 정보 표시
# =====================================================


col1, col2, col3 = st.columns(3)



with col1:

    st.metric(
        "💰 이번 베팅",
        f"{st.session_state.bet_amount} 칩"
    )


with col2:

    st.metric(
        "💎 보석",
        f"{status['gems_found']}개"
    )


with col3:

    st.metric(
        "🔥 배율",
        f"{status['multiplier']}x"
    )
# =====================================================
# 베팅 금액 설정
# =====================================================


st.divider()

st.subheader("🎲 베팅 설정")


bet = st.number_input(
    "이번 게임에 걸 칩",
    min_value=100,
    step=100,
    value=st.session_state.bet_amount
)


# 입력값 저장

st.session_state.bet_amount = int(bet)



# =====================================================
# 게임판
# =====================================================


st.divider()

st.subheader("💎 Mines Board")


board = game.get_board_state()



for row in range(ROWS):

    columns = st.columns(COLS)


    for col in range(COLS):

        cell = board[row][col]


        # 기본 표시

        symbol = "⬜"



        # 열린 칸 표시

        if cell["open"]:


            if cell["bomb"]:

                symbol = "💣"


            elif cell["gem"]:

                symbol = "💎"



        # 아직 안 연 칸

        if not cell["open"]:


            clicked = columns[col].button(
                "⬜",
                key=f"cell_{row}_{col}"
            )


            if clicked:


                result = game.click_cell(
                    row,
                    col
                )



                # 폭탄이면 공개

                if result["result"] == "bomb":

                    game.reveal_all()



                st.rerun()



        # 열린 칸

        else:


            columns[col].button(
                symbol,
                key=f"open_{row}_{col}",
                disabled=True
            )



# =====================================================
# 게임 결과 표시
# =====================================================


if game.game_over:


    if game.cashed_out:

        st.success(
            "🎉 Cash Out 완료!"
        )


    else:

        st.error(
            "💥 폭탄을 밟았습니다!"
        )
# =====================================================
# 다음 배율 안내
# =====================================================

st.divider()

st.subheader("📈 다음 보석 배율")


next_gem = status["gems_found"] + 1


from config import PAYOUTS


if next_gem in PAYOUTS:

    st.info(
        f"💎 {next_gem}개 성공 시 → "
        f"{PAYOUTS[next_gem]}x"
    )

else:

    st.info(
        "더 높은 보석 개수에 도전하세요!"
    )



# =====================================================
# 예상 획득 금액
# =====================================================

estimated_reward = int(
    st.session_state.bet_amount
    *
    status["multiplier"]
)


st.subheader("💰 현재 획득 가능")


st.write(
    f"Cash Out 시 "
    f"**{estimated_reward} 칩** 획득"
)



# =====================================================
# Cash Out 버튼
# =====================================================


if st.button(
    "💰 Cash Out",
    key="cashout"
):


    if game.can_cash_out():


        result = game.cash_out(
            st.session_state.bet_amount
        )


        st.success(
            result["message"]
        )


        st.rerun()


    else:

        st.warning(
            f"💎 보석 {MIN_CASHOUT}개 이상 필요합니다."
        )



# =====================================================
# 게임 종료 처리
# =====================================================


if game.game_over:


    if game.cashed_out:


        st.success(
            "🎉 안전하게 Cash Out 성공!"
        )


    else:

        st.error(
            "💥 폭탄 발견! 실패!"
        )



# =====================================================
# 새 게임 버튼
# =====================================================


st.divider()


if st.button(
    "🔄 다음 게임 시작",
    key="reset_game"
):


    st.session_state.game = Game()

    st.rerun()
