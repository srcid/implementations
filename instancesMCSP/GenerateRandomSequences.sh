max=1

g++ GenerateRandomSequences.cpp -o GenerateRandomSequences

for i in `seq 1 $max`
do
    ./GenerateRandomSequences rand_S8 100 2 0
done
for i in `seq 1 $max`
do
    ./GenerateRandomSequences rand_S8 150 2 0
done
for i in `seq 1 $max`
do
    ./GenerateRandomSequences rand_S8 200 2 0
done
for i in `seq 1 $max`
do
    ./GenerateRandomSequences rand_S8 250 2 0
done
for i in `seq 1 $max`
do
    ./GenerateRandomSequences rand_S8 300 2 0
done
for i in `seq 1 $max`
do
    ./GenerateRandomSequences rand_S8 350 2 0
done

rm GenerateRandomSequences
