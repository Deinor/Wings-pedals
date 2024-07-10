import time
import board
import busio
from adafruit_tca9548a import TCA9548A
from adafruit_as5600 import AS5600

# Initialize I2C bus
i2c = busio.I2C(board.GP5, board.GP4)

# Initialize TCA9548A multiplexer
tca = TCA9548A(i2c)

# Initialize AS5600 sensors on different channels
rudder_sensor = AS5600(tca[7])
left_brake_sensor = AS5600(tca[6])
right_brake_sensor = AS5600(tca[5])

# Function to read the angle from AS5600 sensor and normalize it
def get_encoder_value(sensor):
    angle = sensor.angle
    normalized_value = round(float((angle / 4096.0) * 255), 2)
    return normalized_value

while True:
    # Read sensor values
    rudder_value = get_encoder_value(rudder_sensor)
    left_brake_value = get_encoder_value(left_brake_sensor)
    right_brake_value = get_encoder_value(right_brake_sensor)
    print([rudder_value, right_brake_value, left_brake_value])
    # Delay to avoid spamming the USB bus
    time.sleep(0.2)
