from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16

CV_REF_NAME = 'cv-ref-chan'

class CV_REF(Structure):
	_pack_ = 1
	_fields_ = [("errX",    c_int16),
                ("errY",    c_int16)]
