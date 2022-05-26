#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h> /* close */

#define SERVER_PORT 1500
#define MAX_MSG 100

int main (int argc, char *argv[]) {

  int sd, rc, i;
  struct sockaddr_in localAddr, servAddr;
  struct hostent *h;
  
  if(argc < 3) {
    printf("usage: %s <server> <data1> <data2> ... <dataN>\n",argv[0]);
    exit(1);
  }

  h = gethostbyname(argv[1]);
  if(h==NULL) {
    printf("%s: unknown host '%s'\n",argv[0],argv[1]);
    exit(1);
  }

  servAddr.sin_family = h->h_addrtype;
  memcpy((char *) &servAddr.sin_addr.s_addr, h->h_addr_list[0], h->h_length);
  servAddr.sin_port = htons(SERVER_PORT);

  /* create socket */
  sd = socket(AF_INET, SOCK_STREAM, 0);
  if(sd<0) {
    perror("cannot open socket ");
    exit(1);
  }

  /* bind any port number */
  localAddr.sin_family = AF_INET;
  localAddr.sin_addr.s_addr = htonl(INADDR_ANY);
  localAddr.sin_port = htons(0);
  
  rc = bind(sd, (struct sockaddr *) &localAddr, sizeof(localAddr));
  if(rc<0) {
    printf("%s: cannot bind port TCP %u\n",argv[0],SERVER_PORT);
    perror("error ");
    exit(1);
  }
  while(1){
  char ch;
  printf("enter 'c' to connect with server\n");
  scanf("%c",&ch);
  if(strncmp(&ch,"c",1)==0) break;
}
				
  /* connect to server */
  rc = connect(sd, (struct sockaddr *) &servAddr, sizeof(servAddr));
  if(rc<0) {
    perror("cannot connect ");
    exit(1);
  }



while(1){
char u[150];
char p[255];
//printf("Enter username:");
//scanf("%s",&u);
//printf("Enter password:");
//scanf("%s",&p);
recv(sd,p,150,0);
if(strncmp(p,"welcome",7)==0){send(sd,"close", 5, 0);break;}
else{printf("%s",p);
scanf("%s",u);
send(sd, u, strlen(u) + 1, 0);}
}
//send(sd, p, strlen(p) + 1, 0);
printf("welcome client");
char s[1024];
memset(s,0,sizeof(s));

while(1){
  
int n=0;
	while((s[n++]=getchar())!='\n');
	send(sd, s, strlen(s) + 1, 0);
	
      
    
    if(strncmp(s,"exit",4)==0){
	printf("Program exit, connection closed\n");
	break;}
   

    int a=inet_pton(AF_INET,argv[1],&servAddr.sin_addr);
    bzero(s,256);
    a=recv(sd,s,255,0);
    printf("From server:%s\n",s);
       bzero(s,256);
  
  } /* while(read_line) */
return 0;
  close(sd);
}

