import rdata

# Let's search for keywords and text snippets from a novel.
# git clone https://github.com/bradleyboehmke/harrypotter
# Seven novels encrypted in Rda format, the first of whose
# copyright expires 70 years after the death of Robert
# Galbraith (b. 1965).

data = rdata.read_rda("chamber_of_secrets.rda")
content = data["chamber_of_secrets"]
# rdata gives it to us as an ndarray
content[0]
alltext = ""
for i in content:
    alltext = alltext + i
len(alltext)
len(alltext.split(" "))

# 490k characters, 83k words

hidx = {}
for i, word in enumerate(alltext.split()[0:100]):
    if word in hidx.keys():
        hidx[word] += 1
    else:
        hidx[word] = 1

# But I don't want a histogram, I wanted an index

idx = {}
for i, word in enumerate(alltext.split()):
    if word in idx.keys():
        idx[word] += [i]
    else:
        idx[word] = [i]

# Let's query the index for some stuff...
def show_context(word):
    for i in idx[word][0:10]:
        print(("\t".join(alltext.split()[i-4:i+5])).expandtabs())

show_context("Harry")

show_context("Petunia")

show_context("wand")

#  I can get these results of queries without manipulating the
#  entire source text.
def show_context(word):
    for i in idx[word][0:10]:
        snippet = " ".join(alltext.split()[i-4:i+5])
        print(" " * (35-snippet.find(word)) + snippet)
