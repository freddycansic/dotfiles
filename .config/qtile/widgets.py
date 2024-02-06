import os

from libqtile import bar
from libqtile.lazy import lazy

from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_extras.popup.toolkit import PopupRelativeLayout, PopupImage, PopupText, PopupWidget,  PopupGridLayout
from qtile_extras import widget

from theme import Theme
from constants import *

def show_power_menu(qtile):
    image_config = {
        "mask": True,
    }
    
    controls = [
        PopupImage(
            filename=f"{HOME}/.config/qtile/images/lock.svg",                
            row=0,
            col=0,
            highlight=Theme.bg_green,
            mouse_callbacks={
                "Button1": lazy.spawn("dm-tool lock")
            },
            **image_config
        ),
        PopupText(
            text="Lock",
            h_align="center",
            font="firacode",
            row=1,
            col=0,
        ),
        
        PopupImage(
            filename=f"{HOME}/.config/qtile/images/sleep.svg",
            row=0,
            col=1,
            highlight=Theme.bg_yellow,
            mouse_callbacks={
                "Button1": lazy.spawn("bash -c \"dm-tool lock; systemctl suspend\"")
            },
            **image_config
        ),
        PopupText(
            text="Sleep",
            h_align="center",
            font="firacode",
            row=1,
            col=1
        ),
        
        PopupImage(
            filename=f"{HOME}/.config/qtile/images/reboot.svg",
            row=0,
            col=2,
            highlight=Theme.bg_orange,
            mouse_callbacks={
                "Button1": lazy.spawn("systemctl reboot")
            },
            **image_config
        ),
        PopupText(
            text="Reboot",
            h_align="center",
            font="firacode",
            row=1,
            col=2,
        ),
        
        PopupImage(
            filename=f"{HOME}/.config/qtile/images/shutdown.svg",
            highlight=Theme.bg_red,
            row=0,
            col=3,
            mouse_callbacks={
                "Button1": lazy.spawn("systemctl poweroff")
            },
            **image_config
        ),
        PopupText(
            text="Shutdown",
            h_align="center",
            font="firacode",
            row=1,
            col=3
        ),
        
    ]

    layout = PopupGridLayout(
        qtile,
        width=300,
        height=70,
        margin=10,
        rows=2,
        cols=4,
        controls=controls,
        background=Theme.bg_0,
        initial_focus=None,
    )

    layout.show(
        relative_to=3, # top right
        relative_to_bar=True,
        x=-5,
        y=5,
        #centered=True
    )

separator = widget.Sep(foreground=Theme.bg_gray, padding=8)
powerline = {
    "decorations": [PowerLineDecoration(path="arrow_right")]
}

power_widget = widget.UPowerWidget(
    fill_charge="#ffffff",
    fill_critical=Theme.bg_red,
    fill_low=Theme.fg_yellow,
    border_charge_colour="#ffffff",
    border_colour="#ffffff",
    border_critical_colour="#ffffff",
    text_charging="{percentage:.0f}%",
    text_discharging="{percentage:.0f}%",
    #text_charging="",
    #text_discharging="",
    background=Theme.bg_aqua,
    **powerline
)
#power_widget.show_text = True
#power_widget.mouse_callbacks = [] # Disable showing extra text on click

wifi_widget = widget.WiFiIcon(
    interface="wlp4s0",
    background=Theme.bg_green,
    inactive_colour=Theme.bg_4,
    padding_y=6,
    **powerline
)
#wifi_widget.wifi_width *= 0.3
#wifi_widget.wifi_height *= 0.9
#wifi_widget.icon_size *= 0.7

widget_defaults = dict(
    font="firacode",
    fontsize=14,
    padding=4,
)
extension_defaults = widget_defaults.copy()

cpu_icon_widget = widget.Image(filename=f"{HOME}/.config/qtile/images/cpu.png", mask=True,  background=Theme.bg_5)
cpu_icon_widget.margin_y = 4
cpu_icon_widget.margin_x = -3

memory_icon_widget = widget.Image(filename=f"{HOME}/.config/qtile/images/memory.png", mask=True, background=Theme.bg_3)
memory_icon_widget.margin_y = 2
memory_icon_widget.margin_x = -3

widgets = [
    widget.GroupBox(),
    # Hidden widget, needed for backlight binds to work
    widget.Backlight(fmt="", step=5, backlight_name="amdgpu_bl0"),
    
    # Center prompt
    widget.Spacer(bar.STRETCH),
    widget.Prompt(),
    widget.Spacer(bar.STRETCH, **powerline),

    widget.WidgetBox(widgets=[
        memory_icon_widget,
        widget.Memory(format="{MemPercent:.0f}%", measure_mem='G', background=Theme.bg_3, **powerline),
    
        cpu_icon_widget,
        widget.CPU(format="{load_percent:.0f}%", background=Theme.bg_5, **powerline),

        widget.Net(format="↑ {up:3.1f}{up_suffix}", prefix="k", background=Theme.fg_4, **powerline),
        widget.Net(format="↓ {down:3.1f}{down_suffix}", prefix="M", background=Theme.bg_purple, **powerline),                 
    ],
        text_closed="...",
        text_open="...",
        background=Theme.bg_1,
        **powerline
    ),

    widget.ALSAWidget(mode="icon", theme_path=f"{HOME}/.config/qtile/images", icon_size=18, background=Theme.bg_blue),
    widget.Spacer(length=5, background=Theme.bg_blue, **powerline),
    
    power_widget,
    
    wifi_widget,
    
    widget.Clock(format="%a %-d/%-m/%Y", background=Theme.bg_yellow, **powerline),
    widget.Clock(format="%H:%M", background=Theme.bg_orange, **powerline),

    widget.Image(
        filename=f"{HOME}/.config/qtile/images/shutdown.svg",
        mask=True,
        margin=3,
        mouse_callbacks={"Button1": lazy.function(show_power_menu)},
        background=Theme.bg_red)
]


#volume_colors = list(Color(Theme.fg_aqua).range_to(Color(Theme.fg_red), 20))
#def show_volume_slider(qtile):
#    current_volume = volume_widget.get_volume()
#    width = 80
#    height = 80
#    
#    volume_color = volume_colors[round(current_volume/100 * (len(volume_colors) - 1))].hex
#
#    slider = PopupCircularProgress(
#        value=current_volume,
#        min_value=0,
#        max_value=100,
#        width=width,
#        height=height,
#        colour_below=volume_color,
#        colour_above=Theme.bg_4,
#        bar_size=5
#    )
#
#    text = PopupText(
#        text=f"{current_volume}%",
#        h_align="center",
#        font="firacode",
#        pos_y=height*0.02,
#        width=width,
#        height=height,
#        fontsize=18
#    )
#
#    PopupAbsoluteLayout(
#        qtile,
#        width=width,
#        height=height,
#        controls=[text, slider],
#        background=Theme.bg_0,
#        hide_on_timeout=1,
#    ).show(
#        relative_to=2,
#        y=50
#    )
