import sys
import os
import math

class Collection:
    """
    collection of Documents
    {\n
    \tDocument-Title:
        {\n
        \ttitle-portion: {
            \tword: freqs
            \t}

        \tbody-portion: {
            \tword: freqs
            \t}
        }
    }
    """
    tfs = {}
    def __init__(self):
        tfs = {} #dictionary of doctf for each doc
        self.aggregate_documents()
    
    def aggregate_documents(self):
        """
        this will append all the doctf's for every document
        """
        count = 0   
        for file in os.listdir("text-files"):
            file_path = "text-files/"+file
            # doc = Document(file_path)
            self.tfs[file[:-4]] = self.add_document(file_path)
            # print(file + " Done")
            count += 1
        print(str(count)+" Documents properly parsed!")

    def add_document(self, file_path):
        """
        Create Document_tf (title and body)
        return a {title: {body:{}, title:{} }}
        """
        doc_tf = {
            "title": {},
            "body": {},
            "href": {}
        }
        title = file_path[11:-4] #establish title part needed
        
        #title portion#
        doc_title = title.lower().split()
        for word in doc_title:
            if word not in doc_tf["title"].keys():
                doc_tf["title"][word] = 1
            else:
                doc_tf["title"][word] += 1

        #find body#
        body = ""
        with open(file_path, encoding="utf-8", errors='ignore') as f:
            list_of_lines = f.readlines()
        # Car_name = list_of_lines.pop(0)[:-1]#car name w/out \n
        # Year_range = list_of_lines.pop(0)[:-1]#YYYY-YYYY
        # Car_style = list_of_lines.pop(0)[:-1]#style w/out \n
        # if list_of_lines[0] == "\n":
        #     list_of_lines.pop(0)#removes unnecessary \n char
        for line in list_of_lines:
            if line != "\n":
                body += line[:-1] + " "
        
        #body portion#
        body = body.lower().split()
        for word in body:
            if word not in doc_tf["body"].keys():
                doc_tf["body"][word] = 1
            else:
                doc_tf["body"][word] += 1
        
        #return the document dictionary
        return doc_tf

    def get_tfs(self):
        """
        returns tfs from Dataset
        """
        return self.tfs