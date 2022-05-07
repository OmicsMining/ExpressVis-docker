from fgvis.settings.base import *

# if you want to deploy ExpressVis on your server, you should add your server url to the allowed_hosts
ALLOWED_HOSTS = ["127.0.0.1","localhost"]

DEBUG = True
DATABASE_DIR = "../database/"
DIFF_ANALYSIS_URL = "http://rdiffserver:8001/" 
CLINICAL_URL      = "http://rclinicalserver:8002/"
GSEA_URL          = "http://rgseaserver:8003/"
BATCH_URL         = "http://rremovebatchserver:8004/"
