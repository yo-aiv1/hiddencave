#ifndef FILE_IO
#define FILE_IO

#include "../include/ntdll.h"

int InitFile(
        PHANDLE FileHandle,
        ACCESS_MASK AccessValue,
        POBJECT_ATTRIBUTES ObjectAttributes,
        PIO_STATUS_BLOCK IoStatusBlock,
        ULONG FileStateValue
    );
int WriteBuffer(
        HANDLE FileHandle,
        PIO_STATUS_BLOCK IoStatusBlock,
        BYTE *buffer,
        ULONG BufferSize
    );
int ReadBuffer(
        HANDLE FileHandle,
        PIO_STATUS_BLOCK IoStatusBlock,
        BYTE *buffer,
        ULONG BufferSize
    );

int FileSizeG(
        HANDLE FileHandle,
        PIO_STATUS_BLOCK IOstatus
    );

#endif