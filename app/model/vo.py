from app import util
from datetime import datetime
# class PostMeta(dict):
# 	__allowList=['title','author','createAt','location']

# 	def __init__(self):
# 		self['createAt']=util.getNowFmtDate()
# 	def __getattr__(self,name):
# 		if name in __allowList:
# 			return self[name]
# 	def __setattr__(self,name,value):
# 		if name in __allowList:
# 			self[name]=value
# 		else:
# 			return AttributeError(name+" not found")

class SearchPostVo():
    def __init__(self,location,title='',content='',summary='',createAt=None,modifyAt=None,author=''):
        self.location=location
        self.title=title
        self.content=content
        self.summary=summary
        self.createAt=datetime.strptime(createAt or util.getNowFmtDate(),'%Y-%m-%d %H:%M:%S')
        self.modifyAt=datetime.strptime(modifyAt or util.getNowFmtDate(),'%Y-%m-%d %H:%M:%S')
        self.author=author
    def __repr__(self):
        return "<SearchPostVo %s>" % self.title

