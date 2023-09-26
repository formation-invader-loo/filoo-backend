import sys
sys.path.append('/workspaces/IOL/IOLBackendv2')
from utils.Logger import logger
from utils.configuration import get_config

import glob
import os

from Document import Document
from CollectionException import DocumentAlreadyExists, DocumentDoesNotExist

class Collection:
  """A collection is a Directory containing one or multiple Documents
  """
  def __init__(self, name: str) -> None:
    self.name = name
    self.data_dir = get_config('paths', 'data') + f'/collections/{self.name}'
    self.html_dir = get_config('paths', 'html') + f'/collections/{self.name}'
    self.documents = self.load_documents()

  def load_documents(self) -> dict[Document]:
    """Load all (md)files in the library and parse them into html files in the html_dir

    Returns:
        [str]: List of all files in the library
    """
    documents: dict[str, Document] = {}
    md_files: list[str] = []

    md_files = glob.glob('**/*.md', recursive=True, root_dir=self.data_dir)
    logger.info(f'{Collection.load_documents.__qualname__} found: {[f.__str__() for f in md_files]}')

    for md_file in md_files: # create Document instance
      if md_file in documents.keys():
        raise DocumentAlreadyExists(f'{Collection.load_documents.__qualname__}: A instance of {md_file} already exists.')
      documents[md_file] = Document(self.data_dir + '/' + md_file, md_file, self.html_dir)
            
    return documents
  

  def get_document(self, document_qualified_name: str) -> Document:
    document: Document = {}
    try:
      document = self.documents[document_qualified_name]
    except KeyError as e:
      raise DocumentDoesNotExist(f'{document_qualified_name} does not exist.')
    return document


  def add_document(self, document_qualified_name: str, document_content: str):
    abs_file_path = self.data_dir + '/' + document_qualified_name
    if os.path.isfile(abs_file_path):
       raise DocumentAlreadyExists(f'Document with qualified name {document_qualified_name} already exists.')
    
    path = abs_file_path.split('/')
    path = '/'.join(path[:len(path)-1])

    os.makedirs(path, exist_ok=True)
    with open(abs_file_path, 'w') as new_file:
      new_file.write(document_content)
      logger.debug(f'{Collection.add_document.__qualname__} wrote into {document_qualified_name} ({abs_file_path}):\n{document_content}')
    
    self.documents.append(Document(abs_file_path, document_qualified_name, self.html_dir))
       

  def document_list(self) -> list[str]:
    """List of documents in this Collection instance.

    Returns:
        list[str]: list of the qualified names in the Collection instance
    """
    return [d.qualified_name for d in self.documents.values()]
  

  def __str__(self) -> str:
    return f'Collection: [ name: {self.name} , data_dir = {self.data_dir}, html_dir = {self.html_dir}, documents = {self.documents}'
  
  def __repr__(self):
    return str(self)