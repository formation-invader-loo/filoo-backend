import sys
sys.path.append('/workspaces/IOL/IOLBackendv2')
from utils.Logger import logger
from utils.configuration import get_config

import glob
import os
import uuid
import configparser

from Col.Document import Document
from Col.CollectionException import DocumentAlreadyExists, DocumentDoesNotExist

class Collection:
  """A collection is a Directory containing one or multiple Documents
  """
  def __init__(self, name: str) -> None:
    self.name = name
    self.uuid = 0 # may needed later like if name of collection is changed...
    self.data_dir = get_config('paths', 'data') + f'/collections/{self.name}'
    self.html_dir = get_config('paths', 'html') + f'/collections/{self.name}'
    self.collectionfile = self.data_dir + '/.collectionfile'

    if os.path.isfile(self.collectionfile):
      self.load_collectionfile()
    else:
      self.create_collectionfile()

    self.documents: dict[str, Document] = self.load_documents()


  def load_collectionfile(self):
    config_object = configparser.ConfigParser()
    with open(self.collectionfile, 'r') as file_object:
      config_object.read_file(file_object)
      self.uuid = config_object.get('general', 'uuid')

  
  def create_collectionfile(self):
    config = configparser.ConfigParser()
    self.uuid = uuid.uuid4()
    config.add_section('general')
    config.set('general', 'name', self.name) 
    config.set('general', 'uuid', str(self.uuid))
    config.add_section('documents')

    with open(self.collectionfile, 'w') as collection_file:
      config.write(collection_file)
      

  def load_documents(self) -> dict[Document]:
    """Load all (md)files in the library and parse them into html files in the html_dir

    Returns:
        [str]: List of all files in the library
    """
    documents: dict[str, Document] = {}
    md_files: list[str] = []

    md_files = glob.glob('**/*.md', recursive=True, root_dir=self.data_dir)
    logger.info(f'{Collection.load_documents.__qualname__} found: {[f.__str__() for f in md_files]}')

    config_object = configparser.ConfigParser()
    with open(self.collectionfile, 'r') as file_object:
      config_object.read_file(file_object)
      collection_file_set = set([doc for doc in config_object['documents']])
      md_set = set(md_files) 
      if not collection_file_set == md_set:
        logger.warning(f'the files listed in the collectionfile and files in data are not the same:\ncollectionfile: {collection_file_set}\nfiles from data: {md_set}')
        config = configparser.ConfigParser()
        config.add_section('general')
        config.set('general', 'name', self.name) 
        config.set('general', 'uuid', str(self.uuid))
        config.add_section('documents')
        with open(self.collectionfile, 'w') as collection_file:
          config.write(collection_file)
        logger.warning('A new collectionfile was created.')

    for md_file in md_files: # create Document instance
      doc = {}
      if md_file in documents.keys():
        raise DocumentAlreadyExists(f'{Collection.load_documents.__qualname__}: A instance of {md_file} already exists.')
      doc = Document(self.data_dir + '/' + md_file, md_file, self.html_dir)
      documents[md_file] = doc
      self.load_index(doc)
    
    return documents

  
  def load_index(self, doc: Document):
    config_object = configparser.ConfigParser()
    with open(self.collectionfile, 'r') as file_object:
      config_object.read_file(file_object)
      try:
        index = config_object.get('documents', doc.qualified_name)
        logger.debug(f'{doc.qualified_name} did exist in {self.collectionfile}: {index}.')
        index = index.split(';')
        hash = index[0]
        mod_time = float(index[1])
        if hash != doc.doc_hash:
          logger.info(f'The hash of {doc.qualified_name} was different. Updatet: {hash} => {doc.doc_hash}.')
        if mod_time != doc.doc_mod_time:
          logger.info(f'The las modified time of {doc.qualified_name} was different. Updatet: {mod_time} => {doc.doc_mod_time}.')
        config_object.set('documents', doc.qualified_name, f'{doc.doc_hash};{doc.doc_mod_time}')
      except configparser.NoOptionError:
        logger.info(f'The index of {doc.qualified_name} did not exist. Updatet: {doc.doc_hash};{doc.doc_mod_time}.')
        config_object.set('documents', doc.qualified_name, f'{doc.doc_hash};{doc.doc_mod_time}') 

    with open(self.collectionfile, 'w') as new_file_object:
      config_object.write(new_file_object)
  

  def get_document(self, document_qualified_name: str) -> Document:
    document: Document = {}
    try:
      document = self.documents[document_qualified_name]
    except KeyError as e:
      raise DocumentDoesNotExist(f'{document_qualified_name} does not exist.')
    return document
  

  def delete_document(self, document_qualified_name: str) -> Document:
    document: Document = {}
    try:
      document = self.documents[document_qualified_name]
    except KeyError as e:
      raise DocumentDoesNotExist(f'{document_qualified_name} does not exist.')
    os.remove(document.document_path)
    del self.documents[document_qualified_name]


  def add_document(self, document_qualified_name: str):
    abs_file_path = self.data_dir + '/' + document_qualified_name
    if os.path.isfile(abs_file_path):
       raise DocumentAlreadyExists(f'Document with qualified name {document_qualified_name} already exists.')
    
    path = abs_file_path.split('/')
    path = '/'.join(path[:len(path)-1])

    file_name = document_qualified_name.rsplit('/', 1)
    file_name = file_name[1] if len(file_name) > 1 else file_name[0]

    os.makedirs(path, exist_ok=True)
    src = os.path.join(get_config('paths', 'uploads'), file_name)
    os.replace(src, abs_file_path)
    logger.debug(f'{Collection.add_document.__qualname__} copied {document_qualified_name} ({abs_file_path}) from uploads folder.')

    doc = Document(abs_file_path, document_qualified_name, self.html_dir)
    self.load_index(doc)
    
    self.documents[document_qualified_name] = (doc)
       

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