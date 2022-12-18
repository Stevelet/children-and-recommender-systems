from urllib import request

req = request.urlopen("http://en.wikipedia.org/w/api.php?action=parse&page=China&format=json&prop=text")
content = req.read()
print(content)