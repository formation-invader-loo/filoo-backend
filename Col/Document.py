import sys
sys.path.append('/workspaces/IOL/IOLBackendv2')
from utils.Logger import logger

import markdown
import os
import hashlib

md_converter = markdown.Markdown(extensions=['meta'])

class Document:
  """A Document is a md File with metadata containing information about location of file and resources etc.
  """

  def __init__(self, document_path: str, qualified_name: str, html_dir: str) -> None:
    self.name = os.path.basename(document_path)
    self.qualified_name = qualified_name
    self.document_path = document_path
    self.doc_hash = self.create_doc_hash()
    self.doc_mod_time = os.path.getmtime(self.document_path)
    self.html_dir = html_dir
    self.doc_meta = self.loadMetaData()
    self.resources_path = self.doc_meta['resources'] if 'resources' in self.doc_meta.keys() else None # is this needed??
    self.html_file = self.load_http_from_md()

  
  def create_doc_hash(self):
    with open(self.document_path, 'r') as doc:
      h = hashlib.sha1(doc.read().encode('utf-8'))
      return h.hexdigest()   

  
  def load_http_from_md(self) -> str:
        """convertes the md doc in html and stores it in a file. The dir of the file is determined by the Collection

        Returns:
            str: path to html file that resembles the md file
        """
        with open(self.document_path, 'r', encoding='utf-8') as f:
            temp = f.read()
        temp = md_converter.convert(temp)

        path = self.qualified_name.split('/')
        if len(path) > 1:
            path = '/'.join(path[:len(path)-1])
        else:
            path = ''
        path = '/' + path + '/'

        os.makedirs(self.html_dir + path, exist_ok=True)
        html_file = self.name[:len(self.name) - 2] + 'html'

        with open(self.html_dir + path + html_file, 'w') as f:
            f.write(temp)
            logger.debug(f'{Document.load_http_from_md.__qualname__} wrote into {html_file}:\n {temp}')
        
        return self.html_dir + path + html_file
  

  def loadMetaData(self):
    md_converter.reset()
    with open(self.document_path, 'r', encoding='utf-8') as f:
        temp_md = f.read()
    temp_md = md_converter.convert(temp_md)

    logger.debug(f'{Document.loadMetaData.__qualname__} loaded from {self.qualified_name}: {md_converter.Meta}')
    return md_converter.Meta # pylint: disable=fixme, no-member


  def __str__(self) -> str:
      return f''' Document({self.name})
        qualified_name = {self.qualified_name}
        document_path = {self.document_path}
        self.doc_hash = {self.doc_hash}
        html_dir = {self.html_dir}
        doc_meta = {self.doc_meta}
        resources_path = {self.resources_path}
        html_file = {self.html_file}
        '''
  

  def __repr__(self):
    return str(self)