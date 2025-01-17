import dearpygui.dearpygui as dpg
import subprocess
import threading
import platform
import uuid
import time
import sys
import os
import io

NAME = "Hakkamichi"
VERSION = "1.0.1"
AUTHOR = "batubyte"
TITLE = f"{NAME} {uuid.uuid4()}"
RESOLUTION = (1280, 800)

shell_count = 0


def resize_terminal(cols, lines):
    current_platform = platform.system()

    if current_platform == "Windows":
        os.system(f"mode con: cols={cols} lines={lines}")

    elif current_platform == "Linux" or current_platform == "Darwin":
        os.system(f'printf "\\e[8;{lines};{cols}t"')


def set_terminal_title(title: str):
    system = platform.system()

    if system == "Windows":
        os.system(f"title {title}")
    else:
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()


def activate_window(title):
    system = platform.system()
    if system == "Windows":
        try:
            import pygetwindow as gw

            windows = gw.getWindowsWithTitle(title)
            if windows:
                window = windows[0]
                window.activate()
        except:
            pass


def create_shell():
    global shell_count
    shell_count += 1
    with dpg.window(label=f"Shell {shell_count}", autosize=True, pos=(50, 50)):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="New Window", callback=create_shell)
                dpg.add_menu_item(label="Open")
                dpg.add_menu_item(label="Save")

        with dpg.child_window(auto_resize_x=True, auto_resize_y=True):
            dpg.add_input_text(
                multiline=True,
                tag=f"Shell Source {shell_count}",
                width=500,
                height=200,
                no_horizontal_scroll=False,
            )
            dpg.add_button(
                label="Execute",
                callback=lambda: execute_source(shell_count),
                width=500,
            )


def execute_source(shell):
    source = dpg.get_value(f"Shell Source {shell}")
    try:
        exec(source)
    except Exception as e:
        print(e)
    activate_window(TITLE)


def load_fonts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_files = {
        "FiraCode-Regular": os.path.join(script_dir, "fonts", "FiraCode-Regular.ttf"),
        "FiraCode-Light": os.path.join(script_dir, "fonts", "FiraCode-Light.ttf"),
        "FiraCode-Medium": os.path.join(script_dir, "fonts", "FiraCode-Medium.ttf"),
        "FiraCode-SemiBold": os.path.join(script_dir, "fonts", "FiraCode-SemiBold.ttf"),
        "FiraCode-Bold": os.path.join(script_dir, "fonts", "FiraCode-Bold.ttf"),
    }

    if all(os.path.exists(font_path) for font_path in font_files.values()):
        with dpg.handler_registry():
            with dpg.font_registry():
                for tag, font_path in font_files.items():
                    dpg.add_font(font_path, 17, tag=tag)
        dpg.bind_font("FiraCode-SemiBold")


def setup_gui():
    dpg.create_context()
    dpg.create_viewport(
        title=f"{NAME} {VERSION} by {AUTHOR}", clear_color=(115, 140, 152)
    )

    with dpg.window(tag="Primary Window"):
        with dpg.menu_bar():
            with dpg.menu(label="Applications"):
                dpg.add_menu_item(label="Settings")
                dpg.add_menu_item(
                    label="Shell", callback=lambda: dpg.show_item("Shell Window")
                )

    with dpg.window(
        label="Shell", tag="Shell Window", show=False, autosize=True, pos=(50, 50)
    ):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="New Window", callback=create_shell)
                dpg.add_menu_item(label="Open")
                dpg.add_menu_item(label="Save")

        with dpg.child_window(auto_resize_x=True, auto_resize_y=True):
            dpg.add_input_text(
                multiline=True,
                tag="Shell Source 0",
                default_value="""print('Hello World')\n""",
                width=500,
                height=200,
            )
            dpg.add_button(
                label="Execute", callback=lambda: execute_source(0), width=500
            )

    load_fonts()
    apply_theme()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)


def apply_theme():
    with dpg.theme(tag="Global Theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 2)

            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (105, 113, 126))
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (21, 22, 23))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (21, 22, 23))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (66, 66, 76))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (20, 20, 20))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (75, 92, 101))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (32, 50, 77))
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBgHovered, (32 * 1.2, 50 * 1.2, 77 * 1.2)
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBgActive, (32 * 1.4, 50 * 1.4, 77 * 1.4)
            )
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (10, 10, 10))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (41, 74, 122))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (10, 10, 10))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (36, 36, 36))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (13, 13, 13))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (80, 80, 80))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (104, 105, 105))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (130, 130, 131))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (57, 124, 205))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (61, 133, 224))
            dpg.add_theme_color(
                dpg.mvThemeCol_SliderGrabActive, (61 * 1.2, 133 * 1.2, 224 * 1.2)
            )
            dpg.add_theme_color(dpg.mvThemeCol_Button, (32, 50, 77))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (39, 73, 114))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (51, 108, 175))
            # dpg.add_theme_color(dpg.mvThemeCol_Header, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_Separator, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, (R, G, B))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, (30, 48, 68))
            dpg.add_theme_color(
                dpg.mvThemeCol_ResizeGripHovered, (30 * 1.2, 48 * 0.1, 68 * 1.2)
            )
            dpg.add_theme_color(
                dpg.mvThemeCol_ResizeGripActive, (30 * 1.4, 48 * 1.4, 68 * 1.4)
            )
            # dpg.add_theme_color(dpg.mvThemeCol_Tab, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_TabActive, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_DockingPreview, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_PlotLines, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (R, G, B))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (44, 85, 137))
            # dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_NavHighlight, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg, (R, G, B))
            # dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (R, G, B))
    dpg.bind_theme("Global Theme")


def main():
    resize_terminal(100, 25)
    set_terminal_title(TITLE)

    setup_gui()

    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
