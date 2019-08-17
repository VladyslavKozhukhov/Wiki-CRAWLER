import requests
import lxml.html
import random
import sys
import question2b
prefix = "http://en.wikipedia.org"
primeMap = {}
FirstLvlChildren = {}
SecondLvlChildren ={}
ThirdLvlChildren = {}
checkedWebSites =  []
graph = {}
maxLink = 10
num = 1

def deleteDuplicate(lst):
    checked = set()
    allSet = checked.add
    return [x for x in lst if not (x in checked or allSet(x))]

def crawl(url,lvl):
    urls = []
    r = requests.get(url)
    doc = lxml.html.fromstring(r.content)


    for t in doc.xpath("//a[contains(@href,'/wiki/') and not(contains(@href, ':'))]/@href"):
        urls.append(prefix+t)
    if lvl == 0:
        primeMap[url] = deleteDuplicate(urls)
    elif lvl == 1:
        FirstLvlChildren[url] = deleteDuplicate(urls)
    elif lvl == 2:
        SecondLvlChildren[url] = deleteDuplicate(urls)
    elif lvl ==3:
        ThirdLvlChildren[url] = deleteDuplicate(urls)

def runOnChildren( root, depth, counter ):
    return crawChildren(root, depth, counter)

def buildTree(startPoint):
    global maxLink
    global num
    crawl(startPoint, 0)
    checkedWebSites.append(startPoint)
    counter = maxLink
    top10 = 10
    rootChildren = primeMap[startPoint]
    graph[startPoint] = rootChildren
    ##########################PRINT ROOT#######################################
    if (len(rootChildren)  == 0 ):
        print("" + startPoint + " = " + "{" + startPoint + "}")

    elif( len(rootChildren) > maxLink ):
        print("" + startPoint + " = " + "{" + ' , '.join(str(x) for x in rootChildren[0:maxLink]) + "}")
        graph[startPoint] = rootChildren[0:maxLink]
    else:
        print("" + startPoint + " = " + "{" + ' , '.join(str(x) for x in rootChildren) + "}")
        graph[startPoint] = rootChildren


        #Run on children of children##LEVEL 1
    for child in rootChildren :
        a = runOnChildren(child, 1, counter)
        if a == 0:
            print("" + child + " = " + "{" + child + "}")

        checkedWebSites.append(child)
        deleteDuplicate(checkedWebSites)
        top10-=1
        if(top10 == 0):
            break
    a=0
    ###LEVEL 2###
    for childroot in rootChildren:
        top10 = 10
        crawl(childroot, 2)
        childroot = SecondLvlChildren[childroot]
        for grandOfRoot in childroot:
            if grandOfRoot in checkedWebSites:
                continue
            else:
                a= runOnChildren(grandOfRoot, 2, counter)

                if a == 0:
                    print("" + grandOfRoot + " = " + "{" + grandOfRoot + "}")

                checkedWebSites.append(grandOfRoot)
                deleteDuplicate(checkedWebSites)
                a = 0
                top10-=1
                if (top10 == 0):
                    break
    a=0

    for childroot in rootChildren:
        top10A = 10
        crawl(childroot, 2)
        childroot = SecondLvlChildren[childroot]
        for grandOfRoot in childroot:
            top10B = 10
            crawl(grandOfRoot, 3)
            grandOfRoot = ThirdLvlChildren[grandOfRoot]
            for grandgrandOfRoot in grandOfRoot:
                if grandgrandOfRoot in checkedWebSites:
                    continue
                else:
                    a = runOnChildren(grandgrandOfRoot, 3, counter)
                    if a==0:
                        print("" + grandgrandOfRoot + " = " + "{" + grandgrandOfRoot + "}")

                    checkedWebSites.append(grandgrandOfRoot)
                    deleteDuplicate(checkedWebSites)

                    top10B-=1
                    if (top10B == 0):
                        break
                a=0
            top10A-=1
            if(top10A==0):
                break
        if (top10A == 0):
            break

def crawChildren( root, depth,counter):
    crawl(root,depth)
    global num
    lst =[]
    if(depth == 1):
        rootChildren = FirstLvlChildren[root]
    elif(depth == 2):
        rootChildren = SecondLvlChildren[root]
    else:
        rootChildren = ThirdLvlChildren[root]

    if depth == 3:
        top10 = 10
        lengthLst = int(len(rootChildren))
        i = 0
        lstPrint = []
        while( i<lengthLst):
            if(i>= top10):
                break
            if(rootChildren[i] in checkedWebSites ):
                lstPrint.append(rootChildren[i])
            i+=1
        if len(lstPrint) == 0:
            graph[root] = root
            return 0

        elif len(lstPrint) > 0:
            print("" + root + " = " + "{" + ' , '.join(str(x) for x in lstPrint) + "}")
            graph[root] = lstPrint

        return 1
    else:
        if len(rootChildren) == 0:
            graph[root]=root
            return 0

        elif(len(rootChildren) != 0):
            if(counter - len(rootChildren)<0):
                print("" + root + " = " + "{" +' , '.join(str(x) for x in rootChildren[0:counter] ) + "}")
                graph[root] = rootChildren[0: counter]


            else:
                print("" + root + " = " + "{" +' , '.join(str(x) for x in rootChildren ) + "}")
                graph[root] = rootChildren

        return  1

#buildTree(sys.argv[1])
#question2b.counDamp(**graph)