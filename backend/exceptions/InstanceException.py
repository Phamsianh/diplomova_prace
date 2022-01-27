from exceptions.ORMExceptions import ORMException


class InstanceException(ORMException):
    def __int__(self, message: str = None):
        self.message = message
        super(ORMException, self).__init__(self.message)


class CurrentPhaseNotResolved(InstanceException):
    def __init__(self, ins_cur_state: str):
        self.message = f"current phase has not been resolved. current state of this instance is {ins_cur_state}"
        super(CurrentPhaseNotResolved, self).__init__(self.message)


class NotAvailableNextPhases(InstanceException):
    def __init__(self, phase_id: int, ins_id: int, avl_nxt_phss: list):
        self.message = f"instance {ins_id} can not transit to phase {phase_id}. " \
                       f"instance can only transit to phase {', '.join([str(p.id) for p in avl_nxt_phss])}"
        super(NotAvailableNextPhases, self).__init__(self.message)


class CurrentlyNotRequireHandle(InstanceException):
    def __init__(self):
        self.message = "instance currently doesn't require to be handled."
        super(CurrentlyNotRequireHandle, self).__init__(self.message)
