#
# This is a Plumber API. You can run the API by clicking
# the 'Run API' button above.
#
# Find out more about building APIs with Plumber here:
#
#    https://www.rplumber.io/
#

library(plumber)
library(sva)
library(rjson)

#* @counts
#* @batch
#* @group
#* @post /removebatcheffectrnaseq
function(values, batch, group=NULL) {
  # counts, a matrix
  # batch, a vector
  # group, a vector
  if (length(group) >= 1) {
    adjusted <- sva::ComBat_seq(
      values,
      batch = batch,
      group = group,
      full_mod = TRUE
    )
  
    return (adjusted) # transform the matrix, the matrix will be transformed into a list in toJSON function
  } else {
    adjusted <- sva::ComBat_seq(
      values,
      batch = batch,
      group = NULL,
      full_mod = FALSE
    )
 
    return (adjusted) # 
  }
}
#

#* @values
#* @batch
#* @group
#* @post /removebatcheffectnormalvalues
function(values, batch, group = NULL) {
  # TODO: in these values, only accept group for outcome of interest and other covariate
  if (length(group) >= 1) {
    pheno <- data.frame(group = group)
    mod = model.matrix(~as.factor(group), data = pheno)
    
    adjusted = ComBat(dat = values, batch = batch, mod = mod, par.prior=TRUE, prior.plots=F)
    return (adjusted)
  } else {
    adjusted = ComBat(dat = values, batch = batch, mod = NULL, par.prior=TRUE, prior.plots=F)
    return (adjusted)
  }
}


#* @values
#* @batch
#* @group
#* @post /removebatcheffectnormalvaluesdirect
function(values, batch, group = NULL) {
  # TODO: in these values, only accept group for outcome of interest and other covariate
  # Not through django, call from the client directly
  if (length(group) >= 1) {
    pheno <- data.frame(group = group)
    mod = model.matrix(~as.factor(group), data = pheno)
    
    adjusted = ComBat(dat = values, batch = batch, mod = mod, par.prior=TRUE, prior.plots=F)
    
    return (rjson::toJSON(t(adjusted)))
  } else {
    adjusted = ComBat(dat = values, batch = batch, mod = NULL, par.prior=TRUE, prior.plots=F)
    
    return (rjson::toJSON(t(adjusted)))
  }
}

#' @filter cors
cors <- function(req, res) {
  
  res$setHeader("Access-Control-Allow-Origin", "*")
  
  if (req$REQUEST_METHOD == "OPTIONS") {
    res$setHeader("Access-Control-Allow-Methods","*")
    res$setHeader("Access-Control-Allow-Headers", req$HTTP_ACCESS_CONTROL_REQUEST_HEADERS)
    res$status <- 200 
    return(list())
  } else {
    plumber::forward()
  }
}



#* @apiTitle Plumber Example API
#* @apiDescription Plumber example description.

#* Echo back the input
#* @param msg The message to echo
#* @get /echo
function(msg = "") {
    list(msg = paste0("The message is: '", msg, "'"))
}

#* Plot a histogram
#* @serializer png
#* @get /plot
function() {
    rand <- rnorm(100)
    hist(rand)
}

#* Return the sum of two numbers
#* @param a The first number to add
#* @param b The second number to add
#* @post /sum
function(a, b) {
    as.numeric(a) + as.numeric(b)
}

# Programmatically alter your API
#* @plumber
function(pr) {
    pr %>%
        # Overwrite the default serializer to return unboxed JSON
        pr_set_serializer(serializer_unboxed_json())
}
