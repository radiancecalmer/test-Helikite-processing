library(tidyverse)
library(lubridate)
library(chron)
library(EnvStats)
library(forecast)
library(egg)
library(zoo)
library(peakPick)
library(oce)
library(plotly)

source('./conversion_functions.R')
source('./open_file_functions.R')


date <- "20211014"

ST.dir <- ".../SmartTether/"
FC.dir <- ".../Flight computer/"
POPS.dir <- ".../F"
stap.dir <- ".../STAP_processed/"
ozone.dir <- ".../Brigerbad_2021/Ozone/"
Pico.dir <- ".../summarydata/"
FILT.dir <- ".../FILT/"
cpc.dir <- ".../mCPC21/"


#Open Flight computer data 
FC.file.list <- list.files(path = FC.dir, pattern = date)
FC <- data.frame()
for(FC.path in FC.file.list){
  
  FC.temp <- FC_open(FC.file = FC.path, data.dir = FC.dir, second_shift = -2*3600+32)
  FC <- rbind(FC,FC.temp)
  
}
rm(FC.temp)
FC <- FC %>%
  select(-PartCon)

FC$datetime <- as.character(FC$datetime)
FC <- FC[!duplicated(FC$datetime),]


ggplot(FC) +
  geom_path(aes(x = as.POSIXct(datetime), y = P_baro)) +
  scale_x_datetime() +
  scale_y_reverse() +
  theme_bw()


#Open SmartTether data
ST.file.list <- list.files(path = ST.dir, pattern = date)
ST <- data.frame()
for(ST.path in ST.file.list[2]){
  ST.temp <- SmartTether_open(ST.file = ST.path, data.dir = ST.dir, date_posicx = paste0(substr(date,1,4),"-",substr(date,5,6),"-",substr(date,7,8)))
  ST <- rbind(ST,ST.temp)
  
}
rm(ST.temp)


#Open Flight computer data 
POPS.file.list <- list.files(path = POPS.dir, pattern = "HK")
POPS <- data.frame()
for(POPS.path in POPS.file.list){
  POPS.temp <- POPS_open(POPS.file = POPS.path, data.dir = POPS.dir, time_diff = 2)
    
  POPS <- rbind(POPS,POPS.temp)
  
}
rm(POPS.temp)
POPS$datetime <- as.character(POPS$datetime)
POPS <- POPS[!duplicated(POPS$datetime),]


#Open mSEMS data
mSEMS.dir <- ".../Flight_inverted/"
mSEMS.filename <- "mSEMS_103_211014_085223_INVERTED.txt"
conc.filename <- "mSEMS_103_211014_085223_total_conc.txt"


#A continuer ici (regarder script mSEMS)
mSEMS <- read.table(paste0(mSEMS.dir,mSEMS.filename), header = T)
mSEMS$datetime <- paste0("20",substr(mSEMS$Date,1,2),"-",substr(mSEMS$Date,4,5),"-",substr(mSEMS$Date,7,8)," ",mSEMS$Time)

mSEMS_conc <- read.table(paste0(mSEMS.dir,conc.filename), header = T)

mSEMS_conc <- cbind(mSEMS$datetime, mSEMS_conc)
colnames(mSEMS_conc) <- c("datetime", "mSEMS_conc")


#Open STAP data
stap.file.list <- list.files(path = stap.dir, pattern = substr(date,3,8))
stap <- data.frame()

for(stap.path in stap.file.list){
  stap.temp <- read.table(file = paste0(stap.dir,stap.path), header = T, sep = ",")
  stap <- rbind(stap, stap.temp)
  
}
rm(stap.temp)

#shift stap time by 2 hours
stap <- stap %>%
  mutate(datetime = as.POSIXct(datetime)-2*3600) %>%
  mutate(datetime = as.character(datetime))



start <- "2021-10-14 08:57:48"
end <- "2021-10-14 10:27:28"


POPS <- POPS %>%
  mutate(datetime = as.POSIXct(datetime)) %>%
  filter(datetime >= start & datetime <= end) %>%
  mutate(datetime = as.character(datetime)) %>%
  select(c(datetime, P, PartCon, POPS_Flow, b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15))


ST <- ST %>%
  mutate(datetime = as.POSIXct(datetime)) %>%
  filter(datetime >= start & datetime <= end) %>%
  mutate(datetime = as.character(datetime))

FC <- FC %>%
  mutate(datetime = as.POSIXct(datetime)) %>%
  filter(datetime >= start & datetime <= end) %>%
  mutate(datetime = as.character(datetime))


stap <- stap %>%
  mutate(datetime = as.POSIXct(datetime)) %>%
  filter(datetime >= start & datetime <= end) %>%
  mutate(datetime = as.character(datetime))





