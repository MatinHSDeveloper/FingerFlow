# ============================================================
# FingerFlow
# Camera-Based Air Mouse & Gesture Controller
# ============================================================
#
# Author      : Matin Haji Seftjani
# GitHub      : https://github.com/MatinHSDeveloper
# Website     : https://matinhajiseftjani.ir
#
# Social Media:
# Telegram    : https://t.me/OfficialMatinDeveloper
# Instagram   : https://instagram.com/OfficialMatinDeveloper
# LinkedIn    : https://linkedin.com/in/matindeveloper
#
# Copyright (c) 2026 Matin Haji Seftjani
#
# Licensed under the MIT License.
# See the LICENSE file in the project root for license information.
#
# Project:
# FingerFlow - Control beyond touch.
#
# ============================================================

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import math
import ctypes
import threading


# ============================================================
# CONFIG
# ============================================================

CAMERA_INDEX = 1

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

SMOOTHING = 0.30

# مقدار کمتر = باید انگشت‌ها بیشتر به هم نزدیک شوند
PINCH_THRESHOLD = 0.40

# چند فریم برای تأیید Pinch
PINCH_FRAMES = 3

# چند فریم برای آزاد شدن Pinch
RELEASE_FRAMES = 5

# فاصله حداقل بین دو کلیک
CLICK_COOLDOWN = 0.45

MIRROR_CAMERA = True

SHOW_CAMERA = True


# ============================================================
# PYAutoGUI
# ============================================================

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False


# ============================================================
# MEDIAPIPE
# ============================================================

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


# ============================================================
# SCREEN
# ============================================================

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()


# ============================================================
# GLOBAL STATE
# ============================================================

running = True

mouse_enabled = True

calibration_matrix = None

last_mouse_x = None
last_mouse_y = None

left_pinch_frames = 0
right_pinch_frames = 0

left_triggered = False
right_triggered = False

last_left_click = 0
last_right_click = 0

fps = 0
fps_counter = 0
fps_timer = time.time()


# ============================================================
# UTILS
# ============================================================

def distance(a, b):

    return math.hypot(
        a[0] - b[0],
        a[1] - b[1]
    )


def clamp(value, minimum, maximum):

    return max(
        minimum,
        min(
            value,
            maximum
        )
    )


def smooth(old, new, factor):

    if old is None:
        return new

    return old + (
        new - old
    ) * factor


# ============================================================
# LANDMARKS
# ============================================================

def get_points(hand, width, height):

    result = []

    for lm in hand.landmark:

        result.append(
            (
                int(lm.x * width),
                int(lm.y * height)
            )
        )

    return result


# ============================================================
# FINGER DETECTION
# ============================================================

def is_extended(points, tip, pip):

    return (
        points[tip][1]
        <
        points[pip][1]
    )


def get_fingers(points):

    index = is_extended(
        points,
        8,
        6
    )

    middle = is_extended(
        points,
        12,
        10
    )

    ring = is_extended(
        points,
        16,
        14
    )

    pinky = is_extended(
        points,
        20,
        18
    )

    return (
        index,
        middle,
        ring,
        pinky
    )


# ============================================================
# PINCH DETECTION
# ============================================================

def pinch_ratio(points):

    thumb = points[4]

    index = points[8]

    wrist = points[0]

    middle_base = points[9]

    hand_size = distance(
        wrist,
        middle_base
    )

    if hand_size < 1:

        return 999

    pinch_distance = distance(
        thumb,
        index
    )

    return (
        pinch_distance
        /
        hand_size
    )


# ============================================================
# CAMERA → SCREEN
# ============================================================

def camera_to_screen(x, y):

    if calibration_matrix is None:

        sx = (
            x
            /
            CAMERA_WIDTH
        ) * SCREEN_WIDTH

        sy = (
            y
            /
            CAMERA_HEIGHT
        ) * SCREEN_HEIGHT

    else:

        point = np.array(
            [[[x, y]]],
            dtype=np.float32
        )

        result = cv2.perspectiveTransform(
            point,
            calibration_matrix
        )

        sx = result[0][0][0]

        sy = result[0][0][1]

    sx = clamp(
        sx,
        0,
        SCREEN_WIDTH - 1
    )

    sy = clamp(
        sy,
        0,
        SCREEN_HEIGHT - 1
    )

    return (
        int(sx),
        int(sy)
    )


