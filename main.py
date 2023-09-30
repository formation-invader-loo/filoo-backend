import os
from flask import Flask, request, Request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from utils.Logger import logger
from utils.configuration import get_config
from utils.helper_functions import allowed_file
from utils.HttpExceptions import HttpException
from Col.CollectionsService import CollectionsService
from Col.Document import Document
from Col.Collection import Collection
from Response.JSONResponse import JSONColectionResponse
from Col.CollectionException import CollectionAlreadyExists, DocumentAlreadyExists, DocumentDoesNotExist, CollectionDoesNotExist

APP_NAME = 'Information Over Load'
UPLOAD_FOLDER = get_config('paths', 'uploads')
ALLOWED_EXTENSIONS = ['md']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)
collection_service = CollectionsService()


@app.route('/collections', methods=['GET', 'POST'])
def collections():
  """Get a list of all collection items.

  Returns:
    JSON: JSON Object containing all collection items
  """
  try:
    if request.method == 'GET':
      return get_collections(request)
    if request.method == 'POST':
      return post_collectioins(request)
  except HttpException as e:
    logger.error(e)
    return e.args[0], e.args[1]
    

def get_collections(request: Request):
  offset = request.args.get('offset')
  limit = request.args.get('limit')
  if offset is None:
    offset = 0
  else:
    offset = int(offset)
  
  if limit is None:
    limit = 0
  else:
    limit = int(limit)
      
  logger.debug(f'{collections.__qualname__} request with offset={offset}, limit={limit}')
  if limit > 100:
    limit = 100
  
  response = JSONColectionResponse('/collections', collection_service.collections_names()).get_json()
  return response


def post_collectioins(request: Request):
  if request.args.get('collection'):
    collection = request.args.get('collection')
  else:
    raise HttpException('Collection must be specified', 400)

  try:
    collection_service.new_collection(collection)
  except CollectionAlreadyExists as e:
    logger.error(e)
    raise HttpException('Collection with this name alredy exists.', 409)
  return 'jop', 201


@app.route('/collections/documents', methods=['GET', 'POST', 'DELETE'])
def collections_documents():
  try:
    if request.method == 'GET':
      return get_collections_documents(request)
    if request.method == 'POST':
      return post_collections_documents(request)
    if request.method == 'DELETE':
      return delete_collections_documents(request)
  except HttpException as e:
    logger.error(e)
    return e.args[0], e.args[1]
    
def delete_collections_documents(request: Request):
  """Delete a Document from a Collection

  Args:
      request (Request): the request that was sent to delete a document
  """
  if request.args.get('collection'):
    collection = request.args.get('collection')
  else:
    return 'Collection must be specified', 400
  if collection not in collection_service.collections_names():
    return 'Collection does not exist', 400
  
  if request.args.get('md_file'):
    md_file = request.args.get('md_file')
  else:
    return 'File must be specified', 400
  if md_file not in collection_service.documents_names_of(collection):
    return 'File does not exist', 400
  
  try:
    logger.debug(f'{delete_collections_documents.__qualname__} request with: collection={collection}, md_file={md_file}')
    collection_service.delete_document(collection, md_file)
    return f'{md_file} from {collection} deleted.', 201
  except DocumentDoesNotExist as e:
    logger.error(e)
    return f'{md_file} does not exist in {collection}.', 410
  

def get_collections_documents(request: Request):
  """Get a list of all documents in a collection.

  Returns:
      JSON: JSON Object containing all documents in a collection
  """
  if request.args.get('collection'):
    collection = request.args.get('collection')
  else:
    return 'Collection must be specified', 400
  if collection not in collection_service.collections_names():
    return 'Collection does not exist', 400

  offset = request.args.get('offset')
  limit = request.args.get('limit')
  if offset is None:
    offset = 0
  else:
    offset = int(offset)
  
  if limit is None:
    limit = 0
  else:
    limit = int(limit)
      
  logger.debug(f'{get_collections_documents.__qualname__} request with collection={collection}, offset={offset}, limit={limit}')
  if limit > 100:
    limit = 100
  
  response = JSONColectionResponse('/collections/documents', collection_service.documents_names_of(collection)).get_json()
  return response


@app.route('/collections/documents/<path:filename>', methods=['GET'])
def get_collections_documents_path(filename):
  if request.args.get('collection'):
    collection = request.args.get('collection')
  else:
    return 'Collection must be specified', 400
  
  logger.debug(f'{get_collections_documents_path.__qualname__} request with collection={collection}, filename={filename}')
  try:
    col = collection_service.get_collection(collection)
    doc = collection_service.get_document(collection, filename)
  except CollectionDoesNotExist as e:
    logger.error(e)
    return 'Collection does not exist', 400
  except DocumentDoesNotExist as e:
    logger.error(e)
    return 'File does not exist', 400

  return send_from_directory(col.data_dir, doc.qualified_name)


def post_collections_documents(request: Request):
  if request.args.get('collection'):
    collection = request.args.get('collection')
  else:
    return 'Collection must be specified', 400
  if collection not in collection_service.collections_names():
    return 'Collection does not exist', 400
  
  # check if the post request has the file part
  if 'file' not in request.files:
    raise HttpException('No file uploaded', 406)
  file = request.files['file']
  # If the user does not select a file, the browser submits an
  # empty file without a filename.
  if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
    print(file.filename)
    if not secure_filename(file.filename):
      raise HttpException('Filename insecure', 406)
    file_name = file.filename.rsplit('/', 1)
    file_name = file_name[1] if len(file_name) > 1 else file_name[0]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

  try:
    collection_service.new_document(collection, file.filename)
  except DocumentAlreadyExists as e:
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    logger.error(e)
    raise HttpException(f'Document with name "{file.filename}" alredy exists in the Collection "{collection}" .', 409)
  return 'jop', 201
        

@app.route('/collections/documents/html', methods=['GET'])
def collections_documents_html():
  """Get a HTML representation of specific collection item.

  Returns:
      HTML: HTML representation of specific collection item.
  """
  print(request.args)
  if request.args.get('collection'):
    collection = request.args.get('collection')
  else:
    return 'Collection must be specified', 400
  if collection not in collection_service.collections_names():
    return 'Collection does not exist', 400


  if request.args.get('md_file'):
    md_file = request.args.get('md_file')
  else:
    return 'File must be specified', 400
  if md_file not in collection_service.documents_names_of(collection):
    return 'File does not exist', 400
  
  logger.debug(f'{collections_documents_html.__qualname__} request with: collection={collection}, md_file={md_file}')
  html_file_name = collection_service.get_document_html(collection, md_file)
  with open(html_file_name) as html_file:
    html = html_file.read()
  return html


app.run(host=get_config('server', 'host'), port=get_config('server', 'port'))
