##  Written by Kaikun Xu

## 功能:本节基于蛋白的高低表达分组，计算单蛋白的Hazard Ratio等参数,可用于森林图的绘制.
## 注释:
## 1. 输入为txt或csv表格的路径;
## 2. 输入数据表至少需要包含两类数据：
##    + 临床信息列：
##       - 终点状态列--死亡/未死亡，复发/未复发等，需使用0/1表示；
##       - 随访时间列--时间信息，应为float类型；
##    + 用于计算的高低表达组列：0/1分别对应低表达组/高表达组；
## 备注： 此程序避免了data.frame header中的连词线，空格等被转化为小数点



# 0: ipak()函数检查所需函数包是否安装,并将之加载至环境中.
# 
# ipak <- function(pkg){
#   new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
#   if (length(new.pkg)) {}
#   install.packages(new.pkg, dependencies = TRUE)
#   sapply(pkg, require, character.only = TRUE)
# }
# packages <- c("here","tidyverse","dplyr","survival","survminer")
# ipak(packages)


# 1: 辅助函数定义(本版不使用)
## 1-1 返回默认值

# `%or%` <- function(a, b) {
#   # 函数功能: 本函数用于返回默认值.
#   # << cutoffDict<-c("OS"=60,"DFS"=24)
#   # << cutoffDict["PFS"]%or%24
#   # << 24
#   cmp = function(a,b) if (identical(a, FALSE)|| is.null(a) ||is.na(a) ||
#                           is.nan(a) ||length(a) == 0) {b} else {a}
#   if (length(a) > 1) {mapply(cmp, a, b)} else {cmp(a, b)}
# } 

library("survival")

## 1-2 计算特定时间点的生存概率
probTime <- function(formula,data,event,cutoffTime){
  # 函数功能: 该函数用于计算特定时间点的生存概率;在最长随访时间后的时间点,无法计算对应概率.
  if (max(data[[event]])>=cutoffTime){
    summary(survival::survfit(formula, data = data),times=cutoffTime,extend = FALSE)$surv
  }else{NA}
}


# 2.预后注释函数
survivalAnnotation <- function(splitDF,patientID,time,status){
  # 函数功能: 
  splitDF <- splitDF[!(is.na(splitDF[[time]])) | !(is.na(splitDF[[status]])),]%>% mutate(across(time, as.numeric))
  colName <- colnames(splitDF)
  indexList <- c(patientID,time,status)
  proteinNameList <- setdiff(colName,indexList)%>%as.vector()
  
  coxRes = tibble("Variable"= character(),"n/N in high group"= character(),"n/N in low group"= character(),"favor/unfavor"= character(),
                  "Hazard ratio"= numeric(),"Hazard ratio lower"= numeric(),"Hazard ratio upper"= numeric(),"HR (95% CI)"= character(),
                  "Wald test p-value"= numeric(),"Log-rank test p-value"= numeric())
  for (variable in proteinNameList){
    tryCatch({
      # 公式定义:
      # + *probFormula*用于计算给定数据集上特定时间点的生存概率: probFormula <- as.formula(paste("Surv(`", time, "`,`", status, "`) ~", 1, sep =""))
      # + *survivalFormula*用于对高低表达组进行Cox回归分析和Log-rank检验: survivalFormula <- as.formula(paste("Surv(`", time, "`,`", status, "`) ~`", variable,"`",sep =""))
      survivalFormula <- as.formula(paste("Surv(`", time, "`,`", status, "`) ~`", variable,"`",sep =""))
      data <- select(splitDF,all_of(append(indexList,variable)))
      highData <- data%>%filter(.data[[variable]]==1); lowData <- data%>%filter(.data[[variable]]==0)
      numInHigh <- paste(toString(dim(highData%>%filter(.data[[status]]==1))[1]),toString(dim(highData)[1]),sep="\\")
      numInLow <- paste(toString(dim(lowData%>%filter(.data[[status]]==1))[1]),toString(dim(lowData)[1]),sep="\\")
      # print(numInLow,numInHigh)
      coxModel <- survival::coxph(formula = survivalFormula, data = data)
      hr <-summary(coxModel)$coef[2]; hrLow <-summary(coxModel)$conf.int[, "lower .95"]; hrHigh <-summary(coxModel)$conf.int[, "upper .95"]
      hrCI <- paste(sprintf("%0.2f",hr)," (", sprintf("%0.2f",hrLow),"-",sprintf("%0.2f",hrHigh),")",sep="")
      waldP <- summary(coxModel)$wald[["pvalue"]]; logrankP<-summary(coxModel)$sctest[[3]]
      favorStatus <-  if (summary(coxModel)$coef[2] > 1) "unfavor" else "favor"
      coxRes <- coxRes%>%add_row("Variable"=variable,"n/N in high group"=numInHigh,"n/N in low group"=numInLow,"favor/unfavor"=favorStatus,
                                 "Hazard ratio"=hr,"Hazard ratio lower"=hrLow,"Hazard ratio upper"=hrHigh,"HR (95% CI)"=hrCI,
                                 "Wald test p-value"=waldP,"Log-rank test p-value"=logrankP)
    }, error = function(error_message){
      print(error_message)
      # print(paste(variable,e,sep=": "))
    })
  }
  return(coxRes) 
}