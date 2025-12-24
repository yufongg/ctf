// gcc -o fire-extinguisher fire-extinguisher -fstack-protector
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main(void) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  puts("welcome to the fire extinguisher!");
  puts("-----");
  char extinguish[16];
  char fire[16];
  char preamble1[16] = "fire: %s";
  char preamble2[16] = "extinguish! >";
  printf("what fire are we putting out? > ");
  read(0, fire, 32);
  printf(preamble1, fire);
  printf(preamble2);
  fgets(extinguish, 1000, stdin);
  return 0;
}
