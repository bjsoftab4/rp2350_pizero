// Board and hardware specific configuration
#define MICROPY_HW_BOARD_NAME "RP2350_PIZERO"
#define PICO_FLASH_SIZE_BYTES (16 * 1024 * 1024)
#define MICROPY_HW_FLASH_STORAGE_BYTES (PICO_FLASH_SIZE_BYTES - (2 * 1024 * 1024))

#define MICROPY_HW_MCU_NAME         "RP2350"

// クロック設定（例: 150MHz）
#define MICROPY_HW_CLK_PLL1         (150000000)

// UART 設定（標準 REPL 用）
#define MICROPY_HW_UART_REPL        (0)
#define MICROPY_HW_UART_REPL_BAUD   (115200)

// LED ピン（例: GPIO25）
//#define MICROPY_HW_LED              (25)
