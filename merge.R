setwd('/home/neik/Kaggle/WalmartRecruiting/')

dfStore <- read.csv(file='CSV/stores.csv')
dfTrain <- read.csv(file='CSV/train.csv')
dfTest <- read.csv(file='CSV/test.csv')
dfFeatures <- read.csv(file='CSV/features.csv')

dfFeatures$haveMarkDown <- 1*(as.POSIXct(dfFeatures$Date) > as.POSIXct('2011-11-04'))

markdowns <- c('MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5')
markdown_matrix <- dfFeatures[dfFeatures$haveMarkDown==1, markdowns]
library(timeSeries)
markdown_matrix <- interpNA(markdown_matrix, method = "linear")
dfFeatures[dfFeatures$haveMarkDown==1, markdowns] <- round(markdown_matrix,2)

# replace missing Markdowns by median
dfFeatures$MarkDown1[is.na(dfFeatures$MarkDown1)] <- round(median(dfFeatures$MarkDown1, na.rm=TRUE),2)
dfFeatures$MarkDown2[is.na(dfFeatures$MarkDown2)] <- round(median(dfFeatures$MarkDown2, na.rm=TRUE),2)
dfFeatures$MarkDown3[is.na(dfFeatures$MarkDown3)] <- round(median(dfFeatures$MarkDown3, na.rm=TRUE),2)
dfFeatures$MarkDown4[is.na(dfFeatures$MarkDown4)] <- round(median(dfFeatures$MarkDown4, na.rm=TRUE),2)
dfFeatures$MarkDown5[is.na(dfFeatures$MarkDown5)] <- round(median(dfFeatures$MarkDown5, na.rm=TRUE),2)

store <- unique(dfFeatures$Store)
# extrapolate CPI for missing values
# missing Unemployments were replaced by the unemplyment of nearest month
for (i in store) {
  cpi <- dfFeatures[dfFeatures$Store==i, ]$CPI
  ls1 <- na.omit(cpi)
  dd <- mean(ls1[2:length(ls1)]-ls1[1:length(ls1)-1])
  cpi[is.na(cpi)] <- seq(1,length(cpi)-length(ls1))*dd + ls1[length(ls1)]
  dfFeatures[dfFeatures$Store==i, ]$CPI <- round(cpi,2)
  
  uep <- dfFeatures[dfFeatures$Store==i, ]$Unemployment
  ls2 <- na.omit(uep)
  uep[is.na(uep)] <- ls2[length(ls2)]
  dfFeatures[dfFeatures$Store==i, ]$Unemployment <- round(uep,2)
}

# Merge Type and Size
dfTrainTmp <- merge(x=dfTrain, y=dfStore, all.x=TRUE)
dfTestTmp <- merge(x=dfTest, y=dfStore, all.x=TRUE)

# Merge all the features
dfTrainMerged <- merge(x=dfTrainTmp, y=dfFeatures, all.x=TRUE)
dfTestMerged <- merge(x=dfTestTmp, y=dfFeatures, all.x=TRUE)


# Sort the data by store, dept, date
dfTrainMerged <- dfTrainMerged[with(dfTrainMerged, order(Store, Dept, Date)), ]
dfTestMerged <- dfTestMerged[with(dfTestMerged, order(Store, Dept, Date)), ]

dfTrainMerged$IsHoliday <- 1*dfTrainMerged$IsHoliday
dfTestMerged$IsHoliday <- 1*dfTestMerged$IsHoliday

# Sort the data by names and by store, dept, date
colNames <- c('Store','Dept','Date','IsHoliday','Type','Size','Temperature','Fuel_Price','CPI','Unemployment',
              'haveMarkDown', 'MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5')

dfTrainMerged <- data.frame(dfTrainMerged[, c(colNames,'Weekly_Sales')])
dfTestMerged <- data.frame(dfTestMerged[, colNames])

# Save datasets
write.table(x=dfTrainMerged, file='CSV/trainMerged.csv', sep=',', row.names=FALSE, quote=FALSE)            
write.table(x=dfTestMerged, file='CSV/testMerged.csv', sep=',', row.names=FALSE, quote=FALSE)
=======
# Sort the data by names and by store, dept, date
colNames <- c('Store','Dept','Date','IsHoliday','Type','Size','Temperature','Fuel_Price','CPI','Unemployment',
              'MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','Weekly_Sales')

dfTrainMerged <- data.frame(dfTrainMerged[,colNames])
dfTrainMerged <- dfTrainMerged[with(dfTrainMerged, order(Store, Dept, Date)), ]
dfTestMerged <- data.frame(dfTestMerged[,colNames[-length(colNames)]])
dfTestMerged <- dfTestMerged[with(dfTestMerged, order(Store, Dept, Date)), ]

# Save datasets
write.table(x=dfTrainMerged,file='trainMerged.csv', sep=',', row.names=FALSE, quote=FALSE)
write.table(x=dfTestMerged,file='testMerged.csv', sep=',', row.names=FALSE, quote=FALSE)
