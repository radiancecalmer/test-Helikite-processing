#The following functions can be applied to the different data files of the instruments and format them automatically
# it does not

#load the following libraries
#Prepare data for Brice -> flight with MicroMegas
library(tidyverse)
library(lubridate)
library(chron)



#************************************************************************************************************************************************
#Open SmartTether data 
#
#************************************************************************************************************************************************

SmartTether_open = function(
  ST.file = NULL,
  data.dir = NULL,
  date_posicx = "1970-01-01",
  time_zone = "CET",
  var.sel = c("datetime","P_mbar","T_degC","RH","WD","WS","Lat","Lon")){


    
ST.path = paste0(data.dir,ST.file)  
ST <- read.csv(ST.path, skip = 3) %>%
  mutate(date = date_posicx,
         datetime = paste0(date, " ", Time)) %>%
  relocate(datetime, .before = Time) %>%
  relocate(date, .after = Time)



colnames(ST) <- c("datetime","Computer.time","date","Comment","Module.ID","Alt_m","P_mbar","T_degC","RH","WD","WS","voltST","UTC.time","Lat","Lon","Course_deg","Speed")


return(ST)

}


#************************************************************************************************************************************************
#Open POPS data 
#
#************************************************************************************************************************************************

POPS_open = function(
  POPS.file = NULL,
  data.dir = NULL,
  time_zone = "CET",
  time_diff = 0,
  second_shift = 0,
  var.sel = c("datetime","P","PartCon","N_186","PartCt","POPS_Flow","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","b10","b11","b12","b13","b14","b15","TofP","Temp")){
  

POPS.path <- paste0(data.dir,POPS.file)


POPS <- read.csv(POPS.path)

POPS$DateTime <- as.POSIXct(POPS$DateTime, tz = time_zone, origin = "1970-01-01") - time_diff*60*60
colnames(POPS)[1] <- "datetime"


POPS <- POPS %>%
  mutate(b0 = lag(b0),
         b1 = lag(b1),
         b2 = lag(b2),
         b3 = lag(b3),
         b4 = lag(b4),
         b5 = lag(b5),
         b6 = lag(b6),
         b7 = lag(b7),
         b8 = lag(b8),
         b9 = lag(b9),
         b10 = lag(b10),
         b11 = lag(b11),
         b12 = lag(b12),
         b13 = lag(b13),
         b14 = lag(b14),
         b15 = lag(b15))


POPS <- POPS[-1,]


#POPS$PartCon150 = rowSums(POPS[,c(32:44)])/POPS$POPS_Flow 
POPS$N_186 = rowSums(POPS[,c(32:44)])/mean(POPS$POPS_Flow[which(POPS$POPS_Flow >= 2.9 & POPS$POPS_Flow <= 3.1)]) 


POPS <- POPS %>% 
  select(all_of(var.sel)) %>%
  relocate(N_186, .after = PartCon) %>%
  mutate(datetime = datetime + second_shift) %>%
  mutate(datetime = as.character(datetime))

return(POPS)
}


#************************************************************************************************************************************************
#Open POPS raw
#
#************************************************************************************************************************************************

POPS_open_raw = function(
  POPS.file = NULL,
  data.dir = NULL,
  time_diff = 1,
  time_zone = "CET",
  second_shift = 0){
  
  
  POPS.path <- paste0(data.dir,POPS.file)
  
  
  POPS <- read.csv(POPS.path)
  
  POPS$DateTime <- as.POSIXct(POPS$DateTime, tz = time_zone, origin = "1970-01-01") - time_diff*60*60
  colnames(POPS)[1] <- "datetime"
  
  
 # POPS <- POPS[-1,]
 # POPS$PartCon150 = rowSums(POPS[,c(32:44)])/POPS$POPS_Flow 

  
  return(POPS)
}




#************************************************************************************************************************************************
#Open Flight computer data 
#
#************************************************************************************************************************************************

