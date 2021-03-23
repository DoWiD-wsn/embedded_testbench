EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 10 11
Title "Embedded Testbench (ETB)"
Date ""
Rev "0.1"
Comp "UAS Technikum Wien"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:R R?
U 1 1 6091824C
P 5200 3750
AR Path="/6091824C" Ref="R?"  Part="1" 
AR Path="/607EA52C/6091824C" Ref="R?"  Part="1" 
AR Path="/60913E7F/6091824C" Ref="R25"  Part="1" 
F 0 "R25" H 5270 3796 50  0000 L CNN
F 1 "10k" H 5270 3705 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5130 3750 50  0001 C CNN
F 3 "~" H 5200 3750 50  0001 C CNN
	1    5200 3750
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 60918252
P 5800 3750
AR Path="/60918252" Ref="R?"  Part="1" 
AR Path="/607EA52C/60918252" Ref="R?"  Part="1" 
AR Path="/60913E7F/60918252" Ref="R29"  Part="1" 
F 0 "R29" H 5870 3796 50  0000 L CNN
F 1 "10k" H 5870 3705 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5730 3750 50  0001 C CNN
F 3 "~" H 5800 3750 50  0001 C CNN
	1    5800 3750
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 60918258
P 5800 3100
AR Path="/60918258" Ref="R?"  Part="1" 
AR Path="/607EA52C/60918258" Ref="R?"  Part="1" 
AR Path="/60913E7F/60918258" Ref="R28"  Part="1" 
F 0 "R28" H 5870 3146 50  0000 L CNN
F 1 "10k" H 5870 3055 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5730 3100 50  0001 C CNN
F 3 "~" H 5800 3100 50  0001 C CNN
	1    5800 3100
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 6091825E
P 5200 3100
AR Path="/6091825E" Ref="R?"  Part="1" 
AR Path="/607EA52C/6091825E" Ref="R?"  Part="1" 
AR Path="/60913E7F/6091825E" Ref="R24"  Part="1" 
F 0 "R24" H 5270 3146 50  0000 L CNN
F 1 "10k" H 5270 3055 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5130 3100 50  0001 C CNN
F 3 "~" H 5200 3100 50  0001 C CNN
	1    5200 3100
	1    0    0    -1  
$EndComp
$Comp
L Transistor_FET:BSS138 Q?
U 1 1 60918264
P 5500 3900
AR Path="/60918264" Ref="Q?"  Part="1" 
AR Path="/607EA52C/60918264" Ref="Q?"  Part="1" 
AR Path="/60913E7F/60918264" Ref="Q2"  Part="1" 
F 0 "Q2" V 5400 4050 50  0000 C CNN
F 1 "BSS138" V 5750 3900 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 5700 3825 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/BS/BSS138.pdf" H 5500 3900 50  0001 L CNN
	1    5500 3900
	0    1    1    0   
$EndComp
$Comp
L Transistor_FET:BSS138 Q?
U 1 1 6091826A
P 5500 3250
AR Path="/6091826A" Ref="Q?"  Part="1" 
AR Path="/607EA52C/6091826A" Ref="Q?"  Part="1" 
AR Path="/60913E7F/6091826A" Ref="Q1"  Part="1" 
F 0 "Q1" V 5400 3400 50  0000 C CNN
F 1 "BSS138" V 5750 3250 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 5700 3175 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/BS/BSS138.pdf" H 5500 3250 50  0001 L CNN
	1    5500 3250
	0    1    1    0   
$EndComp
Text HLabel 5200 2850 0    50   Input ~ 0
VLV
Text HLabel 5800 2850 2    50   Input ~ 0
VHV
Text HLabel 5100 3350 0    50   Input ~ 0
LV1
Text HLabel 5100 4000 0    50   Input ~ 0
LV2
Text HLabel 5900 3350 2    50   Input ~ 0
HV1
Text HLabel 5900 4000 2    50   Input ~ 0
HV2
Wire Wire Line
	5100 4000 5200 4000
Wire Wire Line
	5200 3900 5200 4000
Connection ~ 5200 4000
Wire Wire Line
	5200 4000 5300 4000
Wire Wire Line
	5700 4000 5800 4000
Wire Wire Line
	5800 3900 5800 4000
Connection ~ 5800 4000
Wire Wire Line
	5800 4000 5900 4000
Text Label 5800 3600 0    50   ~ 0
HV
Text Label 5800 2950 0    50   ~ 0
HV
Text Label 5200 3600 2    50   ~ 0
LV
Text Label 5200 2950 2    50   ~ 0
LV
Wire Wire Line
	5200 3600 5500 3600
Wire Wire Line
	5500 3600 5500 3700
Wire Wire Line
	5200 2850 5200 2950
Wire Wire Line
	5800 2850 5800 2950
Wire Wire Line
	5200 2950 5500 2950
Wire Wire Line
	5500 2950 5500 3050
Connection ~ 5200 2950
Wire Wire Line
	5100 3350 5200 3350
Wire Wire Line
	5700 3350 5800 3350
Wire Wire Line
	5800 3250 5800 3350
Connection ~ 5800 3350
Wire Wire Line
	5800 3350 5900 3350
Wire Wire Line
	5200 3250 5200 3350
