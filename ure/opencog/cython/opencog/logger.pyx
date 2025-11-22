from ure cimport ure_logger as c_ure_logger
from opencog.logger cimport wrap_clogger, cLogger

def ure_logger():
    cdef cLogger* logger_ptr = &c_ure_logger()
    z = wrap_clogger(logger_ptr)
    return z
