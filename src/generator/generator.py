from random import randint

# local import
try:
    from solver.solver import Solver
except ImportError:
    # for tests purposes
    from src.solver.solver import Solver


class Generator:

    """Trình tạo bảng Sudoku hợp lệ ngẫu nhiên"""

    def __init__(self):
        self.__solver = Solver()

    def generate(self) -> list:
        """Tạo bảng Sudoku hợp lệ ngẫu nhiên

        :Trả về: bảng Sudoku hợp lệ
        :Kiểu trả về: list
        """
        # điền vào vị trí ngẫu nhiên với giá trị ngẫu nhiên
        b = [[0 for r in range(9)] for c in range(9)]
        b[randint(0, 8)][randint(0, 8)] = randint(1, 9)
        # 40%(32) đến 60%(48) ô trống (giá trị ngẫu nhiên)
        unempty = randint(32, 48)
        # danh sách vị trí ngẫu nhiên
        ranpos = []
        # nhận vị trí ngẫu nhiên
        counter = 0
        while counter <= unempty:
            # lấy hàng ngẫu nhiên và cột ngẫu nhiên
            r, c = randint(0, 8), randint(0, 8)
            # kiểm tra các giá trị lặp lại
            if (r, c) not in ranpos:
                ranpos.append((r, c))
                counter += 1
        # giải quyết bảng
        self.__solver.solve(b)
        # áp dụng giải pháp ở các vị trí ngẫu nhiên
        b2 = [[] for i in range(9)]
        # lặp lại các hàng tổng thể
        for r in range(9):
            # lặp lại các cột tổng thể
            for c in range(9):
                # kiểm tra xem vị trí (r, c) trong danh sách vị trí ngẫu nhiên
                if (r, c) in ranpos:
                    b2[r].append(b[r][c])
                else:
                    b2[r].append(0)
        return b2
