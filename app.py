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

        background-color:#0b0b0b;

    }




    div.stButton > button {

        background-color:#222;

        color:white;

        border:2px solid gold;

        border-radius:12px;

        height:65px;

        font-size:24px;

        font-weight:bold;

    }



    div.stButton > button:hover {

        background-color:#444;

        color:gold;

    }



    /* dialog 내부 */



    div[data-testid="stDialog"] p {

        color:white !important;

        font-size:22px;

    }



    </style>
    """,

    unsafe_allow_html=True
)



# =====================================================
# Session State
# =====================================================


if "game" not in st.session_state:

    st.session_state.game = Game()



if "bet_amount" not in st.session_state:

    st.session_state.bet_amount = 100



if "show_game_over" not in st.session_state:

    st.session_state.show_game_over = False



if "show_cashout" not in st.session_state:

    st.session_state.show_cashout = False



if "cashout_reward" not in st.session_state:

    st.session_state.cashout_reward = 0



game = st.session_state.game

status = game.get_status()



# =====================================================
# 팝업 함수
# =====================================================
@st.dialog("💥 GAME OVER")
def game_over_popup():

    st.markdown(
        """
        <style>

        [data-testid="stDialog"] {
            background-color: #111111;
        }

        [data-testid="stDialog"] p {
            color: white !important;
            font-size: 25px !important;
            font-weight: bold !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    st.error(
        "💥 폭탄을 발견했습니다!"
    )


    st.write(
        "이번 게임은 종료되었습니다."
    )


    if st.button(
        "🔄 다시 플레이하기",
        use_container_width=True
    ):

        st.session_state.game = Game()

        st.session_state.show_game_over = False

        st.rerun()
@st.dialog("🎉 SUCCESS")
def cashout_popup(reward):

    st.markdown(
        """
        <style>

        [data-testid="stDialog"] p {
            color: white !important;
            font-size: 25px !important;
            font-weight: bold !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    st.success(
        "🎉 Cash Out 성공!"
    )


    st.write(
        f"💰 획득 칩 : {reward}칩"
    )


    if st.button(
        "🔄 다시 플레이하기",
        use_container_width=True
    ):

        st.session_state.game = Game()

        st.session_state.show_cashout = False

        st.rerun()
# =====================================================
# 제목
# =====================================================


st.title(TITLE)



# =====================================================
# 룰 설명
# =====================================================


with st.expander(
    "📖 게임 방법",
    expanded=False
):

    st.markdown(
        """
        💎 보석을 찾으면 배율이 증가합니다.

        💰 보석 5개 이상 발견 시 Cash Out 가능!

        💣 폭탄을 발견하면 즉시 게임 종료.

        🎯 높은 배율에서 안전하게 Cash Out 하세요.
        """
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
        f"현재 베팅 : {st.session_state.bet_amount}칩"
    )



# =====================================================
# 현재 진행 상황
# =====================================================


st.divider()


st.write(

    f"현재 진행 : 💎 {status['gems_found']}개 발견 | "
    f"🔥 {status['multiplier']}x"

)



# =====================================================
# Cash Out 가능 표시
# =====================================================


if (

    status["gems_found"] >= MIN_CASHOUT

    and not game.game_over

):


    st.success(

        "🎉 Cash Out 가능!"

    )



# =====================================================
# 게임판
# =====================================================


st.subheader(
    "💎 Mines"
)



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



        # 닫힌 칸

        if not cell["open"]:


            if cols[col].button(

                "⬜",

                key=f"cell_{row}_{col}",

                use_container_width=True

            ):


                result = game.click_cell(

                    row,

                    col

                )



                if result["result"] == "bomb":


                    game.reveal_all()


                    st.session_state.show_game_over = True



                st.rerun()



        # 열린 칸

        else:


            cols[col].button(

                symbol,

                key=f"open_{row}_{col}",

                disabled=True,

                use_container_width=True

            )



# =====================================================
# 다음 배율 표시
# =====================================================


next_gem = status["gems_found"] + 1



if next_gem in PAYOUTS:


    st.info(

        f"💎 {next_gem}개 성공 시 → "
        f"{PAYOUTS[next_gem]}x"

    )
# =====================================================
# Cash Out 금액 표시
# =====================================================


current_reward = int(

    st.session_state.bet_amount
    *
    status["multiplier"]

)



st.divider()



st.write(

    f"💰 현재 Cash Out 금액 : "
    f"**{current_reward}칩**"

)



# =====================================================
# Cash Out 버튼
# =====================================================


if st.button(

    "💰 Cash Out",

    use_container_width=True

):


    if game.can_cash_out():


        game.cash_out(

            st.session_state.bet_amount

        )


        st.session_state.cashout_reward = current_reward

        st.session_state.show_cashout = True


        st.rerun()



    else:


        st.warning(

            f"💎 보석 {MIN_CASHOUT}개 이상 필요합니다."

        )



# =====================================================
# 팝업 실행
# =====================================================


if st.session_state.show_game_over:

    game_over_popup()



if st.session_state.show_cashout:

    cashout_popup(

        st.session_state.cashout_reward

    )
