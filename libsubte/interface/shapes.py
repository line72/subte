#
# Copyright (C) 2012 - Marcus Dillavou
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

from gi.repository import Clutter, Cogl, GObject


class Shape(Clutter.Actor):
    '''
    This is based on pyclutter-widgets
    Shape class
    http://code.google.com/p/pyclutter-widgets
    '''

    """Base abstract class to create custom shapes.
    A shape can be filled with a color or a texture,
    and emit the 'clicked' signal when mouse button is released on it.
    """
    __gtype_name__ = 'Shape'
    __gproperties__ = {
        'color' : ( \
            str, 'color', 'Color', None, GObject.PARAM_READWRITE \
                ),
        'texture' : ( \
            str, 'texture', 'Texture', None, GObject.PARAM_READWRITE \
                ),
        }
    __gsignals__ = {
        'clicked' : ( \
            GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, () \
                ),
        }
    
    def __init__ (self, texture=None, color=None):
        Clutter.Actor.__init__(self)
        self._color = Clutter.Color()
        self._color.from_string(color or 'White')
        self._outline_color = Clutter.Color()
        self._outline_color.from_string('Black')
        self._texture = texture
        self._is_pressed = False
        self._has_shadow = False
        self._has_outline = False
        self.connect('button-press-event', self.do_button_press_event)
        self.connect('button-release-event', self.do_button_release_event)
        self.connect('leave-event', self.do_leave_event)
        
    def set_color(self, color):
        """Fill the shape with the color given in parameter.
        color may be a Clutter.Color object or a string representing
        the color name.
        """
        if isinstance(color, Clutter.Color):
            self._color = color
        else:
            self._color = Clutter.Color()
            self._color.from_string(color)
            
    def set_texture(self, image):
        """Fill the shape with a texture given in parameter.
        image may be a Clutter.Texture object or a string
        representing the texture file path.
        """
        if isinstance(image, Clutter.Texture):
            self._texture = image
        else:
            self._texture = Clutter.Texture.new_from_file(image)

    def set_has_shadow(self, shadow):
        self._has_shadow = shadow

    def set_has_outline(self, outline):
        self._has_outline = outline

    def set_outline_color(self, color):
        if isinstance(color, Clutter.Color):
            self._outline_color = color
        else:
            self._outline_color = Clutter.Color()
            self._outline_color.from_string(color)
            
    def do_set_property (self, pspec, value):
        if pspec.name == 'color':
            self._color = self.set_color(value)
        elif pspec.name == 'texture':
            self._color = Clutter.Texture.new_from_file(value)
        elif pspec.name == 'shadow':
            self.set_has_shadow(value)
        elif pspec.name == 'outline':
            self.set_has_outline(value)
        elif pspec.name == 'outline_color':
            self.set_outline_color(value)
        else:
            raise TypeError('Unknown property ' + pspec.name)
        
    def do_get_property (self, pspec):
        if pspec.name == 'color':
            return self._color
        elif pspec.name == 'texture':
            return self._texture
        elif pspec.name == 'shadow':
            return self._has_shadow
        elif pspec.name == 'outline':
            return self._has_outline
        elif pspec.name == 'outline_color':
            return self._outline_color
        else:
            raise TypeError('Unknown property ' + pspec.name)
        
    def do_button_press_event (self, actor, event):
        if event.button == 1:
            self._is_pressed = True
            Clutter.grab_pointer(self)
            return True
        else:
            return False
        
    def do_button_release_event (self, actor, event):
        if event.button == 1 and self._is_pressed == True:
            self._is_pressed = False
            Clutter.ungrab_pointer()
            self.emit('clicked')
            return True
        else:
            return False
        
    def do_leave_event (self, actor, event):
        if self._is_pressed == True:
            self._is_pressed = False
            Clutter.ungrab_pointer()
            return True
        else:
            return False
        
    def do_draw_shape(self, width, height):
        pass
    
    def do_draw_shadow(self, width, height):
        pass

    def do_draw_outline(self, width, height):
        pass

    def __draw_shape(self, width, height, color=None, texture=None):
        if texture:
            Cogl.set_source_texture(texture)
        else:
            tmp_alpha = self.get_paint_opacity() * color.alpha / 255
            Cogl.set_source_color4ub(color.red, color.green, color.blue, tmp_alpha)
        self.do_draw_shape(width, height)
        Cogl.path_fill()

    def __draw_shadow(self, width, height):
        Cogl.set_source_color4ub(0x0e, 0x0e, 0x0e, 0xbe)
        self.do_draw_shadow(width, height)
        Cogl.path_fill()

    def __draw_outline(self, width, height, color=None):
        tmp_alpha = self.get_paint_opacity() * color.alpha / 255
        Cogl.set_source_color4ub(color.red, color.green, color.blue, tmp_alpha)
        self.do_draw_outline(width, height)
        Cogl.path_stroke()
        
    def do_paint (self):
        box = self.get_allocation_box()
        
        if self._has_shadow:
            self.__draw_shadow(box.x2 - box.x1, box.y2 - box.y1)

        if self._texture:
            #self.__draw_shape(box.x2 - box.x1, box.y2 - box.y1, texture = self._texture.get_cogl_texture())
            self.__draw_shape(box.x2 - box.x1, box.y2 - box.y1, self._color, texture = self._texture.get_cogl_texture())
        else:
            self._color.alpha = self.get_paint_opacity()
            self.__draw_shape(box.x2 - box.x1, box.y2 - box.y1, color = self._color)

        if self._has_outline:
            self.__draw_outline(box.x2 - box.x1, box.y2 - box.y1, self._outline_color)

    def do_pick (self, pick_color):
        if self.should_pick_paint() == False:
            return
        
        (x1, y1, x2, y2) = self.get_allocation_box()
        self.__draw_shape(x2 - x1, y2 - y1, pick_color)
        
    def do_clicked (self):
        print "Clicked!"
        
    def do_destroy(self):
        self.unparent()
        
