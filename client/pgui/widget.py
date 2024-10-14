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
    

class Button(Widget):
    def __init__(self, x, y, width, height, text, action, font:str="Calibri", font_color:tuple[int]=(0, 0, 0), bg_color:tuple[int]=(88, 88, 88), outline_color:tuple[int]=(0, 0, 0), font_size:int=30):
        super().__init__(x, y, width, height)
        self.text = text
        self.font = font
        self.font_color = font_color
        self.bg_color = bg_color
        self.action = action
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(font, font_size)
        self.font_size = font_size
        self.outline_color = outline_color
        
    def draw(self, screen):
        if self.visible:
            color = self.bg_color
            if self.rect.collidepoint(*pygame.mouse.get_pos()):
                color = (color[0] + 50, color[1] + 50, color[2] + 50)
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, self.outline_color, self.rect, 2)
            text = self.font.render(self.text, True, self.font_color)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)
    
    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(*event.pos):
                    self.action()
        