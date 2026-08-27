"""
=====================================================
Casino Mines - Streamlit App
=====================================================

화면 구성:

1. 사용자 시작
2. 게임 베팅
3. 게임 진행
4. Cash Out 결과
5. Game Over 결과
6. 계속하기 / 게임 종료
7. 최종 잔액
8. 다음 사용자

팝업을 사용하지 않고 화면 자체를 전환합니다.
=====================================================
"""

import streamlit as st

from config import (
    ROWS,
    COLS,
    MIN_CASHOUT,
    PAYOUTS,
    TITLE,
)

from game import Game


# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="Casino Mines",
    page_icon="🎰",
    layout="centered",
)


# =====================================================
# 화면 스타일
# =====================================================

st.markdown(
    """
    <style>

    /* ================================================
       전체 화면
       ================================================ */

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .stApp {

        background-color: #000000 !important;
        color: #ffffff !important;

    }


    /* ================================================
       기본 Streamlit 텍스트
       ================================================ */

    [data-testid="stMain"] p,
    [data-testid="stMain"] span,
    [data-testid="stMain"] label,
    [data-testid="stMain"] strong,
    [data-testid="stMain"] b {

        color: #ffffff !important;
        opacity: 1 !important;

    }


    /* ================================================
       제목
       ================================================ */

    .casino-title {

        background-color: #ffffff;

        color: #000000;

        font-size: 42px;

        font-weight: 900;

        text-align: center;

        padding: 16px;

        border-radius: 12px;

        margin-bottom: 25px;

    }


    /* ================================================
       일반 안내 문구
       ================================================ */

    .white-text {

        color: #ffffff !important;

        font-size: 20px;

        font-weight: 700;

        text-align: center;

        margin: 10px 0;

    }


    /* ================================================
       잔액
       ================================================ */

    .balance-box {

        background-color: #ffffff;

        color: #000000;

        font-size: 28px;

        font-weight: 900;

        text-align: center;

        padding: 14px;

        border-radius: 10px;

        margin: 15px 0 25px 0;

    }


    /* ================================================
       결과 화면
       ================================================ */

    .result-box {

        background-color: #ffffff;

        color: #000000;

        text-align: center;

        padding: 30px 20px;

        border-radius: 15px;

        margin: 20px 0;

        border: 4px solid #ffffff;

    }


    .result-title {

        color: #000000;

        font-size: 38px;

        font-weight: 900;

        margin-bottom: 15px;

    }


    .result-text {

        color: #000000;

        font-size: 22px;

        font-weight: 700;

        margin: 10px 0;

    }


    .result-money {

        color: #000000;

        font-size: 30px;

        font-weight: 900;

        margin: 15px 0;

    }


    /* ================================================
       게임판
       ================================================ */

    .cell-label {

        color: #ffffff !important;

        font-size: 28px;

        font-weight: 900;

        text-align: center;

    }


    /* ================================================
       게임 정보
       ================================================ */

    .game-info {

        background-color: #151515;

        border: 2px solid #ffffff;

        border-radius: 10px;

        padding: 15px;

        margin: 15px 0;

        text-align: center;

    }


    .game-info-title {

        color: #ffffff;

        font-size: 18px;

        font-weight: 700;

    }


    .game-info-value {

        color: #ffffff;

        font-size: 28px;

        font-weight: 900;

        margin-top: 5px;

    }


    /* ================================================
       입력창
       ================================================ */

    [data-testid="stNumberInput"] input {

        background-color: #ffffff !important;

        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        font-size: 22px !important;

        font-weight: 900 !important;

        border: 3px solid #ffffff !important;

        opacity: 1 !important;

    }


    [data-testid="stNumberInput"] label,
    [data-testid="stNumberInput"] label * {

        color: #ffffff !important;

        -webkit-text-fill-color: #ffffff !important;

        font-weight: 800 !important;

        opacity: 1 !important;

    }


    /* ================================================
       버튼
       ================================================ */

    [data-testid="stButton"] button {

        background-color: #ffffff !important;

        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        border: 3px solid #ffffff !important;

        border-radius: 10px !important;

        min-height: 58px !important;

        font-size: 20px !important;

        font-weight: 900 !important;

        opacity: 1 !important;

    }


    [data-testid="stButton"] button p,
    [data-testid="stButton"] button span,
    [data-testid="stButton"] button div {

        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        font-weight: 900 !important;

        opacity: 1 !important;

    }


    /* ================================================
       게임판 버튼
       ================================================ */

    .board-button {

        font-size: 30px;

        font-weight: 900;

    }


    /* ================================================
       구분선
       ================================================ */

    hr {

        border-color: #ffffff !important;

        opacity: 0.5 !important;

    }


    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# Session State 초기화
# =====================================================

if "screen" not in st.session_state:
    st.session_state.screen = "start"

if "balance" not in st.session_state:
    st.session_state.balance = 0

if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 0

if "game" not in st.session_state:
    st.session_state.game = None

if "last_reward" not in st.session_state:
    st.session_state.last_reward = 0

if "last_change" not in st.session_state:
    st.session_state.last_change = 0


# =====================================================
# 공통 함수
# =====================================================

def show_title():
    """
    게임 제목 표시
    """

    st.markdown(
        """
        <div class="casino-title">
            🎰 Casino Mines
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_balance():
    """
    현재 잔액 표시
    """

    st.markdown(
        f"""
        <div class="balance-box">
            💰 현재 잔액 : {st.session_state.balance:,}칩
        </div>
        """,
        unsafe_allow_html=True,
    )


def reset_for_new_user():
    """
    다음 사용자를 위한 전체 초기화
    """

    st.session_state.screen = "start"

    st.session_state.balance = 0

    st.session_state.bet_amount = 0

    st.session_state.game = None

    st.session_state.last_reward = 0

    st.session_state.last_change = 0


def start_game(bet_amount):
    """
    베팅 금액을 잔액에서 차감하고
    새로운 게임 시작
    """

    st.session_state.balance -= bet_amount

    st.session_state.bet_amount = bet_amount

    st.session_state.game = Game()

    st.session_state.last_reward = 0

    st.session_state.last_change = 0

    st.session_state.screen = "game"


# =====================================================
# 제목
# =====================================================

show_title()


# =====================================================
# SCREEN 1
# 새 사용자 시작
# =====================================================

if st.session_state.screen == "start":

    st.markdown(
        """
        <div class="white-text">
            🎰 Casino Mines에 오신 것을 환영합니다!
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="game-info">
            <div class="game-info-title">
                게임 방법
            </div>

            <div style="
                color:#ffffff;
                font-size:18px;
                font-weight:700;
                line-height:1.8;
                margin-top:10px;
            ">
                💎 보석을 찾을수록 배율이 올라갑니다.<br>
                💣 폭탄을 찾으면 게임이 즉시 종료됩니다.<br>
                💰 보석 5개부터 Cash Out이 가능합니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="white-text">
            처음 시작하는 사용자의 잔액을 입력하세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    initial_balance = st.number_input(
        "초기 잔액",
        min_value=100,
        step=100,
        value=10000,
        key="initial_balance_input",
    )

    if st.button(
        "🎰 게임 시작",
        use_container_width=True,
    ):

        if initial_balance < 100:

            st.error("잔액은 100칩 이상이어야 합니다.")

        else:

            st.session_state.balance = int(
                initial_balance
            )

            st.session_state.bet_amount = 0

            st.session_state.game = None

            st.session_state.screen = "bet"

            st.rerun()


# =====================================================
# SCREEN 2
# 베팅
# =====================================================

elif st.session_state.screen == "bet":

    show_balance()

    st.markdown(
        """
        <div class="white-text">
            🎲 이번 게임에 얼마를 베팅하시겠습니까?
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="game-info">
            <div class="game-info-title">
                베팅 가능한 최대 금액
            </div>

            <div class="game-info-value">
                {st.session_state.balance:,}칩
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    bet_amount = st.number_input(
        "베팅 금액",
        min_value=100,
        max_value=max(
            100,
            int(st.session_state.balance)
        ),
        step=100,
        value=min(
            100,
            int(st.session_state.balance)
        ),
        key="bet_input",
    )

    if st.button(
        "🎲 베팅하고 게임 시작",
        use_container_width=True,
    ):

        bet_amount = int(bet_amount)

        # 잔액보다 큰 베팅 방지
        if bet_amount > st.session_state.balance:

            st.error(
                "보유 잔액보다 큰 금액은 베팅할 수 없습니다."
            )

        elif bet_amount < 100:

            st.error(
                "베팅 금액은 100칩 이상이어야 합니다."
            )

        elif bet_amount % 100 != 0:

            st.error(
                "베팅 금액은 100칩 단위로 입력해야 합니다."
            )

        else:

            start_game(bet_amount)

            st.rerun()


# =====================================================
# SCREEN 3
# 게임 진행
# =====================================================

elif st.session_state.screen == "game":

    game = st.session_state.game

    show_balance()

    # -------------------------------------------------
    # 게임 정보
    # -------------------------------------------------

    multiplier = game.current_multiplier

    if game.gems_found in PAYOUTS:

        next_multiplier = PAYOUTS.get(
            game.gems_found + 1,
            None
        )

    else:

        next_multiplier = PAYOUTS.get(
            MIN_CASHOUT,
            None
        )


    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="game-info">
                <div class="game-info-title">
                    💎 발견한 보석
                </div>

                <div class="game-info-value">
                    {game.gems_found}개
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="game-info">
                <div class="game-info-title">
                    📈 현재 배율
                </div>

                <div class="game-info-value">
                    {multiplier:.1f}x
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # -------------------------------------------------
    # 다음 배율
    # -------------------------------------------------

    if next_multiplier is not None:

        st.markdown(
            f"""
            <div class="white-text">
                다음 보석 배율 : {next_multiplier:.1f}x
            </div>
            """,
            unsafe_allow_html=True,
        )


    # -------------------------------------------------
    # Cash Out 가능 알림
    # -------------------------------------------------

    if game.can_cash_out():

        reward_preview = int(
            st.session_state.bet_amount
            * game.current_multiplier
        )

        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                color:#000000;
                padding:15px;
                border-radius:10px;
                text-align:center;
                font-size:20px;
                font-weight:900;
                margin:15px 0;
            ">
                💰 Cash Out 가능!<br>
                지금 받기 : {reward_preview:,}칩
            </div>
            """,
            unsafe_allow_html=True,
        )


    # -------------------------------------------------
    # 게임판
    # -------------------------------------------------

    board = game.get_board_state()

    for row in range(ROWS):

        columns = st.columns(COLS)

        for col in range(COLS):

            cell = board[row][col]

            if cell["open"]:

                if cell["bomb"]:

                    symbol = "💣"

                elif cell["gem"]:

                    symbol = "💎"

                else:

                    symbol = "?"

                with columns[col]:

                    st.button(
                        symbol,
                        key=f"open_{row}_{col}",
                        disabled=True,
                        use_container_width=True,
                    )

            else:

                with columns[col]:

                    if st.button(
                        "❓",
                        key=f"cell_{row}_{col}",
                        use_container_width=True,
                    ):

                        result = game.click_cell(
                            row,
                            col
                        )

                        # --------------------------------
                        # 폭탄
                        # --------------------------------

                        if result["result"] == "bomb":

                            # 폭탄이 나오면 베팅금은 이미 차감되어 있음
                            game.reveal_all()

                            st.session_state.last_reward = 0

                            st.session_state.last_change = (
                                -st.session_state.bet_amount
                            )

                            st.session_state.screen = "result_bomb"

                            st.rerun()


                        # --------------------------------
                        # 보석
                        # --------------------------------

                        elif result["result"] == "gem":

                            st.rerun()


    # -------------------------------------------------
    # Cash Out 버튼
    # -------------------------------------------------

    st.markdown("---")

    if game.can_cash_out():

        if st.button(
            "💰 CASH OUT",
            use_container_width=True,
        ):

            result = game.cash_out(
                st.session_state.bet_amount
            )

            if result["success"]:

                reward = result["reward"]

                st.session_state.balance += reward

                st.session_state.last_reward = reward

                st.session_state.last_change = (
                    reward
                    - st.session_state.bet_amount
                )

                st.session_state.screen = "result_cashout"

                st.rerun()

    else:

        st.markdown(
            f"""
            <div class="white-text">
                💰 Cash Out은 보석 {MIN_CASHOUT}개부터 가능합니다.
            </div>
            """,
            unsafe_allow_html=True,
        )


# =====================================================
# SCREEN 4
# 폭탄 결과
# =====================================================

elif st.session_state.screen == "result_bomb":

    st.markdown(
        """
        <div class="result-box">

            <div class="result-title">
                💥 GAME OVER
            </div>

            <div class="result-text">
                폭탄을 발견했습니다!
            </div>

            <div class="result-text">
                이번 게임의 베팅 금액을 잃었습니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="result-box">

            <div class="result-text">
                이번 게임 결과
            </div>

            <div class="result-money">
                -{st.session_state.bet_amount:,}칩
            </div>

            <div class="result-text">
                현재 잔액
            </div>

            <div class="result-money">
                {st.session_state.balance:,}칩
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="white-text">
            다음 게임을 진행하시겠습니까?
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶ 계속하기",
            use_container_width=True,
        ):

            st.session_state.game = None

            st.session_state.bet_amount = 0

            st.session_state.screen = "bet"

            st.rerun()


    with col2:

        if st.button(
            "⏹ 게임 끝내기",
            use_container_width=True,
        ):

            st.session_state.screen = "final"

            st.rerun()


# =====================================================
# SCREEN 5
# Cash Out 결과
# =====================================================

elif st.session_state.screen == "result_cashout":

    st.markdown(
        """
        <div class="result-box">

            <div class="result-title">
                🎉 CASH OUT 성공!
            </div>

            <div class="result-text">
                게임을 성공적으로 종료했습니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="result-box">

            <div class="result-text">
                획득 칩
            </div>

            <div class="result-money">
                +{st.session_state.last_reward:,}칩
            </div>

            <div class="result-text">
                현재 잔액
            </div>

            <div class="result-money">
                {st.session_state.balance:,}칩
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="white-text">
            다음 게임을 진행하시겠습니까?
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶ 계속하기",
            use_container_width=True,
        ):

            st.session_state.game = None

            st.session_state.bet_amount = 0

            st.session_state.screen = "bet"

            st.rerun()


    with col2:

        if st.button(
            "⏹ 게임 끝내기",
            use_container_width=True,
        ):

            st.session_state.screen = "final"

            st.rerun()


# =====================================================
# SCREEN 6
# 최종 결과
# =====================================================

elif st.session_state.screen == "final":

    st.markdown(
        """
        <div class="result-box">

            <div class="result-title">
                🎰 GAME FINISHED
            </div>

            <div class="result-text">
                게임이 종료되었습니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="result-box">

            <div class="result-text">
                최종 잔액
            </div>

            <div class="result-money">
                {st.session_state.balance:,}칩
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="white-text">
            다음 사용자가 게임을 시작할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🎰 다음 사용자 시작",
        use_container_width=True,
    ):

        reset_for_new_user()

        st.rerun()
