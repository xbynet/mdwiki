import re,os,sys
from urllib.parse import unquote
import bleach 
import shutil
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor

srcpath=r'F:\test\pages'
dest=r'F:\test\pages_out'
prefix='/pages/dokuwiki'
if  os.path.exists(dest):
    shutil.rmtree(dest)
os.mkdir(dest)

def concatlist(list1,list2):
    t=list1[:]
    t.extend(list2)
    return t
def writeindex(baseDir,walktuple):
    title=baseDir[len(srcpath):]
    baseDir=dest+baseDir[len(srcpath):]
    with open(baseDir+os.sep+'index.md','a',encoding='utf-8') as f:
        f.write("title: %s \n\n" % title)
        base=prefix+walktuple[0][len(srcpath):].replace(os.sep,'/')+'/'
        for i in walktuple[1]:
            f.write('['+i+']('+base+i+'/index)\n')
        for i in walktuple[2]:
            i=i.rsplit('.',1)[0]
            f.write('['+unquote(i)+']('+base+unquote(i)+')\n')

def walkDir(dirname,dirlist=[]):
    if not os.path.exists(dirname):
        return
    for path,dirs,files in os.walk(dirname):
        writeindex(dirname,(path,dirs,files))
        for dirfile in dirs:
            if dirfile=='.' or dirfile=='..':
                continue
            fullpath=os.path.join(path,dirfile)
            destPath=dest+fullpath[len(srcpath):]
            if not os.path.exists(destPath):
                os.makedirs(destPath)
            dirlist.append(fullpath)


dirlist=[srcpath]
walkDir(srcpath,dirlist)


def process(path):
    for item in os.listdir(path):
        if os.path.isdir(path+os.sep+item) or item=='index.md' or not item.endswith('.txt'):
            continue    
        print("process: %s to %s " %(item,unquote(item)))
        with open(path+os.sep+item,encoding='utf-8') as f:
            content=f.read()
            picRelist=re.findall('\{\{(.+?)\}\}',content)
            replacelist=['/data/dokuwiki'+t.replace(':','/') for t in picRelist]
            for i,v in enumerate(picRelist):
                content=content.replace('{{'+v+'}}','![]('+replacelist[i]+')')
            nowikiRelist=re.findall('\<nowiki\>.*?\</nowiki\>',content,flags=re.S)
            for v in nowikiRelist:
                content=content.replace(v,bleach.clean(v))
            linklist=re.findall(r"\[\[(.*?)\|(.*?)\]\]",content)
            linkRelist=[]

            for url,title in linklist:
                if url.startswith('http') or url.startswith('www'):
                    linkRelist.append('[%s](%s)' % (title,url.strip()))
                else:
                    url=url.strip().replace(':','/')
                    if url[0]!='/':
                        url='/'+url
                    linkRelist.append('[%s](%s)' % (title,(prefix+url)))
                    print(prefix+url)
            for i,v in enumerate(linklist):
                    content=content.replace('[[%s|%s]]' % v,linkRelist[i])
                
            #,r'[\g<1>]('+prefix+'\g<2>)'
            title=unquote(item).rsplit('.',1)[0]
            regs=[(r'={6}(.*?)={6}',r'# \g<1>'),(r'={5}(.*?)={5}',r'## \g<1>'),(r'={4}(.*?)={4}',r'### \g<1>'),
            (r'={3}(.*?)={3}',r'#### \g<1>'),(r'<code.*?>((.*\n*)*?)</code>',r'```\n\g<1>\n```'),
            (r"\'\'(.*?)\'\'",r'` \g<1> `'),(r'<(fc|wrap).*?>(.*?)</(fc|wrap)>',r'` \g<2> `'),
            (r'\{\{(/.*?)\}\}',r'![](\g<1>)')]
            #re.sub('={6}(.*?)={6}','# \g<1>',content)
            #print("开始处理文件 %s" % item)
            for reg in regs:
                print("%s to %s " % reg )
                content=re.sub(reg[0],reg[1],content)
            item=item.replace('.txt','.md')

            with open(dest+path[len(srcpath):]+os.sep+unquote(item).encode('gb2312').decode('gb2312'),'w+',encoding='utf-8') as f2:
                f2.write(("title: %s \n\n" % title)+content)
                f2.flush()

for path in dirlist:
    process(path)

