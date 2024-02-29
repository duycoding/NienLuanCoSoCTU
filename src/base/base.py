import pygame


class GUIBase:

    """Lớp GUI class

    :Tham số size: screen size (width height)
    :Kiểu size: tuple
    :Tham số screen: pygame screen
    :Kiểu screen: pygame.Surface
    """

    def __init__(self, size: tuple, screen: pygame.Surface):
        self.__size = size
        self.__screen = screen

    @property
    def size(self):
        """Thuộc tính size (getter)"""
        return self.__size

    @property
    def screen(self):
        """Thuộc tính screen (getter)"""
        return self.__screen

    def draw(self):
        """Hàm vẽ"""
        pass

    def _type(self, txt: str, rgb: tuple, pos: tuple, fsize: int):
        """Vẽ chuỗi trên màn hình

        :Tham số txt: chữ cần vẽ
        :Kiểu txt: str
        :Tham số rgb: màu chữ
        :Kiểu rgb: tuple
        :Tham sô pos: vị trí để vẽ
        :Kiểu pos: tuple
        :Tham sô fsize: kích cỡ chữ
        :Kiểu fsize: int
        """
        # create font object
        font = pygame.font.Font("../assets/Rubik-font/Rubik-Regular.ttf", fsize)
        # render font object with text
        v = font.render(txt, 1, rgb)
        # draw font obj on the surface
        self.__screen.blit(v, pos)
