# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import fontawesome as fa
import os.path


mod         = "mod4"
terminal    = "kitty"
MainFont    = "Hack"
IconFont    = "FontAwesome"
WallDir     = os.path.expandvars("$HOME/.cache/")

icons = {
    "music":    fa.icons["music"],
    "battery":  fa.icons["battery-empty"],
    "term":     fa.icons["terminal"],
    "globe": fa.icons["globe"],
    "play": fa.icons["play-circle"],
    "code":     fa.icons["code"],
    ".":        fa.icons["empire"],
}


# import colors made with pywal
# this way of doing things is recommended by pywal's wiki
# https://github.com/dylanaraps/pywal/wiki/Customization#qtile
colors = []
cache=WallDir+"/wal/colors"
def load_colors(cache):
    with open(cache, 'r') as file:
        for i in range(8):
            colors.append(file.readline().strip())
    colors.append('#ffffff')
    lazy.reload()
load_colors(cache)


keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),


    Key([mod], "d", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
]

groups = []
groups_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

dot = icons["."]
groups_labels = [
            icons["term"], icons["globe"], dot,dot,dot,
            dot,dot,dot, icons["code"], icons["play"],
        ]

for i in range(len(groups_names)):
        groups.append(
        Group(
        name=groups_names[i],
        label=groups_labels[i],
    ))

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])


layouts = [
    layout.MonadTall(margin=8, border_width=4, border_focus=colors[7], border_normal=colors[0]),
    layout.Floating(margin=8, border_width=4, border_focus=colors[7], border_normal=colors[0])
]


widget_defaults = dict(
    font=MainFont,
    fontsize=14,
    padding=3,
    foreground=colors[7],
    background=colors[0]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper = WallDir+"current_wallpaper",
        wallpaper_mode = "fill",
        top=bar.Bar(
            [
                widget.TextBox( text=" "),
                widget.GroupBox(margin_y=5,
                                margin_x=2,
                                padding_y=5,
                                padding_x=4,
                                borderwidth=5,
                                active=colors[7],
                                inactive=colors[3],
                                rounded=True,
                                highlight_color=colors[0],
                                highlight_method="line",
                                this_current_screen_border=colors[6],
                                fontsize=17),
                widget.TextBox( text="| "),
                widget.Prompt(  cursos_color=colors[7]),
                widget.Spacer(),
                #widget.TextBox( font=IconFont,
                                #fontsize=13,
                                #text=icons["clock"]),
                widget.Clock(   fontsize=13),
                widget.Spacer(),
                widget.TextBox( text="|"),
                widget.Systray(icon_size=25),
                widget.TextBox( text="|"),
                widget.TextBox( font=IconFont,
                                fontsize=13,
                                text=icons["music"],),
                widget.Volume(),
                widget.TextBox( text="|"),
                widget.Clock(   format='%d %m | %a |'),
                widget.TextBox( font=IconFont,
                                text=icons["battery"]),
                widget.Battery( format='{percent:2.0%}'),
                widget.QuickExit(default_text=" X"),
                widget.TextBox( text=" "),
            ],
            40,
            opacity=0.9,
            margin=[6,80,6,80]
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
jmname = "LG3D"
