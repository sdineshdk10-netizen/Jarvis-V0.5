import unittest
from voice import VoiceEngine
class Mock:
    def synthesize(self,text,*,language,voice):
        return f'{language}:{voice}:{text}'.encode()
class TestVoice(unittest.TestCase):
    def test_languages(self):
        for lang, reply in [('ta','வணக்கம்'),('en','Good afternoon'),('tanglish','Meeting எப்போது?')]:
            self.assertEqual(VoiceEngine(Mock(),'approved').speak(reply,lang),f'{lang}:approved:{reply}'.encode())
    def test_empty(self):
        with self.assertRaises(ValueError): VoiceEngine(Mock(),'approved').speak(' ')
    def test_language(self):
        with self.assertRaises(ValueError): VoiceEngine(Mock(),'approved').speak('hello','xx')
if __name__=='__main__': unittest.main()
