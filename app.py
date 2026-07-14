"""
app.py

Casino Mines Streamlit UI

게임 화면을 담당한다.
게임 로직은 game.py에서 처리한다.
"""

import streamlit as st

from game import Game


# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="Casino Mines",
    page_icon="💎",
    layout="centered"
)


# --------------------------------------------------
# 게임 생성
# --------------------------------------------------

def create_game():
    """
    새로운 Game 객체 생성
    """

    return Game()


# --------------------------------------------------
# Session 관리
# --------------------------------------------------

def get_game():
    """
    현재 게임 반환.

    Streamlit rerun 때문에
    session_state 사용.
    """

    if "game" not in st.session_state:
        st.session_state.game = create_game()

    return st.session_state.game


# --------------------------------------------------
# 게임 리셋
# --------------------------------------------------

def reset_game():
    """
    새 게임 시작
    """

    st.session_state.game = create_game()


# --------------------------------------------------
# 메인 화면
# --------------------------------------------------

def main():

    game = get_game()

    st.title("💎 Casino Mines")

    st.divider()

    # 상태 표시

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "보석",
            f"{game.get_gems()}개"
        )

    with col2:
        st.metric(
            "배율",
            f"{game.get_multiplier()}x"
        )


    st.divider()


    # 보드 출력

    for row in range(5):

        cols = st.columns(5)

        for col in range(5):

            with cols[col]:

                state = game.get_cell_state(
                    row,
                    col
                )

                if state == "hidden":

                    if st.button(
                        "⬜",
                        key=f"{row}_{col}"
                    ):

                        game.reveal(
                            row,
                            col
                        )

                        st.rerun()

                elif state == "gem":

                    st.button(
                        "💎",
                        key=f"{row}_{col}",
                        disabled=True
                    )

                elif state == "bomb":

                    st.button(
                        "💣",
                        key=f"{row}_{col}",
                        disabled=True
                    )


    st.divider()


    # Cash Out

    if game.can_cash_out():

        if st.button("💰 Cash Out"):

            reward = game.cash_out()

            st.success(
                f"성공! {reward}배 획득"
            )

            st.rerun()


    # 새 게임

    if st.button("🔄 New Game"):

        reset_game()

        st.rerun()



if __name__ == "__main__":

    main()
