import threading
import time


class Solver:

    """Lop Solver dùng thuật toán quay lui để giải bàn cờ Sudoku

    :Tham số board: thực thể là một bảng Sudoku
    :Kiểu board: Board
    :Tham số delay: độ trễ khi giải
    :Kiểu delay: float
    """

    def __init__(self, board=None, delay: float = 0.0):
        self.board = board
        self.__delay = delay / 1000
        self.__e = threading.Event()
        self.__kill = False
        self.__e.set()

    @property
    def delay(self) -> float:
        """Thuộc tính delay (getter)"""
        return self.__delay

    @delay.setter
    def delay(self, delay: float):
        """Thuộc tính delay (setter)

        :Tham số delay: đô trễ
        :Kiểu delay: float
        """
        self.__delay = delay / 1000

    @property
    def e(self):
        """Thuộc tính e (getter)"""
        return self.__e.is_set()

    @e.setter
    def e(self, set: bool):
        """Thuộc tính e (setter)

        :Tham số set: set of not
        :Kiểu set: bool
        """
        if set:
            self.__e.set()
        else:
            self.__e.clear()

    @property
    def kill(self):
        """Dừng chức năng giải để tham gia và luồng"""
        return self.__kill

    @kill.setter
    def kill(self, kill: bool):
        """Thuộc tính kill (setter)

        :Tham số kill: value
        :Kiểu kill: bool
        """
        self.__kill = kill

    def auto_solver(self) -> bool:
        """Giải bàn ờ sử dung dụng thuật toán quay lui (tự dộng giải (trạng thái bàn cờ thay đổi))

        :trả về: True nếu bàn cờ được giải ngược lại là False
        :Kiểu trả về: bool
        """
        if not self.__kill:
            # Lấy vị trí chưa được giải từ trái sang phải và từ trên xuống dưới
            pos = self.nextpos(self.board.board)
            # Kiểm tra xem còn vị trí chưa giải không
            if not pos:
                return True
            # Duyệt qua tất cả các số khả dụng ( từ 1 đến 9)
            for n in range(1, 10):
                # Kiểm tra nếu số hợp lệ với quy tắc sudoku
                if not self.exists(self.board.board, n, pos):
                    # Tạm dừng nếu cần
                    self.__e.wait()
                    # Thay đổi trạng thái bảng
                    self.board.set_sq_value(n, (pos[0], pos[1]))
                    self.board.board[pos[0]][pos[1]] = n
                    # sleep (solution case)
                    time.sleep(self.__delay)
                    # Tiếp tục giải
                    if self.auto_solver():
                        return True
                    if not self.__kill:
                        # Thạm dừng
                        self.__e.wait()
                        # Quay lui
                        # Thay đổi trạng thái bàn cờ
                        self.board.set_sq_value(0, (pos[0], pos[1]))
                        self.board.board[pos[0]][pos[1]] = 0
            # sleep (backtracking case)
            time.sleep(self.__delay)
            # Không có giải pháp nào thỏa
            return False

    def solve(self, board: list) -> bool:
        """Giải bàn cờ dựa trên thuật toán quay lui

        :Tham số board: bàn cờ sudoku bằng mảng hai chiều
        :Kiểu board: list
        :returns: true nếu bàn cờ được giải và false nếu ngược lại
        :rtype: bool
        """
        # Lấy giá trị chưa giải (bắt đầu từ trái sang phải từ trên xuống dưới)
        pos = self.nextpos(board)
        # Kiểm tra xem vị trí đó có tồn tại
        if not pos:
            return True
        # Duyệt qua các số khả dụng từ 1 - 9
        for n in range(1, 10):
            # Kiểm tra xem số đó có thỏa mãn quy tắc sudoku hay không
            if not self.exists(board, n, pos):
                # Đặt giá trị phù hợp
                board[pos[0]][pos[1]] = n
                # Tiếp tục giải
                if self.solve(board):
                    return True
                # quay lui
                board[pos[0]][pos[1]] = 0
        # Không có giải pháp phù hợp
        return False

    def nextpos(self, board: list) -> tuple:
        """Lấy giá trị chưa được giải từ trái sang phải và từ trên xuống dưới

        :Tham số board: Bảng sudoku là một mảng hai chiều
        :Kiểu board: list
        :Trả về: vị trí tiếp theo chưa được giải hoặc tupble rỗng nếu không tồn tai vi trí đó
        :Kiểu: tuple
        """
        # Lặp qua các dòng
        for r in range(9):
            # Lặp qua các cột
            for c in range(9):
                # Kiểm tra nghữn gái trị chưa giải
                if board[r][c] == 0:
                    return (r, c)
        # Kết thúc nếu đi đến vị trí cuối cùng của bàn cờ
        return ()

    def exists(self, board: list, n: int, rc: tuple) -> tuple:
        """Kiểm tra thỏa mãn quy tắc sudoku

        :Tham số board: Bàn cờ sudoku là một mảng hai chiều
        :Kiểu board: list
        :Tham số n: số nguyên là giải pháp
        :Kiểu n: int
        :Tham số rc: Vị trí trên bảng được biểu diễn dưới dạng (hàng, cột)
        :Kiểu rc: tuple
        :Trả về: tuple chứa vị trí số tồn tại hoặc tuple rỗng nếu vị trí không tồn tại
        :Kiểu trả về: tuple
        """
        # Kiểm tra quy tắc hàng
        # Duyệt qua tất cả các cột
        for c in range(len(board)):
            # Kiểm tra xem số có tồn tại cùng một hàng
            if board[rc[0]][c] == n:
                return (rc[0], c)
        # Kiểu tra quy tắc cột
        # Duyệt qua tất cả các cột
        for r in range(len(board)):
            # Kiểm tra xem số có tồn tại trong cùng một cột
            if board[r][rc[1]] == n:
                return (r, rc[1])
        # Kiem tra luật trong vùng 3*3
        # Tính toán vị trí bắt đầu của khu vực 3*3
        spos = ((rc[0] // 3) * 3, (rc[1] // 3) * 3)
        # Lặp qua khu vực 3x3 từ spos[0] đến spos[0] + 3 (hàng)
        for r in range(spos[0], spos[0] + 3):
            # Lặp qua khu vực 3x3 từ spos[1] đến spos[1] + 3 (cột)
            for c in range(spos[1], spos[1] + 3):
                # Kiểm tra xem số có tồn tại trong cùng một khu vực 3*3 không
                if board[r][c] == n:
                    return (r, c)
        # Vị trí không hợp lệ
        return ()
