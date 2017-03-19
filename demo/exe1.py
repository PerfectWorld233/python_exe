import urllib.request
url = 'http://aima.cs.berkeley.edu/data/iris.csv'
u = urllib.request.urlopen(url)
localFile = open('iris.csv', 'w')
localFile.write(u.read())
localFile.close()


