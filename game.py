"""
=====================================================
Casino Mines - Game Logic
=====================================================

게임의 핵심 로직을 담당합니다.

구성:
- Cell : 게임판 한 칸
- Game : 한 게임의 전체 상태 및 진행
=====================================================
"""

import random

from config import (
    ROWS,
    COLS,
    BOMB_COUNT,
    FIRST_CLICK_SAFE,
    MIN_CASHOUT,
    PAYOUTS,
)


# =====================================================
# Cell
# =====================================================

class Cell:

    def __init__(self):
        self.is_bomb = False
        self.is_gem = False
        self.is_open = False

    def open(self):
        self.is_open = True


# =====================================================
# Game
# =====================================================

class Game:

    def __init__(self):
        self.reset()


    # =================================================
    # 게임 초기화
    # =================================================

    def reset(self):

        self.board = self.create_board()

        self.first_click = True

        self.gems_found = 0

        self.current_multiplier = 1.0

        self.game_over = False

        self.cashed_out = False

        self.result = None


    # =================================================
    # 보드 생성
    # =================================================

    def create_board(self):

        board = []

        for _ in range(ROWS):

            row = []

            for _ in range(COLS):

                row.append(Cell())

            board.append(row)

        return board


    # =================================================
    # 폭탄 배치
    # =================================================

    def place_bombs(self, safe_position):

        possible_positions = []

        for row in range(ROWS):

            for col in range(COLS):

                if (row, col) != safe_position:

                    possible_positions.append(
                        (row, col)
                    )


        bomb_positions = random.sample(
            possible_positions,
            BOMB_COUNT
        )


        for row, col in bomb_positions:

            self.board[row][col].is_bomb = True


        # 폭탄이 아닌 모든 칸은 보석
        for row in range(ROWS):

            for col in range(COLS):

                cell = self.board[row][col]

                if not cell.is_bomb:

                    cell.is_gem = True


    # =================================================
    # 칸 클릭
    # =================================================

    def click_cell(self, row, col):

        # 게임이 끝난 경우
        if self.game_over:

            return {
                "result": "error",
                "message": "게임이 이미 종료되었습니다."
            }


        # 좌표 검증
        if not (
            0 <= row < ROWS
            and
            0 <= col < COLS
        ):

            return {
                "result": "error",
                "message": "잘못된 위치입니다."
            }


        cell = self.board[row][col]


        # 이미 선택한 칸
        if cell.is_open:

            return {
                "result": "error",
                "message": "이미 선택한 칸입니다."
            }


        # =============================================
        # 첫 클릭
        # =============================================

        if self.first_click:

            if FIRST_CLICK_SAFE:

                self.place_bombs(
                    (row, col)
                )

            self.first_click = False


        # 칸 열기
        cell.open()


        # =============================================
        # 폭탄
        # =============================================

        if cell.is_bomb:

            self.game_over = True

            self.result = "bomb"

            return {
                "result": "bomb",
                "message": "💥 폭탄을 발견했습니다!"
            }


        # =============================================
        # 보석
        # =============================================

        if cell.is_gem:

            self.gems_found += 1

            self.update_multiplier()

            return {
                "result": "gem",
                "message": "💎 보석 발견!"
            }


        return {
            "result": "unknown",
            "message": "알 수 없는 결과"
        }


    # =================================================
    # 배율 업데이트
    # =================================================

    def update_multiplier(self):

        if self.gems_found in PAYOUTS:

            self.current_multiplier = PAYOUTS[
                self.gems_found
            ]

        else:

            self.current_multiplier = 1.0


    # =================================================
    # Cash Out 가능 여부
    # =================================================

    def can_cash_out(self):

        return (
            self.gems_found >= MIN_CASHOUT
            and not self.game_over
            and not self.cashed_out
        )


    # =================================================
    # Cash Out
    # =================================================

    def cash_out(self, bet_amount):

        if not self.can_cash_out():

            return {
                "success": False,
                "reward": 0,
                "message": "아직 Cash Out 할 수 없습니다."
            }


        reward = int(
            bet_amount * self.current_multiplier
        )


        self.cashed_out = True

        self.game_over = True

        self.result = "cashout"


        return {
            "success": True,
            "reward": reward,
            "message": "🎉 Cash Out 성공!"
        }


    # =================================================
    # 전체 보드 공개
    # =================================================

    def reveal_all(self):

        for row in self.board:

            for cell in row:

                cell.open()


    # =================================================
    # 보드 상태 반환
    # =================================================

    def get_board_state(self):

        board_state = []

        for row in self.board:

            row_state = []

            for cell in row:

                row_state.append(
                    {
                        "bomb": cell.is_bomb,
                        "gem": cell.is_gem,
                        "open": cell.is_open
                    }
                )

            board_state.append(row_state)

        return board_state


    # =================================================
    # 현재 상태
    # =================================================

    def get_status(self):

        return {
            "gems_found": self.gems_found,
            "multiplier": self.current_multiplier,
            "game_over": self.game_over,
            "cashed_out": self.cashed_out,
            "result": self.result
        }
