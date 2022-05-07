import json
from annotation.annotationQuery import obtainMicroarrayProbeIDannoInfoForDisplay

annoPkgName = "hugene20sttranscriptcluster.db"
probesInfo  = obtainMicroarrayProbeIDannoInfoForDisplay(annoPkgName = annoPkgName)
genesAnnotation = {
  "IDtype": annoPkgName, 
  "genesInfoDic": probesInfo
}


with open("/media/thudxz/Research/process/bioinformatics_tools/angular_django_time_series/client/src/assets/genesAnno.json", "w") as fileOpen:
  json.dump(genesAnnotation, fileOpen)

