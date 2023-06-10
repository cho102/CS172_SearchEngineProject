import logging, sys
logging.disable(sys.maxsize)
import json
import lucene
import os
import ast
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity
from datetime import datetime
import time
import operator

from flask import request, Flask, render_template, redirect, flash, session

app = Flask(__name__)
app.secret_key = 'class041'

# finalDocJson = 'group01_reddit_data.json'
finalDocJson = 'sample_tennis_data.json'
finalDoc = []
with open(finalDocJson, 'r') as index_file:
    finalDoc = json.load(index_file)

#SHOULD FIX JSON OBJECTS IN COMMENTS(IP)
def fix_comments_field(comments):
    try:
        if comments is None:
            return []
        if isinstance(comments, str):
            # Check if comments are in valid JSON format
            try:
                comments = json.loads(comments)
            except json.JSONDecodeError:
                pass
        elif isinstance(comments, list):
            for i in range(len(comments)):
                if isinstance(comments[i], dict) and 'replies' in comments[i]:
                    replies = comments[i]['replies']
                    if isinstance(replies, str):
                        try:
                            replies = json.loads(replies)
                            comments[i]['replies'] = replies
                        except json.JSONDecodeError:
                            pass
        return comments
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    
    parser = QueryParser('title', StandardAnalyzer())
    parsed_query = parser.parse(query)

    print(parsed_query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    redditURLPrefix = "https://www.reddit.com"
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        comments = doc.get("comments")
        comments_list = ast.literal_eval(comments) if comments else []
        first_comment = comments_list[0] if comments_list else {}
        post_url = redditURLPrefix + doc.get("permalink")
        newDoc = {
            "documentScore": hit.score,
            "title": doc.get("title"),
            "body": first_comment.get('body', ''),
            "post_date": datetime.fromtimestamp(float(doc.get("created_utc"))).strftime('%Y-%m-%d %H:%M:%S'), # referenced https://stackoverflow.com/a/46914259
            "post_score": doc.get("score"),
            "num_comments": doc.get("num_comments"),
            "url": post_url,
            "created_utc": doc.get("created_utc"),
        }
        if not newDoc in topkdocs:    
            topkdocs.append(newDoc)
    return topkdocs

def validateDateInput(dateInput): # referenced https://stackoverflow.com/a/16870699
    try:
        if dateInput != datetime.strptime(dateInput, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

@app.route("/")
def home():
    return redirect("/input")

@app.errorhandler(404)
def everythingelse(e):
    return redirect("/input")

@app.route('/input', methods = ['POST', 'GET'])
def input():
    return render_template('input.html')

@app.route('/output', methods = ['POST', 'GET'])
def output():
    if request.method == 'GET':
        return redirect("/input")
    if request.method == 'POST':
        form_data = request.form
        query = form_data['query']
        if (query == ""):
            return redirect("/input")
        startDate = form_data['search-range-start-query']
        endDate = form_data['search-range-end-query']
        startEndDateQuery = ''
        if (startDate != "" and endDate !=""):
            if (validateDateInput(startDate) and validateDateInput(endDate)):
                dateSearchCombine = ' TO '
                startDateUnix = time.mktime(datetime.strptime(startDate, "%Y-%m-%d").timetuple())
                endDateUnix = time.mktime(datetime.strptime(endDate, "%Y-%m-%d").timetuple())
                if (endDateUnix > startDateUnix):
                    startEndDateQuery = str(int(startDateUnix)) + dateSearchCombine + str(int(endDateUnix))
        if (startEndDateQuery != ""):
            query = query + ' AND created_utc:[' + startEndDateQuery + ']'
        print(f"this is the query: {query}")
        lucene.getVMEnv().attachCurrentThread()
        #docs = retrieve('lucene_partB_index/', str(query))
        docs = retrieve('sample_lucene_partB_index/', str(query))
        if (form_data['button'] == 'Search by document score'):
            pass
        elif (form_data['button'] == 'Search by document score ascending post date'):
            docs.sort(key=operator.itemgetter("created_utc"), reverse=True);
        else:
            docs.sort(key=operator.itemgetter("created_utc"), reverse=False);
        print(docs)
        
        return render_template('output.html',lucene_output = docs)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

if __name__ == "__main__":
    app.run(debug=True)
