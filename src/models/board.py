import pygame

# local import
from base.base import GUIBase
from solver.solver import Solver


class Board(GUIBase):

    """Bảng Sudoku

    :Tham số board: Bảng Sudoku được biểu diễn dưới dạng một mảng hai chiều
    :Kiểu board: list
    :Tham số size: Kích thước màn hình (đơn vị pixel) (chiều rộng, chiều cao)
    :type size: tuple
    :param screen: màn hình pygame
    :type screen: pygame.Surface
    """

    def __init__(self, size: tuple, board: list, screen: pygame.Surface):
        super().__init__((size[1], size[1], size[0] - size[1]), screen)
        self.__board = board
        self.__solver = Solver(self)
        # Tạo ra danh sách các ô
        self.__squares = [
            [
                Square(
                    self.__board[c][r],
                    (r, c),
                    (self.size[0], self.size[2]),
                    self.screen,
                    True if self.__board[c][r] == 0 else False,
                )
                for r in range(9)
            ]
            for c in range(9)
        ]
        self.__selected = None
        self.__wrong = None

    @property
    def wrong(self):
        """Thuộc tính khi người chơi sai (getter)"""
        return self.__wrong

    @property
    def squares(self) -> list:
        """Thuộc tính các ô (trong bàn cờ) (getter)"""
        return self.__squares

    def update_squares(self):
        """Thuộc tính các ô (trong bàn cờ) (updatter)"""
        # Lặp qua tất cả các ô vuông
        for r in range(9):
            for c in range(9):
                # Cập nhật giá trị
                self.__squares[r][c].value = self.__board[r][c]
                self.__squares[r][c].pencil = 0

    @property
    def board(self) -> list:
        """Thuộc tính bảng (getter)"""
        return self.__board

    @board.setter
    def board(self, board: list):
        """Thuộc tính bảng (setter) & cập nhật các ô (trong bàn cờ)

        :Tham số board: Bảng Sudoku được biểu diễn dưới dạng một mảng hai chiều
        :Kiểu board: list
        """
        # Đặt bảng mới
        self.__board = board
        # Làm lại các ô
        self.__squares = [
            [
                Square(
                    self.__board[c][r],
                    (r, c),
                    (self.size[0], self.size[2]),
                    self.screen,
                    True if self.__board[c][r] == 0 else False,
                )
                for r in range(9)
            ]
            for c in range(9)
        ]

    @property
    def selected(self) -> tuple:
        """Thuộc tính selected (getter)"""
        return self.__selected

    @selected.setter
    def selected(self, pos: tuple):
        """Thuộc tính selected (setter) & làm mới các ô

        :Tham số pos: chọn các ô theo vị trí (dòng, cột)
        :Kiểu pos: tuple
        """
        if not self.__wrong:
            # Xóa sự lựa chọn trước
            if self.__selected != None:
                self.__squares[self.__selected[0]][self.__selected[1]].selected = False
            if pos:
                # Chọn một ô mới
                self.__selected = pos
                self.__squares[self.__selected[0]][self.__selected[1]].selected = True
            else:
                # Đặt la thành None nếu có vị trí nằm ngoài bảng
                self.__selected = None

    @property
    def get_pencil(self) -> int:
        """selected square pencil (getter)"""
        # Lấy ô được chọn
        r, c = self.__selected
        return self.__squares[r][c].pencil

    def set_pencil(self, value: int):
        """Gắn giá trị pencil

        :Tham số value: pencil value
        :Kiểu value: int
        """
        # Lấy ô được chọn
        r, c = self.__selected
        if self.__squares[r][c].value == 0:
            self.__squares[r][c].pencil = value

    @property
    def get_value(self) -> int:
        """Lấy giá trị ô được chọn (getter)"""
        # Lấy ô được chọn
        r, c = self.__selected
        return self.__squares[r][c].value

    def set_value(self) -> str:
        """Đặt giá trị ô

        :returns: board state ('s' -> success, 'w' -> wrong, 'c' -> unsolvable board)
        :rtype: str
        """
        # Lấy ô được chọn
        r, c = self.__selected
        if self.get_value == 0:
            # Kiểm tra cho trường hợp giá trị pencil khác 0
            pencil = self.get_pencil
            if pencil != 0:
                # Kiểm tra xem số đã chọn có tuân thủ quy tắc sudoku không
                w = self.__solver.exists(self.__board, pencil, (r, c))
                if w:
                    # Thay đổi trạng thái ô sai (màu đỏ)
                    self.__squares[r][c].wrong = True
                    self.__squares[w[0]][w[1]].wrong = True
                    self.__squares[r][c].value = pencil
                    self.__board[r][c] = pencil
                    self.__wrong = w
                    return "w"
                else:
                    # Thay đổi giá trị ô và trả về true
                    self.__squares[r][c].value = pencil
                    self.__board[r][c] = pencil
                    # copy board
                    # Khởi tạo bản sao dưới dạng mảng hai chiều với 9 hàng
                    copy = [[] for r in range(9)]
                    # Lặp qua tất cả các hàng
                    for r in range(9):
                        # Lặp qua tất cả các cột
                        for c in range(9):
                            # Thêm sô vào
                            copy[r].append(self.__board[r][c])
                    # Kiểm tra nếu bàn cơ không được giải
                    if not self.__solver.solve(copy):
                        return "c"
                    return "s"

    @property
    def clear(self):
        """Xóa giá trị ô được chọn"""
        # Lấy ô được chọn
        r, c = self.__selected
        # Xóa giá trị ô và pencil
        self.__squares[r][c].value = 0
        self.__squares[r][c].pencil = 0
        self.__board[r][c] = 0
        # Thay đổi trạng thái sai
        if self.__wrong:
            self.__squares[r][c].wrong = False
            self.__squares[self.__wrong[0]][self.__wrong[1]].wrong = False
            self.__wrong = None

    @property
    def isfinished(self):
        """Trả về True nếu không còn ô trống nào, ngược lại trả về False

        :returns: Trả về True nếu không còn ô nào trống, ngược lại trả về false
        :rtype: bool
        """
        return not self.__solver.nextpos(self.board)

    def set_sq_value(self, value: int, pos: tuple):
        """Thay đổi giá trị ô theo vị trí

        :Tham số value: một giá trị mới cho ô
        :Kiểu value: int
        :Tham số pos: vị trí ô
        :Kiểu pos: tuple
        """
        self.__squares[pos[0]][pos[1]].value = value

    def draw(self):
        """Vẽ bàn cờ trên màn hình"""
        # Vẽ các ô
        # Lặp qua tất cả các dòng
        for r in range(9):
            # Lặp qua tất cả các cột
            for c in range(9):
                # vẽ giá trị ô
                self.__squares[c][r].draw()
        # Vẽ lưới
        # Đặt khoảng trống giữa các ô
        space = self.size[0] // 9
        # Vẽ 10 đường ngang và dọc
        for r in range(10):
            # set line weight (bold at the end of 3*3 area)
            w = 4 if r % 3 == 0 and r != 0 else 1
            # draw horizontal line (screen, (color), (start_pos), (end_pos), width)
            pygame.draw.line(
                self.screen,
                (72, 234, 54),
                (self.size[2], r * space),
                (self.size[0] + self.size[2], r * space),
                w,
            )
            # draw vertical line (screen, (color), (start_pos), (end_pos), width)
            pygame.draw.line(
                self.screen,
                (72, 234, 54),
                (r * space + self.size[2], 0),
                (r * space + self.size[2], self.size[1]),
                w,
            )


