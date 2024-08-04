from circuitpython_mocks import monkey_patch_sys_paths  # noqa: F401 (1)
from circuitpython_mocks.busio.operations import (
    I2CRead,
    I2CWrite,
    I2CTransfer,
)


def test_i2c():
    import board
    from busio import I2C

    from adafruit_bus_device.i2c_device import I2CDevice

    address = 0x42
    # do setup
    with I2C(board.SCL, board.SDA) as i2c_bus:
        assert i2c_bus.scan() == []

        # set expectation for probing performed by I2CDevice.__init__()
        i2c_bus.expectations.append(I2CWrite(address, b""))
        # set expectations for I2C bus
        i2c_bus.expectations.extend(
            [
                I2CRead(address, bytearray(1)),
                I2CWrite(address, bytearray(1)),
                I2CTransfer(address, bytearray(1), bytearray(1)),
            ]
        )
        i2c_dev = I2CDevice(i2c_bus, device_address=address)

        # do test
        buf = bytearray(1)
        with i2c_dev as i2c:
            assert not i2c_bus.try_lock()
            i2c.readinto(buf, end=1)
        with i2c_dev as i2c:
            i2c.write(buf, end=1)
        with i2c_dev as i2c:
            i2c.write_then_readinto(buf, buf, out_end=1, in_end=1)
