from threading import Thread, ThreadError


class Threads:

    """Quản lý các luồng"""

    def __init__(self):
        self.__threads = []

    def start(self, func, _args_: list = []) -> bool:
        """Tạo một luồng mới và sử dụng nó

        :Tham số function: Hàm mục tiêu để bắt đầu
        :Kiểu func: function
        :Tham số _args_: func arguments (default => [])
        :Kiểu _args_: list (optional)
        :Kiểu trả về: true nếu luồng bắt đầu và ngược lại
        :Kiểu trả về: bool
        """
        try:
            # Tạo một đối tượng luồng
            process = Thread(target=func, args=_args_, daemon=True)
            # Bắt đầu luồng
            process.start()
            # nối luồng vào danh sách luồng
            self.__threads.append(process)
            return True
        except (ThreadError, RuntimeError) as threadStartEX:
            try:
                # đừng luồng nếu nó đang chạy
                process.join()
            except RuntimeError:
                pass
            print(f"Thread start Error: {threadStartEX}")
            return False

    def stop(self) -> bool:
        """Dừng tất cả các luồng trong danh sách

        :Trả về: true nếu luồng bị dừng hoặc gược lại:
        :Kiểu trả về: bool
        """
        try:
            # Lặp qua danh sách self.__threads
            for process in self.__threads:
                # dừng luồng
                process.join(1)
            # Xóa danh sách
            self.__threads.clear()
            return True
        except (ThreadError, RuntimeError) as threadStopEX:
            print(f"Thread stop Error: {threadStopEX}")
            return False
