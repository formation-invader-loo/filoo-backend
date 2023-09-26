import sys
sys.path.append('/workspaces/IOL/IOLBackendv2')
from utils.Logger import logger

from Collection import Collection
from Document import Document
from CollectionException import CollectionDoesNotExist

class Collections:
  """Collections holds multiple Collection instances.
  """
  def __init__(self) -> None:
    self.collections = {}

  
  def get_document(self, collection_name: str, document_qualified_name) -> Document:
    collection: Collection = {}
    try:
      collection = self.collections.get(collection_name)
    except KeyError as e:
      raise CollectionDoesNotExist(f'Collection not found!\n{e}')
    
    collection.get_document(document_qualified_name)


  def add_collection(self, collection_name: str) -> None:
      self.collections.update({collection_name: Collection(collection_name)})

  
  def new_document(self, collection_name: str, document_qualified_name: str, document_content: str):
    collection: Collection = {}
    try:
      collection = self.collections.get(collection_name)
    except KeyError as e:
      raise CollectionDoesNotExist(f'Collection not found!\n{e}')
    
    collection.add_document(document_qualified_name, document_content)


  def collections_list(self) -> list[str]:
    """
    Returns:
        list[str]: List of all collection names
    """
    collection_list: list[Collection] = self.collections.values()
    return [c.name for c in collection_list]


  def collections_list_with_documents(self) -> dict[str, str]:
    """
    Returns:
        dict[str, str]: Dictionary with collection name as key and a list of 
        qualified document names of that collection as value
    """
    collection_list: list[Collection] = self.collections.values()
    return {c.name: c.document_list() for c in collection_list}
  

  def document_list_of(self, collection_name: str) -> list[str]:
    """List of documents in the Collection with the name ``collection_name``.

    Args:
        collection_name (str): name of the Collection

    Raises:
        CollectionDoesNotExist: when no Collection with the name collection_name exists.

    Returns:
        list[str]: list of the qualified names in the Collection
    """
    collection: Collection = {}
    try:
      collection = self.collections.get(collection_name)
    except KeyError as e:
      raise CollectionDoesNotExist(f'Collection not found!\n{e}')
    
    return collection.document_list()


  def __str__(self) -> str:
    return f'Collections: [ collections: {self.collections} ]'


  def __repr__(self):
    return str(self)
