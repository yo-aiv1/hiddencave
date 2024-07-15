#ifndef PATH_OPS
#define PATH_OPS

#include "../include/ntdll.h"

void InitPathObj(WORD *SourceString, POBJECT_ATTRIBUTES ObjectAttributes, PUNICODE_STRING PathInfo);
int InitPath(WORD *FilePath, char PathStart, WORD *OutBuffer);


#endif