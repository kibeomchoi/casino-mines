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
# CSS
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
    }


    h2, h3 {
        color: white;
    }


    p {
        color: white;
    }


    div.stButton > button {

        background-color: #222;
        color: white;

        border: 2px solid gold;
        border-radius: 10px;

        height: 55px;

        font-size: 20px;
        font-weight: bold;

    }


    div.stButton > button:hover {

        background-color: #444;
        color: gold;

    }

    </style>
    """,

    unsafe_allow_html=True
)



# =====================================================
# 게임 초기화
# =====================================================


if "game" not in st.session_state:

    st.session_state.game = Game()



if "bet_amount" not in st.session_state:

    st.session_state.bet_amount = 100



game = st.session_state.game

status = game.get_status()



# =====================================================
# 제목
# =====================================================


st.title(TITLE)



# =====================================================
# 게임 설명
# =====================================================


with st.expander(
    "📖 게임 방법 (클릭해서 보기)",
    expanded=True
):

    st.markdown(
        """
        💎 **보석을 찾을수록 배율이 증가합니다.**

        🔥 더 많은 보석을 찾을수록 더 높은 보상을 받을 수 있습니다.

        💰 **보석 5개 이상 발견 시 Cash Out 가능**

        💣 **폭탄 발견 시 즉시 게임 종료**

        🎯 목표:
        최대한 높은 배율에서 안전하게 Cash Out 하세요!
        """
    )



# =====================================================
# 현재 정보
# =====================================================


col1, col2, col3 = st.columns(3)



with col1:

    st.metric(
        "💰 이번 베팅",
        f"{st.session_state.bet_amount}칩"
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
# Cash Out 가능 알림
# =====================================================


if status["gems_found"] >= MIN_CASHOUT and not game.game_over:

    st.success(
        "🎉 Cash Out 가능! "
        "계속 도전하면 더 높은 배율을 얻을 수 있습니다."
    )



# =====================================================
# 베팅 설정
# =====================================================


if (
    not game.game_over
    and status["gems_found"] == 0
):


    bet = st.number_input(

        "🎲 이번 게임 베팅",

        min_value=100,

        step=100,

        value=st.session_state.bet_amount

    )


    st.session_state.bet_amount = int(bet)



else:


    st.info(
        f"현재 베팅: {st.session_state.bet_amount}칩"
    )



# =====================================================
# 게임판
# =====================================================


st.divider()

st.subheader("💎 Mines")



board = game.get_board_state()



for row in range(ROWS):

    cols = st.columns(COLS)


    for col in range(COLS):

        cell = board[row][col]


        symbol = "⬜"


        if cell["open"]:

            if cell["bomb"]:

                symbol = "💣"

            elif cell["gem"]:

                symbol = "💎"



        if not cell["open"]:


            if cols[col].button(

                "⬜",

                key=f"{row}_{col}"

            ):


                result = game.click_cell(
                    row,
                    col
                )


                if result["result"] == "bomb":

                    game.reveal_all()


                st.rerun()



        else:


            cols[col].button(

                symbol,

                disabled=True,

                key=f"open_{row}_{col}"

            )



# =====================================================
# 다음 배율
# =====================================================


next_gem = status["gems_found"] + 1



if next_gem in PAYOUTS:

    st.info(

        f"💎 {next_gem}개 성공 시 → "
        f"{PAYOUTS[next_gem]}x"

    )



# =====================================================
# Cash Out
# =====================================================


current_reward = int(

    st.session_state.bet_amount
    *
    status["multiplier"]

)


st.write(
    f"💰 현재 Cash Out 금액: **{current_reward}칩**"
)



if st.button(
    "💰 Cash Out"
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
# 결과
# =====================================================


if game.game_over:


    if game.cashed_out:

        st.success(
            "🎉 안전하게 Cash Out 완료!"
        )


    else:

        st.error(
            "💣 폭탄 발견! 게임 종료!"
        )



# =====================================================
# 새 게임
# =====================================================


st.divider()


if st.button(
    "🔄 다음 게임 시작"
):


    st.session_state.game = Game()

    st.rerun()
