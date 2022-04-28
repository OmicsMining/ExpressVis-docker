from fgvis.settings import DATABASE_DIR
import pandas as pd
#import feather
import os

# def obtainProbesFromEntrez(annoPkgName, genes):
#   # use feather file generated using function generateArrayBiocFileForMapping in processDatabaseData
#   # in biocpackage feather file, the id types are "PROBEID", "ENTREZID", "SYMBOL", "GENENAME"
#   annoFile  = os.path.join(DATABASE_DIR, "annotations", "biocpackages", annoPkgName + ".ftr")
#   annoFrame = pd.read_feather(annoFile)

#   annoFilter = annoFrame.loc[annoFrame["ENTREZID"].isin(genes), ]
#   # delete probes that have multiple genes annotations
#   annoFilter = annoFilter.drop_duplicates(subset = ["PROBEID"], keep = "first")
#   return annoFilter

