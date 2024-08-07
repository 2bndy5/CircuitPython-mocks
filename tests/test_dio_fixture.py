from circuitpython_mocks.digitalio.operations import SetState, GetState

pytest_plugins = ["circuitpython_mocks.fixtures"]


def test_dio(mock_blinka_imports):
    from digitalio import DigitalInOut, Direction
    import board

    with DigitalInOut(board.D42) as dio:
        assert dio.direction == Direction.INPUT
        assert dio.pull is None

        # set expectations for the pin state changes
        dio.expectations.append(GetState(True))
        assert dio.value
        dio.expectations.extend([SetState(False), SetState(True)])
        dio.switch_to_output()
        dio.value = True

        # assert all expectation were used
        dio.done()
