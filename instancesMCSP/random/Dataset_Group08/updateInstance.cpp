#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<iostream>
#include<fstream>

using namespace std;

int updateFile(char *fileName, char *instanceTypeName, int a) {
	char seq_c1[4000], seq_c2[4000], linestr[4000], outputFileName[1000];
	int cont=0, n, k=0;
	double maxsubstr= 0.0;

	FILE *f;
	fstream instanceFile, outputFile;

	f = fopen(fileName, "r");
	fflush(stdin);
	fscanf(f,"FILE: rand_S8-n%d-A%d-%d.dat",&n,&a,&k);
	fclose(f);
	instanceFile.open(fileName, ios::in | ios::out);
	instanceFile >> outputFileName >> linestr;
	instanceFile >> n;
	instanceFile >> a;
	instanceFile >> maxsubstr;
        instanceFile >> seq_c1;
        instanceFile >> seq_c2;

        sprintf(outputFileName,"%s-n%d-A%d-D%.2lf-%d.dat",instanceTypeName,n,a,maxsubstr,k);
        outputFile.open(outputFileName, ios::in | ios::out | ios::trunc);
        outputFile << "FILE: " << outputFileName << endl;
        outputFile << n << endl << a << endl << maxsubstr << endl << seq_c1 << endl << seq_c2 << endl;
        outputFile.close();
	instanceFile.close();
	return 0;
}

int main (int argc, char *argv[]) {
    	int a=0;
	fstream instanceFile;

	if (argc < 4) {
		printf("Please, specify the sequence file, the instance type name and alphabet length.\n");
		return 0;
	}
	instanceFile.open(argv[1], ios::in | ios::out);
	if (instanceFile == NULL) {
		printf("Could not open %s.\n", argv[1]);
		return 0;
	}
	instanceFile.close();
    	a = atoi(argv[3]);

	updateFile(argv[1],argv[2],a);
	return 0;
}
