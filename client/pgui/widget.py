import pygame

class Widget:
    """
    Base class for all widgets

    Attributes:
    x ----------------------- x coordinate of the widget
    y ----------------------- y coordinate of the widget
    width ------------------- width of the widget
    height ------------------ height of the widget
    rect -------------------- pygame.Rect object representing the widget
    visible ----------------- boolean indicating if the widget is visible
    
    Methods:
    draw() ------------------ draw the widget on the screen
    handle_event(event) ----- handle the event
    set_visible(visible) ---- set the visibility of the widget
    is_visible() ------------ check if the widget is visible
    get_rect() -------------- get the pygame.Rect object representing the widget
    set_position(x, y) ------ set the position of the widget
    get_position() ---------- get the position of the widget
    set_size(width, height) - set the size of the widget
    get_size() -------------- get the size of the widget

    Dunder methods:
    __contains__(coords) ---- check if the widget contains the given coordinates
    __str__() --------------- return a string representation of the widget
    __repr__() -------------- return a string representation of the widget

    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True

    def __str__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.width}, {self.height})"
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.width}, {self.height})"

    def draw(self, screen):
        raise NotImplementedError

    def handle_event(self, event):
        raise NotImplementedError

    def set_visible(self, visible):
        self.visible = visible

    def is_visible(self):
        return self.visible

    def get_rect(self):
        return self.rect

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def get_position(self):
        return (self.x, self.y)

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.rect.width = width
        self.rect.height = height

    def get_size(self):
        return (self.width, self.height)

    def __contains__(self, coords:tuple):
        return self.rect.collidepoint(*coords)
    


Widget