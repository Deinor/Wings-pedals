import board
import busio
from adafruit_tca9548a import TCA9548A
from adafruit_as5600 import AS5600
from joystick_xl.inputs import Axis
from joystick_xl.joystick import Joystick

# Initialize I2C bus
i2c = busio.I2C(board.GP5, board.GP4)

# Initialize TCA9548A multiplexer
tca = TCA9548A(i2c)

# Initialize AS5600 sensors on different channels corespondnig to pins on TCA9548A
rudder_sensor = AS5600(tca[7])
left_brake_sensor = AS5600(tca[6])
right_brake_sensor = AS5600(tca[5])

# Function to read the angle from AS5600 sensor and normalize it, for higher accuracy angle value[x.xxx] * 1000
def get_encoder_value(sensor):
    angle = sensor.angle
    normalized_value = int(round(float((angle / 4096.0) * 255), 3) * 1000)
    return normalized_value

# Set up minimum and maximum values corespodning to normalized values at extremes 
AXIS_MIN_lb = 131000  # Minimum raw axis value.
AXIS_MIN_rb = 50000  # Minimum raw axis value.
AXIS_MIN_ru = 73960  # Minimum raw axis value.
AXIS_MAX_lb = 164000  # Maximum raw axis value.
AXIS_MAX_rb = 83000  # Maximum raw axis value.
AXIS_MAX_ru = 114560  # Maximum raw axis value.

rudder_peddals = Joystick()

rudder_peddals.add_input(
    Axis(min=AXIS_MIN_ru, max=AXIS_MAX_ru, invert=False),
    Axis(min=AXIS_MIN_lb, max=AXIS_MAX_lb, invert=True),
    Axis(min=AXIS_MIN_rb, max=AXIS_MAX_rb, invert=False),
)

while True:    
    rudder_peddals.axis[0].source_value = get_encoder_value(rudder_sensor)
    rudder_peddals.axis[1].source_value = get_encoder_value(left_brake_sensor)
    rudder_peddals.axis[2].source_value = get_encoder_value(right_brake_sensor)
    
    rudder_peddals.update()