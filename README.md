# Embedded Testbench (ETB)

The **E**mbedded **T**est**b**ench (**ETB**) is a platform consisting of a Raspberry Pi add-on and a Python library designed to enable the testing, analyzing, and profiling of embedded systems.
A focus is laid on low-power embedded systems such as wireless sensor nodes.
Additionally, the ETB supports test automation with the possibility of remote control via TCP/IP.

## Key Facts

* 40-pin expansion header for Raspberry Pi [2|3|4] model B+
* 4 mounting holes matching the Raspberry Pi [2|3|4] model B+ layout
* Compact size of 122 x 56 mm
* 4 controllable voltage domains supplied via own 12V input  
    (0.64 to 5.25V, in 5|10|30|50 mV steps, with a current limit of 3A each; see [MIC24045 datasheet](docs/datasheets/mic24045.pdf))
* 6 wattmeter: one per voltage domain + 2 additional  
    (0 to 26V, +/- 3.2A (max), 1.5 mA resolution, 1% precision; see [INA219 datasheet](docs/datasheets/ina219.pdf))
* 4 channel 16-bit ADC: 2 general + 2 for thermistor (see [ADS1115 datasheet](docs/datasheets/ads1115.pdf))
* I2C multiplexer for easier channel selection (voltage supply + wattmeter; see [TCA9548A datasheet](docs/datasheets/tca9548a.pdf))
* 12-pin expansion header (2x PWM, 6x GPIO, +3V3/+5V, and 2x GND)
* 4 test control signals (reset, enable, running, result)
* Connectors for TWI (2x), OWI (1x), SPI (1x), and UART (1x)
* Connectors for UART (1x) and test control signals (1x)  
    (with MOSFET-based bi-directional level shifter for voltage domain #1)
* Connectors for +3V3, +5V, and GND 
* Dsub 15 HD connector for DUT (e.g., useful for climate chamber experiments)


## Contents

```
.
├── docs                : documents & project documentation
│   └── datasheets      : datasheets of components used
├── kicad               : KiCad files
├── media               : Miscellaneous media (images, etc.)
│   ├── pcb             : Photos and rendered images of the PCB
│   └── schematic       : SVG images of the schematics
└── source              : Python library and example scripts
```

For more information on the PCB (and its design) refer to [docs/pcb_design.md](docs/pcb_design.md).
The python library, its functionality, and usage as well as example scripts are presented in [docs/python_library.md](docs/python_library.md).


## Built with

* [KiCad EAD 5.1.9](https://kicad.org/) - PCB design
* [Python 3.7.3](https://www.python.org/) - Python library


## Contributors

* **Dominik Widhalm** - [***DC-RES***](https://informatics.tuwien.ac.at/doctoral/resilient-embedded-systems/) - [*UAS Technikum Wien*](https://embsys.technikum-wien.at/staff/widhalm/)

Contributions of any kind to improve the project are highly welcome.
For coding bugs or minor improvements simply use pull requests.
However, for major changes or general discussions please contact [Dominik Widhalm](mailto:widhalm@technikum-wien.at?subject=Embedded%20Testbench%20(ETB)%20on%20GitHub).


## Publications

- Dominik Widhalm, Karl M. Goeschka, and Wolfgang Kastner, "*An open-source wireless sensor node platform with active node-level reliability for monitoring applications*", Sensors 21, no. 22: 7613, 2021, DOI: [10.3390/s21227613](https://doi.org/10.3390/s21227613)
- Dominik Widhalm, Karl M. Goeschka, and Wolfgang Kastner, "*Undervolting on wireless sensor nodes: a critical perspective*", in The 23rd International Conference on Distributed Computing and Networking (ICDCN 2022), January 4-7, 2022, DOI: [10.1145/3491003.3491018O](https://doi.org/10.1145/3491003.3491018O)
- Dominik Widhalm, Karl M. Goeschka, and Wolfgang Kastner, "*Is Arduino a suitable platform for sensor nodes?*", in The 47th Annual Conference of the IEEE Industrial Electronics Society (IECON 2021), October 13-16, 2021, DOI: tba
- Dominik Widhalm, Karl M. Goeschka, and Wolfgang Kastner, "*Node-level indicators of soft faults in wireless sensor networks*", in The 40th International Symposium on Reliable Distributed Systems (SRDS 2021), September 20-23, 2021, DOI: [10.1109/SRDS53918.2021.00011](https://doi.org/10.1109/SRDS53918.2021.00011)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
