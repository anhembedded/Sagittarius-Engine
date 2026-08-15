import threading
from enum import Enum

import pytest

from sagittarius_engine.extensions.fsm import (
    BaseStateMachine,
    InvalidStateTransitionError,
)


class DoorState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    LOCKED = "LOCKED"


def test_fsm_initial_state():
    fsm = BaseStateMachine[DoorState](DoorState.CLOSED)
    assert fsm.current_state == DoorState.CLOSED


def test_fsm_invalid_initial_state():
    with pytest.raises(TypeError):
        BaseStateMachine[DoorState]("NOT_AN_ENUM")


def test_valid_transitions():
    fsm = BaseStateMachine[DoorState](DoorState.CLOSED)
    fsm.add_transition(DoorState.CLOSED, DoorState.OPEN)
    fsm.add_transition(DoorState.OPEN, DoorState.CLOSED)

    assert fsm.transition_to(DoorState.OPEN) is True
    assert fsm.current_state == DoorState.OPEN

    assert fsm.transition_to(DoorState.CLOSED) is True
    assert fsm.current_state == DoorState.CLOSED


def test_invalid_transitions():
    fsm = BaseStateMachine[DoorState](DoorState.CLOSED)
    fsm.add_transition(DoorState.CLOSED, DoorState.OPEN)

    with pytest.raises(InvalidStateTransitionError) as exc_info:
        fsm.transition_to(DoorState.LOCKED)

    assert exc_info.value.from_state == "CLOSED"
    assert exc_info.value.to_state == "LOCKED"
    assert "Invalid transition from 'CLOSED' to 'LOCKED'" in str(exc_info.value)

    # State should remain unchanged
    assert fsm.current_state == DoorState.CLOSED


def test_lifecycle_hooks():
    fsm = BaseStateMachine[DoorState](DoorState.CLOSED)
    fsm.add_transition(DoorState.CLOSED, DoorState.OPEN)

    enter_called = False
    exit_called = False

    def on_enter_open():
        nonlocal enter_called
        enter_called = True

    def on_exit_closed():
        nonlocal exit_called
        exit_called = True

    fsm.on_enter(DoorState.OPEN, on_enter_open)
    fsm.on_exit(DoorState.CLOSED, on_exit_closed)

    fsm.transition_to(DoorState.OPEN)

    assert enter_called is True
    assert exit_called is True


def test_global_transition_hook():
    fsm = BaseStateMachine[DoorState](DoorState.CLOSED)
    fsm.add_transition(DoorState.CLOSED, DoorState.OPEN)

    global_hook_called = False
    recorded_old = None
    recorded_new = None

    def global_hook(old_st: DoorState, new_st: DoorState):
        nonlocal global_hook_called, recorded_old, recorded_new
        global_hook_called = True
        recorded_old = old_st
        recorded_new = new_st

    fsm.add_global_callback(global_hook)

    fsm.transition_to(DoorState.OPEN)

    assert global_hook_called is True
    assert recorded_old == DoorState.CLOSED
    assert recorded_new == DoorState.OPEN


def test_thread_safety_spam():
    fsm = BaseStateMachine[DoorState](DoorState.CLOSED)
    fsm.add_transition(DoorState.CLOSED, DoorState.OPEN)
    fsm.add_transition(DoorState.OPEN, DoorState.CLOSED)

    def spam_transitions():
        try:
            for _ in range(100):
                current = fsm.current_state
                if current == DoorState.CLOSED:
                    fsm.transition_to(DoorState.OPEN)
                elif current == DoorState.OPEN:
                    fsm.transition_to(DoorState.CLOSED)
        except InvalidStateTransitionError:
            pass  # Expected if thread races on the transition logic, but state won't corrupt

    threads = [threading.Thread(target=spam_transitions) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # As long as it didn't throw uncaught exceptions and is in a valid state
    assert fsm.current_state in [DoorState.OPEN, DoorState.CLOSED]
