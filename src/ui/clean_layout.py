"""
Clean, readable layout system focused on large text and simple design
"""

import pygame
from typing import Dict, Tuple, List

class CleanLayout:
    """
    Simple, clean layout system with large, readable text
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Large, readable font sizes
        self.title_size = max(32, int(screen_height * 0.06))
        self.header_size = max(24, int(screen_height * 0.04))
        self.body_size = max(18, int(screen_height * 0.03))
        self.small_size = max(16, int(screen_height * 0.025))
        
        # Generous margins and spacing
        self.margin = max(20, int(min(screen_width, screen_height) * 0.03))
        self.spacing = max(15, int(min(screen_width, screen_height) * 0.02))
        
        # Usable area
        self.content_width = screen_width - 2 * self.margin
        self.content_height = screen_height - 2 * self.margin
        self.content_x = self.margin
        self.content_y = self.margin
    
    def create_simple_layout(self) -> Dict[str, pygame.Rect]:
        """
        Create a simple, clean layout with large sections
        """
        areas = {}
        current_y = self.content_y
        
        # Title area - large and prominent
        title_height = max(60, int(self.content_height * 0.1))
        areas["title"] = pygame.Rect(self.content_x, current_y, self.content_width, title_height)
        current_y += title_height + self.spacing
        
        # Main game area - takes most of the space
        main_height = int(self.content_height * 0.65)
        areas["main"] = pygame.Rect(self.content_x, current_y, self.content_width, main_height)
        current_y += main_height + self.spacing
        
        # Controls area - medium size
        controls_height = max(80, int(self.content_height * 0.12))
        areas["controls"] = pygame.Rect(self.content_x, current_y, self.content_width, controls_height)
        current_y += controls_height + self.spacing
        
        # Dialogue area - remaining space
        dialogue_height = (self.content_y + self.content_height) - current_y
        areas["dialogue"] = pygame.Rect(self.content_x, current_y, self.content_width, dialogue_height)
        
        return areas
    
    def split_horizontal(self, rect: pygame.Rect, parts: int) -> List[pygame.Rect]:
        """
        Split a rectangle horizontally into equal parts with spacing
        """
        if parts <= 0:
            return []
        
        total_spacing = (parts - 1) * self.spacing
        available_width = rect.width - total_spacing
        part_width = available_width // parts
        
        rects = []
        for i in range(parts):
            x = rect.x + i * (part_width + self.spacing)
            rects.append(pygame.Rect(x, rect.y, part_width, rect.height))
        
        return rects
    
    def render_text(self, surface: pygame.Surface, text: str, rect: pygame.Rect, 
                   font_size: int, color: Tuple[int, int, int] = (255, 255, 255),
                   align: str = "center") -> None:
        """
        Render text with automatic wrapping and alignment
        """
        font = pygame.font.Font(None, font_size)
        words = text.split(' ')
        lines = []
        current_line = []
        
        # Word wrap
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= rect.width - 20:  # 10px padding each side
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Force long words
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Render lines
        line_height = font.get_height() + 5
        total_height = len(lines) * line_height
        
        # Vertical centering
        start_y = rect.y + (rect.height - total_height) // 2
        
        for i, line in enumerate(lines):
            if start_y + i * line_height > rect.bottom - line_height:
                break  # Don't overflow
            
            text_surface = font.render(line, True, color)
            
            # Horizontal alignment
            if align == "center":
                x = rect.centerx - text_surface.get_width() // 2
            elif align == "right":
                x = rect.right - text_surface.get_width() - 10
            else:  # left
                x = rect.x + 10
            
            surface.blit(text_surface, (x, start_y + i * line_height))
    
    def draw_panel(self, surface: pygame.Surface, rect: pygame.Rect, 
                   bg_color: Tuple[int, int, int] = (30, 40, 60),
                   border_color: Tuple[int, int, int] = (100, 150, 200),
                   border_width: int = 2) -> None:
        """
        Draw a clean panel with background and border
        """
        pygame.draw.rect(surface, bg_color, rect, border_radius=8)
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=8)