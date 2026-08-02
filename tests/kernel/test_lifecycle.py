from sagittarius_engine.kernel.lifecycle import EngineLifecycle, EngineState, Lifecycle


def test_engine_lifecycle_states():
    lifecycle = EngineLifecycle(context=None)

    # Initial state
    assert lifecycle.state == EngineState.STOPPED
    assert lifecycle.is_stopped is True
    assert lifecycle.is_booting is False
    assert lifecycle.is_booted is False
    assert lifecycle.is_stopping is False

    # Booting
    lifecycle.set_booting()
    assert lifecycle.state == EngineState.BOOTING
    assert lifecycle.is_booting is True
    assert lifecycle.is_stopped is False

    # Booted
    lifecycle.set_booted()
    assert lifecycle.state == EngineState.BOOTED
    assert lifecycle.is_booted is True
    assert lifecycle.is_booting is False

    # Stopping
    lifecycle.set_stopping()
    assert lifecycle.state == EngineState.STOPPING
    assert lifecycle.is_stopping is True
    assert lifecycle.is_booted is False

    # Stopped
    lifecycle.set_stopped()
    assert lifecycle.state == EngineState.STOPPED
    assert lifecycle.is_stopped is True
    assert lifecycle.is_stopping is False


def test_engine_state_enum_values():
    assert EngineState.STOPPED.value == "stopped"
    assert EngineState.BOOTING.value == "booting"
    assert EngineState.BOOTED.value == "booted"
    assert EngineState.STOPPING.value == "stopping"


def test_lifecycle_initial_state():
    lifecycle = Lifecycle(context=None)
    assert lifecycle._state == "created"