FC_open = function(
  FC.file = NULL,
  data.dir = NULL,
  time_zone = "CET",
  second_shift = 0){
  
  FC.path <- paste0(data.dir,FC.file)
  
  FC <- read.table(FC.path, sep = ",", header = T)
  #FC <- FC[,-1]
  if("DateTime" %in% FC$DateTime){
  FC <- FC[-which(FC$DateTime == "DateTime"),] #removes lines with headers 
  }
  #FC$DateTime <- substr(FC$DateTime, 2, nchar(FC$DateTime))
  
  FC$DateTime <- gsub(FC$DateTime, pattern = "$", fixed = T, replacement = "")
  FC$DateTime <- as.POSIXct(as.numeric(FC$DateTime), tz = time_zone, origin = "1970-01-01")
  colnames(FC)[1] <- "datetime"

  #FC$vBat <- as.numeric(substr(FC$vBat,1,nchar(FC$vBat)-1))
    
   FC <- FC %>%
     mutate(CO2 = as.numeric(CO2), P_baro = as.numeric(P_baro), TEMPbox = as.numeric(TEMPbox), TEMPsamp = as.numeric(TEMPsamp), mFlow = as.numeric(mFlow), RHsamp = as.numeric(RHsamp), vBat = as.numeric(vBat)) 
  # 
  
  FC$datetime <- FC$datetime + second_shift
  
  FC <- FC[!duplicated(FC$datetime),]
  
  return(FC)
  
}


FC_open_ALPACA = function(
  FC.file = NULL,
  data.dir = NULL,
  time_zone = "CET",
  second_shift = 0){
  
  FC.path <- paste0(data.dir,FC.file)
  
  FC <- read.table(FC.path, sep = ",", header = T, fill = T)
  #FC <- FC[,-1]
  if("DateTime" %in% FC$DateTime){
    FC <- FC[-which(FC$DateTime == "DateTime"),] #removes lines with headers 
  }
  #FC$DateTime <- substr(FC$DateTime, 2, nchar(FC$DateTime))
  FC <- FC[,-1]
  #FC$DateTime <- gsub(FC$DateTime, pattern = "$", fixed = T, replacement = "")
  FC$DateTime <- as.POSIXct(as.numeric(FC$DateTime), tz = time_zone, origin = "1970-01-01")
  colnames(FC)[1] <- "datetime"
  
  FC$vBat <- as.numeric(substr(FC$vBat,1,nchar(FC$vBat)-1))
  
  FC <- FC %>%
    mutate(CO2 = as.numeric(CO2), 
           P_baro = as.numeric(P_baro), 
           TEMPbox = as.numeric(TEMPbox), 
           TEMPsamp = as.numeric(TEMPsamp), 
           mFlow = as.numeric(mFlow), 
           RHsamp = as.numeric(RHsamp), 
           vBat = as.numeric(vBat)) 
  # 
  
  FC$datetime <- FC$datetime + second_shift
  
  FC <- FC[!duplicated(FC$datetime),]
  
  return(FC)
}


FC_open2 = function(
  FC.file = NULL,
  data.dir = NULL,
  time_zone = "CET",
  second_shift = 0,
  CO2 = F){
  
  FC.path <- paste0(data.dir,FC.file)
  
  FC <- read.table(FC.path, header = T, sep = ",")
  #FC <- FC[,-1]
  
  FC$hour <- as.numeric(gsub("\\$", "", FC$hour))
  FC$hour <- sprintf("%02d",FC$hour)
  FC$minute <- sprintf("%02d",FC$minute)
  FC$second <- sprintf("%02d",FC$second)
  FC$month <- sprintf("%02d",FC$month)
  FC$day <- sprintf("%02d",FC$day)
  
  
  FC$datetime <- paste0(FC$year,"-",FC$month,"-",FC$day," ",FC$hour,":",FC$minute,":",FC$second)
  

  FC <- FC %>%
    select(c(datetime,P_baro,CO2,TEMPbox,mFlow,TEMPsamp,RHsamp,vBat))
  
  if(!CO2){
    FC$CO2 <- NA
  }
    
  #mutate(CO2 = as.numeric(CO2), P_baro = as.numeric(P_baro), TEMPbox = as.numeric(TEMPbox), TEMPsamp = as.numeric(TEMPsamp), mFlow = as.numeric(mFlow), RHsamp = as.numeric(RHsamp), vBat = as.numeric(vBat)) 
   
  FC$datetime <- as.POSIXct(FC$datetime)
  
  FC$datetime <- FC$datetime + second_shift
  
  FC <- FC[!duplicated(FC$datetime),]
  
  return(FC)
  
}

