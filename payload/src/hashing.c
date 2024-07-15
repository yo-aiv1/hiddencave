#include "../include/hashing.h"

#define K1          21
#define K2          5421

unsigned long HashStrW(const unsigned short *str) {
    unsigned long   result  = 0;
    int             idx     = 0;
    char            CurrentChar;

    while (*str != 0) {
        idx++;

        CurrentChar = *str;

        if (CurrentChar >= 0x6C) {
            CurrentChar -= 0x19;
        }

        result = ((CurrentChar * K2) / K1) + (idx * result);
        str++;

    }
    
    return (result >> 1);
}

unsigned long HashStr(const char *str) {
    unsigned long   result  = 0;
    int             idx     = 0;
    char            CurrentChar;

    while (*str != 0) {
        idx++;

        CurrentChar = *str;

        if (CurrentChar >= 0x6C) {
            CurrentChar -= 0x19;
        }

        result = ((CurrentChar * K2) / K1) + (idx * result);
        str++;

    }
    
    return (result >> 1);
}