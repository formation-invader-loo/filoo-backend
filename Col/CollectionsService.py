"""CollectionsService handles the loading and manipulating of Collections.
"""
import sys
sys.path.append('/workspaces/IOL/IOLBackendv2')
sys.path.append('/workspaces/IOL/IOLBackendv2/Col')
from utils.Logger import logger
from utils.configuration import get_config

from CollectionException import CollectionAlreadyExists
from Collections import Collections
from Collection import Collection
from Document import Document
import os


class CollectionsService:
  """CollectionsService handles the loading and manipulating of Collections.
  """

  def __init__(self) -> None:
    self.collections_dir = get_config('paths', 'data') + '/collections'
    
    self.collections = Collections()
    for c in os.listdir(self.collections_dir):
      self.collections.add_collection(c)

  def __str__(self) -> str:
    return f'''CollectionService:[
      collections_dir = {self.collections_dir}
      collections = {self.collections}
    '''
  

  def new_collection(self, collection_name: str) -> None:
    """Create a new Collection and the corresponding directories f with the given name.

    Args:
        collection_name (str): name of the new Collection

    Raises:
        CollectionAlreadyExists: If a Collection with the same name already exists, a CollectionAlreadyExists Exception is raised.
    """
    collection_dir = self.collections_dir + '/' + collection_name
    if os.path.isdir(collection_dir):
      raise CollectionAlreadyExists(f'Collection with name "{collection_name}" already exists.')
    os.makedirs(collection_dir, exist_ok=True)
    self.collections.add_collection(collection_name)


  def collections_names(self) -> list[str]:
    return self.collections.collections_list()
  

  def documents_names_of(self, collection_name: str) -> list[str]:
    return self.collections.document_list_of(collection_name)
  

  def get_document_html(self, collection_name: str, document_qualified_name: str) -> str:
    return self.collections.get_document(collection_name, document_qualified_name).html_file


  def new_document(self, collection_name: str, document_qualified_name: str, document_content: str):
    self.collections.new_document(collection_name, document_qualified_name, document_content)


def main():
  c_service = CollectionsService()
  print(c_service)

  print(f'Collections List:\n{c_service.collections.collections_list()}')

if __name__ == '__main__':
  main()