FC_open3 = function(
  FC.file = NULL,
  data.dir = NULL,
  CO2 = F,
  MOUDI = F){
  
  FC.path <- paste0(data.dir,FC.file)
  
  FC <- read.table(FC.path, header = T, sep = ",")
  
  FC <- FC[,-1]
  
  FC <- FC %>%
    mutate(CO2 = as.numeric(CO2), P_baro = as.numeric(P_baro), TEMPbox = as.numeric(TEMPbox), TEMPsamp = as.numeric(TEMPsamp), mFlow = as.numeric(mFlow), RHsamp = as.numeric(RHsamp), vBat = as.numeric(vBat)) 
  # 
  
  if(!CO2){
    FC$CO2 <- NA
  }
  
  if(!MOUDI){
    FC$mFlow <- NA
  }
  
  
  return(FC)
  
}




#************************************************************************************************************************************************
#Open Pico data 
#
#************************************************************************************************************************************************


Pico_open = function(
  Pico.file = NULL,
  data.dir = NULL,
  var.sel = c("datetime","Inlet.Number","N2O_ppm","H2O_ppm","CO_ppm")){


Pico.path <- paste0(data.dir,Pico.file)

Pico <- read.table(Pico.path, sep = ",", header = T)

Pico$Time.Stamp <- as.POSIXct(Pico$Time.Stamp, format = '%m/%d/%Y %H:%M:%S')
Pico$Time.Stamp <- as.POSIXct(Pico$Time.Stamp, format = '%Y-%m%-%d %H:%M:%S')

colnames(Pico) <- c("datetime","Inlet.Number","P_pico","T_pico","N2O_ppm","H2O_ppm","CO_ppm","vBat","Power","Current","SOC")


Pico <- Pico %>%
  select(all_of(var.sel))

}


#*********************************************************************************************************************************************
#*
#* LOAD ozone data
#* 
#* *******************************************************************************************************************************************

ozone_open = function(
  O3.file = NULL,
  data.dir = NULL,
  var.sel = c("datetime","ozone","cell_temp","cell_pressure","flow_rate")){


O3.path <- paste0(data.dir,O3.file) 

O3 <- read.table(O3.path, sep = ",", header = F, skip = 2, fill = T)

O3 <- O3[,-7]
colnames(O3) <- c("ozone","cell_temp","cell_pressure","flow_rate","date","time")

O3$datetime <- paste0("20",substr(O3$date,7,8),"-",substr(O3$date,4,5),"-",substr(O3$date,1,2)," ",O3$time)

O3 <- O3 %>%
  select(all_of(var.sel))

}


#*********************************************************************************************************************************************
#*
#* LOAD CPC data
#* 
#* *******************************************************************************************************************************************


cpc_open = function(
  cpc.file = NULL,
  data.dir = NULL,
  skip = 13){
  
cpc.path <- paste0(data.dir,cpc.file) 

cpc <- read.table(cpc.path, header = T, comment.char = "", fill = T, skip = skip)
colnames(cpc)[1] <- "YY.MM.DD"

cpc <- cpc[-nrow(cpc),]

cpc$datetime <- paste0("20",substr(cpc$YY.MM.DD,1,2),"-",substr(cpc$YY.MM.DD,4,5),"-",substr(cpc$YY.MM.DD,7,8)," ",cpc$HR.MN.SC)

cpc <- cpc %>%
  relocate(datetime, .before = YY.MM.DD)
}


#*********************************************************************************************************************************************
#*
#* LOAD SEMS scan data
#* 
#* *******************************************************************************************************************************************


SEMS_open = function(
    SEMS.file = NULL,
    data.dir = NULL,
    skip = 53,
    adjust.EndDatetime = T){
  
  path <- paste0(data.dir,SEMS.file) 
  
  SEMS <- read.table(path, header = T, comment.char = "", fill = T, skip = skip)
  colnames(SEMS)[1] <- "StartDate"
  
  SEMS <- SEMS %>%
    mutate(StartDatetime = paste0("20",substr(StartDate,1,2),"-",substr(StartDate,3,4),"-",substr(StartDate,5,6)," ",StartTime))
  
  if(adjust.EndDatetime){
    
  SEMS$EndDatetime <- NA
  SEMS$EndDatetime[c(1:(nrow(SEMS)-1))] <- SEMS$StartDatetime[c(2:nrow(SEMS))]
  dT <- as.numeric(as.POSIXct(SEMS$EndDatetime[1]))-as.numeric(as.POSIXct(SEMS$StartDatetime[1]))
  SEMS$EndDatetime[nrow(SEMS)] <- as.character(as.POSIXct(SEMS$StartDatetime[nrow(SEMS)])+dT)
  
  } else {
    
    SEMS <- SEMS %>%
      mutate(EndDatetime = paste0("20",substr(EndDate,1,2),"-",substr(EndDate,3,4),"-",substr(EndDate,5,6)," ",EndTime))
    
  }
  
  SEMS <- SEMS %>%
    relocate(StartDatetime, 1) %>%
    relocate(EndDatetime, .after = StartDatetime) %>%
    select(-c(StartDate,StartTime,EndDate,EndTime))
  
}



