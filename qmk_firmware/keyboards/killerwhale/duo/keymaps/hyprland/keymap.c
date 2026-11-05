// Copyright 2021 Hayashi (@w_vwbw)
// SPDX-License-Identifier: GPL-2.0-or-later
//
// Hyprland / HyprOSD layers for a Killer Whale DUO with a joystick on the
// left, a trackball on the right and ADD units (two keys, a wheel, a toggle
// switch) on both sides. The plan, pictures and Hyprland binds are in
// hyprland/README.md at the root of this repository.
//
// On top of the stock firmware this keymap turns auto mouse off while the
// Game layer is on (left toggle switch) and back to your setting when it is
// switched off: see housekeeping_task_user() at the end.

#include QMK_KEYBOARD_H
#include "lib/add_keycodes.h"
#include "lib/common_killerwhale.h"

enum layer_number {
    BASE = 0,
    GAME,          // left toggle switch
    FREE,          // right toggle switch
    GAME2,         // in GAME: hold left side key 1
    HYPR,          // hold left side key 1
    NAV,           // hold right side key 1
    SYM,           // hold right side key 2
    MOUSE,         // auto mouse (AUTO_MOUSE_DEFAULT_LAYER 7)
    BALL_SETTINGS, // hold 4 / 7
    SPARE
};

#define C_ESC   LCTL_T(KC_ESC)

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
  [BASE] = LAYOUT(
        // left: top
        KC_ESC,  KC_1,         KC_2,            KC_3, LT(BALL_SETTINGS, KC_4), KC_5,
        KC_TAB,  KC_Q,         KC_W,            KC_E, KC_R, KC_T,
        C_ESC,   KC_A,         LT(MOUSE, KC_S), KC_D, KC_F, KC_G,
                 LSFT_T(KC_Z), KC_X,            KC_C, KC_V, KC_B,
                               KC_LGUI,
        // side keys
        MO(HYPR), KC_SPC,
        // joystick (key mode)                     joystick press
        KC_UP, KC_DOWN, KC_LEFT, KC_RGHT,          L_CHMOD,
        // ADD keys                                toggle switch
        KC_LALT, MS_BTN1,                          MO(GAME),
        // right: top
        KC_6, LT(BALL_SETTINGS, KC_7), KC_8, KC_9, KC_0, KC_BSPC,
        KC_Y, KC_U, KC_I,    KC_O,             KC_P,    KC_ENT,
        KC_H, KC_J, KC_K,    LT(MOUSE, KC_L),  KC_SCLN, KC_RSFT,
        KC_N, KC_M, KC_COMM, KC_DOT,           KC_SLSH,
                             MOD_SCRL,
        MO(NAV), MO(SYM),
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,        R_CHMOD,
        MS_BTN1, MS_BTN2,                          MO(FREE)
    ),
  [GAME] = LAYOUT(
        _______, KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,
        _______, _______, _______, KC_W,    _______, _______,
        KC_LCTL, _______, KC_A,    KC_S,    KC_D,    _______,
                 KC_Z,    _______, _______, _______, _______,
                          _______,
        MO(GAME2), KC_SPC,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______,
        KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,  _______,
        KC_1,    KC_2,    KC_3,    KC_4,    KC_5,    _______,
        _______, MS_BTN1, MS_BTN2, MS_BTN3, _______, _______,
        KC_6,    KC_7,    KC_8,    KC_9,    KC_0,
                                   _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______
    ),
  [FREE] = LAYOUT(
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
                 _______, _______, _______, _______, _______,
                          _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______,
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______,
                                   _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______
    ),
  [GAME2] = LAYOUT(
        KC_F11,  KC_1,    KC_2,    KC_3,    KC_4,    KC_5,
        _______, _______, _______, KC_E,    _______, _______,
        _______, _______, KC_S,    KC_D,    KC_F,    _______,
                 _______, _______, _______, _______, _______,
                          _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______,
        KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    KC_F12,
        KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,    _______,
        KC_H,    KC_J,    KC_K,    KC_L,    KC_SCLN, _______,
        KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH,
                                   _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______
    ),
  [HYPR] = LAYOUT(
        G(KC_ESC), G(KC_1), G(KC_2), G(KC_3), G(KC_4), G(KC_5),
        G(KC_TAB), G(KC_Q), G(KC_W), LSG(KC_W), XXXXXXX, G(KC_T),
        _______,   G(KC_A), G(KC_S), G(KC_D), G(KC_F), G(KC_G),
                   _______, XXXXXXX, G(KC_C), G(KC_V), G(KC_B),
                            _______,
        _______, G(KC_SPC),
        LSG(KC_K), LSG(KC_J), LSG(KC_H), LSG(KC_L),      _______,
        _______, _______,                            _______,
        G(KC_6), G(KC_7), G(KC_8), G(KC_9), G(KC_0), XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, G(KC_ENT),
        G(KC_H), G(KC_J), G(KC_K), G(KC_L), G(KC_SCLN), _______,
        G(KC_N), G(KC_M), XXXXXXX, XXXXXXX, XXXXXXX,
                                   _______,
        LSG(KC_SPC), XXXXXXX,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______
    ),
  [NAV] = LAYOUT(
        _______, KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,
        _______, KC_F11,  KC_F12,  KC_MPRV, KC_MPLY, KC_MNXT,
        _______, KC_MUTE, KC_VOLD, KC_VOLU, KC_BRID, KC_BRIU,
                 _______, XXXXXXX, KC_PSCR, XXXXXXX, XXXXXXX,
                          _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______,
        KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,  KC_DEL,
        KC_HOME, KC_PGDN, KC_PGUP, KC_END,  KC_INS,  _______,
        KC_LEFT, KC_DOWN, KC_UP,   KC_RGHT, XXXXXXX, _______,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
                                   _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______
    ),
  [SYM] = LAYOUT(
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
                 _______, _______, _______, _______, _______,
                          _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______,
        _______, _______, _______, _______, _______, _______,
        KC_GRV,  KC_LBRC, KC_RBRC, KC_MINS, KC_EQL,  KC_BSLS,
        KC_TILD, KC_LCBR, KC_RCBR, KC_UNDS, KC_PLUS, KC_QUOT,
        KC_PIPE, KC_LPRN, KC_RPRN, KC_LT,   KC_GT,
                                   _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______
    ),
  [MOUSE] = LAYOUT(
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, MS_BTN2, MS_BTN1, MOD_SCRL,
                 QK_USER_4, _______, _______, _______, _______,
                          _______,   // left SCROLL stays Super (SUPER + drag)
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______,
        _______, _______, _______, _______, _______, _______,
        _______, MS_BTN3, _______, _______, _______, _______,
        MOD_SCRL, MS_BTN1, MS_BTN2, _______, _______, _______,
        _______, _______, _______, _______, QK_USER_4,
                                   MOD_SCRL,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______
    ),
  [BALL_SETTINGS] = LAYOUT(
        XXXXXXX,    XXXXXXX, XXXXXXX, QK_USER_14, _______, L_CHMOD,
        XXXXXXX,    XXXXXXX, XXXXXXX, XXXXXXX, L_SPD_I, XXXXXXX,
        AUTO_MOUSE, XXXXXXX, XXXXXXX, L_ANG_D, L_INV,   L_ANG_I,
                    XXXXXXX, XXXXXXX, XXXXXXX, L_SPD_D, XXXXXXX,
                             INV_SCRL,
        XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,          XXXXXXX,
        XXXXXXX, INV_SCRL,                           XXXXXXX,
        R_CHMOD, _______, QK_USER_14, XXXXXXX, XXXXXXX, XXXXXXX,
        XXXXXXX, R_SPD_I, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        R_ANG_D, R_INV,   R_ANG_I, XXXXXXX, XXXXXXX, AUTO_MOUSE,
        XXXXXXX, R_SPD_D, XXXXXXX, XXXXXXX, XXXXXXX,
                                   INV_SCRL,
        XXXXXXX, XXXXXXX,
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,          XXXXXXX,
        XXXXXXX, XXXXXXX,                            XXXXXXX
    ),
  [SPARE] = LAYOUT(
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
                 _______, _______, _______, _______, _______,
                          _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______,
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______,
                                   _______,
        _______, _______,
        _______, _______, _______, _______,          _______,
        _______, _______,                            _______
    )
};

