
formatGEOfilePath <- function(geoSeriesAcc) {
  if(nchar(geoSeriesAcc) >= 6) {
    seriesSub <- paste(substr(geoSeriesAcc, 1, nchar(geoSeriesAcc) - 3), "nnn", sep = "")
  } else {
    seriesSub <- "GSEnnn"
  }
  return (seriesSub)
}



