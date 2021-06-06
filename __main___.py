from event_tools import EventServer
from tkinter_event_components import *


@dataclass(frozen=True)
class Moving:
    start: Position
    end: Position


class App:
    EVENTS = [
        '<Button>',
        '<Motion>',
        '<ButtonRelease>',
        '<Double-Button>',
        '<Enter>',
        '<Leave>',
        '<FocusIn>',
        '<FocusOut>',
        '<Return>',
        '<Key>',
        '<Configure>',
        '<MouseWheel>'
    ]

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MicroPaint")

        self.__last_pos = None
        self.line = False

        self.canvas = tk.Canvas(width=700, height=700, bg='black')
        self.canvas.pack()

        self.event_server = EventServer()

        for event in self.EVENTS:
            self.root.bind(event, self.register_event)

        self.event_server.register_system(self.cursor_system, pos=Position)
        self.event_server.register_system(self.line_drawing, moving=Moving)
        self.event_server.register_system(self.line_tracking, types=Type, button=ButtonNum)
        self.event_server.register_system(self.window_resized, window_size=WindowSize)

    def register_event(self, event):
        components = [Type(event.type), Widget(event.widget)]
        if event.state != '??':
            components.append(State(event.state))
        if event.time != '??':
            components.append(Time(event.time))
        if event.num != "??":
            components.append(ButtonNum(event.num))
        if hasattr(event, "focus"):
            components.append(Focus(event.focus))
        if event.height != '??' and event.width != '??':
            components.append(WindowSize(event.width, event.height))
        if event.keycode != '??':
            components.append(Keycode(event.keycode))
        if event.x != '??' and event.y != "??":
            components.append(Position(event.x, event.y))
        if event.x_root != '??' and event.y_root != '??':
            components.append(RootPosition(event.x_root, event.y_root))
        if event.char != '??':
            components.append(Char(event.char))
        if hasattr(event, "send_event"):
            components.append(SendEvent(event.send_event))
        if event.keysym != '??':
            components.append(Keysym(event.keysym))
        if event.keysym_num != '??':
            components.append(KeysymNum(event.keysym_num))
        if event.delta != 0:
            components.append(Delta(event.delta))
        self.event_server.spawn(*components)

    def line_tracking(self, types, button):
        for type_, btn in zip(types, button):
            if type_.t == tk.EventType.ButtonPress and btn.num == 1:
                self.line = True
            elif type_.t == tk.EventType.ButtonRelease and btn.num == 1:
                self.line = False
                self.__last_pos = None

    def process(self):
        self.root.after(1, self.process)
        self.event_server.tick()

    def cursor_system(self, pos):
        positions = list(pos)
        if self.__last_pos is None:
            self.__last_pos = positions.pop(0)
        for pos in positions:
            self.event_server.spawn(Moving(self.__last_pos, pos))
            self.__last_pos = pos

    def line_drawing(self, moving):
        if self.line:
            line = tuple((mov.start.x, mov.start.y, mov.end.x, mov.end.y) for mov in moving)
            self.canvas.create_line(line, fill='cyan')

    def window_resized(self, window_size):
        # - 4 because of window border
        self.canvas['width'] = window_size[0].width - 4
        self.canvas['height'] = window_size[0].height - 4

    def run(self):
        self.process()
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
