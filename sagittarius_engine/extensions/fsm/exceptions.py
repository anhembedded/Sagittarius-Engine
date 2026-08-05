class FSMError(Exception):
    """
    @brief Base exception class for all FSM-related errors.
    """
    pass


class InvalidStateTransitionError(FSMError):
    """
    @brief Raised when an invalid state transition is attempted.
    """
    def __init__(self, from_state: str, to_state: str):
        super().__init__(f"Invalid transition from '{from_state}' to '{to_state}'.")
        self.from_state = from_state
        self.to_state = to_state
