from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16

PID_REF_NAME = 'pid-ref-chan'

class PID_REF(Structure):
	_pack_ = 1
	_fields_ = [('move', c_double)]
