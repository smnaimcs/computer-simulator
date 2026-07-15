from typing import Dict, Optional, Any, Tuple
from .device import Device
from .exceptions import BusError, DeviceNotFoundError

class Bus:
	"""System bus connecting all devices"""

	def __inti__(self):
		self.devices: Dict[Any, Device] = {} # address -> device
		self.interrupt_lines: List[int] = []
		self.logger = logging.getLogger("bus")

	def attach_device(self, device: Device, base_address: int, size: int) -> None:
		"""Attach a device to the bus at a specific address range"""
		for addr in range(base_address, base_address+size):
			if addr in self.devices:
				raise BusError(f"Address {hex(addr)} already occupied")
			self.devices[addr] = device
		self.logger.info(f"Attached {device.name} at {hex(base_address)} size {size}")

	def read(self, address: int, size: int = 1) -> bytes:
		"""Read from the bus"""
		device = self._find_device(address)
		if not device:
			raise DeviceNotFoundError(f"No device at {hex(address)}")
		return device.read(address, size)

	def write(self, address: int, data: bytes) -> None:
		"""Write to the bus"""
		device = self._find_device(address)
		if not device:
			raise DeviceNotFoundError(f"No device at {hex(address)}")
		return device.write(address, data)

	def _find_device(self, address: int) -> Optional[Device]:
		return self.devices.get(address)

	def raise_interrupt(self, line: int) -> None:
		"""Raise an interrupt on a specific line"""
		if line not in self.interrupt_lines:
			self.interrupt_lines.append(line)

	def clear_interrupt(self, line: int) -> None:
		"""Clear an interrupt line"""
		if line in self.interrupt_lines:
			self.interrupt_lines.remove(line)

	def get_pending_interrupts(self) -> List[line]:
		"Get all pending interrupts"
		return self.interrupt_lines.copy()