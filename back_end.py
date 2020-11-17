# using flask_restful 
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from collection import Collection
from core import VSM

import sys
import os
import math
import copy
import json
# creating the flask app 
app = Flask(__name__) 
# creating an API object 
api = Api(app) 
  
# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 
class API(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    
    def get(self, query): 
        collect = Collection()
        query = query.replace("_", " ")
        # print("Query is :"+query)
        vsm = VSM(query, collect)
        # print("\n\n")
        # print(vsm.ds.tfs)
        # print("\n\n")
        normalize_tfs = vsm.normalizeTFS(vsm.ds.tfs)

        tfQuery = vsm.getQueryfreqs()
        score_list = {}
        for doc in collect.tfs:
            score_list[doc] = vsm.getDocScore(doc, normalize_tfs, tfQuery)
            # print("Value of "+doc+" is "+str(vsm.getDocScore(doc, normalize_tfs, tfQuery)))
        # print("VSM DONE\n----------------\n")
        top_ten = []
        i=1
        for i in range(10):
            max_key = max(score_list, key=score_list.get)
            max_key_txt = "text-files/" + max_key + ".txt" #add path name
            top_ten.append(max_key_txt)
            score_list.pop(max_key)
        # print(top_ten)
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
        print("\nTop Ten Documents:\n--------------\n")
        print(top_ten_dictionary.keys())
        return jsonify(top_ten_dictionary) 
  
    # Corresponds to POST request 
    def post(self): 
          
        data = request.get_json()     # status code 
        return jsonify({'data': data}), 201
  
  

  
  
# adding the defined resources along with their corresponding urls 
api.add_resource(API, '/vsm/<string:query>') 
 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True)