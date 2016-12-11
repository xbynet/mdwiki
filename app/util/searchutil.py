import sys, os, shutil

from whoosh.highlight import HtmlFormatter,ContextFragmenter, WholeFragmenter
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.searching import Hit
from app import config
from jieba.analyse import ChineseAnalyzer
from app import util
from app.model import vo

INDEX_DIR = config.DATA_DIR + os.sep + 'searchIndex'


def checkIndexDir():
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
        analyzer = ChineseAnalyzer()
        schema = Schema(title=TEXT(stored=True, analyzer=analyzer), location=ID(stored=True, unique=True),
                        content=TEXT(stored=True, analyzer=analyzer),
                        summary=TEXT(stored=True, analyzer=analyzer), author=ID(stored=True),createAt=DATETIME(stored=True), modifyAt=DATETIME(stored=True))  #

        ix = create_in(INDEX_DIR, schema)  # for create new index
        ix.close()


checkIndexDir()
ix = open_dir(INDEX_DIR)
# writer = ix.writer()
# writer.add_field("createAt", DATETIME())
# writer.add_field("modifyAt", DATETIME())
# writer.commit();

def reBuildIndex():
    global ix
    ix.close()
    if os.path.exists(INDEX_DIR):
        shutil.rmtree(INDEX_DIR)
        checkIndexDir()
    ix = open_dir(INDEX_DIR)
    # todo
    pathlist=[]
    util.walkDirGenDataUrl('pages',pathlist=pathlist)
    doclist=[]
    for path in pathlist:
        with open(path,encoding='utf-8') as f:
            content=f.read()
            meta=util.parsePostMeta(content.split('\n\n',1)[0])
            if not ('location' in meta and meta['location']):
                meta["location"]=path[len(config.PAGE_DIR):].rsplit('.',1)[0]
            content=content.split('\n\n',1)[1]
            postvo = vo.SearchPostVo(content=content, summary=content[:100], **meta)
            doclist.append(postvo)
    updateDocument(doclist)


def indexDocument(doclist):
    writer=ix.writer()
    for doc in doclist:
        writer.add_document(**util.objToDict(doc))
    writer.commit()


def updateDocument(doclist):
    writer = ix.writer()
    for doc in doclist:
        writer.update_document(**util.objToDict(doc))
    writer.commit()


def deleteDocument(termlist):
    writer = ix.writer()
    for term in termlist:
        writer.delete_by_term(term["fieldName"], term['text'])
    writer.commit()


def search(keyword):
    with ix.searcher() as searcher:
        # res=dict()
        # parser = QueryParser('content', schema=ix.schema)
        parser = MultifieldParser(["title", "content",'createAt'], schema=ix.schema)
        q = parser.parse(keyword)
        results = searcher.search(q)
        return results


def searchPage(keyword, curPage=1, pagelen=10):
    with ix.searcher() as searcher:
        # res=dict()
        # parser = QueryParser('content', schema=ix.schema)
        hf = HtmlFormatter(tagname="code", classname="match", termclass="term")
        fragmenter=WholeFragmenter(charlimit=None)
        parser = MultifieldParser(["title", "content",'createAt'], schema=ix.schema)
        parser.add_plugin(DateParserPlugin())
        q = parser.parse(keyword)
        page = searcher.search_page(q, curPage, pagelen)#,terms=True
        page.results.fragmenter=fragmenter
        #page.results.fragmenter.charlimit=None
        page.results.formatter = hf
        # terms = page.results.matched_terms()
        # key=[ e for e in terms ][0][1].decode('UTF-8')
        resPage=dict(pagenum=page.pagenum,pagecount=page.pagecount,total=page.total,posts=[])
        for hint in page:
            tmp=dict()
            tmp['title']=hint.highlights("title",minscore=0)
            tmp['author']=hint["author"]
            tmp['location']=hint["location"].replace(os.sep,'/').replace('//','/')
            if tmp['location'].startswith('/'):
                tmp['location']=tmp['location'][1:]
            tmp['summary']=hint.highlights("summary",minscore=0)#hint["content"].replace(key,"<code>%s</code>" % key)

            resPage['posts'].append(tmp)
        return resPage
