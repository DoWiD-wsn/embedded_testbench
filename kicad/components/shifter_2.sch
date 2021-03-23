EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 11 11
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
U 1 1 607EBC1E
P 5300 4050
AR Path="/607EBC1E" Ref="R?"  Part="1" 
AR Path="/607EA52C/607EBC1E" Ref="R33"  Part="1" 
F 0 "R33" H 5370 4096 50  0000 L CNN
F 1 "10k" H 5370 4005 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5230 4050 50  0001 C CNN
F 3 "~" H 5300 4050 50  0001 C CNN
	1    5300 4050
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 607EBC24
P 5900 4050
AR Path="/607EBC24" Ref="R?"  Part="1" 
AR Path="/607EA52C/607EBC24" Ref="R35"  Part="1" 
F 0 "R35" H 5970 4096 50  0000 L CNN
F 1 "10k" H 5970 4005 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5830 4050 50  0001 C CNN
F 3 "~" H 5900 4050 50  0001 C CNN
	1    5900 4050
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 607EBC2A
P 5900 3400
AR Path="/607EBC2A" Ref="R?"  Part="1" 
AR Path="/607EA52C/607EBC2A" Ref="R34"  Part="1" 
F 0 "R34" H 5970 3446 50  0000 L CNN
F 1 "10k" H 5970 3355 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5830 3400 50  0001 C CNN
F 3 "~" H 5900 3400 50  0001 C CNN
	1    5900 3400
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 607EBC30
P 5300 3400
AR Path="/607EBC30" Ref="R?"  Part="1" 
AR Path="/607EA52C/607EBC30" Ref="R32"  Part="1" 
F 0 "R32" H 5370 3446 50  0000 L CNN
F 1 "10k" H 5370 3355 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5230 3400 50  0001 C CNN
F 3 "~" H 5300 3400 50  0001 C CNN
	1    5300 3400
	1    0    0    -1  
$EndComp
$Comp
L Transistor_FET:BSS138 Q?
U 1 1 607EBC36
P 5600 4200
AR Path="/607EBC36" Ref="Q?"  Part="1" 
AR Path="/607EA52C/607EBC36" Ref="Q6"  Part="1" 
F 0 "Q6" V 5500 4350 50  0000 C CNN
F 1 "BSS138" V 5850 4200 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 5800 4125 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/BS/BSS138.pdf" H 5600 4200 50  0001 L CNN
	1    5600 4200
	0    1    1    0   
$EndComp
$Comp
L Transistor_FET:BSS138 Q?
U 1 1 607EBC3C
P 5600 3550
AR Path="/607EBC3C" Ref="Q?"  Part="1" 
AR Path="/607EA52C/607EBC3C" Ref="Q5"  Part="1" 
F 0 "Q5" V 5500 3700 50  0000 C CNN
F 1 "BSS138" V 5850 3550 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 5800 3475 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/BS/BSS138.pdf" H 5600 3550 50  0001 L CNN
	1    5600 3550
	0    1    1    0   
$EndComp
Text HLabel 5300 3150 0    50   Input ~ 0
VLV
Text HLabel 5900 3150 2    50   Input ~ 0
VHV
Text HLabel 5200 3650 0    50   Input ~ 0
LV1
Text HLabel 5200 4300 0    50   Input ~ 0
LV2
Text HLabel 6000 3650 2    50   Input ~ 0
HV1
Text HLabel 6000 4300 2    50   Input ~ 0
HV2
Wire Wire Line
	5200 4300 5300 4300
Wire Wire Line
	5300 4200 5300 4300
Connection ~ 5300 4300
Wire Wire Line
	5300 4300 5400 4300
Wire Wire Line
	5800 4300 5900 4300
Wire Wire Line
	5900 4200 5900 4300
Connection ~ 5900 4300
Wire Wire Line
	5900 4300 6000 4300
Text Label 5900 3900 0    50   ~ 0
HV
Text Label 5900 3250 0    50   ~ 0
HV
Text Label 5300 3900 2    50   ~ 0
LV
Text Label 5300 3250 2    50   ~ 0
LV
Wire Wire Line
	5300 3900 5600 3900
Wire Wire Line
	5600 3900 5600 4000
Wire Wire Line
	5300 3150 5300 3250
Wire Wire Line
	5900 3150 5900 3250
Wire Wire Line
	5300 3250 5600 3250
Wire Wire Line
	5600 3250 5600 3350
Connection ~ 5300 3250
Wire Wire Line
	5200 3650 5300 3650
Wire Wire Line
	5800 3650 5900 3650
Wire Wire Line
	5900 3550 5900 3650
Connection ~ 5900 3650
Wire Wire Line
	5900 3650 6000 3650
Wire Wire Line
	5300 3550 5300 3650
Connection ~ 5300 3650
Wire Wire Line
	5300 3650 5400 3650
$EndSCHEMATC
