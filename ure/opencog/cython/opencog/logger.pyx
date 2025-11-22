from ure cimport ure_logger as c_ure_logger
from opencog.logger cimport Logger, cLogger

def ure_logger():
    cdef Logger z = Logger.__new__(Logger)
    z.clog = &c_ure_logger()
    z.not_singleton_logger = False
    cdef cLogger* logger_ptr = &c_ure_logger()
    z = wrap_clogger(logger_ptr)
    return z