class Square(GUIBase):

    """Ô trong bàn cờ

    :Tham số value: số ô hiển thị
    :Kiểu value: int
    :Tham số pos: vị trí ô (dòng, cột)
    :Kiểu pos: tuple
    :Tham số width: độ rộng màn hình và khoảng cách bên trái (rộng, khoảng trống bên trái)
    :Kiểu width: tuple
    :Tham số screen: pygame screen
    :Kiểu screen: pygame.Surface
    :Tham số changeable: changeabllity
    :Kiểu changeable: bool
    """

    def __init__(
        self,
        value: int,
        pos: tuple,
        widthpos: tuple,
        screen: pygame.Surface,
        changeable: bool,
    ):
        super().__init__(0, screen)
        self.__value = value
        self.__pos = pos
        self.__widthpos = widthpos
        self.__pencil = 0
        self.__selected = False
        self.__changeable = changeable
        self.__wrong = False

    @property
    def changeable(self):
        """Thuoc tính changeable (getter)"""
        return self.__changeable

    @property
    def selected(self) -> tuple:
        """Thuộc tính selected (getter)"""
        return self.__selected

    @selected.setter
    def selected(self, v: bool):
        """Thuộc tính selected (setter)

        :Tham số v: giá trị được chọn
        :Kiểu v: bool
        """
        self.__selected = v

    @property
    def value(self) -> int:
        """Thuộc tính value (getter)"""
        return self.__value

    @value.setter
    def value(self, value: int):
        """Thuộc tính value (setter)

        :Tham số value: giá trị ô
        :Kiểu value: int
        """
        if self.__changeable:
            self.__value = value

    @property
    def pencil(self) -> int:
        """Tham số pencil (getter)"""
        return self.__pencil

    @pencil.setter
    def pencil(self, value: int):
        """Thuộc tính pencil (setter)

        :Tham số value: pencil square value
        :Kiểu value: int
        """
        if self.__changeable:
            self.__pencil = value

    @property
    def wrong(self):
        """Thuộc tính wrong (getter)"""
        return self.__wrong

    @wrong.setter
    def wrong(self, w: bool):
        """Thuộc tính wrong (setter)

        :Tham số w: wrong value
        :Kiểu w: bool
        """
        self.__wrong = w

    def draw(self):
        """Draw square value"""
        # Vẽ khoảng trống giữa các ô
        space = self.__widthpos[0] // 9
        # Đặt giá trị ô thực tế trên màn hình
        r, c = self.__pos[0] * space + self.__widthpos[1], self.__pos[1] * space
        # Kiểm tra xem ô có thể thay đổi giá trị Khong
        if not self.__changeable:
            sqsize = self.__widthpos[0] // 9
            # Vẽ khung
            pygame.draw.rect(self.screen, (10, 30, 0), ((r, c), (sqsize, sqsize)))
        # Kiểm tra giá trị ô có khác 0 hay không
        if self.__value != 0:
            font = pygame.font.Font("../assets/Rubik-font/Rubik-Regular.ttf", 38)
            # Đặt màu
            rgb = (72, 234, 54) if not self.__wrong else (234, 72, 54)
            # Tạo ra đối tượng surface
            v = font.render(str(self.__value), 1, rgb)
            # Vẽ trên màn hình
            self.screen.blit(
                v,
                (
                    int(r + ((space / 2) - (v.get_width() / 2))),
                    int(c + ((space / 2) - (v.get_height() / 2))),
                ),
            )
        elif self.__pencil != 0:
            font = pygame.font.Font("../assets/Rubik-font/Rubik-Regular.ttf", 30)
            # Tạo ra đối tượng surface
            v = font.render(str(self.__pencil), 1, (2, 164, 0))
            # Vẽ trên màn hình
            self.screen.blit(
                v,
                (
                    int(r + ((space / 2) - (v.get_width() / 2)) - 20),
                    int(c + ((space / 2) - (v.get_height() / 2)) - 15),
                ),
            )
        # Vễ ô được chọn có viền đậm
        if self.__selected:
            # Vẽ khung
            pygame.draw.rect(self.screen, (52, 214, 34), ((r, c), (space, space)), 3)