mSEMS_conc <- mSEMS_conc %>%
  mutate(datetime = as.POSIXct(datetime)) %>%
  filter(datetime >= start & datetime <= end) %>%
  mutate(datetime = as.character(datetime))

data <- POPS %>%
  full_join(FC) %>% 
  full_join(ST) %>%
  full_join(stap) %>%
  full_join(mSEMS_conc)

data <- data[!duplicated(data$datetime),]

data <- arrange(data, as.POSIXct(datetime))

for(c in c(33:43)){
  data[,c] <- na.interp(data[,c])
}

p <- ggplot(data) +
  #geom_path(aes(x = as.POSIXct(datetime), y = stap_pres+11, color = "STAP")) +
  geom_path(aes(x = as.POSIXct(datetime), y = P+1, color = "POPS")) +
  geom_path(aes(x = as.POSIXct(datetime), y = P_baro+1, color = "FC")) +
  geom_path(aes(x = as.POSIXct(datetime), y = P_mbar+2.9, color = "SmartTether")) +
  scale_x_datetime() +
  scale_y_reverse() +
  theme_bw()

ggplotly(p)



#Average the pressure of all sensors 
data$P_avg <- rowMeans(data[c("P","P_mbar", "P_baro")], na.rm = T)

#remove wind speed spikes 
ggplot(data) +
  geom_path(aes(x = as.POSIXct(datetime), y = P_avg, color = "P_avg"), size = 1) +
  #geom_path(aes(x = as.POSIXct(datetime), y = smoothed_WS, color = "smoothed WS"), size = 1) +
  scale_x_datetime() +
  scale_y_reverse() +
  theme_bw()


inter1 <- as.POSIXct("2021-10-14 09:46:30")

ggplot(data) +
  geom_path(aes(x = as.POSIXct(datetime), y = P_avg, color = "P_avg"), size = 1) +
  geom_vline(xintercept = inter1) +
  scale_x_datetime() +
  scale_y_reverse() +
  theme_bw()




#Altitude calculation 
data$P_ref <- NA
data$P_ref[1] <- mean(data$P_avg[c(1:10)])
data$P_ref[which(as.POSIXct(data$datetime)==inter1)] <- data$P_avg[which(as.POSIXct(data$datetime)==inter1)]
data$P_ref[dim(data)[1]] <- mean(tail(data$P_avg, 10))
data$P_ref <- na.interp(data$P_ref)

data$T_ref <- NA
data$T_ref[1] <- mean(data$T_degC[c(1:10)])
data$T_ref[which(as.POSIXct(data$datetime)==inter1)] <- data$T_degC[which(as.POSIXct(data$datetime)==inter1)]
data$T_ref[dim(data)[1]] <- mean(tail(data$T_degC, 10))
data$T_ref <- na.interp(data$T_ref)


ggplot(data) +
  geom_path(aes(x = as.POSIXct(datetime), y = P_avg, color = "Pressure"), size = 1) +
  geom_path(aes(x = as.POSIXct(datetime), y = P_ref, color = "Ref"), size = 1) +
  scale_x_datetime() +
  scale_y_reverse() +
  theme_bw()


ggplot(data) +
  geom_path(aes(x = as.POSIXct(datetime), y = T_degC, color = "T"), size = 1) +
  #geom_path(aes(x = as.POSIXct(datetime), y = smoothed_T, color = "smoothed T"), size = 1) +
  scale_x_datetime() +
  scale_y_continuous() +
  theme_bw()


data$altitude <- round(p.to.alt(p = data$P_avg, p0 = data$P_ref, t0 = data$T_ref, h0 = 654.5), digits = 1) - 653.5
data$altitude[which(data$altitude<0)] = 0

ggplot(data) +
  geom_path(aes(x = as.POSIXct(datetime), y = altitude), size = 1) +
  scale_x_datetime() +
  scale_y_continuous() +
  theme_bw()


#Check POPS flow 

ggplot(data) +
  geom_path(aes(x = as.POSIXct(datetime), y = POPS_Flow)) +
  scale_x_datetime() +
  scale_y_continuous() +
  theme_bw()

#compute mean flow 
mean_flow <- mean(data$POPS_Flow, na.rm = T)  

#Extract bins counts to recalculate concentration 
bins <- paste0("b",c(3:15))
counts.df <- data %>%
  select(all_of(bins))


data$N150 <- rowSums(counts.df)/mean_flow



#Final variable selection 


data.final <- data %>%
  select(datetime, altitude, T_degC, RH, P_avg, WD, WS, Lat, Lon, PartCon, N150, mSEMS_conc, CO2, sigmab_smth_invmm, sigmag_smth_invmm, sigmar_smth_invmm, 
         POPS_Flow, b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15,
         TEMPbox, mFlow, TEMPsamp, RHsamp, vBat)  
data.final$flight = 25


write.table(data.final, ".../flight_data.txt", row.names = F, sep = ",")





