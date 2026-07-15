from typing import bytearray
from .device import Device

class Memory(Device):
	"""Basic Memory Device"""

	def __init__(self, name: str, size: int):
		super().__init__(name)
		self.size = size
		self._data = bytearray(size)

	def read(self, address: int, size: int = 1) -> bytes:
		self._check_bounds(address, size)
		return bytes(self._data[address:address+size])

	def write(self, address: int, data: bytes) -> None:
		self._check_bounds(address, len(data))
		self._data[address:address+len(data)] = data

	def _check_bounds(self, address: int, size: int) -> None:
		if address + size > self.size:
			raise MemoryError(f"Address {hex(address)} out of bounds")

	def reset(self) -> None:
		self._data = bytearray(self.size)