Connection ~ 5200 3350
Wire Wire Line
	5200 3350 5300 3350
$Comp
L Device:R R?
U 1 1 6091BCB1
P 5200 4400
AR Path="/6091BCB1" Ref="R?"  Part="1" 
AR Path="/607EA52C/6091BCB1" Ref="R?"  Part="1" 
AR Path="/60913E7F/6091BCB1" Ref="R26"  Part="1" 
F 0 "R26" H 5270 4446 50  0000 L CNN
F 1 "10k" H 5270 4355 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5130 4400 50  0001 C CNN
F 3 "~" H 5200 4400 50  0001 C CNN
	1    5200 4400
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 6091BCB7
P 5800 4400
AR Path="/6091BCB7" Ref="R?"  Part="1" 
AR Path="/607EA52C/6091BCB7" Ref="R?"  Part="1" 
AR Path="/60913E7F/6091BCB7" Ref="R30"  Part="1" 
F 0 "R30" H 5870 4446 50  0000 L CNN
F 1 "10k" H 5870 4355 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5730 4400 50  0001 C CNN
F 3 "~" H 5800 4400 50  0001 C CNN
	1    5800 4400
	1    0    0    -1  
$EndComp
$Comp
L Transistor_FET:BSS138 Q?
U 1 1 6091BCBD
P 5500 4550
AR Path="/6091BCBD" Ref="Q?"  Part="1" 
AR Path="/607EA52C/6091BCBD" Ref="Q?"  Part="1" 
AR Path="/60913E7F/6091BCBD" Ref="Q3"  Part="1" 
F 0 "Q3" V 5400 4700 50  0000 C CNN
F 1 "BSS138" V 5750 4550 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 5700 4475 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/BS/BSS138.pdf" H 5500 4550 50  0001 L CNN
	1    5500 4550
	0    1    1    0   
$EndComp
Text HLabel 5100 4650 0    50   Input ~ 0
LV3
Text HLabel 5900 4650 2    50   Input ~ 0
HV3
Wire Wire Line
	5100 4650 5200 4650
Wire Wire Line
	5200 4550 5200 4650
Connection ~ 5200 4650
Wire Wire Line
	5200 4650 5300 4650
Wire Wire Line
	5700 4650 5800 4650
Wire Wire Line
	5800 4550 5800 4650
Connection ~ 5800 4650
Wire Wire Line
	5800 4650 5900 4650
Text Label 5800 4250 0    50   ~ 0
HV
Text Label 5200 4250 2    50   ~ 0
LV
Wire Wire Line
	5200 4250 5500 4250
Wire Wire Line
	5500 4250 5500 4350
$Comp
L Device:R R?
U 1 1 6091DBF9
P 5200 5050
AR Path="/6091DBF9" Ref="R?"  Part="1" 
AR Path="/607EA52C/6091DBF9" Ref="R?"  Part="1" 
AR Path="/60913E7F/6091DBF9" Ref="R27"  Part="1" 
F 0 "R27" H 5270 5096 50  0000 L CNN
F 1 "10k" H 5270 5005 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5130 5050 50  0001 C CNN
F 3 "~" H 5200 5050 50  0001 C CNN
	1    5200 5050
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 6091DBFF
P 5800 5050
AR Path="/6091DBFF" Ref="R?"  Part="1" 
AR Path="/607EA52C/6091DBFF" Ref="R?"  Part="1" 
AR Path="/60913E7F/6091DBFF" Ref="R31"  Part="1" 
F 0 "R31" H 5870 5096 50  0000 L CNN
F 1 "10k" H 5870 5005 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5730 5050 50  0001 C CNN
F 3 "~" H 5800 5050 50  0001 C CNN
	1    5800 5050
	1    0    0    -1  
$EndComp
$Comp
L Transistor_FET:BSS138 Q?
U 1 1 6091DC05
P 5500 5200
AR Path="/6091DC05" Ref="Q?"  Part="1" 
AR Path="/607EA52C/6091DC05" Ref="Q?"  Part="1" 
AR Path="/60913E7F/6091DC05" Ref="Q4"  Part="1" 
F 0 "Q4" V 5400 5350 50  0000 C CNN
F 1 "BSS138" V 5750 5200 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 5700 5125 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/BS/BSS138.pdf" H 5500 5200 50  0001 L CNN
	1    5500 5200
	0    1    1    0   
$EndComp
Text HLabel 5100 5300 0    50   Input ~ 0
LV4
Text HLabel 5900 5300 2    50   Input ~ 0
HV4
Wire Wire Line
	5100 5300 5200 5300
Wire Wire Line
	5200 5200 5200 5300
Connection ~ 5200 5300
Wire Wire Line
	5200 5300 5300 5300
Wire Wire Line
	5700 5300 5800 5300
Wire Wire Line
	5800 5200 5800 5300
Connection ~ 5800 5300
Wire Wire Line
	5800 5300 5900 5300
Text Label 5800 4900 0    50   ~ 0
HV
Text Label 5200 4900 2    50   ~ 0
LV
Wire Wire Line
	5200 4900 5500 4900
Wire Wire Line
	5500 4900 5500 5000
$EndSCHEMATC
