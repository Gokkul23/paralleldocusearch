import re
search_word = "saai"
file_name = str(u"1.txt")
file = "/Users/gokkul/Desktop/olu/" + str(file_name)
with open(file,"r") as f:
    f_text = f.read()
    print(f_text)
    if(re.search(search_word,f_text,re.IGNORECASE)):
        print("Match found")
    #print("Performing the word search ", search_word, ", on", file_name, " file")
    """
    self.search_word = self.search_word.lower()
    if(re.search(self.search_word,f_text)):
        print(self.search_word, " found in file '", string,"'" )
    else:
        print("No match found")           
    """    