import os
import subprocess

from libqtile import bar, layout, qtile, hook
from libqtile.widget.backlight import ChangeDirection
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import get_config_file
from libqtile.log_utils import logger

# from qtile_extras.popup.toolkit import PopupAbsoluteLayout, PopupText, PopupWidget, PopupSlider, PopupCircularProgress
# from qtile_extras.widget.mixins import ExtendedPopupMixin
# from qtile_extras.widget.decorations import PowerLineDecoration

from colour import Color

from widgets import widgets, extension_defaults, widget_defaults
from theme import Theme

HOME = os.path.expanduser("~")
MOD = "mod4"
FUNCTION = "mod1"
TERMINAL = "urxvt"
EDITOR = os.environ.get("EDITOR", "/usr/bin/nano")

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([f"{HOME}/.config/qtile/autostart.sh"])

# Custom commands
edit_qtile_config = f"{TERMINAL} {EDITOR} {get_config_file()}"
show_qtile_logs = f"{TERMINAL} tail -f {HOME}/.local/share/qtile/qtile.log"

start_hotreload_config = f"{TERMINAL} {HOME}/.config/qtile/hotreload_config.sh"

keys = [
    Key([MOD], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([MOD], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([MOD], "j", lazy.layout.down(), desc="Move focus down"),
    Key([MOD], "k", lazy.layout.up(), desc="Move focus up"),
    Key([MOD], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([MOD, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([MOD, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([MOD, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([MOD, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [MOD, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([MOD], "Return", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([MOD], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([MOD], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([MOD], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([MOD], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([MOD, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([MOD], "p", lazy.spawn(f"{HOME}/.config/rofi/launchers/type-4/launcher.sh"), desc="Spawn a rofi menu"),
    
    # Dev
    Key([MOD, "control"], "e", lazy.spawn(edit_qtile_config), lazy.spawn(start_hotreload_config), desc="Edit the Qtile config, with hotreloading"),
    Key([MOD, "control"], "t", lazy.spawn(show_qtile_logs), desc="Show the Qtile logs"),
    Key([MOD, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([MOD], "o", lazy.spawn("light-locker-command -l"), desc="Lock the screen"),

    # Function keys
    Key([], "XF86AudioRaiseVolume", lazy.widget["alsawidget"].volume_up(), desc="Raise the volume"),
    Key([], "XF86AudioLowerVolume", lazy.widget["alsawidget"].volume_down(), desc="Lower the volume"),
    Key([], "XF86AudioMute", lazy.widget["alsawidget"].toggle_mute(), desc="Toggle mute the volume"),
    # For some reason, the brightness keys are swapped on my keyboard
    Key([], "XF86MonBrightnessUp", lazy.widget['backlight'].change_backlight(ChangeDirection.DOWN), desc="Raise the brightness"),
    Key([], "XF86MonBrightnessDown", lazy.widget['backlight'].change_backlight(ChangeDirection.UP), desc="Lower the brightness"),
    Key(["shift"], "Print", lazy.spawn("bash -c 'maim -s /home/freddy/Pictures/Screenshots/$(date +%s).png'"), desc="Take a screenshot and save"),
    Key([], "Print", lazy.spawn("bash -c 'maim -s | xclip -selection clipboard -t image/png'"), desc="Take a screenshot and copy to clipboard"),
]

groups = [
    Group(name="1", screen_affinity=0),
    Group(name="2", screen_affinity=0),
    Group(name="3", screen_affinity=0),
    Group(name="4", screen_affinity=1),
    Group(name="5", screen_affinity=1),
    Group(name="6", screen_affinity=1),
]

def go_to_group(group: Group):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[group.name].toscreen()
            return

        qtile.focus_screen(group.screen_affinity)
        qtile.groups_map[group.name].toscreen()

    return _inner

def go_to_group_and_move_window(group: Group):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.current_window.togroup(group.name, switch_group=True)
            return

        qtile.current_window.togroup(group.name, switch_group=False)
        qtile.focus_screen(group.screen_affinity)
        qtile.groups_map[group.name].toscreen()

    return _inner

for group in groups:
    keys.extend([
        Key([MOD, "shift"], group.name, lazy.function(go_to_group_and_move_window(group))),
        Key([MOD], group.name, lazy.function(go_to_group(group))),
        Key(
            ["control", "mod1"],
            f"f{group.name}",
            lazy.core.change_vt(group.name).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{group.name}",
        )
    ])

layouts = [
    layout.MonadTall(
        border_focus=Theme.blue_highlight_dark,
        border_focus_stack=Theme.blue_highlight_dark,
        border_normal=Theme.grey,
        border_width=3,
        single_border_width=0,
        margin=5,
    )
]

bar = bar.Bar(            
    widgets,
    28,
    margin=[5, 5, 0, 5],
    background="#00000000"
)

screens = [
    Screen(
        wallpaper=Theme.wallpaper,
        wallpaper_mode="fill",
        top=bar,
    ),
    Screen(
        wallpaper=Theme.wallpaper,
        wallpaper_mode="fill",
        # top=bar,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="editor"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True

wl_input_rules = None

wmname = "Qtile"

# @hook.subscribe.screen_change
# def _(notify_event):
    
