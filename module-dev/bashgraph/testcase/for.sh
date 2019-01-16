for file in $(ls /); do
    if [ $number -ne 0 ]; then 
        echo "$number$file" 
    fi 
done
exit 0