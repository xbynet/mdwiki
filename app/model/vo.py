from app import util
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

