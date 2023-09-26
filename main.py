from flask import Flask, render_template, request, json, jsonify
from flask_cors import CORS
from utils.Logger import logger
from Col.CollectionsService import CollectionsService
from Response.JSONResponse import JSONColectionResponse

APP_NAME = 'Information Over Load'

app = Flask(__name__)
CORS(app)
collection_service = CollectionsService()


@app.route('/collections', methods=['GET'])
def collection_list():
    """Get a list of all collection items.

    Returns:
        JSON: JSON Object containing all collection items
    """    
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
        
    logger.debug(f'{collection_list.__qualname__} request with offset={offset}, limit={limit}')
    if limit > 100:
        limit = 100
    
    response = JSONColectionResponse('/collections', collection_service.collections_names()).get_json()
    return response


@app.route('/collections/documents', methods=['GET'])
def collection_document_list():
    """Get a list of all documents in a collection.

    Returns:
        JSON: JSON Object containing all documents in a collection
    """    
    if request.args.get('collection'):
        collection = request.args.get('collection')
    else:
        return 'Collection must be specified', 404
    if collection not in collection_service.collections_names():
        return 'Collection does not exist', 404

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
        
    logger.debug(f'{collection_document_list.__qualname__} request with collection={collection}, offset={offset}, limit={limit}')
    if limit > 100:
        limit = 100
    
    response = JSONColectionResponse('/collections/documents', collection_service.documents_names_of(collection)).get_json()
    return response
        

@app.route('/collections/documents/html', methods=['GET'])
def collection_html():
    """Get a HTML representation of specific collection item.

    Returns:
        HTML: HTML representation of specific collection item.
    """
    print(request.args)
    if request.args.get('collection'):
        collection = request.args.get('collection')
    else:
        return 'Collection must be specified', 404
    if collection not in collection_service.collections_names():
        return 'Collection does not exist', 404


    if request.args.get('md_file'):
        md_file = request.args.get('md_file')
    else:
        return 'File must be specified', 404
    if md_file not in collection_service.documents_names_of(collection):
        return 'File does not exist', 404
    
    logger.debug(f'{collection_html.__qualname__} request with: collection={collection}, md_file={md_file}')
    html_file_name = collection_service.get_document_html(collection, md_file)
    with open(html_file_name) as html_file:
        html = html_file.read()
    return html


app.run(host='0.0.0.0', port=80)
