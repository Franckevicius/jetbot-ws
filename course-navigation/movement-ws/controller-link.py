from evdev import list_devices, InputDevice, categorize, ecodes
from robot import Robot

STICK_MAX = 65536
CENTER_TOLERANCE_NORM = 0.15
BUTTON_CODE_A = 304
BUTTON_CODE_B = 305
BUTTON_CODE_X = 306
BUTTON_CODE_Y = 307
GEAR_1_MULT = 0.2
GEAR_2_MULT = 0.4
GEAR_3_MULT = 0.6
GEAR_4_MULT = 0.8
GEAR_5_MULT = 1.0
GEAR_MULTS = [GEAR_1_MULT, GEAR_2_MULT, GEAR_3_MULT, GEAR_4_MULT, GEAR_5_MULT]
curr_gear_index = 0

def normalize_joystick(value):    
    return -((value-2**15)/2**15)

def increase_gear():
    return min(curr_gear_index + 1, len(GEAR_MULTS) - 1)

def decrease_gear():
    return max(curr_gear_index-1, 0)

robot = Robot()
dev = InputDevice( list_devices()[0] )
axis = {
    ecodes.ABS_X: 'ls_x', # 0 - 65,536   the middle is 32768
    ecodes.ABS_Y: 'ls_y',
    ecodes.ABS_Z: 'rs_x',
    ecodes.ABS_RZ: 'rs_y',
    ecodes.ABS_BRAKE: 'lt', # 0 - 1023
    ecodes.ABS_GAS: 'rt',

    ecodes.ABS_HAT0X: 'dpad_x', # -1 - 1
    ecodes.ABS_HAT0Y: 'dpad_y'
}

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.code == BUTTON_CODE_B:            
            robot.right_motor.value = 0
            robot.left_motor.value = 0 
            exit()
        elif event.code == BUTTON_CODE_X and event.value == 1:
            curr_gear_index = decrease_gear()
            print("curr_gear_index:", curr_gear_index)
        elif event.code == BUTTON_CODE_Y and event.value == 1:
            curr_gear_index = increase_gear()
            print("curr_gear_index:", curr_gear_index)     

    #read stick axis movement
    elif event.type == ecodes.EV_ABS:
        if axis[event.code] in ['ls_x', 'ls_y', 'rs_x', 'rs_y']:
            value_norm = normalize_joystick(event.value) * GEAR_MULTS[curr_gear_index]

            if axis[event.code] == 'rs_y':
                print('right')
                if abs(value_norm) <= CENTER_TOLERANCE_NORM:
                    robot.right_motor.value = 0
                else:
                    robot.right_motor.value = value_norm
                print(value_norm)

            elif axis[event.code] == 'ls_y':
                print("left")
                if abs(value_norm) <= CENTER_TOLERANCE_NORM:
                    robot.left_motor.value = 0
                else:
                    robot.left_motor.value = value_norm
                print(value_norm)
            