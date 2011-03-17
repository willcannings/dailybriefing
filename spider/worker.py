from threading import Thread
from lxml import html
import urllib2
import re

HEADING_TAGS  = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
CLEAN_REGEX   = re.compile("[\r\n\t ]+")
WORD_REGEX    = re.compile("[a-zA-Z0-9_+\.]+")
MIN_WORDS     = 20

class Worker(Thread):
  def __init__(self, queue, logger):
    Thread.__init__(self)
    self.queue = queue
    self.logger = logger
    self.running = True

  def run(self):
    self.logger.info("Worker starting")
    
    while(self.running):
      page = self.queue.get_page()      
      if page == None:
        continue
      self.logger.debug("Spidering: " + page.url)
      
      # attempt to download the page
      try:
        doc = html.parse(page.url)
      except IOError:
        self.logger.debug("Error retrieving: " + page.url)
        page.error()
        continue
      
      # extract the page title
      page.title = doc.xpath("//title")[0].text_content()
      
      # extract links
      self.queue.add_pages(doc.xpath("body//a[string(@href)]"), page)
      
      # completely remove script tags and other non text elements
      for code_tag in doc.xpath("body//script | body//object | body//map | body//iframe | body//button | body//noscript"):
        code_tag.drop_tree()
      
      # FIXME: the text of these elements needs to be wrapped in spaces since <p>one<b>two</b></p> will become <p>onetwo</p> otherwise
      # remove inline text tags so <p>one <b>two</b> three</p> becomes <p>one two three</p>
      for inline_tag in doc.xpath("body//a | body//b | body//i | body//u | body//em | body//strong | body//font | body//abbr | body//acronym | body//small | body//span | body//sub | body//sup | body//tt | body//var | body//strike | body//aside | body//section | body//code | body//cite | body//defn | body//big"):
        inline_tag.drop_tag()
        
      # blocks of text are relevant if they contain >= MIN words, or are contained in a heading element
      text_fragments = []
      for element in doc.xpath("body//*"):
        text = element.text_content()
        if (element.tag in HEADING_TAGS) or (len(WORD_REGEX.findall(text)) >= MIN_WORDS):
          text_fragments.append(CLEAN_REGEX.sub(' ', text))
      
      text = ' '.join(text_fragments)
      page.complete(text)
      self.queue.remove_page(page)
      self.logger.debug("Completed spidering: " + page.url)
        
    self.logger.info("Worker finishing")
