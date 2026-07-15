class ComputerError(Exception):
	pass

class BusError(ComputerError):
	pass

class DeviceNotFoundError(ComputerError):
	pass

class MemoryError(ComputerError):
	pass

class CPUError(ComputerError):
	pass

class HaltError(CPUError):
	pass