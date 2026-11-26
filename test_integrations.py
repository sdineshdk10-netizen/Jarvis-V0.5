import unittest, asyncio
from integrations import select_tool,retrieve,execute
class Tests(unittest.TestCase):
 def test_time(self): self.assertEqual(select_tool('current time?'),'time')
 def test_gmail(self): self.assertEqual(select_tool('show my emails'),'gmail')
 def test_drive(self): self.assertEqual(select_tool('list my drive files'),'drive')
 def test_calendar(self): self.assertEqual(select_tool('show my calendar'),'calendar')
 def test_no_write(self): self.assertIsNone(select_tool('delete my emails'))
 def test_no_embedded(self): self.assertIsNone(select_tool('do not show my emails'))
 def test_memory(self): self.assertEqual(retrieve('DJ music',['office','DJ music'],1),['DJ music'])
 def test_clock(self): self.assertTrue(asyncio.run(execute('time')).endswith('+05:30'))
if __name__=='__main__': unittest.main()