#*********************************************************************************************************************************************
#*
#* LOAD SEMS raw data
#* 
#* *******************************************************************************************************************************************


rawSEMS_open = function(
    SEMS.file = NULL,
    data.dir = NULL,
    skip = 72,
    adjust.EndDatetime = F){
  
  path <- paste0(data.dir,SEMS.file) 
  
  rawSEMS <- read.table(path, header = T, comment.char = "", fill = T, skip = skip)
  colnames(rawSEMS)[1] <- "StartDate"
  
  rawSEMS <- rawSEMS %>%
    mutate(StartDatetime = paste0("20",substr(StartDate,1,2),"-",substr(StartDate,3,4),"-",substr(StartDate,5,6)," ",StartTime))
  
  if(adjust.EndDatetime){
    
    rawSEMS$EndDatetime <- NA
    rawSEMS$EndDatetime[c(1:(nrow(rawSEMS)-1))] <- rawSEMS$StartDatetime[c(2:nrow(rawSEMS))]
    dT <- as.numeric(as.POSIXct(rawSEMS$EndDatetime[1]))-as.numeric(as.POSIXct(rawSEMS$StartDatetime[1]))
    rawSEMS$EndDatetime[nrow(rawSEMS)] <- as.character(as.POSIXct(rawSEMS$StartDatetime[nrow(rawSEMS)])+dT)
    
  } else {
    
    rawSEMS <- rawSEMS %>%
      mutate(EndDatetime = paste0("20",substr(EndDate,1,2),"-",substr(EndDate,3,4),"-",substr(EndDate,5,6)," ",EndTime))
    
  }
  
  rawSEMS <- rawSEMS %>%
    relocate(StartDatetime, 1) %>%
    relocate(EndDatetime, .after = StartDatetime) %>%
    select(-c(StartDate,StartTime,EndDate,EndTime)) %>% 
    mutate(Conc_int = NA,
           Cnts_int = NA) %>%
    relocate(Cnts_int, .before = Bin_Cnts1) %>%
    relocate(Conc_int, .before = Bin_Cnts1)
  
  rawSEMS$Cnts_int <- rowSums(rawSEMS[,which(colnames(rawSEMS)=="Bin_Cnts1"):ncol(rawSEMS)]) 
  rawSEMS$Conc_int <- rawSEMS$Cnts_int / (rawSEMS$CPC_A_FlwAvg*1000/60)         #(rawSEMS$CPC_A_FlwAvg*1000*(as.numeric(as.POSIXct(rawSEMS$EndDatetime))-as.numeric(as.POSIXct(rawSEMS$StartDatetime)))/60)
  
  return(rawSEMS)
  
}


#*********************************************************************************************************************************************
#*
#* LOAD inverted mSEMS scan data
#* 
#* *******************************************************************************************************************************************


mSEMS_open = function(
    mSEMS.file = NULL,
    data.dir = NULL,
    bin_time = 1){  #default bin time = 1 sec
  
  path <- paste0(data.dir,mSEMS.file) 
  
  mSEMS <- read.table(path, header = T, comment.char = "", fill = T)
  
  colnames(mSEMS)[1] <- "Date"
  
  #Re-arrange datetime 
  mSEMS$StartDatetime <- as.POSIXct(paste0("20",substr(mSEMS$Date,1,2),"-",substr(mSEMS$Date,4,5),"-",substr(mSEMS$Date,7,8)," ",mSEMS$Time))
  mSEMS$EndDatetime <- NA
  mSEMS$EndDatetime[c(1:(nrow(mSEMS)-1))] <-  mSEMS$StartDatetime[c(2:nrow(mSEMS))] -1
  mSEMS <- mSEMS %>%
    relocate(StartDatetime, .before = Date) %>%
    relocate(EndDatetime, .before = Date) 
  
  mSEMS$EndDatetime <- as.POSIXct(mSEMS$EndDatetime, origin = "1970-01-01")
  
  #add last EndDatetime
  mSEMS$EndDatetime[nrow(mSEMS)] <- as.POSIXct(mSEMS$StartDatetime[nrow(mSEMS)])+(mSEMS$NumBins[1]*bin_time)-bin_time 
  
  mSEMS$StartDatetime <- as.character(mSEMS$StartDatetime)
  mSEMS$EndDatetime <- as.character(mSEMS$EndDatetime)
  
  return(mSEMS)
  
  
}