# ============================================================
# MOVE MOUSE
# ============================================================

def move_mouse(x, y):

    global last_mouse_x
    global last_mouse_y

    x = smooth(
        last_mouse_x,
        x,
        SMOOTHING
    )

    y = smooth(
        last_mouse_y,
        y,
        SMOOTHING
    )

    last_mouse_x = x
    last_mouse_y = y

    try:

        pyautogui.moveTo(
            int(x),
            int(y),
            duration=0
        )

    except Exception:

        pass


# ============================================================
# LEFT CLICK
# ============================================================

def left_click(pinch):

    global left_pinch_frames
    global left_triggered
    global last_left_click

    now = time.time()

    if pinch <= PINCH_THRESHOLD:

        left_pinch_frames += 1

    else:

        left_pinch_frames = 0

        left_triggered = False

    if (
        left_pinch_frames >= PINCH_FRAMES
        and not left_triggered
        and now - last_left_click
        >= CLICK_COOLDOWN
    ):

        try:

            pyautogui.mouseDown(
                button="left"
            )

            time.sleep(0.03)

            pyautogui.mouseUp(
                button="left"
            )

            print("LEFT CLICK")

        except Exception as e:

            print(
                "Left click error:",
                e
            )

        left_triggered = True

        last_left_click = now


# ============================================================
# RIGHT CLICK
# ============================================================

def right_click(pinch):

    global right_pinch_frames
    global right_triggered
    global last_right_click

    now = time.time()

    if pinch <= PINCH_THRESHOLD:

        right_pinch_frames += 1

    else:

        right_pinch_frames = 0

        right_triggered = False

    if (
        right_pinch_frames >= PINCH_FRAMES
        and not right_triggered
        and now - last_right_click
        >= CLICK_COOLDOWN
    ):

        try:

            pyautogui.mouseDown(
                button="right"
            )

            time.sleep(0.03)

            pyautogui.mouseUp(
                button="right"
            )

            print("RIGHT CLICK")

        except Exception as e:

            print(
                "Right click error:",
                e
            )

        right_triggered = True

        last_right_click = now


# ============================================================
# RESET
# ============================================================

def reset_click_state():

    global left_pinch_frames
    global right_pinch_frames

    global left_triggered
    global right_triggered

    left_pinch_frames = 0

    right_pinch_frames = 0

    left_triggered = False

    right_triggered = False


# ============================================================
# CALIBRATION
# ============================================================

