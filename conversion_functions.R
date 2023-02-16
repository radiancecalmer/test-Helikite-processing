#Conversion functions for vertical atmospheric measurements
#Author: Roman Pohorsky
#Date of creation: 08/03/2021
#Last update: 09/03/2021

library(aiRthermo)
library(humidity)

#stp.convert.dry
#Function to convert a scalar measurement to STP conditions

# Pressure in hPa 
# temperature in °C

stp.convert.dry <- function(x,t,p){
  p = p*100 
  t = t + 273.15
  v_stp <- (273.15/t)*(p/101315)
  x_stp <- x / v_stp
  return(x_stp)
}


# stp.convert.moist 
#Function to convert a scalar measurement to STP conditions, taking moisture in account
#The function first calculates the water vapor saturation saturation pressure based on the equations from Huang_2018
#which allows to define e based on rh. It then calculates the virtual temperature and replaces it in the stp conversion formula 

# Pressure in hPa 
# temperature in °C

stp.convert.moist <- function(x,t,p,rh){
p = p*100 #convert pressure in hPa to Pa 
t = t + 273.15 

  if(t>273.15){
    e_s <- exp(34.494 - (4924.9/((t-273.15)+237.1)))/((t-273.15)+105)^1.57 
  } else {
    e_s <- exp(43.494 - (6545.8/((t-273.15)+278)))/((t-273.15)+868)^2
  }

e <- (rh*e_s)/100
t_v <- t / (1-(e/p)*(1-0.622)) 

v_stp <- (273.15/t_v)*(p/101315)
x_stp <- x / v_stp
return(x_stp)

}


#Function to convert pressure to altitude, given a reference pressure and altitude 
p.to.alt <- function(p,p0,t0,h0){
t0 <- t0 + 273.15  
t <- t0   
p_sl <- p0*((1-((0.0065*h0)/(t0+(0.0065*h0))))^-5.257)
#return(p_sl)
h <- (((p_sl/p)^(1/5.257)-1)*t)/0.0065
return(h)

}

#Function to calculate potential temperature
#takes into account mixing ratio for c_p correction 
pot.temp <- function(p,t,rh=0){
  P <- p*100
  Temp <- t + 273.15
  w <- rh2w(P = P, Temp = Temp, rh = rh)
  theta <- PT2Theta(P = P, Temp = Temp, w = w)
  return(theta)
}

#Function to calculate theta e (equivalent potential temperature)
#see airThermo package 

equ.pot.temp <- function(p0,t0,rh0,p,t,rh){
  p <- p*100
  p0 <- p0*100
  t <- t + 273.15
  t0 <- t0+273.15
  w0 <- rh2w(P = p0, Temp = t0, rh = rh0)
  w <- rh2w(P = p, Temp = t, rh = rh)
  lcl <- find_lcl(Ptop = 50000, P0 = p0, T0 = t0, w0 = w0, deltaP = 5)
  TLCL <- lcl$Tlcl
  theta_e <- equivalentPotentialTemperature(P = p, Temp = t, w = w, TLCL = TLCL)
  return(theta_e)
}


stp.volume.convert <- function(v,p,t){
  p = p*100
  t = t + 273.15
  v0 = (v*p*273.15)/(101315*t)
  
  return(v0)
}


CO2_correction <- function(c_raw,
                           p_hPa){
  
  
  #Parameters and constants
  Ap2 = -155.36  #from vaisala calculation sheet
  Bp2 = 209.51
  Cp2 = -68.42
  Dp2 = 9.2681
  Ep2 = 0
  
  
  #First iteration
  
  c_i <- c_raw / (p_hPa/1013)
  
  for(i in c(1:10)){
    kp2 = Ap2*((c_i/10000)^4) + Bp2*((c_i/10000)^3) + Cp2*((c_i/10000)^2) + Dp2*(c_i/10000) + Ep2   
    c_i2 = c_raw /((p_hPa/1013)*(kp2*((p_hPa-1013)/1013) + 1))
    c_i = c_i2
    
  }
  
  
  return(c_i)
  
}

# fit function for PSD

PSD_lognormal_fit <- function(x,
                              y0 = 0,
                              A,
                              x0,
                              width){
  
  y = y0 + A* exp(-(((log(x/x0))/width)^2))
  return(y)
}

logno_moments <- function(meanlog, sdlog) {
  m <- exp(meanlog + (1/2)*sdlog^2)
  s <- exp(meanlog + (1/2)*sdlog^2)*sqrt(exp(sdlog^2) - 1)
  return(list(mean = m, sd = s))
}

  

#Calculate wind direction mean angle 
mean.angle <- function(theta, r=1, ...) {
  ## Function for averaging angles
  ## Polar coordinates -> Cartesian coordinates -> polar coordinates
  ##   'theta' is in degrees
  ##   'r=1' for unit circle
  ##   returns value is mean theta in degrees
  theta.rad <- theta * pi/180
  x <- mean(r * cos(theta.rad), ...)
  y <- mean(r * sin(theta.rad), ...)
  theta.deg <- atan2(y, x) * 180/pi
  ifelse(sign(theta.deg) < 0, (theta.deg + 360) %% 360, theta.deg) # -179--180 to 0--359
}




rh_to_absHumidity <- function(rh = NULL,
                              T = NULL){
  #calculate the saturation vapor pressure at T
  e_s = 0.611*exp((17.502*T)/(240.97+T))
  e_a = e_s*rh/100
  pw = (e_a*18.02)/(8.3145*(T+273.15))*1000   #18.02 g/mol = water molecular weight
  #pw = water density in the air in g/m3 
  return(pw)
}

# rh_to_specHumidity <- function(rh = NULL,
#                               T = NULL){
#   #calculate the saturation vapor pressure at T
#   e_s = 0.611*exp((17.502*T)/(240.97+T))
#   e_a = e_s*rh/100
#   pw = (e_a*18.02)/(8.3145*(T+273.15))   #18.02 g/mol = water molecular weight
#   #pw = water density in the air in kg/m3
#   q = pw/(pw+1)
#   
#   return(q)
# }


rh_to_sh <- function(rh = NULL,
                     t = NULL,
                     p = NULL){
  t <- t+273.15
  Es <- SVP(t)
  e <- WVP2(rh, Es)
  sh <- SH(e = e, p = p*100)
  return(sh)  
  
}

#Angstrom exponent calculation 


AAE_calc <- function(C_abs1,
                     C_abs2,
                     lambda1,
                     lambda2){
  
  AAE <- -(log(C_abs1/C_abs2)/log(lambda1/lambda2))
  return(AAE)
}










