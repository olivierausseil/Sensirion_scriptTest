#define SHT21_I2CADDR	      (0x40)

#define SHT21_CMD_TEMPERATURE (0xE3)
#define SHT21_CMD_HUMIDITY    (0xE5)


unsigned char SHT21_script[] =
{
  // set device address
  GEN_I2C_CMD_SET_DEV_ADR, SHT21_I2CADDR_DEFAULT,
  // wait 20ms
  GEN_I2C_CMD_SLEEP, 0x00, 0x14,


  ///----- Humidity -----
  // read output registers
  GEN_I2C_CMD_READ_REGS,SHT21_CMD_HUMIDITY, 3,
  // data are in resgiters 0-2
  GEN_I2C_CMD_STORE, 0, // MSB of humidity
  GEN_I2C_CMD_STORE, 1, // LSB of humidity
  GEN_I2C_CMD_STORE, 2, // CRC

  /// ----- Temperature -----
  // read output registers
  GEN_I2C_CMD_READ_REGS,SHT21_CMD_TEMPERATURE, 3,
  // data are in resgiters 0-2
  GEN_I2C_CMD_STORE, 0, // MSB of temperature
  GEN_I2C_CMD_STORE, 1, // LSB of temperature
  GEN_I2C_CMD_STORE, 2, // CRC
};
