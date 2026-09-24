import article
data = open("input.txt")

text = data.read()
textinput = str(text)

print(article.isArticle(text))
