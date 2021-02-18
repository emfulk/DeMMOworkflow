# This script takes outputs of proteins identified in InterProScan and filters out proteins of interest. 
# List of proteins of interest can be changed with the true and false HK and RR lists. 
# Can be generalized to just be true and false lists for any proteins, not specifically only HKs and RRs. 

import csv
import collections
import os
import re

# Change working directory path 
os.chdir("/Users/annelisegoldman/Documents/TCS Mining Project/DeMMO1 Outputs")

# Input file paths for InterProScan results (this is just the first file in the working directory), 
# true and false HK and RR lists. All files should be in .tsv format.
IPRresults = "/Users/annelisegoldman/Documents/TCS Mining Project/DeMMO1 Outputs/orf_DeMMO1_1.fa.tsv"

HKtrue_list = "/Users/annelisegoldman/Documents/TCS Mining Project/HK and RR Lists/HK1ListTSV.txt"
HKfalse_list = "/Users/annelisegoldman/Documents/TCS Mining Project/HK and RR Lists/HKFalseListTSV.txt"
RRtrue_list = "/Users/annelisegoldman/Documents/TCS Mining Project/HK and RR Lists/RR1ListTSV.txt"
RRfalse_list = "/Users/annelisegoldman/Documents/TCS Mining Project/HK and RR Lists/RRFalseListShortTSV.txt"

def IPR_results(file):
  #Create dictionary from InterProScan results with ORFs as keys and IPR list as values
  with open(file, "rt") as tsvFile:
    IPRReader= csv.reader(tsvFile, delimiter="\t")
    workingProtDict = collections.defaultdict(list)
    for line in IPRReader:
      if len(line)>=12:
        protID=line[0]
        interpro=line[11]
        if interpro != '':
          workingProtDict[protID].append(interpro)
          continue
      else:
        continue
  return workingProtDict

def IPR_list(file):
  #Imports list of IPRs for HKs (both positve and negative hits) and RRs
  with open(file, "rt") as tsvFile:
    temp = csv.reader(tsvFile, delimiter="\t")
    IPRlist = []
    #Turn IPR signatures in file into a list
    for line in temp:
      IPRlist.append(line)
    #Flatten nested sublists
    IPRlist = [val for sublist in IPRlist for val in sublist]
  return IPRlist

def IPR_filter(IPRdict, pos_list, neg_list): # Filters ORFS for IPRs matching true (but not false) IPR signatures
  posdict = {}
  filtdict = {}
  pos_set = set(pos_list)
  neg_set = set(neg_list)
  # Create dictionary (posdict) containing only OFRs with at least one true associated IPR signature 
  for key, val in IPRdict.items():
    val_set = set(val)
    if len(val_set.intersection(pos_set)) > 0:
      posdict[key] = val
  # Create dictionary containing only ORFs with at least one true IPR signature but not one of the false IPR signatures
  for key, val in posdict.items():
    val_set = set(val)
    if len(val_set.intersection(neg_set)) == 0:
     filtdict[key] = val
  return filtdict

def filewriter(filtdict, fileout): # Writes .csv file containing each ORF associated with the desired IPR set
  cats=filtdict.keys()
  with open(fileout, "w") as outfile:
    wr = csv.writer(outfile)
    headers=["ORF", "IPRs"]
    wr.writerow(headers)
    for cat in cats:
      data = [cat, filtdict[cat]]
      wr.writerow(data)

def main(): # sets positive and negative lists and input based on the input files above 
  IPRdict = IPR_results(IPRresults)
  HKpos = IPR_list(HKtrue_list)
  HKneg = IPR_list(HKfalse_list)
  RRpos = IPR_list(RRtrue_list)
  RRneg = IPR_list(RRfalse_list)
  
  # performs the filtering using the functions defined above 
  HKfilt = IPR_filter(IPRdict, HKpos, HKneg)
  RRfilt = IPR_filter(IPRdict, RRpos, RRneg)
  print("The number of HKs is",len(HKfilt))
  print("The number of RRs is",len(RRfilt))
  
  # write results to two files, one for HKs, one for RRs
  filewriter(HKfilt, "DeMMO1_1_HK.csv") # Change file name to desired output file
  filewriter(RRfilt, "DeMMO1_1_RR_FalsePosShort.csv") # Change file name to desired output file

# Do the complete filtering based on functions defined above
if __name__ == "__main__":
  main()
