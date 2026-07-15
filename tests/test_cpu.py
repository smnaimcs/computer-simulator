import unittest
from cpu.registers import RegisterFile, Register
from cpu.alu import ALU

class TestRegisters(unittest.TestCase):
    def test_register_basic(self):
        reg = Register("test", 32)
        reg.value = 42
        self.assertEqual(reg.value, 42)
        reg.value = -1
        self.assertEqual(reg.value, 0xFFFFFFFF)  # 32-bit wrap
    
    def test_register_file(self):
        rf = RegisterFile()
        rf.set("R0", 100)
        self.assertEqual(rf.get("R0"), 100)
        rf.set("PC", 0x1000)
        self.assertEqual(rf.get("PC"), 0x1000)
        
        rf.set_flag("Z", True)
        self.assertTrue(rf.get_flag("Z"))

class TestALU(unittest.TestCase):
    def setUp(self):
        self.alu = ALU(32)
    
    def test_add(self):
        result, carry, overflow, zero = self.alu.add(5, 3)
        self.assertEqual(result, 8)
        self.assertFalse(carry)
        self.assertFalse(overflow)
        self.assertFalse(zero)
    
    def test_add_overflow(self):
        result, carry, overflow, zero = self.alu.add(0x7FFFFFFF, 1)
        self.assertTrue(overflow)
    
    def test_sub(self):
        result, borrow, overflow, zero = self.alu.sub(10, 3)
        self.assertEqual(result, 7)
        self.assertFalse(borrow)
    
    def test_sub_borrow(self):
        result, borrow, overflow, zero = self.alu.sub(3, 10)
        self.assertTrue(borrow)
        self.assertEqual(result, 0xFFFFFFF9)

if __name__ == '__main__':
    unittest.main()