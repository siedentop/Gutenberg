import urllib2
from BeautifulSoup import BeautifulSoup

def remove_script(html):
	# removes everything (including the tag itself) between '<script' and '</script'
	# Only the first <script> block is included.
	splits =  html.split('<script')
	front = splits[0]
	back = ''.join(splits[1:])
	back = ''.join(back.split('</script>')[1:])
	return front + back
	


	

class Book():
	def __init__(self, book_id):
		self.base_url = 'http://gutenberg.spiegel.de/'
		self.book_id = book_id
		
	def download(self):
		self.filename_tmp = 'gutenberg_book_%d.html.tmp' % self.book_id
		fh = open(self.filename_tmp, 'w')
		for chapter in self.chapters():
			fh.write(str(chapter))
		fh.close()
			
	def chapters(self):
		chapter = 1
		while True:
			content = self.get_chapter(chapter)
			if content == None:
				break
			yield content
			chapter += 1
			
	def get_chapter(self, chapter):
		uri = self.generate_uri(chapter=chapter)
		soup = self.get_soup(uri)
		content = soup.find('div', id='gb_texte')
		return content
			
	def get_soup(self, chapter):
		uri = self.generate_uri(chapter)
		response = urllib2.urlopen(uri)
		html = remove_script(response.read())
		return BeautifulSoup(html)
		
	def generate_uri(self, chapter):
		id = 12 # The id-parameter determines which page is called. 12 is "printable", 5 is standard text
		return self.base_url + '?id=' + str(id) + '&xid=' + str(self.book_id) + '&kapitel=' + str(chapter)
	
	def save_as(self, filename):
		if not self.filename_tmp:
			self.download()
		in_file = open(self.filename_tmp, 'r')
		out_file = open(filename, 'w')
		header = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="%sfileadmin/gb_css/prosa.css" />
</head>
<body>
<div id=gb_contentl>''' % (self.base_url)
		footer = '''</div>
</body>
</html>'''
		out_file.write(header)
		out_file.write(in_file.read()) 
		out_file.write(footer)
		out_file.close()
		
		
	def __del__(self):
		#Implement something to delete the self.filename_tmp file.
		pass

if __name__=='__main__':
	book = Book(book_id = 2418)
	#book.download()
	book.filename_tmp = 'gutenberg_book_2418.html.tmp'
	book.save_as('Kabale_und_Liebe.html')