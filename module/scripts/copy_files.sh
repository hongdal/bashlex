#!/bin/bash
function recursive_copy_file()
{
    dirlist=$(ls $1)
    for name in ${dirlist[*]}
    do
        if [ -f $1/$name ]; then
            # 如果是文件，并且$2不存在该文件，则直接copy
            if [ ! -f $2/$name ]; then
                cp $1/$name $2
            fi
        elif [ -d $1/$name ]; then
            # 如果是目录，并且$2不存在该目录，则先创建目录
            # 递归拷贝
            recursive_copy_file $1/$name $2
        fi
    done
}
 
source_dir="/home/guoze/Work/03_projectsDev/bashlex/0_data/bashData/Bash"
dest_dir="/home/guoze/Work/03_projectsDev/bashlex/0_data/bashData/allbashscripts/"
 
recursive_copy_file $source_dir $dest_dir
