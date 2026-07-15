from typing import Dict, Optional

class Register:
    """Single register with bit width"""
    
    def __init__(self, name: str, width: int = 64):
        self.name = name
        self.width = width
        self._value = 0
    
    @property
    def value(self) -> int:
        return self._value
    
    @value.setter
    def value(self, val: int) -> None:
        mask = (1 << self.width) - 1
        self._value = val & mask
    
    def __repr__(self):
        return f"Register({self.name}, {hex(self._value)})"

class RegisterFile:
    """Collection of CPU registers"""
    
    def __init__(self):
        self.registers: Dict[str, Register] = {}
        self._init_registers()
    
    def _init_registers(self) -> None:
        # General purpose registers
        for i in range(32):
            self.registers[f"R{i}"] = Register(f"R{i}")
        
        # Special registers
        self.registers["PC"] = Register("PC")  # Program Counter
        self.registers["SP"] = Register("SP")  # Stack Pointer
        self.registers["FLAGS"] = Register("FLAGS", 32)
    
    def get(self, name: str) -> int:
        return self.registers[name].value
    
    def set(self, name: str, value: int) -> None:
        self.registers[name].value = value
    
    def get_flag(self, flag: str) -> bool:
        """Get specific flag value"""
        flags = self.registers["FLAGS"].value
        flag_positions = {
            "Z": 0,  # Zero
            "N": 1,  # Negative
            "C": 2,  # Carry
            "V": 3,  # Overflow
        }
        return bool(flags & (1 << flag_positions.get(flag, 0)))
    
    def set_flag(self, flag: str, value: bool) -> None:
        flag_positions = {
            "Z": 0, "N": 1, "C": 2, "V": 3
        }
        position = flag_positions.get(flag, 0)
        flags = self.registers["FLAGS"].value
        if value:
            flags |= (1 << position)
        else:
            flags &= ~(1 << position)
        self.registers["FLAGS"].value = flags
    
    def reset(self) -> None:
        for reg in self.registers.values():
            reg.value = 0