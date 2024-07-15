#ifndef DECODE_YS
#define DECODE_YS

void DecodeString(const char *str, unsigned short *DecodedString);
unsigned int DecodeBase64(const char *Base64String, unsigned int StringLength, unsigned char *DecodedString);

#endif