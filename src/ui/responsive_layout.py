"""
Responsive Layout System for Neural Network Adventure RPG
Ensures all UI elements are properly sized and positioned for any screen size
"""

import pygame
from typing import Dict, Tuple, List, Optional

class ResponsiveLayout:
    """
    Manages responsive layout for the entire game using flex-like behavior
    Ensures no overlapping elements and proper spacing
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.min_font_size = 14  # Much larger minimum
        self.max_font_size = 48  # Larger maximum
        
        # Define safe margins (percentage of screen)
        self.margin_x = 0.01  # 1% margin on sides
        self.margin_y = 0.01  # 1% margin on top/bottom
        
        # Calculate usable area
        self.usable_width = int(screen_width * (1 - 2 * self.margin_x))
        self.usable_height = int(screen_height * (1 - 2 * self.margin_y))
        self.start_x = int(screen_width * self.margin_x)
        self.start_y = int(screen_height * self.margin_y)
        
        # Much larger spacing between elements
        self.min_spacing = max(15, int(min(screen_width, screen_height) * 0.02))
    
    def get_font_size(self, base_percentage: float, min_size: int = None, max_size: int = None) -> int:
        """
        Calculate responsive font size based on screen height with much larger defaults
        
        Args:
            base_percentage: Percentage of screen height (0.0 to 1.0)
            min_size: Minimum font size (default: self.min_font_size)
            max_size: Maximum font size (default: self.max_font_size)
        """
        if min_size is None:
            min_size = self.min_font_size
        if max_size is None:
            max_size = self.max_font_size
            
        # Make fonts much larger by default
        calculated_size = int(self.screen_height * base_percentage * 1.5)  # 50% larger
        return max(min_size, min(max_size, calculated_size))
    
    def get_rect(self, x_percent: float, y_percent: float, 
                 width_percent: float, height_percent: float,
                 min_width: int = 50, min_height: int = 30) -> pygame.Rect:
        """
        Create a responsive rectangle based on percentages of usable area
        
        Args:
            x_percent: X position as percentage of usable width (0.0 to 1.0)
            y_percent: Y position as percentage of usable height (0.0 to 1.0)
            width_percent: Width as percentage of usable width (0.0 to 1.0)
            height_percent: Height as percentage of usable height (0.0 to 1.0)
            min_width: Minimum width in pixels
            min_height: Minimum height in pixels
        """
        x = self.start_x + int(self.usable_width * x_percent)
        y = self.start_y + int(self.usable_height * y_percent)
        width = max(min_width, int(self.usable_width * width_percent))
        height = max(min_height, int(self.usable_height * height_percent))
        
        return pygame.Rect(x, y, width, height)
    
    def get_centered_rect(self, width_percent: float, height_percent: float,
                         y_percent: float = 0.5, min_width: int = 50, min_height: int = 30) -> pygame.Rect:
        """
        Create a centered rectangle
        
        Args:
            width_percent: Width as percentage of usable width
            height_percent: Height as percentage of usable height
            y_percent: Y center position as percentage of usable height
            min_width: Minimum width in pixels
            min_height: Minimum height in pixels
        """
        width = max(min_width, int(self.usable_width * width_percent))
        height = max(min_height, int(self.usable_height * height_percent))
        
        x = self.start_x + (self.usable_width - width) // 2
        y = self.start_y + int(self.usable_height * y_percent) - height // 2
        
        return pygame.Rect(x, y, width, height)
    
    def create_grid_layout(self, container_rect: pygame.Rect, rows: int, cols: int, 
                          spacing: int = None) -> List[List[pygame.Rect]]:
        """
        Create a responsive grid layout within a container
        
        Args:
            container_rect: Container rectangle to divide
            rows: Number of rows
            cols: Number of columns
            spacing: Spacing between grid items (auto-calculated if None)
        
        Returns:
            2D list of rectangles [row][col]
        """
        if spacing is None:
            spacing = self.min_spacing
        
        # Calculate available space after spacing
        available_width = container_rect.width - (cols - 1) * spacing
        available_height = container_rect.height - (rows - 1) * spacing
        
        # Calculate cell dimensions
        cell_width = available_width // cols
        cell_height = available_height // rows
        
        grid = []
        for row in range(rows):
            grid_row = []
            for col in range(cols):
                x = container_rect.x + col * (cell_width + spacing)
                y = container_rect.y + row * (cell_height + spacing)
                grid_row.append(pygame.Rect(x, y, cell_width, cell_height))
            grid.append(grid_row)
        
        return grid
    
    def distribute_horizontally(self, container_rect: pygame.Rect, count: int, 
                              spacing: int = None) -> List[pygame.Rect]:
        """
        Distribute rectangles horizontally within a container with equal spacing
        
        Args:
            container_rect: Container rectangle
            count: Number of rectangles
            spacing: Spacing between rectangles (auto-calculated if None)
        """
        if spacing is None:
            spacing = self.min_spacing
        
        # Calculate available space after spacing
        available_width = container_rect.width - (count - 1) * spacing
        rect_width = available_width // count
        
        rects = []
        for i in range(count):
            x = container_rect.x + i * (rect_width + spacing)
            rects.append(pygame.Rect(x, container_rect.y, rect_width, container_rect.height))
        
        return rects
    
    def distribute_vertically(self, container_rect: pygame.Rect, count: int, 
                            spacing: int = None) -> List[pygame.Rect]:
        """
        Distribute rectangles vertically within a container with equal spacing
        
        Args:
            container_rect: Container rectangle
            count: Number of rectangles
            spacing: Spacing between rectangles (auto-calculated if None)
        """
        if spacing is None:
            spacing = self.min_spacing
        
        # Calculate available space after spacing
        available_height = container_rect.height - (count - 1) * spacing
        rect_height = available_height // count
        
        rects = []
        for i in range(count):
            y = container_rect.y + i * (rect_height + spacing)
            rects.append(pygame.Rect(container_rect.x, y, container_rect.width, rect_height))
        
        return rects
    
    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """
        Wrap text to fit within specified width
        
        Args:
            text: Text to wrap
            font: Font to use for measuring
            max_width: Maximum width in pixels
        
        Returns:
            List of text lines that fit within max_width
        """
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word is too long, force it
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def render_text_block(self, screen: pygame.Surface, text: str, font: pygame.font.Font,
                         rect: pygame.Rect, color: Tuple[int, int, int],
                         align: str = "left", vertical_align: str = "top") -> None:
        """
        Render text block with proper wrapping and alignment
        
        Args:
            screen: Surface to render on
            text: Text to render
            font: Font to use
            rect: Rectangle to render within
            color: Text color
            align: Horizontal alignment ("left", "center", "right")
            vertical_align: Vertical alignment ("top", "center", "bottom")
        """
        lines = self.wrap_text(text, font, rect.width - 10)  # 5px padding on each side
        line_height = font.get_height() + 2
        
        total_height = len(lines) * line_height
        
        # Calculate starting Y position based on vertical alignment
        if vertical_align == "center":
            start_y = rect.y + (rect.height - total_height) // 2
        elif vertical_align == "bottom":
            start_y = rect.bottom - total_height - 5
        else:  # top
            start_y = rect.y + 5
        
        for i, line in enumerate(lines):
            if start_y + i * line_height > rect.bottom - line_height:
                break  # Don't render lines that would overflow
            
            line_surface = font.render(line, True, color)
            
            # Calculate X position based on alignment
            if align == "center":
                x = rect.centerx - line_surface.get_width() // 2
            elif align == "right":
                x = rect.right - line_surface.get_width() - 5
            else:  # left
                x = rect.x + 5
            
            screen.blit(line_surface, (x, start_y + i * line_height))
    
    def create_flex_layout(self, phase: str) -> Dict[str, pygame.Rect]:
        """
        Create a flex-like layout that prevents overlapping and ensures proper spacing
        
        Args:
            phase: Current game phase ("briefing", "investigating", "boss_fight", "victory")
        
        Returns:
            Dictionary of area names to rectangles
        """
        areas = {}
        current_y = self.start_y
        
        # Calculate minimum heights based on content needs
        title_height = max(30, int(self.usable_height * 0.06))
        progress_height = max(25, int(self.usable_height * 0.05))
        dialogue_min_height = max(80, int(self.usable_height * 0.15))
        controls_height = max(60, int(self.usable_height * 0.08))
        
        if phase == "boss_fight":
            # Compact layout for boss fight
            boss_header_height = max(40, int(self.usable_height * 0.08))
            
            # Title
            areas["title"] = pygame.Rect(self.start_x, current_y, self.usable_width, title_height)
            current_y += title_height + self.min_spacing
            
            # Boss header
            areas["boss_header"] = pygame.Rect(self.start_x, current_y, self.usable_width, boss_header_height)
            current_y += boss_header_height + self.min_spacing
            
            # Calculate remaining space for main content and dialogue
            remaining_height = (self.start_y + self.usable_height) - current_y - controls_height - dialogue_min_height - (2 * self.min_spacing)
            main_content_height = max(200, int(remaining_height * 0.7))
            
            # Main content
            areas["main_content"] = pygame.Rect(self.start_x, current_y, self.usable_width, main_content_height)
            current_y += main_content_height + self.min_spacing
            
            # Controls
            areas["controls"] = pygame.Rect(self.start_x, current_y, self.usable_width, controls_height)
            current_y += controls_height + self.min_spacing
            
            # Dialogue (remaining space)
            dialogue_height = (self.start_y + self.usable_height) - current_y
            areas["dialogue"] = pygame.Rect(self.start_x, current_y, self.usable_width, dialogue_height)
            
        elif phase == "briefing":
            # Briefing layout with more space for content
            
            # Title
            areas["title"] = pygame.Rect(self.start_x, current_y, self.usable_width, title_height)
            current_y += title_height + self.min_spacing
            
            # Progress
            areas["progress"] = pygame.Rect(self.start_x, current_y, self.usable_width, progress_height)
            current_y += progress_height + self.min_spacing
            
            # Calculate remaining space
            remaining_height = (self.start_y + self.usable_height) - current_y - dialogue_min_height - self.min_spacing
            main_content_height = max(300, remaining_height - dialogue_min_height)
            
            # Main content
            areas["main_content"] = pygame.Rect(self.start_x, current_y, self.usable_width, main_content_height)
            current_y += main_content_height + self.min_spacing
            
            # Dialogue (remaining space)
            dialogue_height = (self.start_y + self.usable_height) - current_y
            areas["dialogue"] = pygame.Rect(self.start_x, current_y, self.usable_width, dialogue_height)
            
        else:
            # Standard layout for investigating and victory - much more generous spacing
            
            # Title - larger
            title_height = max(40, int(self.usable_height * 0.08))
            areas["title"] = pygame.Rect(self.start_x, current_y, self.usable_width, title_height)
            current_y += title_height + self.min_spacing
            
            # Progress - larger
            progress_height = max(35, int(self.usable_height * 0.06))
            areas["progress"] = pygame.Rect(self.start_x, current_y, self.usable_width, progress_height)
            current_y += progress_height + self.min_spacing
            
            # Calculate remaining space - give more to main content
            controls_height = max(80, int(self.usable_height * 0.12))
            dialogue_min_height = max(100, int(self.usable_height * 0.18))
            
            remaining_height = (self.start_y + self.usable_height) - current_y - controls_height - dialogue_min_height - (2 * self.min_spacing)
            main_content_height = max(300, remaining_height)
            
            # Main content - much larger
            areas["main_content"] = pygame.Rect(self.start_x, current_y, self.usable_width, main_content_height)
            current_y += main_content_height + self.min_spacing
            
            # Controls - larger
            areas["controls"] = pygame.Rect(self.start_x, current_y, self.usable_width, controls_height)
            current_y += controls_height + self.min_spacing
            
            # Dialogue - remaining space, but ensure minimum
            dialogue_height = max(dialogue_min_height, (self.start_y + self.usable_height) - current_y)
            areas["dialogue"] = pygame.Rect(self.start_x, current_y, self.usable_width, dialogue_height)
        
        return areas
    
    def create_layout_areas(self, phase: str) -> Dict[str, pygame.Rect]:
        """Backward compatibility wrapper"""
        return self.create_flex_layout(phase)

class ResponsiveButton:
    """A button that scales with screen size"""
    
    def __init__(self, layout: ResponsiveLayout, x_percent: float, y_percent: float,
                 width_percent: float, height_percent: float, text: str,
                 font_size_percent: float = 0.025):
        self.layout = layout
        self.rect = layout.get_rect(x_percent, y_percent, width_percent, height_percent)
        self.text = text
        self.font_size = layout.get_font_size(font_size_percent)
        self.font = pygame.font.Font(None, self.font_size)
        
        self.bg_color = (70, 130, 180)
        self.hover_color = (100, 149, 237)
        self.text_color = (255, 255, 255)
        self.border_color = (255, 255, 255)
        
        self.is_hovered = False
        self.is_pressed = False
    
    def handle_event(self, event) -> bool:
        """Handle mouse events, returns True if clicked"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                return True
            self.is_pressed = False
        
        return False
    
    def render(self, screen: pygame.Surface):
        """Render the button"""
        # Choose color based on state
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # Draw button background
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=8)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class ResponsiveSlider:
    """A slider that scales with screen size"""
    
    def __init__(self, layout: ResponsiveLayout, rect: pygame.Rect, 
                 label: str, min_val: float = -1.0, max_val: float = 1.0, initial_val: float = 0.0):
        self.layout = layout
        self.rect = rect
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        
        self.bg_color = (60, 60, 60)
        self.fill_color = (100, 255, 100)
        self.handle_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        
        self.font_size = layout.get_font_size(0.02, min_size=10, max_size=16)
        self.font = pygame.font.Font(None, self.font_size)
    
    def handle_event(self, event) -> bool:
        """Handle mouse events, returns True if value changed"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_value_from_mouse(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value_from_mouse(event.pos[0])
            return True
        
        return False
    
    def _update_value_from_mouse(self, mouse_x: int):
        """Update slider value based on mouse position"""
        relative_x = mouse_x - self.rect.x
        relative_x = max(0, min(self.rect.width, relative_x))
        
        # Convert to value range
        ratio = relative_x / self.rect.width
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
    
    def render(self, screen: pygame.Surface):
        """Render the slider"""
        # Draw background
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=4)
        
        # Draw fill
        fill_ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        fill_width = int(self.rect.width * fill_ratio)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            color = self.fill_color if self.value >= 0 else (255, 100, 100)
            pygame.draw.rect(screen, color, fill_rect, border_radius=4)
        
        # Draw border
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2, border_radius=4)
        
        # Draw handle
        handle_x = self.rect.x + int(fill_ratio * self.rect.width) - 4
        handle_rect = pygame.Rect(handle_x, self.rect.y - 2, 8, self.rect.height + 4)
        pygame.draw.rect(screen, self.handle_color, handle_rect, border_radius=2)
        
        # Draw label above
        label_surface = self.font.render(self.label, True, self.text_color)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 22))
        
        # Draw value below
        value_text = f"{self.value:.2f}"
        value_surface = self.font.render(value_text, True, (200, 200, 200))
        value_rect = value_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 12))
        screen.blit(value_surface, value_rect)