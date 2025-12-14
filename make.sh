cd $HOME/1-gitenv/micropython/ports/rp2
make USER_C_MODULES="$HOME/1-gitenv/rp2350_pizero/micropython.cmake" BOARD=RP2350_PIZERO
cp build-RP2350_PIZERO/firmware.uf2 $HOME/rp2350_pizero_firmware.uf2
