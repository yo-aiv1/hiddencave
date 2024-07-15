#include "../include/AddrResolution.h"
#include "../include/syscalls.h"
#include "../include/FileIO.h"
#include "../include/macros.h"
#include "../include/ntdll.h"


typedef unsigned __int64 QWORD;

extern void *pNTDLL;
extern DWORD NtCreateFileSSN;
extern QWORD NtCreateFileSyscall;
extern DWORD NtReadFileSSN;
extern QWORD NtReadFileSyscall;
extern DWORD NtQueryInformationFileSSN;
extern QWORD NtQueryInformationFileSyscall;

int InitFile(PHANDLE FileHandle, ACCESS_MASK AccessValue, POBJECT_ATTRIBUTES ObjectAttributes, PIO_STATUS_BLOCK IoStatusBlock, ULONG FileStateValue) {
    if (NtCreateFileSSN == 0) {
        if (pNTDLL == NULL) {
            pNTDLL = GetDllAddress(NTDHASH);
        }

        NtCreateFileSyscall = (QWORD)GetFuncAddress(pNTDLL, NTCREATEFILE); + 0x12;
        NtCreateFileSSN     = ((PBYTE)(NtCreateFileSyscall - 0xe))[0];
    }

    NTSTATUS status;
    status = NtCreateFile(
        FileHandle,
        AccessValue,
        ObjectAttributes,
        IoStatusBlock,
        NULL,
        FILE_ATTRIBUTE_NORMAL,
        FILE_SHARE_READ,
        FileStateValue,
        FILE_SYNCHRONOUS_IO_NONALERT,
        NULL,
        0
    );
    if (status != 0x00000000) {
        return 1;
    }
    return 0;
}

int ReadBuffer(HANDLE FileHandle, PIO_STATUS_BLOCK IoStatusBlock, unsigned char *buffer, ULONG BufferSize) {
    if (NtReadFileSSN == 0) {
        if (pNTDLL == NULL) {
            pNTDLL = GetDllAddress(NTDHASH);
        }
        NtReadFileSyscall   = (QWORD)GetFuncAddress(pNTDLL, NTREADFILE) + 0x12;
        NtReadFileSSN       = ((PBYTE)(NtReadFileSyscall - 0xe))[0];
    }

    NTSTATUS status;
    status = NtReadFile(
            FileHandle,
            NULL,
            NULL,
            NULL,
            IoStatusBlock,
            buffer,
            BufferSize,
            NULL,
            NULL
    );
    if (status != 0x00000000) {
#if DEBUG == 0
        printf("READ error %x\n", status);
#endif
        return 1;
    }
    return 0;
}

int FileSizeG(HANDLE FileHandle, PIO_STATUS_BLOCK IOstatus) {
    FILE_STANDARD_INFORMATION   standardInfo    = {0};
    NTSTATUS                    status          = 0;

    if (NtQueryInformationFileSSN == 0) {
        if (pNTDLL == NULL) {
            pNTDLL = GetDllAddress(NTDHASH);
        }
        NtQueryInformationFileSyscall   = GetFuncAddress(pNTDLL, NTQINFOFILE) + 0x12;
        NtQueryInformationFileSSN       = ((PBYTE)(NtQueryInformationFileSyscall - 0xe))[0];
    }

    status = NtQueryInformationFile(
        FileHandle,
        IOstatus,
        &standardInfo,
        sizeof(standardInfo),
        FileStandardInformation
    );

    if (status != 0x00000000) {
        return -1;
    }
    return (int)standardInfo.EndOfFile.QuadPart;
}