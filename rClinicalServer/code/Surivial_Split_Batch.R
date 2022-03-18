# These code is written by Kaikun Xu


# 1: 该函数用于根据指定阈值分割高低表达组
.dichotomize <- function(x,cutpoint,right=TRUE,labels = c("low", "high")){
  groups = cut(x,breaks=c(-Inf,cutpoint,Inf),labels=labels,right=right)%>%as.character()
  return(groups)
}

# 2: 该函数用于对每个蛋白计算高低表达阈值
## 从maxstat::maxstat.test()函数修改而来,使maxprop参数的值可以单独指定,而非默认的1-minprop;
## variable需要为string而非vector.
survCutpoint <- function(data, variable,time = "time", event = "event",minprop = 0.6, maxprop=0.9, progressbar = TRUE)
{
  library("maxstat")
  if(!inherits(data, "data.frame")){stop("data should be an object of class data.frame")}
  data <- as.data.frame(data)
  if(!all(c(time, event) %in% colnames(data))){stop("Specify correct column names containing time and event values.")}
  if(!(variable %in% colnames(data))){stop("Specified variable is not found in the data.")}
  surv_data <- tibble(time = data[, time], event = data[, event])
  surv_data$variable <- data[,variable]
  max_stat_i <- maxstat::maxstat.test(survival::Surv(time, event) ~ variable,data = surv_data,
                                      smethod = "LogRank", pmethod="none",minprop = minprop, maxprop = maxprop,alpha = alpha)
  res <- list()
  res[["minprop"]] <- minprop;res[["maxprop"]] <- maxprop;res[[variable]] <- max_stat_i
  res[["data"]] <- surv_data%>%rename(!!variable := "variable")
  res[["cutpoint"]] <- res[[variable]]$estimate[["estimated cutpoint"]]
  return(res)
} 

# 3: 该函数与survCutpoint()联用，基于maxstats方法对输入矩阵划分高低表达类别，高低表达组使用0/1表示，保存为tibble.
maxStatSplit <- function(survivalDF,patientID="PatientID",time="time",status="status",minProb=0.1,maxProb=0.9){
  
  survivalDF <- survivalDF[!(is.na(survivalDF[[time]])) | !(is.na(survivalDF[[status]])),]
  colName <- colnames(survivalDF)
  eventList <- c(patientID,time,status)
  survivalRes <- select(survivalDF,all_of(eventList))
  proteinNameList <- setdiff(colName,eventList)%>%as.vector()
  
  for (proteinName in proteinNameList) {
    tryCatch(
      {
        cutRes <- survCutpoint(survivalDF,time = time,event = status,minprop = minProb,maxprop = maxProb,variable = proteinName)
        survivalRes[proteinName] <- .dichotomize(
          x=cutRes$data[proteinName]%>%as_vector(),cutpoint=cutRes$cutpoint,right=TRUE,labels=c(0,1))%>% as_tibble()
      }, error = function(e) {
        print(e)
        # print(paste(proteinName,e,sep=": "))
      }
    )
  }
  return (survivalRes)
}


# 4.该函数基于指定分位数进行组别划分, 高低表达组使用0/1表示，保存为tibble;
percentageSplit <- function(survivalDF,patientID="PatientID",time="time",status="status",percentageThreshold=50){
  
  psplit <- function(x,percentageThreshold=50){
    cutoffThreshold = quantile(x,probs=percentageThreshold/100,na.rm=TRUE)
    tryCatch(
      {
        groups = .dichotomize(x,cutpoint=cutoffThreshold,right=TRUE,labels=c(0,1))%>%as.character()
      }, error = function(e){
        groups = rep(NULL, length(x))
      })
    return(groups)
  }
  
  survivalDF <- survivalDF[!(is.na(survivalDF[[time]])) | !(is.na(survivalDF[[status]])),]
  colName <- colnames(survivalDF)
  eventList <- c(patientID,time,status)
  survivalRes <- select(survivalDF,all_of(eventList))
  intensityDF <- select(survivalDF,setdiff(colName,eventList)%>%as.vector())
  groupDF <- apply(X=intensityDF,MARGIN=2,FUN=function(x) psplit(x,percentageThreshold=percentageThreshold))%>%as_tibble()
  survivalRes<-bind_cols(survivalRes,groupDF)
  return (survivalRes)
}

survivalSplit <- function(survivalDF,patientID="PatientID",time="time",status="status",method="percentageSplit",
                          percentageThreshold=0.5,minProb=0.1,maxProb=0.9){
  survivalRes <- NULL
  if (method=="maxstatSplit"){
    survivalRes <- maxStatSplit(survivalDF=survivalDF,patientID=patientID,time=time,status=status,minProb=minProb,maxProb=maxProb)
  }else if (method=="percentageSplit"){
    survivalRes <- percentageSplit(survivalDF=survivalDF,patientID=patientID,time=time,status=status,percentageThreshold=percentageThreshold)
  }else {
    cat("'method' parameter should be 'maxstatSplit' or 'percentageSplit'." )
  }
  return (survivalRes)
}



