-- Hyprland binds for the Killer Whale "Hypr" layer (layer 4) and the
-- media keys on the Nav layer (layer 5). See README.md in this folder.
--
-- Load it from hyprland.lua:
--   dofile(os.getenv("HOME") .. "/.config/hypr/killerwhale.lua")
--
-- HyprOSD's own binds (SUPER + A C D S V W B T N Escape Space, Print) are in
-- HyprOSD's README and are not repeated here. Delete any bind below that
-- your hyprland.lua already has: two binds on one key both run.
--
-- Tools: wireplumber (wpctl), brightnessctl, playerctl, xdg-terminal-exec,
-- uwsm (all in Arch's extra/core).

local mod = "SUPER"

-- Lock: the power menu's Lock without the menu. With hypridle running it
-- asks hypridle (`loginctl lock-session`, its lock_cmd), without it (Awake
-- on) HyprOSD's own lock screen. Next to L, the usual SUPER + L.
hl.bind(mod .. " + semicolon", hl.dsp.exec_cmd("qs -c hyprosd ipc call power run lock"))

-- Windows -----------------------------------------------------------------
hl.bind(mod .. " + Q", hl.dsp.window.close())
hl.bind(mod .. " + F", hl.dsp.window.fullscreen({ action = "toggle" }))
hl.bind(mod .. " + G", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mod .. " + RETURN", hl.dsp.exec_cmd("uwsm app -- xdg-terminal-exec"))

-- Focus with h j k l, move the window with SHIFT + h j k l (also what the
-- joystick sends in the Hypr layer while it is in key mode).
local dirs = { H = "left", J = "down", K = "up", L = "right" }
for key, dir in pairs(dirs) do
  hl.bind(mod .. " + " .. key, hl.dsp.focus({ direction = dir }))
  hl.bind(mod .. " + SHIFT + " .. key, hl.dsp.window.move({ direction = dir }))
end

-- Drag / resize windows with the real Super key (left SCROLL key) held.
hl.bind(mod .. " + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind(mod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

-- Workspaces ----------------------------------------------------------------
-- Number row in the Hypr layer: go there; with Shift (hold Z): send the
-- window there.
for i = 1, 10 do
  local key = tostring(i % 10)          -- 10 is on the 0 key
  local ws = tostring(i)
  hl.bind(mod .. " + " .. key, hl.dsp.focus({ workspace = ws }))
  hl.bind(mod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = ws }))
end

-- Right wheel in the Hypr layer, and Tab for the last workspace.
hl.bind(mod .. " + Prior", hl.dsp.focus({ workspace = "e-1" }))
hl.bind(mod .. " + Next", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mod .. " + TAB", hl.dsp.focus({ workspace = "previous" }))

-- Media keys (Nav layer, left wheel) -------------------------------------
-- HyprOSD's volume and brightness meters show up on their own when these
-- change the values.
local opt = { repeating = true, locked = true }
hl.bind("XF86AudioRaiseVolume",
  hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"), opt)
hl.bind("XF86AudioLowerVolume",
  hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"), opt)
hl.bind("XF86AudioMute",
  hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"), { locked = true })
hl.bind("XF86MonBrightnessUp",
  hl.dsp.exec_cmd("brightnessctl set 5%+"), opt)
hl.bind("XF86MonBrightnessDown",
  hl.dsp.exec_cmd("brightnessctl set 5%-"), opt)
hl.bind("XF86AudioPlay", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPrev", hl.dsp.exec_cmd("playerctl previous"), { locked = true })
hl.bind("XF86AudioNext", hl.dsp.exec_cmd("playerctl next"), { locked = true })
