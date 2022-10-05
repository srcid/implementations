FILES=*.txt
for f in $FILES
do
    ./updateInstance $f rand_S8 2
done
