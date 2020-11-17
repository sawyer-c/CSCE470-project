"""
VSM is the core query-ranking algorithm for is-that-a-supra
"""

import os
import sys
from collection import Collection
import copy
import json

collect = None
class VSM:
    """
    VSM Class
    """
    queryWords = []
    ds = None
    collection_length = 0
    Weights = {
        "title": 0.8,
        "body": 0.2
    }


    def __init__(self, query, collect):
        self.ds = collect
        self.collection_length = len(self.ds.tfs.keys()) #number of documents
        query = query.lower() #list of query words
        self.queryWords = query.split()
        #print(self.ds)
        #do you term frequencies from ds (getdocterm)
        #do you get term frequency for query in ds (getQueryfreq)

    def getQueryfreqs(self):
        """
        {
            word: freq
        }

        """
        tfQuery = {}
        docFreq = 0
        for word in self.queryWords:
            #tf 
            #double numOccur = (double) (utils.totalNumDocs() / utils.docFreq(qwordLower) );
            for doc in self.ds.tfs:
                tfs = self.ds.tfs[doc]
                if word in tfs["title"].keys():
                    docFreq += tfs["title"].get(word)
                if word in tfs["body"].keys():
                    docFreq += tfs["body"].get(word)
            # print(docFreq)
            tfQuery[word] = float(self.collection_length / docFreq)
            # print(tfQuery[word])
        return tfQuery

    

    def getNetScore(self, tfQuery, doc, normalize_tfs):
        """
        TODO: 
        -Dictionary of all term freqs in the whole dataset v/
        -Query q <string>
        -<Dictionary> tfQuery is a term frequency for every term in that query
        {
            doc_title: score_value
        }
        """
        totalscore = float(0)
        for word in self.queryWords:
            titlescore = normalize_tfs[doc]["title"][word]*self.Weights["title"] 
            bodyscore = normalize_tfs[doc]["body"][word]*self.Weights["body"]
            wordscore = float(self.collection_length / tfQuery[word])
            totalscore += float(wordscore * (titlescore + bodyscore))
            # print("Title: ")
            # print('%.8f'%titlescore)
            # print("\nBody: ")
            # print(bodyscore)
            # print("\nTotal: ")
            # print(totalscore)
        return totalscore


    def normalizeTFS(self, tfs):
        """
        TODO:
        Go through every word in Query q
        Divide the times it appears by the total length
        
        void return
        """
        copy_tfs = copy.deepcopy(tfs)

        for word in self.queryWords:
            for doc in self.ds.tfs.keys():
                if word in tfs[doc]["title"].keys():
                    title_val = copy_tfs[doc]["title"][word]

                    tfs[doc]["title"][word] = float(title_val/len(copy_tfs[doc]["title"].keys()))
                    
                    # print(tfs[doc]["title"][word])
                else:
                    tfs[doc]["title"][word] = float(0)
                if word in tfs[doc]["body"].keys():
                    body_val = copy_tfs[doc]["body"][word]
                    tfs[doc]["body"][word] = float(body_val/len(copy_tfs[doc]["body"].keys()))
                    # print(tfs[doc]["body"][word])
                else:
                    tfs[doc]["body"][word] = float(0)

        return tfs
        
    def getDocScore(self, doc, normalize_tfs, tfQuery):
        """
        docstring
        """
        doc_score = float(0.0)
        # tfQuery = self.getQueryfreqs()
        doc_score = self.getNetScore(tfQuery, doc, normalize_tfs)
        return doc_score

    def print_values(self, parameter_list):
        """
        TODO:
        This will print all scores for each document
        """
        pass

def main(query):
    collect = Collection()
    vsm = VSM(query, collect)
    normalize_tfs = vsm.normalizeTFS(vsm.ds.tfs)

    tfQuery = vsm.getQueryfreqs()
    score_list = {}
    for doc in collect.tfs:
        score_list[doc] = vsm.getDocScore(doc, normalize_tfs, tfQuery)
    #     print("Value of "+doc+" is "+str(vsm.getDocScore(doc, normalize_tfs, tfQuery)))
    # print("VSM DONE\n----------------\n")
    top_ten = []
    i=1
    for i in range(10):
        max_key = max(score_list, key=score_list.get)
        max_key_txt = "text-files/" + max_key + ".txt" #add path name
        top_ten.append(max_key_txt)
        score_list.pop(max_key)
    print(top_ten)
    #pass along the name and WHOLE DOCUMENT txt file
    
    #make dictionary for the top 10#
    top_ten_dictionary = {}
    
    for txt_file in top_ten:
        file_lines = open(txt_file, "r")
        file_lines = file_lines.readlines()
        file_data = ""
        for line in file_lines:
            if line is file_lines[0]:
                file_data = line[:-1]
            else:
                file_data = file_data + " " + line[:-1]
        top_ten_dictionary[txt_file[11:-4]] = file_data
    
    json_file = json.dumps(top_ten_dictionary)
    
    with open("top_ten.json", "w") as outfile:
        outfile.write(json_file)
    

    """
    JSON{
        txt_file_name 1: <STRING>,
        txt_file_name 2: <STRING>,
        ........
        txt_file_name 10: <STRING>
    }
    """



if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        main("hello world")