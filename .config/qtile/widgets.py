import os

from libqtile import bar
from libqtile.lazy import lazy

from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_extras.popup.toolkit import PopupRelativeLayout, PopupImage, PopupText, PopupWidget,  PopupGridLayout
from qtile_extras import widget

from theme import Theme

widget_defaults = dict(
    font=Theme.font,
    fontsize=14,
    padding=8,
    foreground=Theme.text,
    background="#e5e6ebaa",
)
extension_defaults = widget_defaults.copy()

widgets = [

    # ***************************
    # LEFT
    # ***************************
    widget.Spacer(length=3), 
    widget.GroupBox(
        highlight_method="block",
        foreground=Theme.text,
        active=Theme.blue,
        this_current_screen_border=Theme.lightblue,
        this_screen_border=Theme.blue,
        block_highlight_text_color=Theme.darkgrey
    ),
    # Hidden widget, needed for backlight binds to work
    widget.Backlight(fmt="", step=5, backlight_name="amdgpu_bl1"),
    
    widget.Spacer(bar.STRETCH),

    # **************************
    # RIGHT
    # **************************

    widget.WidgetBox(widgets=[
        widget.Image(
            filename="~/.config/qtile/images/memory.png",
            mask=True,
            colour=Theme.text,
            margin_y=3,
            margin_x=-3
        ),
        widget.Memory(
            format="{MemPercent:.0f}%",
            measure_mem='G',
            foreground=Theme.text
        ),
        
        widget.Image(
            filename="~/.config/qtile/images/cpu.png",
            mask=True,
            colour=Theme.text,
            margin=4
        ),
        widget.CPU(
            format="{load_percent:.0f}%",
            foreground=Theme.text
        ),

        widget.Net(
            format="↑ {up:3.1f}{up_suffix}",
            prefix="k",
            foreground=Theme.text
        ),
        widget.Net(
            format="↓ {down:3.1f}{down_suffix}",
            prefix="M",
            foreground=Theme.text
        ),                 
    ],
        text_closed="...",
        text_open="...",
        foreground=Theme.text
    ),

    widget.ALSAWidget(
        mode="icon",
        theme_path="~/.config/qtile/images",
        icon_size=16
    ),
    widget.Spacer(length=8),
    
    widget.UPowerWidget(
        fill_charge=Theme.blue_highlight_light,
        fill_critical=Theme.lightred,
        fill_low=Theme.yellow_highlight_light,
        fill_normal=Theme.text,
        border_charge_colour=Theme.text,
        border_colour=Theme.text,
        border_critical_colour=Theme.text,
        text_charging="Charging {percentage:.0f}%",
        text_discharging="{percentage:.0f}%",
    ),
    widget.Spacer(length=5),

    widget.WiFiIcon(
        interface="wlan0",
        active_colour=Theme.text,
        foreground=Theme.text,
        inactive_colour=Theme.bg_darkest,
        padding_y=6
    ),
    
    widget.Clock(format="%a %-d/%-m/%Y", foreground=Theme.text),
    widget.Clock(format="%H:%M", foreground=Theme.text),
    widget.Spacer(length=4)
]
