setwd('/home/neik/Kaggle/WalmartRecruiting/')
library("forecast")
library("plyr")
# manipulate strings
library("stringr")
library("reshape2")

# read raw training and test sets
rawTrain <- read.csv(file='CSV/train.csv')
rawTest <- read.csv(file='CSV/test.csv')
# build id
rawTrain$id <- str_c(rawTrain$Store, "_", rawTrain$Dept)
rawTest$id <- str_c(rawTest$Store, "_", rawTest$Dept)

# build "train" with 143 dates for all departments in training and test sets
# fill missing weekly sales with 0.
#
df.date <- rawTrain$Date[1:143]
df.dept <- data.frame( unique( c(rawTrain$id, rawTest$id) )  )
df <- merge(df.date, df.dept)
names(df) <- c("Date","id")

train <- merge(df, rawTrain[,c("id","Date","Weekly_Sales")], all.x=T, all.y=T)
train[is.na(train)] <- 0.0
train <- train[, c("id","Date","Weekly_Sales")]

## ===============================================
## MODELS: will predict weekly sales for 39 days
## ===============================================
##Exponential Smoothing using state space approach
ets.f <- ddply(train, "id", function(x) stlf(ts(x[,3],frequency=52),method="ets",s.window=3,h=39)$mean)

##Arima
# ets.f <- ddply(train, "id", function(x) stlf(ts(x[,3],frequency=52),method="arima",h=39,stepwise=FALSE,approx=FALSE)$mean)

##Naive Method
# ets.f <- ddply(train, "id", function(x) stlf(ts(x[,3],frequency=52),method="naive", h=39)$mean)

# variable: dates;   value: predicted weekly_sales
names(ets.f) <- c("dept", lapply(rawTest$Date[1:39], as.character))
test.pred <- data.frame(melt(ets.f, id=c("dept")))
test.pred$id <- str_c(test.pred$dept, "_", test.pred$variable)


sampleSubmit <- read.csv(file='CSV/sampleSubmission.csv')
sampleSubmit$Weekly_Sales <- round(test.pred[match(sampleSubmit$Id, test.pred$id), ]$value, 2)

write.csv(sampleSubmit, file = "CSV/submission.May20.csv", row.names = FALSE, quote=FALSE)


arima <- read.csv(file='CSV/submission.May20.arima.csv')
naive <- read.csv(file='CSV/submission.May20.naive.csv')
ets <- read.csv(file='CSV/submission.May20.ets.csv')
gbr <- read.csv(file='CSV/submission_May5.gbr.csv')
average <- data.frame(Id = arima$Id, 
                      Weekly_Sales = round((arima$Weekly_Sales + naive$Weekly_Sales + 
                                              ets$Weekly_Sales + gbr$Weekly_Sales)/4, 2)  )
write.csv(average, file = "CSV/submission.May20.average.csv", row.names = FALSE, quote=FALSE)
