#include <windows.h>


typedef unsigned __int64 QWORD;

DWORD NtReadFileSSN                 = 0;
QWORD NtReadFileSyscall             = 0;
DWORD NtCreateFileSSN               = 0;
QWORD NtCreateFileSyscall           = 0;
DWORD NtQueryInformationFileSSN     = 0;
QWORD NtQueryInformationFileSyscall = 0;
DWORD NtQueryDirectoryFileSSN       = 0;
QWORD NtQueryDirectoryFileSyscall   = 0;
DWORD NtWaitForSingleObjectSSN      = 0;
QWORD NtWaitForSingleObjectSyscall  = 0;
DWORD NtFreeVirtualMemorySSN        = 0;
QWORD NtFreeVirtualMemorySyscall    = 0;


/* DWORD NtAllocateVirtualMemorySSN = 0; */
/* QWORD NtAllocateVirtualMemorySyscall = 0; */

void *pNTDLL    = {0};
void *pSOCK     = {0};