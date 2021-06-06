from dataclasses import dataclass
import tkinter as tk


@dataclass(frozen=True)
class Position:
    """
    Положение курсора относительно виджета
    Position of the cursor relative to the widget
    """
    x: int
    y: int


@dataclass(frozen=True)
class Focus:
    """
    Имеет ли окно фокус
    Does the window have focus
    """
    value: bool


@dataclass(frozen=True)
class ButtonNum:
    """
    Номер кнопки мыши
    Mouse Button Number
    """
    num: int


@dataclass(frozen=True)
class WindowSize:
    """
    Размеры окна
    Window dimensions
    """
    width: int
    height: int


@dataclass(frozen=True)
class Keycode:
    """
    Код нажатой клавиши
    Pressed key code
    """
    keycode: int


@dataclass(frozen=True)
class State:
    """
    Наличие модификаторов, например shift, alt, ctrl
    The presence of modifiers such as shift, alt, ctrl
    """
    state: str


@dataclass(frozen=True)
class Time:
    """
    Время наступления события
    Time of the event
    """
    time: int


@dataclass(frozen=True)
class RootPosition:
    """
    Координыты курсора на экране
    Screen cursor coordinates
    """
    x: int
    y: int


@dataclass(frozen=True)
class Char:
    """
    Набранный на клавиатуре символ
    The character typed on the keyboard
    """
    char: str


@dataclass(frozen=True)
class Keysym:
    """
    Набранный на клавиатуре символ
    The character typed on the keyboard
    """
    keysym: str


@dataclass(frozen=True)
class KeysymNum:
    """
    Набранный на клавиатуре символ в виде числа
    The character typed on the keyboard as a number
    """
    num: int


@dataclass(frozen=True)
class Type:
    """
    Тип события
    Event type
    """
    t: tk.EventType


@dataclass(frozen=True)
class Widget:
    """
    Виджет, получивший событие
    The widget that received the event
    """
    widget: tk.Widget


@dataclass(frozen=True)
class Delta:
    """
    Направление и величина прокрутки
    Scrolling direction and amount
    """
    delta: int


@dataclass(frozen=True)
class SendEvent:
    val: bool


