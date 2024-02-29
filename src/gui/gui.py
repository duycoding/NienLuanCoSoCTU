import pygame, time

# local import
from models.board import Board
from models.left_panel import LeftPanel
from solver.solver import Solver
from generator.generator import Generator


class GUI:

    """Giao diện đồ họa người dùng (GUI) cho trình giải Sudoku

    :Tham số screen_size: kích thước màn hình
    :Kiểu screen_size: tuple
    """

    def __init__(self):
        # đặt kích thước màn hình chính trong Pygame
        self.__screen_size = (1000, 720)
        self.__screen = pygame.display.set_mode(self.__screen_size[:2])
        # hay đổi biểu tượng hiển thị
        pygame.display.set_icon(pygame.image.load("../assets/icon.png"))
        self.__generator = Generator()
        self.__board = self.__generator.generate()
        # Tạo ra đối tượng bảng
        self.__board_model = Board(self.__screen_size, self.__board, self.__screen)
        # Tạo ra đối tượng solver
        self.__solver = Solver(self.__board_model, 500)
        # tạo ra panel bên trái
        self.__left_panel = LeftPanel(self.__solver, self.__screen_size, self.__screen)
        # Gắn tiêu đề
        pygame.display.set_caption("Sudoku")

    def __refresh(self):
        """Vẽ lại màn hình và hiển thị nó"""
        # Set màu nền là màu đen
        self.__screen.fill((0, 0, 0))
        # vẽ lại bảng
        self.__board_model.draw()
        # vẽ lại panel bên trái
        self.__left_panel.draw()
        # cập nhật màn hình
        pygame.display.update()
        # reset lại kiểu nút
        # reset lại nút auto solver
        for b in self.__left_panel.auto_solver.buttons:
            b.reset
        # reset lại nút tùy chọn
        for b in self.__left_panel.options.buttons:
            b.reset

    def loop(self):
        """Vòng lặp pygame chính"""
        jump_mode = False
        # chạy vòng lặp pygame chính
        while True:
            # lắng nghe các sự kiện
            for e in pygame.event.get():
                    # sự kiện nút đóng cửa sổ
                if e.type == pygame.QUIT:
                    return
                # sự kiện chọn ô vuông bằng chuột
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.__select_by_mouse()
                    self.__auto_solver_buttons_mouse()
                    self.__options_buttons_mouse()
                # sự kiện gắn giá trị và xóa
                elif e.type == pygame.KEYDOWN:
                    # ngăn chặn tất cả sự kiện đang diễn ra khi người chơi thua/thắng
                    if (
                        not self.__left_panel.gamesystem.lost
                        and not self.__left_panel.gamesystem.won
                    ):
                        # đặt và xóa giá trị ô vuông bằng các phím
                        self.__set_del_value_by_key(e)
                        # thay đổi ô vuông được chọn bằng các phím mũi tên
                        self.__select_by_arrows(
                            e, self.__board_model.selected, jump_mode
                        )
                    # phím tắt thoát
                    if e.key == pygame.K_q:
                        return
                    # phím tắt chế độ di chuyển nhanh
                    elif e.key == pygame.K_j:
                        jump_mode = not jump_mode
            # cập nhật màn hình
            self.__refresh()

    def __select_by_mouse(self):
        """Select board square by MOUSEBUTTONDOWN event"""
        # Lấy vị trí click chuột
        p = pygame.mouse.get_pos()
        # tính toán ô vuông (hàng, cột) từ vị trí chuột
        left_space = self.__screen_size[0] - self.__screen_size[1]
        if p[0] > left_space:
            self.__board_model.selected = (
                p[1] // (self.__screen_size[1] // 9),
                (p[0] - left_space) // (self.__screen_size[1] // 9),
            )

    def __auto_solver_buttons_mouse(self):
        """Sự kiện của nút """
        # lấy vị trí click chuột
        p = pygame.mouse.get_pos()
        # lặp lại tất cả các nút giải quyết tự động
        for b in self.__left_panel.auto_solver.buttons:
            # kiểm tra xem vị trí có khớp với phạm vi nhấp chuột không
            if p[0] in b.click_range[0] and p[1] in b.click_range[1]:
                # gọi sự kiện click
                b.click()

    def __options_buttons_mouse(self):
        """Sự kiện nút"""
        # lấy vị trí click chuột
        p = pygame.mouse.get_pos()
        s = True
        # lặp lại tất cả các nút tùy chọn
        for b in self.__left_panel.options.buttons:
            # kiểm tra xem vị trí có khớp với phạm vi nhấp chuột không
            if p[0] in b.click_range[0] and p[1] in b.click_range[1]:
                # gọi sự kiện click
                if b.innertxt == "selected":
                    # sao chép bảng
                    # Khởi tạo bản sao dưới dạng mảng hai chiều có 9 dòng
                    copy = [[] for r in range(9)]
                    # Lặp qua tất cả các dòng
                    for r in range(9):
                        # Lặp qua tất cả các cột
                        for c in range(9):
                            # Thêm số vào
                            copy[r].append(self.__board_model.board[r][c])
                    s = b.click((copy, self.__board_model.selected))
                elif b.innertxt == "generate":
                    # Đặt lại số trận thắng/trận thua/số lần đoán sai
                    self.__left_panel.gamesystem.reset()
                    # Đặt lại thời gian
                    self.__left_panel.time.init_time = time.time()
                    # Đặt lại gợi ý
                    self.__left_panel.hints.hint = "everything is well"
                    s = b.click((self.__board_model,))
                elif b.innertxt == "reset":
                    # Đặt lại số trận thắng/trận thua/số lần đoán sai
                    self.__left_panel.gamesystem.reset()
                    # Đặt lại thời gian
                    self.__left_panel.time.init_time = time.time()
                    # Đặt lại gợi ý
                    self.__left_panel.hints.hint = "everything is well"
                    s = b.click()
                else:
                    s = b.click()
        # Kiểm tra trường hợp không thể giải
        if not s:
            self.__left_panel.hints.hint = "unsolvable board"

    def __set_del_value_by_key(self, e: pygame.event.Event):
        """Đặt và xóa giá trị ô vuông bằng sự kiện pygame.KEYDOWN


        :Tham số e: pygame event
        :Kiểu e: pygame.event.Event
        """
        v = 0
        # Phím xóa / backspace
        if e.key == pygame.K_BACKSPACE or e.key == pygame.K_DELETE:
            # Xóa mục được chọn
            self.__board_model.clear
            # Đặt lại gợi ý
            self.__left_panel.hints.hint = "everything is well"
        # Phím trả về / enter
        elif e.key == pygame.K_RETURN:
            issuccess = self.__board_model.set_value()
            if issuccess == "s":
                # Kiểm tra xem người chơi đã giải bảng chưa
                if self.__board_model.isfinished:
                    self.__left_panel.gamesystem.won = True
            elif issuccess == "w":
                # Tăng sô lần đoán sai
                self.__left_panel.gamesystem.wrongs_counter
                # Đặt lại gợi ý
                self.__left_panel.hints.hint = "press delete"
            elif issuccess == "c":
                # Đặt lại gợi ý
                self.__left_panel.hints.hint = "unsolvable board"
        # pencil 1-9
        elif e.key == pygame.K_1:
            v = 1
        elif e.key == pygame.K_2:
            v = 2
        elif e.key == pygame.K_3:
            v = 3
        elif e.key == pygame.K_4:
            v = 4
        elif e.key == pygame.K_5:
            v = 5
        elif e.key == pygame.K_6:
            v = 6
        elif e.key == pygame.K_7:
            v = 7
        elif e.key == pygame.K_8:
            v = 8
        elif e.key == pygame.K_9:
            v = 9
        if 0 < v < 10:
            self.__board_model.set_pencil(v)

    def __select_by_arrows(self, e: pygame.event.Event, pos: tuple, jump_mode: bool):
        """Thay đổi ô vuông được chọn bằng các phím mũi tên

        :Tham số e: pygame event
        :Kiểu e: pygame.event.Event
        :Tham số pos: Vị trí hiện tại
        :Kiểu pos: tuple
        :Tham số jump_mode: Nếu đúng, sự chọn sẽ di chuyển đến vị trí trống tiếp theo
        :Kiểu jump_mode: bool
        """
        # Đặt giá trị thay đổi hàng, cột
        r, c = 0, 0
        if e.key == pygame.K_UP or e.key == pygame.K_w:
            r = -1
        elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
            r = 1
        elif e.key == pygame.K_RIGHT or e.key == pygame.K_d:
            c = 1
        elif e.key == pygame.K_LEFT or e.key == pygame.K_a:
            c = -1
        # Kiểm tra xem có ô vuông được chọn hay không
        if pos:
            if jump_mode:
                # Tìm vị trí trống tiếp theo theo cùng một hướng
                while -1 < pos[0] + r < 9 and -1 < pos[1] + c < 9 and r + c != 0:
                    pos = (pos[0] + r, pos[1] + c)
                    if self.__board_model.board[pos[0]][pos[1]] == 0:
                        break
                # Chỉ di chuyển nếu vị trí tiếp theo là trống -(xử lý trường hợp biên trước đó)
                if self.__board_model.board[pos[0]][pos[1]] == 0:
                    self.__board_model.selected = pos
            else:
                # Di chuyển đến vị trí tiếp theo
                pos = (pos[0] + r, pos[1] + c)
                if -1 < pos[0] < 9 and -1 < pos[1] < 9:
                    self.__board_model.selected = pos