def calibrate(cap, hands):

    global calibration_matrix

    print()
    print("=" * 60)
    print("CALIBRATION")
    print("=" * 60)
    print()
    print("انگشت اشاره را روی دایره قرار بده.")
    print("حدود نیم ثانیه ثابت نگه دار.")
    print()

    window = "Air Mouse Calibration"

    cv2.namedWindow(
        window,
        cv2.WINDOW_NORMAL
    )

    cv2.setWindowProperty(
        window,
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN
    )

    margin_x = int(
        SCREEN_WIDTH * 0.12
    )

    margin_y = int(
        SCREEN_HEIGHT * 0.12
    )

    targets = [

        (
            margin_x,
            margin_y
        ),

        (
            SCREEN_WIDTH - margin_x,
            margin_y
        ),

        (
            SCREEN_WIDTH - margin_x,
            SCREEN_HEIGHT - margin_y
        ),

        (
            margin_x,
            SCREEN_HEIGHT - margin_y
        )
    ]

    camera_points = []

    screen_points = []

    current = 0

    stable = 0

    while current < 4:

        ret, frame = cap.read()

        if not ret:
            continue

        if MIRROR_CAMERA:

            frame = cv2.flip(
                frame,
                1
            )

        h, w = frame.shape[:2]

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = hands.process(
            rgb
        )

        display = np.zeros(
            (
                SCREEN_HEIGHT,
                SCREEN_WIDTH,
                3
            ),
            dtype=np.uint8
        )

        target = targets[current]

        cv2.circle(
            display,
            target,
            35,
            (255, 255, 255),
            -1
        )

        cv2.circle(
            display,
            target,
            12,
            (0, 0, 0),
            -1
        )

        cv2.putText(
            display,
            f"CALIBRATION {current + 1}/4",
            (40, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            (255, 255, 255),
            3
        )

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            points = get_points(
                hand,
                w,
                h
            )

            index = points[8]

            px = int(
                index[0]
                / w
                * SCREEN_WIDTH
            )

            py = int(
                index[1]
                / h
                * SCREEN_HEIGHT
            )

            px = clamp(
                px,
                0,
                SCREEN_WIDTH - 1
            )

            py = clamp(
                py,
                0,
                SCREEN_HEIGHT - 1
            )

            cv2.circle(
                display,
                (px, py),
                15,
                (255, 255, 255),
                -1
            )

            stable += 1

            if stable >= 20:

                camera_points.append(
                    [
                        index[0],
                        index[1]
                    ]
                )

                screen_points.append(
                    [
                        target[0],
                        target[1]
                    ]
                )

                print(
                    "Calibration point:",
                    current + 1
                )

                current += 1

                stable = 0

                time.sleep(
                    0.3
                )

        else:

            stable = 0

        cv2.imshow(
            window,
            display
        )

        key = cv2.waitKey(1) & 0xFF

        if key == 27:

            cv2.destroyWindow(
                window
            )

            return False

    camera_points = np.array(
        camera_points,
        dtype=np.float32
    )

    screen_points = np.array(
        screen_points,
        dtype=np.float32
    )

    calibration_matrix = \
        cv2.getPerspectiveTransform(
            camera_points,
            screen_points
        )

    cv2.destroyWindow(
        window
    )

    print()
    print("Calibration completed.")
    print()

    return True


# ============================================================
# GLOBAL KEYBOARD
# ============================================================

def keyboard_listener():

    global running
    global mouse_enabled

    previous_f8 = False
    previous_esc = False

    while running:

        f8 = bool(
            ctypes.windll.user32.GetAsyncKeyState(
                0x77
            )
            &
            0x8000
        )

        esc = bool(
            ctypes.windll.user32.GetAsyncKeyState(
                0x1B
            )
            &
            0x8000
        )

        if f8 and not previous_f8:

            mouse_enabled = \
                not mouse_enabled

            reset_click_state()

            print(
                "Mouse:",
                "ON"
                if mouse_enabled
                else
                "OFF"
            )

        if esc and not previous_esc:

            running = False

            reset_click_state()

        previous_f8 = f8

        previous_esc = esc

        time.sleep(
            0.03
        )


# ============================================================
# MAIN
# ============================================================

def main():

    global running

    global fps
    global fps_counter
    global fps_timer

    global last_mouse_x
    global last_mouse_y

    print()
    print("=" * 60)
    print("AIR MOUSE")
    print("=" * 60)
    print()
    print("Controls:")
    print("  C   = Calibration")
    print("  F8  = Mouse ON/OFF")
    print("  ESC = Exit")
    print()
    print("Gestures:")
    print("  INDEX          = Move")
    print("  PINCH          = Left Click")
    print("  TWO FINGERS + PINCH = Right Click")
    print()
    print("Starting camera...")
    print()

    # ========================================================
    # CAMERA
    # ========================================================

    cap = cv2.VideoCapture(
        CAMERA_INDEX,
        cv2.CAP_DSHOW
    )

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        CAMERA_WIDTH
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        CAMERA_HEIGHT
    )

    cap.set(
        cv2.CAP_PROP_FPS,
        60
    )

    if not cap.isOpened():

        print(
            "ERROR: Cannot open camera."
        )

        return

    # ========================================================
    # MEDIAPIPE
    # ========================================================

    hands = mp_hands.Hands(

        static_image_mode=False,

        max_num_hands=1,

        model_complexity=1,

        min_detection_confidence=0.60,

        min_tracking_confidence=0.60
    )

    # ========================================================
    # GLOBAL KEYBOARD THREAD
    # ========================================================

    keyboard_thread = threading.Thread(
        target=keyboard_listener,
        daemon=True
    )

    keyboard_thread.start()

    # ========================================================
    # CAMERA WINDOW
    # ========================================================

    window = "Air Mouse"

    cv2.namedWindow(
        window,
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        window,
        1280,
        720
    )

    print()
    print("Camera started.")
    print()
    print("C = Calibration")
    print("F8 = Mouse ON/OFF")
    print("ESC = Exit")
    print()

    # ========================================================
    # LOOP
    # ========================================================

    while running:

        ret, frame = cap.read()

        if not ret:

            continue

        if MIRROR_CAMERA:

            frame = cv2.flip(
                frame,
                1
            )

        height, width = frame.shape[:2]

        # ====================================================
        # FPS
        # ====================================================

        fps_counter += 1

        elapsed = (
            time.time()
            -
            fps_timer
        )

        if elapsed >= 1:

            fps = (
                fps_counter
                /
                elapsed
            )

            fps_counter = 0

            fps_timer = time.time()

        # ====================================================
        # MEDIAPIPE
        # ====================================================

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = hands.process(
            rgb
        )

        gesture = "NONE"

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            points = get_points(
                hand,
                width,
                height
            )

            mp_drawing.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            (
                index_open,
                middle_open,
                ring_open,
                pinky_open
            ) = get_fingers(
                points
            )

            pinch = pinch_ratio(
                points
            )

            index_tip = points[8]

            # =================================================
            # TWO FINGERS
            # =================================================

            two_fingers = (

                index_open

                and middle_open

                and not ring_open

                and not pinky_open
            )

            # =================================================
            # RIGHT CLICK
            # =================================================

            if two_fingers:

                if pinch <= PINCH_THRESHOLD:

                    gesture = "RIGHT CLICK"

                    if mouse_enabled:

                        screen_x, screen_y = \
                            camera_to_screen(
                                index_tip[0],
                                index_tip[1]
                            )

                        move_mouse(
                            screen_x,
                            screen_y
                        )

                        right_click(
                            pinch
                        )

                else:

                    gesture = "TWO FINGERS"

                    right_pinch_frames = 0

                    right_triggered = False

            # =================================================
            # LEFT CLICK
            # =================================================

            else:

                if pinch <= PINCH_THRESHOLD:

                    gesture = "LEFT CLICK"

                    if mouse_enabled:

                        left_click(
                            pinch
                        )

                else:

                    # MOVE
                    gesture = "MOVE"

                    left_pinch_frames = 0

                    left_triggered = False

                    if mouse_enabled:

                        screen_x, screen_y = \
                            camera_to_screen(
                                index_tip[0],
                                index_tip[1]
                            )

                        move_mouse(
                            screen_x,
                            screen_y
                        )

            # =================================================
            # DEBUG
            # =================================================

            cv2.circle(
                frame,
                index_tip,
                14,
                (255, 255, 255),
                -1
            )

            cv2.putText(
                frame,
                f"Gesture: {gesture}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Pinch: {pinch:.2f}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Index: {'OPEN' if index_open else 'CLOSED'}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Middle: {'OPEN' if middle_open else 'CLOSED'}",
                (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

        else:

            reset_click_state()

        # ====================================================
        # STATUS
        # ====================================================

        status = (
            "MOUSE: ON"
            if mouse_enabled
            else
            "MOUSE: OFF"
        )

        cv2.putText(
            frame,
            status,
            (
                20,
                height - 60
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (
                20,
                height - 25
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "C: Calibration | F8: ON/OFF | ESC: Exit",
            (
                20,
                height - 95
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        # ====================================================
        # SHOW
        # ====================================================

        if SHOW_CAMERA:

            cv2.imshow(
                window,
                frame
            )

        # ====================================================
        # WINDOW KEYBOARD
        # ====================================================

        key = cv2.waitKey(1) & 0xFF

        if key == ord("c") or key == ord("C"):

            reset_click_state()

            calibrate(
                cap,
                hands
            )

            last_mouse_x = None

            last_mouse_y = None

        elif key == 27:

            running = False

    # ========================================================
    # CLEANUP
    # ========================================================

    reset_click_state()

    cap.release()

    hands.close()

    cv2.destroyAllWindows()

    print()
    print("Air Mouse stopped.")
    print()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        running = False

        reset_click_state()

        try:

            pyautogui.mouseUp(
                button="left"
            )

            pyautogui.mouseUp(
                button="right"
            )

        except:
            pass

        cv2.destroyAllWindows()

        print()
        print("Stopped by user.")

    except Exception as e:

        running = False

        reset_click_state()

        try:

            pyautogui.mouseUp(
                button="left"
            )

            pyautogui.mouseUp(
                button="right"
            )

        except:
            pass

        try:

            cv2.destroyAllWindows()

        except:
            pass

        print()
        print("=" * 60)
        print("ERROR")
        print("=" * 60)
        print(e)
        print()

        input("Press Enter to exit...")