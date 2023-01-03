x=1
while [ $x -le 100000 ]
do
  curl http://localhost:7990/create_person
  echo $x
  x=$(( $x + 1 ))
done
