library(tm)
library(wordcloud)


messages <- read.csv("messages.csv", header=TRUE)

corp <- Corpus(VectorSource(messages$message))
corp <- tm_map(corp, stripWhitespace)
corp <- tm_map(corp,  content_transformer(tolower))
corp <- tm_map(corp, removeWords, stopwords("english"))
corp <- tm_map(corp, removeWords, stopwords("german"))
corp <- tm_map(corp, stemDocument)

wordcloud(
  corp,
  scale=c(5, 0.5),
  #max.words=100,
  random.order=FALSE,
  rot.per=0.35,
  use.r.layout=FALSE,
  colors=brewer.pal(8, "Dark2")
)
