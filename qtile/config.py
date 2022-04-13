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

import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401from typing import List  # noqa: F401

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "kitty"      # My terminal of choice
myBrowser = "firefox" # My browser of choice

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm+" -e fish"),
             desc='Launches My Terminal'
             ),
         Key([mod], "d",
             lazy.spawn("discord"),
             desc='Launches Discord',
             ),
         Key([mod], "s",
             lazy.spawn("spotify"),
             desc='launches spotify'
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn("/home/philipp/.config/rofi/launchers/misc/launcher.sh"),
             desc='Run Launcher'
             ),
         Key([mod], "b",
             lazy.spawn(myBrowser),
             desc='Firefox'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod], "q",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key(["control", "shift"], "e",
             lazy.spawn("emacsclient -c -a emacs"),
             desc='Doom Emacs'
             ),
          ### Volume control
    Key([], "XF86AudioStop", lazy.spawn('playerctl play-pause')),
    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause')),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous')),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next')),
    Key([], "XF86AudioMute", lazy.spawn('pamixer -t')),
    Key([], "XF86AudioRaiseVolume", lazy.spawn('pamixer -i 3')),
    Key([], "XF86AudioLowerVolume", lazy.spawn('pamixer -d 3')),


### Switch focus to specific monitor (out of three)
         Key([mod], "w",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "e",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Treetab controls
          Key([mod, "shift"], "h",
             lazy.layout.move_left(),
             desc='Move up a section in treetab'
             ),
         Key([mod, "shift"], "l",
             lazy.layout.move_right(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
                  Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
          Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
         # Emacs programs launched using the key chord CTRL+e followed by 'key'
         KeyChord(["control"],"e", [
             Key([], "e",
                 lazy.spawn("emacsclient -c -a 'emacs'"),
                 desc='Launch Emacs'
                 ),
             Key([], "b",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(ibuffer)'"),
                 desc='Launch ibuffer inside Emacs'
                 ),
             Key([], "d",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(dired nil)'"),
                 desc='Launch dired inside Emacs'
                 ),
             Key([], "i",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(erc)'"),
                 desc='Launch erc inside Emacs'
                 ),
             Key([], "m",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(mu4e)'"),
                 desc='Launch mu4e inside Emacs'
                 ),
             Key([], "n",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(elfeed)'"),
                 desc='Launch elfeed inside Emacs'
                 ),
             Key([], "s",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(eshell)'"),
                 desc='Launch the eshell inside Emacs'
                 ),
             Key([], "v",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(+vterm/here nil)'"),
                 desc='Launch vterm inside Emacs'
                 )
         ])         
]

groups = [#Group(" ﳎ ", layout='monadtall'),
          Group("  ", layout='monadtall'),
          #Group("  ", layout='monadtall'),
          #Group("  ", layout='monadtall'),
          Group("  ", layout='monadtall'),
          Group("  ", layout='monadtall'),
          #Group("  ", layout='monadtall'),
          Group("  ", layout='monadtall'),
          Group("  ", layout='monadtall')
         ]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "1A5149",
                "border_normal": "112D39"
                }

layouts = [
    layout.MonadWide(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Stack(stacks=2, **layout_theme),
    layout.Columns(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.VerticalTile(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
         font = "Iosevka",
         fontsize = 10,
         sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
         section_fontsize = 10,
         border_width = 2,
         bg_color = "112D39",
         active_bg = "1A5149",
         active_fg = "1A5149",
         inactive_bg = "112D39",
         inactive_fg = "112D39",
         padding_left = 0,
         padding_x = 0,
         padding_y = 5,
         section_top = 10,
         section_bottom = 20,
         level_shift = 8,
         vspace = 3,
         panel_width = 200,
         ),
        layout.Floating(**layout_theme),
]
colors = [["#151515", "#151515"], #0,background
          ["#182823", "#182823"], #1,black
          ["#E8E3E3", "#E8E3E3"], #2,white
          ["#B66467", "#B66467"], #3,Red
          ["#8C977D", "#8C977D"], #4,Green
          ["#D9BC8C", "#D9BC8C"], #5,Yellow
          ["#8AA6A2", "#8AA6A2"], #6,cyan
          ["#A988B0", "#A988B0"], #7,Magenta
          ["#8DA3B9", "#8DA3B9"], #8,blue
          ["#EB7500", "#EB7500"]] #9,Purple(in this case orange)

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 10,
    padding = 2,
    background=colors[0]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 20,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.TextBox(
                  font = "Ubuntu Mono",
                  text='',
                  foreground=colors[1],
                  background=colors[0],
                  padding = 0,
                  fontsize= 24
                  ),
              widget.TextBox(
                       text = '  ',
                       foreground = colors[3],
                       background = colors[1],
                       fontsize = 30,
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('/home/philipp/.config/rofi/powermenu/powermenu.sh')}
                       ),
              widget.TextBox(
                  text='',
                  foreground=colors[1],
                  background=colors[0],
                  padding = 0,
                  fontsize= 23
                  ),
              widget.Sep(
                       linewidth = 0,
                       padding = 20,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.TextBox(
                  font = "Ubuntu Mono",
                  text='',
                  foreground=colors[1],
                  background=colors[0],
                  padding = 0,
                  fontsize= 24
                  ),
              widget.GroupBox(
                        font="FontAwesome",
                        fontsize=23,
                        margin_y=2,
                        margin_x=0,
                        padding_y=6,
                        padding_x=4,
                        disable_drag=True,
                        use_mouse_wheel=True,
                        active=colors[6],
                        inactive=colors[0],
                        rounded=True,
                        highlight_color=colors[2],
                        block_highlight_text_color=colors[4],
                        highlight_method="text",
                        foreground=colors[2],
                        background=colors[1],
                        urgent_border=colors[3],
        ),
                      widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[2],
                       background = colors[1],
                       padding = 0,
                       scale = 0.6,

                       ),
              widget.TextBox(
                  text='',
                  foreground=colors[1],
                  background=colors[0],
                  padding = 0,
                  fontsize= 23
                  ),
               widget.Sep(
                       linewidth = 0,
                       padding = 20,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0,
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("rofi -show")},
                       ),
              #widget.Cmus(
               #       backgound = colors[0],
                #      foreground = colors[6],
                 #     padding = 0,
                  #    ),

              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.TextBox(
                  font = "Ubuntu Mono",
                  text='',
                  foreground=colors[1],
                  background=colors[0],
                  padding = 0,
                  fontsize= 24
                  ),
               widget.Net(
                       interface = "enp34s0",
                       format ='net : {down} ↓↑ {up}',
                       foreground = colors[3],
                       background = colors[1],
                       padding = 5
                       ),        
              widget.ThermalSensor(
                       foreground = colors[5],
                       background = colors[1],
                       threshold = 90,
                       fmt = ' CPU : {}',
                       padding = 5
                       ),
              widget.NvidiaSensors(
                       foreground = colors[4],
                       fmt = ' GPU :{}',
                       padding = 5,
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e nvtop')},
                       background = colors[1]
                       ),
               widget.TextBox(
                      text = "",
                      font = "Ubuntu Mono",
                      fontsize = 25,
                      foreground = colors[6],
                      background = colors[1],
                      ),
              widget.Memory(
                       foreground = colors[6],
                       background = colors[1],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e gotop')},
                       padding = 5
                       ),
              widget.TextBox(
                  text='',
                  foreground=colors[1],
                  background=colors[0],
                  padding = 0,
                  fontsize= 23
                  ),
              widget.Sep(
                       linewidth = 0,
                       padding = 20,
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.TextBox(
                    text='',
                    foreground=colors[1],
                    background=colors[0],
                    padding = 0,
                    fontsize= 24
                  ),
             widget.Clock(
                       foreground = colors[9],
                       background = colors[1],
                       format = "%A, %B %d - %H:%M ",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('/home/philipp/.config/rofi/applets/menu/time.sh')},
                       ),
             widget.TextBox(
                     text='|',
                     foreground=colors[2],
                     background=colors[1],
                     ),
             widget.OpenWeather(
                       foreground = colors[8],
                       background = colors[1],
                       location='Gauting',
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' sh -c "curl v2.wttr.in/starnberg;bash" ')},
                       padding = 5
                       ),
             widget.TextBox(
                  text='',
                  foreground=colors[1],
                  background=colors[0],
                  padding = 0,
                  fontsize= 23
                  ),
             widget.Sep(
                       linewidth = 0,
                       padding = 20,
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.TextBox(
                    text='',
                    foreground=colors[1],
                    background=colors[0],
                    padding = 0,
                    fontsize= 24
                  ),  
              widget.TextBox(
                      text = "墳",                                            
                      font = "Ubuntu Mono",
                      fontsize = 25,
                      foreground = colors[7],                       
                      background = colors[1], 
                      ),
              widget.PulseVolume(
                     foreground=colors[7],
                     background=colors[1],
                     mouse_callbacks= {"Button1": lambda: qtile.cmd_spawn("pavucontrol")},
                     #fmt = ' 墳: {}',
                     padding= 5
                     ),
              widget.CheckUpdates(
                      update_interval = 100,
                      foreground=colors[5],
                      background=colors[1],
                      colour_have_updates = colors[5],
                      colour_no_updates = colors[2],
                      distro= 'Arch_checkupdates',
                      display_format = "Updates: {updates} ",
                      mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},                        
                      ),
              widget.Systray(  
                        background = colors[1],
                        foreground = colors[3],                       
                        ),
              widget.TextBox(
                  text='',
                  foreground=colors[1],
                  background=colors[0],
                  padding = 0,
                  fontsize= 24
                  ),
              widget.Sep(
                       linewidth = 0,
                       padding = 20,
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.TextBox(
                    text='',
                    foreground=colors[1],
                    background=colors[0],
                    padding = 0,
                    fontsize= 23
                  ),
              widget.TextBox(
                      text = "  ",
                      background = colors[1],
                      foreground = colors[5],
                      mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('/home/philipp/.config/rofi/launchers/misc/launcher.sh &')},
                      fontsize = 30,
                      padding = 4,
                      ),
                widget.TextBox(                                                                                                                          
                  text='',                     
                  foreground=colors[1],                                                                                                                 
                  background=colors[0],                                                                                                                 
                  padding = 0,                                                                                                                        
                  fontsize= 23                                                                                                                                             ),
              widget.Sep(
                       linewidth = 0,
                       padding = 20,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              ]
    return widgets_list
widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2


widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen1(),
                size=25,
                background="#151515",
                border_color=["#151515", "#151515", "#151515", "#151515"],
                border_width=[4, 4, 4, 4],
                opacity=1,
                margin=[4, 8, 0, 8],
            )
        ),
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen2(),
                size=26,
                opacity=1,
                margin=[2, 8, 0, 8],
            )
        ),
    ]


screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################
# assgin apps to groups #
#########################


# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #################################################################################
#     # Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient #
#     #################################################################################
#     d[group_names[0]] = [
#         "Navigator",
#         "Firefox",
#         "Vivaldi-stable",
#         "Vivaldi-snapshot",
#         "Chromium",
#         "Google-chrome",
#         "Brave",
#         "Brave-browser",
#         "navigator",
#         "firefox",
#         "vivaldi-stable",
#         "vivaldi-snapshot",
#         "chromium",
#         "google-chrome",
#         "brave",
#         "brave-browser",
#     ]
#     d[group_names[1]] = [
#         "Atom",
#         "Subl",
#         "Geany",
#         "Brackets",
#         "Code-oss",
#         "Code",
#         "TelegramDesktop",
#         "Discord",
#         "atom",
#         "subl",
#         "geany",
#         "brackets",
#         "code-oss",
#         "code",
#         "telegramDesktop",
#         "discord",
#     ]
#     d[group_names[2]] = [
#         "Inkscape",
#         "Nomacs",
#         "Ristretto",
#         "Nitrogen",
#         "Feh",
#         "inkscape",
#         "nomacs",
#         "ristretto",
#         "nitrogen",
#         "feh",
#     ]
#     d[group_names[3]] = ["Gimp", "gimp"]
#     d[group_names[4]] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld"]
#     d[group_names[5]] = ["Vlc", "vlc", "Mpv", "mpv"]
#     d[group_names[6]] = [
#         "VirtualBox Manager",
#         "VirtualBox Machine",
#         "Vmplayer",
#         "virtualbox manager",
#         "virtualbox machine",
#         "vmplayer",
#     ]
#     d[group_names[7]] = [
#         "Thunar",
#         "Nemo",
#         "Caja",
#         "Nautilus",
#         "org.gnome.Nautilus",
#         "Pcmanfm",
#         "Pcmanfm-qt",
#         "thunar",
#         "nemo",
#         "caja",
#         "nautilus",
#         "org.gnome.nautilus",
#         "pcmanfm",
#         "pcmanfm-qt",
#     ]
#     d[group_names[8]] = [
#         "Evolution",
#         "Geary",
#         "Mail",
#         "Thunderbird",
#         "evolution",
#         "geary",
#         "mail",
#         "thunderbird",
#     ]
#     d[group_names[9]] = [
#         "Spotify",
#         "Pragha",
#         "Clementine",
#         "Deadbeef",
#         "Audacious",
#         "spotify",
#         "pragha",
#         "clementine",
#         "deadbeef",
#         "audacious",
#     ]
#
#
#####################################################################################
#
# wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen(toggle=False)

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME


main = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])


@hook.subscribe.client_new
def set_floating(window):
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
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
        Match(wm_class="Arcolinux-welcome-app.py"),
        Match(wm_class="Arcolinux-tweak-tool.py"),
        Match(wm_class="Arcolinux-calamares-tool.py"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="Arandr"),
        Match(wm_class="feh"),
        Match(wm_class="Galculator"),
        Match(wm_class="arcolinux-logout"),
        Match(wm_class="xfce4-terminal"),
        Match(wm_class="Yad"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="Bluetooth"),
    ],
    fullscreen_border_width=0,
    border_width=0,
)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smar

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