// Wheels: e0/e1 and e4/e5 are the top unit (not fitted here), e2/e6 the
// side unit wheels, e3/e7 the ADD wheels. Side and ADD share their keys.
#define TRNS_WHEEL ENCODER_CCW_CW(_______, _______)
#define LEFT_RIGHT(l, r) { TRNS_WHEEL, TRNS_WHEEL, l, l, TRNS_WHEEL, TRNS_WHEEL, r, r }

const uint16_t PROGMEM encoder_map[][NUM_ENCODERS][2] = {
    [BASE]          = LEFT_RIGHT(ENCODER_CCW_CW(KC_VOLD, KC_VOLU),
                                 ENCODER_CCW_CW(MS_WHLU, MS_WHLD)),
    [GAME]          = LEFT_RIGHT(TRNS_WHEEL, TRNS_WHEEL),
    [FREE]          = LEFT_RIGHT(TRNS_WHEEL, TRNS_WHEEL),
    [GAME2]         = LEFT_RIGHT(TRNS_WHEEL, TRNS_WHEEL),
    [HYPR]          = LEFT_RIGHT(ENCODER_CCW_CW(KC_BRID, KC_BRIU),
                                 ENCODER_CCW_CW(G(KC_PGUP), G(KC_PGDN))),
    [NAV]           = LEFT_RIGHT(ENCODER_CCW_CW(KC_LEFT, KC_RGHT),
                                 ENCODER_CCW_CW(KC_PGUP, KC_PGDN)),
    [SYM]           = LEFT_RIGHT(TRNS_WHEEL, TRNS_WHEEL),
    [MOUSE]         = LEFT_RIGHT(TRNS_WHEEL, TRNS_WHEEL),
    [BALL_SETTINGS] = LEFT_RIGHT(TRNS_WHEEL, TRNS_WHEEL),
    [SPARE]         = LEFT_RIGHT(TRNS_WHEEL, TRNS_WHEEL),
};

// Auto mouse off while GAME is on. The mouse layer (7) sits above GAME, so
// with auto mouse on, moving the trackball would turn the WASD keys (E S D
// F) into clicks for a moment. Done here rather than in
// layer_state_set_user (the keyboard's lib already uses that for the LEDs,
// and turning auto mouse off can itself change layers). The saved setting
// (kw_config.auto_mouse, the AUTO_MOUSE key in layer 8) is not touched, so
// leaving GAME restores whatever it is.
void housekeeping_task_user(void) {
    static bool was_game = false;
    bool game = layer_state_is(GAME);
    if (game != was_game) {
        was_game = game;
        set_auto_mouse_enable(game ? false : kw_config.auto_mouse);
    }
}