class Bubble(Shape):
    __gtype_name__ = 'Bubble'

    def do_draw_shape(self, width, height):
        w = width / 5
        h = 35

        Cogl.path_move_to((width / 2) + (w / 3.), height - h)
        Cogl.path_line_to(0, height - h)
        Cogl.path_line_to(0, 0)
        Cogl.path_line_to(width, 0)
        Cogl.path_line_to(width, height - h)
        Cogl.path_line_to((width / 2) + (w / 3. * 4), height - h)
        Cogl.path_line_to(width / 2, height)
        Cogl.path_line_to((width / 2) + (w / 3.), height - h)
        Cogl.path_close()

    def do_draw_shadow(self, width, height):
        w = width / 5
        h = 35

        offset_x = 15
        offset_y = 15

        Cogl.path_move_to((width / 2) + (w / 3.) + offset_x, height - h + offset_y)
        Cogl.path_line_to(0 + offset_x, height - h + offset_y)
        Cogl.path_line_to(0 + offset_x, 0 + offset_y)
        Cogl.path_line_to(width + offset_x, 0 + offset_y)
        Cogl.path_line_to(width + offset_x, height - h + offset_y)
        Cogl.path_line_to((width / 2) + (w / 3. * 4) + offset_x, height - h + offset_y)
        Cogl.path_line_to(width / 2 + offset_x, height + offset_y)
        Cogl.path_line_to((width / 2) + (w / 3.) + offset_x, height - h + offset_y)
        Cogl.path_close()

    def do_draw_outline(self, width, height):
        w = width / 5
        h = 35

        Cogl.path_move_to((width / 2) + (w / 3.), height - h)
        Cogl.path_line_to(0, height - h)
        Cogl.path_line_to(0, 0)
        Cogl.path_line_to(width, 0)
        Cogl.path_line_to(width, height - h)
        Cogl.path_line_to((width / 2) + (w / 3. * 4), height - h)
        Cogl.path_line_to(width / 2, height)
        Cogl.path_line_to((width / 2) + (w / 3.), height - h)
        Cogl.path_close()

GObject.type_register(Bubble)
