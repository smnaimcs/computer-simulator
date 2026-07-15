from abc import ABC, abstractmethod
from typing import Optional, Any
import logging

class Device
(ABC):
	"""Base class for all computer devices"""

	def __init__(self, name: str):
		self.name = name
		self.logger = logging.getLogger(f"device.{name}")
		self.enabled = True

	@abstractmethod
	def read(self, address: int, size: int = 1) -> bytes:
		"""Read data from device"""
		pass

	@abstractmethod
	def write(self, address: int, data: bytes) -> None:
		"""Write data to device"""
		pass

	@abstractmethod
	def reset(self) -> None:
		"""Reset device to initial state"""
		pass

	def interrupt(self) -> Optional[int]:
		"""Return interrupt if device needs attention"""
		return None

	def tick(self, cycle: int) -> None:
		"""Called each clock cycle"""
		pass