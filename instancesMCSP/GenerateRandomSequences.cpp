#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#include<string.h>
#include<string>
#include<iostream>
#include<fstream>
#include<unistd.h>

using namespace std;

void shuffle(char *str, int n) {
    if (n > 1) {
        int i;
        for (i = 0; i < n - 1; i++)
        {
          int j = i + rand() / (RAND_MAX / (n - i) + 1);
          char t = str[j];
          str[j] = str[i];
          str[i] = t;
        }
    }
}

void preKmp(string x, int t, int kmpNext[]) {
    int i, j;

    i = 0;
    j = kmpNext[0] = -1;
    while (i < t) {
        while (j > -1 && x[i] != x[j])
            j = kmpNext[j];
        i++;
        j++;
        if (x[i] == x[j])
            kmpNext[i] = kmpNext[j];
        else
            kmpNext[i] = j;
    }
}


// Calculate maximum substring commom size and the number of variables in the complete model
int maximumBlockSize(char *seq1_c, char *seq2_c, int n, long long &nvariables) {
    int tmax= 1, kmpNext[n+1];

    nvariables = 0;
    // Calculate maximum substring commom size
    tmax= 1;
    for(int t=1; t<=n; t++)
        for(long long i=0;i<=(n-t);i++) {
            string substr1(&seq1_c[i],t);
            // KMP Preprocessing
            preKmp(substr1,t,kmpNext);
            int j=0, w=0;
            int m=-2;
            bool found = false;
            // KMP Searching substring1 on substring2
            while(m != -1) {
                w = 0;
                if(m == -2) j = 0;
		else j = m+1;
                m = -1;
                if(j > (n-t)) break;
                found = false;
                while (j < n) {
                    while (w > -1 && substr1[w] != seq2_c[j]) w = kmpNext[w];
                    w++;
                    j++;
                    if (w >= t) {
                        m = j-w;
                        found = true;
                        break;
                    }
                }
                if(!found) break;   // Substring not found on substr2. Go to the next iteration of i
                j = m;
		// END KMP Searching

                if( t>tmax ) tmax= t;
                //cout << "t= " << t << endl;
                nvariables++;
            }
        }

    return tmax;
}

// Density option is not implemented!
int createSequenceFile(char *instanceTypeName, int n, int a, int density) {
	char linestr[4000], seq1_c[4000], seq2_c[4000], outputFileName[1000];
	int x=0, cont=0, go=0;
	double dens=0;
	long long nvar;
	fstream outputFile;

    srand( (unsigned)time(NULL) );

    if(a <= 9) {
        for(int i=0;i<n;i++) {
            x = (rand()%a) + 1;
            seq1_c[i] = '0' + x;
            seq2_c[i] = '0' + x;
        }
    } else {
        for(int i=0;i<n;i++) {
            x = (rand()%a) + 1;
            seq1_c[i] = 'a' + x;
            seq2_c[i] = 'a' + x;
        }
    }
    seq1_c[n] = '\0';
    seq2_c[n] = '\0';
    shuffle(seq2_c,n);

    int tmax = maximumBlockSize(seq1_c,seq2_c,n,nvar);
    dens = tmax/(double) n;

    cont = 1; go=0;
    while(!go) {
		sprintf(outputFileName,"%s-n%d-A%d-%d.dat",instanceTypeName,n,a,/*dens*/cont);
		int errcode = access(outputFileName, F_OK);
		if (errcode != 0) go=1;     // file doesnt exist
		else cont++;                // file already exist
	}
    outputFile.open(outputFileName, ios::in | ios::out | ios::trunc);
    outputFile << "FILE: " << outputFileName << endl;
    outputFile << n << endl;
    outputFile << a << endl;
    outputFile << dens << endl;
    outputFile << seq1_c << endl;
    outputFile << seq2_c;
    outputFile.close();

	return 0;
}

int main (int argc, char *argv[]) {
    int a=0, d=0, n=0;

	if (argc < 5) {
		printf("Please, specify the instance type name, number of vertices, lenght of the alphabet and density.\n");
		return 0;
	}
    n = atoi(argv[2]);
    a = atoi(argv[3]);
    d = atoi(argv[4]);

    //printf("n= %d, d= %d\n",n,d);
	createSequenceFile(argv[1],n,a,d);
	return 0;
}
