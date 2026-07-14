"""
game.py

카지노 Mines 게임의 핵심 로직.

이 파일은 Game 클래스와 Cell 클래스를 정의한다.
UI(Streamlit)는 app.py에서 담당하고,
이 파일은 오직 게임 상태만 관리한다.
"""

import random

from config import (
    BOARD_SIZE,
    GEM_COUNT,
    BOMB_COUNT,
    MIN_CASHOUT_GEMS,
    MULTIPLIERS,
)


class Cell:
    """
    보드의 한 칸을 나타내는 클래스.

    bomb      : 폭탄 여부
    revealed  : 공개 여부
    """

    def __init__(self):
        """기본 상태로 초기화"""

        self.bomb = False
        self.revealed = False


class Game:
    """
    카지노 Mines 게임 클래스.

    게임 진행에 필요한
    모든 상태를 저장한다.
    """

    def __init__(self):
        """새 게임 생성"""

        # 보드 생성
        self.board = self._create_board()

        # 첫 클릭 여부
        # False면 아직 폭탄이 생성되지 않음
        self.first_click = False

        # 게임 종료 여부
        self.game_over = False

        # 승리 여부
        self.win = False

        # 획득한 보석 수
        self.gems = 0

        # 현재 배율
        self.multiplier = 1.0

    # --------------------------------------------------
    # 보드 생성
    # --------------------------------------------------

    def _create_board(self):
        """
        빈 보드를 생성한다.

        Returns
        -------
        list[list[Cell]]
        """

        board = []

        for _ in range(BOARD_SIZE):

            row = []

            for _ in range(BOARD_SIZE):
                row.append(Cell())

            board.append(row)

        return board

    # --------------------------------------------------
    # 좌표 검사
    # --------------------------------------------------

    def is_valid(self, row, col):
        """
        좌표가 보드 안인지 확인.

        Returns
        -------
        bool
        """

        return (
            0 <= row < BOARD_SIZE
            and
            0 <= col < BOARD_SIZE
        )

    # --------------------------------------------------
    # 셀 반환
    # --------------------------------------------------

    def get_cell(self, row, col):
        """
        Cell 객체 반환.

        Parameters
        ----------
        row : int
        col : int
        """

        if not self.is_valid(row, col):
            return None

        return self.board[row][col]

    # --------------------------------------------------
    # 공개 가능한지 확인
    # --------------------------------------------------

    def can_reveal(self, row, col):
        """
        해당 칸을 공개할 수 있는지 확인.

        Returns
        -------
        bool
        """

        if self.game_over:
            return False

        cell = self.get_cell(row, col)

        if cell is None:
            return False

        if cell.revealed:
            return False

        return True

    # --------------------------------------------------
    # 현재 배율 계산
    # --------------------------------------------------

    def update_multiplier(self):
        """
        현재 획득한 보석 수에 따라
        배율을 계산한다.
        """

        self.multiplier = MULTIPLIERS.get(
            self.gems,
            1.0
        )

    # --------------------------------------------------
    # Cash Out 가능 여부
    # --------------------------------------------------

    def can_cash_out(self):
        """
        Cash Out 가능한지 확인.

        Returns
        -------
        bool
        """

        return self.gems >= MIN_CASHOUT_GEMS
      # --------------------------------------------------
    # 폭탄 생성
    # --------------------------------------------------

    def generate_bombs(self, safe_row, safe_col):
        """
        첫 클릭 이후 폭탄을 생성한다.

        Parameters
        ----------
        safe_row : int
            첫 클릭한 행

        safe_col : int
            첫 클릭한 열
        """

        positions = []

        # 첫 클릭한 칸을 제외한 좌표 저장
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):

                if row == safe_row and col == safe_col:
                    continue

                positions.append((row, col))

        # 랜덤 섞기
        random.shuffle(positions)

        # 폭탄 배치
        for row, col in positions[:BOMB_COUNT]:
            self.board[row][col].bomb = True

        # 첫 클릭 완료
        self.first_click = True

    # --------------------------------------------------
    # 모든 칸 공개
    # --------------------------------------------------

    def reveal_all(self):
        """
        게임 종료 시
        모든 칸을 공개한다.
        """

        for row in self.board:
            for cell in row:
                cell.revealed = True

    # --------------------------------------------------
    # 게임 종료
    # --------------------------------------------------

    def end_game(self, win=False):
        """
        게임을 종료한다.

        Parameters
        ----------
        win : bool
            승리 여부
        """

        self.game_over = True
        self.win = win

        self.reveal_all()

    # --------------------------------------------------
    # 승리 여부 확인
    # --------------------------------------------------

    def check_win(self):
        """
        모든 보석을 찾았는지 확인한다.

        Returns
        -------
        bool
        """

        return self.gems >= GEM_COUNT

    # --------------------------------------------------
    # 셀 공개
    # --------------------------------------------------

    def reveal(self, row, col):
        """
        셀 하나를 공개한다.

        Returns
        -------
        bool

        True  : 보석

        False : 폭탄
        """

        # 클릭 가능한지 확인
        if not self.can_reveal(row, col):
            return None

        # 첫 클릭이면 폭탄 생성
        if not self.first_click:
            self.generate_bombs(row, col)

        cell = self.get_cell(row, col)

        cell.revealed = True

        # 폭탄 클릭
        if cell.bomb:
            self.end_game(False)
            return False

        # 보석 획득
        self.gems += 1

        # 배율 갱신
        self.update_multiplier()

        # 승리 확인
        if self.check_win():
            self.end_game(True)

        return True
          # --------------------------------------------------
    # Cash Out 실행
    # --------------------------------------------------

    def cash_out(self):
        """
        현재 게임을 Cash Out 한다.

        Returns
        -------
        float
            현재 배율

        None
            Cash Out 불가능
        """

        if not self.can_cash_out():
            return None

        self.end_game(True)

        return self.multiplier


    # --------------------------------------------------
    # 게임 초기화
    # --------------------------------------------------

    def reset(self):
        """
        새로운 게임으로 초기화한다.
        """

        self.board = self._create_board()

        self.first_click = False

        self.game_over = False

        self.win = False

        self.gems = 0

        self.multiplier = 1.0


    # --------------------------------------------------
    # 현재 상태 반환
    # --------------------------------------------------

    def get_status(self):
        """
        현재 게임 상태를 반환한다.

        Streamlit 화면 출력용.

        Returns
        -------
        dict
        """

        return {
            "gems": self.gems,
            "multiplier": self.multiplier,
            "game_over": self.game_over,
            "win": self.win,
        }


    # --------------------------------------------------
    # 셀 상태 반환
    # --------------------------------------------------

    def get_cell_state(self, row, col):
        """
        특정 칸의 상태 반환.

        Streamlit에서
        버튼 표시용으로 사용한다.

        Returns
        -------
        str
        """

        cell = self.get_cell(row, col)

        if cell is None:
            return "empty"

        if not cell.revealed:
            return "hidden"

        if cell.bomb:
            return "bomb"

        return "gem"
        # --------------------------------------------------
    # 보드 전체 상태 반환
    # --------------------------------------------------

    def get_board_state(self):
        """
        현재 보드 상태를 반환한다.

        Streamlit에서
        전체 보드를 그릴 때 사용한다.

        Returns
        -------
        list[list[str]]
        """

        state = []

        for row in range(BOARD_SIZE):

            row_state = []

            for col in range(BOARD_SIZE):

                row_state.append(
                    self.get_cell_state(row, col)
                )

            state.append(row_state)

        return state


    # --------------------------------------------------
    # 남은 클릭 가능 칸 확인
    # --------------------------------------------------

    def remaining_cells(self):
        """
        아직 공개하지 않은 칸 개수를 반환한다.

        Returns
        -------
        int
        """

        count = 0

        for row in self.board:

            for cell in row:

                if not cell.revealed:
                    count += 1

        return count


    # --------------------------------------------------
    # 게임 진행 가능 여부
    # --------------------------------------------------

    def is_playing(self):
        """
        현재 게임 진행 중인지 확인한다.

        Returns
        -------
        bool
        """

        return not self.game_over


    # --------------------------------------------------
    # 현재 보석 개수 반환
    # --------------------------------------------------

    def get_gems(self):
        """
        현재 획득한 보석 개수를 반환한다.
        """

        return self.gems
    # --------------------------------------------------
    # 현재 배율 반환
    # --------------------------------------------------

    def get_multiplier(self):
        """
        현재 배율 반환.
        """

        return self.multiplier
