from enum import Enum
from typing import Dict, Optional, Any
from dataclasses import dataclass

class PipelineStage(Enum):
	FETCH = "fetch"
	DECODE = "decode"
	EXECUTE = "execute"
	MEMORY = "memory"
	WRITEBACK = "writeback"

@dataclass
class Instruction:
	"""Represents an instruction in the pipeline"""
	opcode: int
	operands: list
	address: int
	stage: PipelineStage = PipelineStage.FETCH

	def __repr__(self):
		return f"Inst(op={self.opcode:#x}, addr={self.address:#x}, stage={self.stage.value})"

class Pipeline:
	"""Simple 5-stage pipeline with hazard detection"""

	def __init__(self, depth: int = 5):
		self.depth = depth
		self.stages = {
			PipelineStage.FETCH: None,
			PipelineStage.DECODE: None,
			PipelineStage.EXECUTE: None,
			PipelineStage.MEMORY: None,
			PipelineStage.WRITEBACK: None,
		}
		self.stalls = 0
		self.flushes = 0

	def advance(self) -> Dict[PipelineStage, Optional[Instruction]]:
		"""Advance pipeline one cycle, return new stage contents"""

		old_stages = self.stages.copy()
		new_stages = {stage: None for stage in PipelineStage}

		new_stages[PipelineStage.WRITEBACK] = old_stages[PipelineStage.MEMORY]
		new_stages[PipelineStage.MEMORY] = old_stages[PipelineStage.EXECUTE]
		new_stages[PipelineStage.EXECUTE] = old_stages[PipelineStage.DECODE]
		new_stages[PipelineStage.DECODE] = old_stages[PipelineStage.FETCH]

		self.stages = new_stages
		return new_stages

	def stall(self, cycles: int = 1) -> None:
		"""Stall the pipeline for n cycles"""
		self.stalls += cycles
		# keep current instructions in place
		# (no advancement for stalled cycles)

	def flush(self) -> None:
		"""Flush the pipeline (e.g. on branch misprediction)"""
		self.flushes += 1
		for stage in self.stages:
			self.stages[stage] = None

	def insert(self, stage: PipelineStage, instruction: Optional[Instruction]) -> None:
		"""Insert an instruction into a specific stage"""
		self.stages[stage] = instruction

	def get_stage(self, stage: PipelineStage) -> Optional[Instruction]:
		"""Get Instruction at specific stage"""
		return self.stages.get(stage)

	def is_stalled(self) -> bool:
		"""Check if pipeline is stalled"""
		return self.stalls > 0

	def clear_stall(self) -> None:
		"""Clear one stall cycle"""
		if self.stalls > 0:
			self.stalls -= 1

	def is_empty(self) -> bool:
		"""Check if pipeline is empty"""
		return all(inst is None for inst in self.stages.values())

	def is_full(self) -> bool:
		"""check if pipeline is full"""
		return all(inst is not None for inst in self.stages.values())