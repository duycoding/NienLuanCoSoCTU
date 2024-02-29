import pygame, time

# local import
from base.base import GUIBase
from solver.parallel import Threads
from generator.generator import Generator


class LeftPanel(GUIBase):

    """Left control panel

    :Tham số solver: đối tượng solver
    :Kiểu solver: Solver
    :Tham số size: screen size (width height)
    :Kiểu size: tuple
    :Tham số screen: pygame screen
    :Kiểu screen: pygame.Surface
    """

    def __init__(self, solver, size: tuple, screen: pygame.Surface):
        super().__init__((size[0] - size[1], size[1]), screen)
        self.gamesystem = GameSystem(self.size, self.screen)
        self.time = Time(self.size, self.screen)
        self.hints = Hints(self.size, self.screen)
        self.auto_solver = AutoSolver(solver, self.size, self.screen)
        self.options = Options(solver, self.size, self.screen)

    def draw(self):
        """Vẽ panel bên trái màn hình"""
        # Vẽ khung chính
        # Đặt độ rộng của đường viền khung
        w = 3
        # Vẽ khung
        pygame.draw.rect(
            self.screen, (72, 234, 54), ((0, 0), (self.size[0], self.size[1])), w
        )

        pygame.draw.rect(
            self.screen,
            (72, 234, 54),
            ((0, 0), (self.size[0], self.size[1] // 9)),
            w // 3,
        )
        self._type("Sudoku", (72, 234, 54), (self.size[0] // 4, 14), 42)
        # Vẽ panel gợi ý/trạng thái
        self.hints.draw()
        # Vẽ panel Sudoku solver
        self.auto_solver.draw()
        # Vẽ panel đếm thời gian
        self.time.draw()
        # Vễ panel hiển thị trạng thái hê thống
        self.gamesystem.draw()
        # Vẽ panel (solve, select, reset, generate)
        self.options.draw()


class GameSystem(GUIBase):

    """GameSystem system class

    :Tham số size: kích thước màn hình (rộng cao)
    :Kiểu size: tuple
    :Tham số screen: pygame screen
    :Kiểu screen: pygame.Surface
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__wrongs_counter = 0
        self.__lost = False
        self.__won = False

    def reset(self):
        """Đặt lại giá trị khi thắng/thua và số lỗi"""
        self.__lost = False
        self.__won = False
        self.__wrongs_counter = 0

    @property
    def wrongs_counter(self):
        """Tăng biến đếm lỗi"""
        # Tăng biến đếm lỗi (max=5)
        if self.__wrongs_counter < 5:
            self.__wrongs_counter += 1
        else:
            # Đặt cờ thua
            self.__lost = True

    @property
    def lost(self) -> bool:
        """Thuộc tính lost (getter)"""
        return self.__lost

    @lost.setter
    def lost(self, value: bool):
        """Thuộc tính lost (setter)

        :Tham số value: lost value
        :Kiểu value: bool
        """
        self.__lost = value

    @property
    def won(self) -> bool:
        """Thuộc tính won (getter)"""
        return self.__won

    @won.setter
    def won(self, value: bool):
        """Thuộc tính won (setter)

        :Tham số value: won value
        :Kiểu value: bool
        """
        self.__won = value

    def draw(self):
        """Vẽ khung lỗi"""
        # Vẽ khung chính
        # Đặt độ rộng đường viền cho khung
        w = 1
        # Vẽ khung
        pygame.draw.rect(
            self.screen,
            (72, 234, 54),
            ((0, self.size[1] * 8), (self.size[0], self.size[1])),
            w,
        )

        # Kiem tra nếu người chơi thắng hoặc thua
        if self.__won:
            self._type(
                "You Won",
                (72, 234, 54),
                (self.size[0] // 4 - 10, self.size[1] * 8 + 15),
                38,
            )
        elif not self.__lost:
            self._type(
                "X  " * self.__wrongs_counter,
                (234, 72, 54),
                (40, self.size[1] * 8 + 15),
                38,
            )
        else:
            self._type(
                "You Lost",
                (234, 72, 54),
                (self.size[0] // 4 - 15, self.size[1] * 8 + 15),
                38,
            )


class Time(GUIBase):

    """Time managment class

    :Tham số size: Kích thước màn hình (rộng cao)
    :Kiểu size: tuple
    :Tham số screen: pygame screen
    :Kiểu screen: pygame.Surface
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__init_time = time.time()

    @property
    def init_time(self):
        """Thuôc tinh init_time (getter)"""
        return self.__init_time

    @init_time.setter
    def init_time(self, value: time.time):
        """Thuộc tính init_time (setter)

        :Tham số value: giá trị thời gian khỏi tạo
        :Kiểu value: time.time
        """
        self.__init_time = value

    def __time_formatter(self, delta: float) -> str:
        """Chuyển đổi số giây dạng số thực thành chuỗi định dạng HH:MM:SS

        :Tham số delta: Hiệu số giữa thời gian khởi tạo và thời gian hiện tại
        :Kiểu delta: float
        :Trả về: Chuỗi thời gian định dạng HH:MM:SS
        :Kieu: str
        """
        # Tính giờ, phút, giây từ số giây có phần thập phân
        hms = [delta // 60 // 60, delta // 60, delta % 60]
        # Chuyển đổi thành chuỗi với số 0 ở đầu nếu số < 10
        for i in range(len(hms)):
            hms[i] = f"0{int(hms[i])}" if hms[i] < 10 else f"{int(hms[i])}"
        return f"{hms[0]}:{hms[1]}:{hms[2]}"

    def draw(self):
        """Vẽ khung thời gian"""
        # Vẽ khung chính
        # Đặt độ rộng đường viền của khung
        w = 1
        # Vẽ khung
        pygame.draw.rect(
            self.screen,
            (72, 234, 54),
            ((0, self.size[1] * 7), (self.size[0], self.size[1])),
            w,
        )

        ftime = self.__time_formatter(time.time() - self.__init_time)
        self._type(
            f"Time: {ftime}",
            (72, 234, 54),
            (self.size[0] // 9 - 3, self.size[1] * 7 + 21),
            32,
        )


class Hints(GUIBase):

    """Hints system class

    :Tham số size: kích thước mành hình (rộng cao)
    :Kiểu size: tuple
    :Tham số screen: pygame screen
    :Kiểu screen: pygame.Surface
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__hint = "everything is well"

    @property
    def hint(self) -> str:
        """Thuộc tính hint (getter)"""
        return self.__hint

    @hint.setter
    def hint(self, value: str):
        """Thuộc tính hint (setter)

        :Tham số value: hint value
        :Kiểu value: str
        """
        self.__hint = value

    def draw(self):
        """Draw Hint rect"""
        # Vẽ khung chính
        # Đặt độ
        w = 1
        # Vẽ khung
        pygame.draw.rect(
            self.screen,
            (72, 234, 54),
            ((0, self.size[1]), (self.size[0], self.size[1])),
            w,
        )
        # Vẽ gợi ý
        self._type(
            f"Hint: {self.__hint}",
            (72, 234, 54),
            (self.size[0] // 9 - 18, self.size[1] + 25),
            24,
        )


class AutoSolver(GUIBase):

    """Auto solver control panel class

    :Tham số solver: đối tượng solver
    :Kiểu solver: Solver
    :Tham số size: kích thước màn hình (rộng cao)
    :Kiểu size: tuple
    :Tham số screen: pygame screen
    :Kiểu screen: pygame.Surface
    """

    def __init__(self, solver, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__threads = Threads()
        self.__solver = solver
        # Tạo ra các nút
        controlsize = (self.size[0] - self.size[0] // 2 - 25, self.size[1] // 2)
        self.__buttons = [
            Button(*i, controlsize, self.screen)
            for i in (
                (self.pause, (), (-2, -2), "pause", 24, (20, 220)),
                (self.resume, (), (-10, -2), "resume", 24, (145, 220)),
                (self.start, (), (2, 0.8), "start", 24, (20, 270)),
                (self.kill, (), (2.3, 0.9), "stop", 24, (145, 270)),
            )
        ]
        # Tạo ra nút delay
        delaysize = (self.size[0] - self.size[0] // 2 - 25, self.size[1] // 4)
        self.__buttons.extend(
            [
                Button(*i, delaysize, self.screen)
                for i in (
                    (self.delay, (1000), (15, -1), "1.0", 16, (20, 345)),
                    (self.delay, (500), (15, -1), "0.5", 16, (20, 373)),
                    (self.delay, (750), (10, -1), "0.75", 16, (145, 345)),
                    (self.delay, (250), (10, -1), "0.25", 16, (145, 373)),
                )
            ]
        )
        self.__run = False

    @property
    def delay(self) -> float:
        """Thuộc tính delay (getter)"""
        return self.__solver.delay

    def delay(self, value: float):
        """Thuộc tính delay (setter)

        :Tham số value: delay value
        :Kiểu value: float
        """
        self.__solver.delay = value

    @property
    def buttons(self):
        """Thuộc tính buttons (getter)"""
        return self.__buttons

    def start(self):
        """Bắt đầu giải tự động"""
        if not self.__run:
            self.__solver.kill = False
            self.__solver.e = True
            self.__threads.start(self.__solver.auto_solver)
            self.__run = True

    def kill(self):
        """Dừng quá trình giải tự động"""
        self.__solver.kill = True
        self.__threads.stop()
        self.__run = False

    def pause(self):
        """Tạm đừng giải tự động bằng cách xóa cờ"""
        if self.__run and self.__solver.e:
            self.__solver.e = False
            self.__run = False

    def resume(self):
        """Tiếp tục giải tự động bằng cách đặt cờ"""
        if not self.__run and not self.__solver.e:
            self.__solver.e = True
            self.__run = True

    def draw(self):
        """Vẽ khung Sudoku solver"""
        # Vẽ khung chính
        # Đặt độ rộng cho khung
        w = 1

        pygame.draw.rect(
            self.screen,
            (72, 234, 54),
            ((0, self.size[1] * 2), (self.size[0], self.size[1] * 3)),
            w,
        )
        # Đặt tựa đề cho panel
        self._type(
            "Sudoku solver",
            (72, 234, 54),
            (self.size[0] // 9 + 10, self.size[1] * 2.15),
            30,
        )
        # Đặt tựa đề cho phần độ trễ
        self._type(
            "Delay (secs)", (72, 234, 54), (self.size[0] // 3, self.size[1] * 4), 18
        )
        # Vẽ các nút
        for b in self.__buttons:
            b.draw()


class Options(GUIBase):

    """Options class

    :Tham số solver: đối tượng solver
    :Kiểu solver: Solver
    :Tham số size: kích thước màn hình (rộng cao)
    :Kiểu size: tuple
    :Tham sô screen: pygame screen
    :Kiểu screen: pygame.Surface
    """

    def __init__(self, solver, size: tuple, screen: pygame.Surface):
        super().__init__((size[0], size[1] // 9), screen)
        self.__solver = solver
        self.__generator = Generator()
        # Tao nút điều khiển
        controlsize = (self.size[0] - self.size[0] // 2 - 25, self.size[1] // 2)
        self.__buttons = [
            Button(*i, controlsize, self.screen)
            for i in (
                (self.solve_all, (), (14.25, -1.8), "all", 24, (20, 450)),
                (self.solve_selected, (), (-16, -1.8), "selected", 24, (145, 450)),
                (self.reset, (), (1.8, 0.7), "reset", 24, (20, 500)),
                (self.generate, (), (-18.3, 0.7), "generate", 24, (145, 500)),
            )
        ]

    @property
    def buttons(self):
        """Thuộc tính buttons (getter)"""
        return self.__buttons

    def solve_all(self) -> bool:
        """Giải toàn bộ bảng

        :Trả về: solvability
        :Kiểu trả về: bool
        """
        # Giải tất cả
        s = self.__solver.solve(self.__solver.board.board)
        self.__solver.board.update_squares()
        return s

    def solve_selected(self, board: list, pos: tuple):
        """Giải ô được chọn

        :Tham sô board: bảng cờ cần giải
        :Kiểu board: list
        :Tham số pos: vị trí ô được chọn
        :Kiểu pos: tuple
        """
        # Giải bàn cờ
        solution = self.__solver.solve(board)
        # NẾu có thể giải đặt giá trị cho ô được chọn
        if solution and pos:
            self.__solver.board.board[pos[0]][pos[1]] = board[pos[0]][pos[1]]
            self.__solver.board.update_squares()
        return solution

    def generate(self, board: list) -> bool:
        """ Làm lại một bàn cờ mới

        :Tham số board: bàn cờ sudoku
        :Kiểu board: list
        """
        # Đặt một bàn cờ mới ngẫu nhiên
        board.board = self.__generator.generate()
        return True

    def reset(self) -> bool:
        """Làm mới lại bàn cờ"""
        # Khác với generate đây là một bàn cờ cũ và xóa hết
        # giá trị tại nhưng ô đã giải trước đó
        # Lập qua tất cả các ô
        for r in range(9):
            for c in range(9):
                # Kiểm tra các ô có thể thay đổi
                if self.__solver.board.squares[r][c].changeable:
                    # Đặt lại giá trị của nó là 0
                    self.__solver.board.board[r][c] = 0
        # Xóa ô sai
        if self.__solver.board.wrong:
            self.__solver.board.clear
        # cập nhật các ô
        self.__solver.board.update_squares()
        return True

    def draw(self):
        """Vẽ lại khung solver"""
        # sovle txt
        self._type("solve", (72, 234, 54), (110, 420), 22)
        # Vẽ các nút
        for b in self.__buttons:
            b.draw()


class Button(GUIBase):

    """Button class

    :Tham số target: chức năng mục tiêu để bắt đầu onclicked
    :Kiểu target: function
    :Tham số _args: đối số của hàm mục tiêu
    :Kiểu _args: tuple
    :Tham số s: khoảng trống bên trái và bên trên
    :Kiểu s: tuple
    :Tham số innertxt: inner text
    :Kiểu innertxt: str
    :Tham số fontsize: innertxt size
    :Kiểu fontsize: int
    :Tham số pos: square position (row, column)
    :Kiểu pos: tuple
    :Tham số size: screen size (width height)
    :Kiểu size: tuple
    :Tham số screen: pygame screen
    :Kiểu screen: pygame.Surface
    """

    def __init__(
        self,
        target,
        _args: tuple,
        s: tuple,
        innertxt: str,
        fontsize: int,
        pos: tuple,
        size: tuple,
        screen: pygame.Surface,
    ):
        super().__init__(size, screen)
        self.__pos = pos
        self.__innertxt = innertxt
        self.__fontsize = fontsize
        self.__target = target
        self.__args = _args
        self.__fill = (0, 0, 0)
        self.__w = 1
        self.__s = s
        self.__click_range = (
            range(self.__pos[0], self.__pos[0] + self.size[0] + 1),
            range(self.__pos[1], self.__pos[1] + self.size[1] + 1),
        )

    @property
    def innertxt(self):
        """Thuộc tính innertxt(getter)"""
        return self.__innertxt

    @property
    def click_range(self):
        """click range property"""
        return self.__click_range

    @property
    def reset(self):
        """Reset button style"""
        self.__fill = (0, 0, 0)
        self.__w = 1

    def click(self, args: tuple = ()):
        """Xử lý sự kiện click

        :Tham số args: đối số hàm mục tiêu nếu đối số không là hằng số
        :type args: tuple
        """
        # Thay đổi phong cách nút
        self.__fill = (30, 50, 20)
        self.__w = 2

        if self.__args:
            return self.__target(self.__args)
        elif args:
            return self.__target(*args)
        else:
            return self.__target()

    def draw(self):
        """Draw button rect"""
        # Vẽ khung chính

        pygame.draw.rect(
            self.screen,
            (72, 234, 54),
            (self.__pos, self.size),
            self.__w,
        )
        # Đặt inner txt
        self._type(
            self.__innertxt,
            (72, 234, 54),
            (
                self.__pos[0] + self.size[0] // 4 + self.__s[0],
                self.__pos[1] + self.size[1] // 8 + self.__s[1],
            ),
            self.__fontsize,
        )
