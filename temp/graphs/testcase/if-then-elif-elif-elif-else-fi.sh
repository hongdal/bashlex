if [ -z $1 ]; then 
    ls
elif [ $2 -gt 2 ]; then 
    assignment=$1
elif [ $3 -lt 3 ]; then 
    $(ls)
    $(ls)
    $(ls)
elif [ $4 -ne 4 ]; then 
    ls; ls; ls 
else
    while [ 1 ]; do 
        ls; ls; ls;
    done
    while [ 2 ]; do 
        cat; cat;
    done 
fi