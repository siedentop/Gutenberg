import unittest
import main

class TestMain(unittest.TestCase):
	def setUp(self):
		self.book = main.Book(book_id=2418)
		
	def testGenerateURI(self):
		# make sure the generated uri is correct
		original = 'http://gutenberg.spiegel.de/?id=12&xid=2418&kapitel=2'
		kapitel = 2
		self.assertEqual(original, self.book.generate_uri(kapitel))
		
	def test_script_remove(self):
		html_mockup = 'This is a test string with some <script nuisannce> in it. </script> The text continues here. '
		html_cleaned = 'This is a test string with some  The text continues here. '
		self.assertEqual(main.remove_script(html_mockup), html_cleaned)
		
		
if __name__=='__main__':
	unittest.main()