#*********************************************************************************************************************************************
#*
#* LOAD raw mSEMS scan data
#* 
#* *******************************************************************************************************************************************


mSEMS_rawScan_open = function(
    rawScan.file = NULL,
    data.dir = NULL,
    skip = 55){
  
  path <- paste0(data.dir,rawScan.file) 
  
  rawScan <- read.table(path, header = T, comment.char = "", fill = T, skip = skip)
  colnames(rawScan)[1] <- "YY.MM.DD"
  
  rawScan$datetime <- paste0("20",substr(rawScan$YY.MM.DD,1,2),"-",substr(rawScan$YY.MM.DD,4,5),"-",substr(rawScan$YY.MM.DD,7,8)," ",rawScan$HR.MN.SC)
  
  rawScan <- rawScan %>%
    relocate(datetime, .before = YY.MM.DD)
}



#*********************************************************************************************************************************************
#*
#* LOAD raw mSEMS readings
#* 
#* *******************************************************************************************************************************************


mSEMS_readings_open = function(
    readings.file = NULL,
    data.dir = NULL){
  
  path <- paste0(data.dir,readings.file) 
  
  mSEMS.readings <- read.table(path, header = T, comment.char = "", fill = T, skip = 31)
  colnames(mSEMS.readings)[1] <- "YY.MM.DD"
  
  mSEMS.readings$datetime <- paste0("20",substr(mSEMS.readings$YY.MM.DD,1,2),"-",substr(mSEMS.readings$YY.MM.DD,4,5),"-",substr(mSEMS.readings$YY.MM.DD,7,8)," ",mSEMS.readings$HR.MN.SC)
  
  mSEMS.readings <- mSEMS.readings %>%
    relocate(datetime, .before = YY.MM.DD)
}





#*********************************************************************************************************************************************
#*
#* LOAD STAP data
#* 
#* *******************************************************************************************************************************************


stap_open = function(
  stap.file = NULL,
  data.dir = NULL){

stap.path <- paste0(data.dir,stap.file)

stap <- read.table(stap.path, header = T, nrow =
                     length(count.fields(stap.path)) - 2)


}


#*********************************************************************************************************************************************
#*
#* LOAD weather station data
#* 
#* *******************************************************************************************************************************************




meteo_open = function(
  meteo.file = NULL,
  data.dir = NULL,
  time_zone = "CET"){
  
  meteo.path <- paste0(data.dir,meteo.file)
  
  meteo <- read.table(meteo.path, sep = ",", header = T)
  
  colnames(meteo)[1] <- "datetime"
  meteo <- meteo %>%
    mutate(datetime = as.POSIXct(datetime,"%Y-%m-%d %H:%M:%S", tz = time_zone))# %>%
    #select(-c(RECORD,BattV_Min,PTemp_C_Avg))
  
}



#*********************************************************************************************************************************************
#*
#* LOAD Partector data
#* 
#* *******************************************************************************************************************************************



partector_open = function(
    partector.file = NULL,
    data.dir = NULL,
    tz = "CET"){

partector <- read.table(paste0(data.dir,partector.file), header = T, skip = 19)


part.start <- readLines(paste0(data.dir,partector.file), n = 9)[9]

part.start <- substr(part.start,8,25)
part.start <- as.POSIXct(part.start, format = "%d.%m.%Y %H:%M:%S", tz = tz)
part.start <- as.numeric(part.start)

partector <- partector %>%
  mutate(datetime = as.POSIXct(time-1+part.start, origin = "1970-01-01"))


partector <- partector %>%
  relocate(datetime, .before = time) %>%
  mutate(P_part = P,
         T_part = T,
         RH_part = RH) %>%
  select(-c(P,T,RH,time)) %>%
  mutate(datetime = as.character(datetime))

return(partector)

}








