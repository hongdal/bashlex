for ((number=1; number<10; number++)) 
{ 
    if (( $number % 5 == 0 )); then 
        echo "$number is divisible by 5" 
    fi 
    
} 
exit 0