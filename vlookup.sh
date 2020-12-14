    #!/bin/bash

    #判断参数个数
    if [ $# != 3 ];
    then
        echo "\n$0 关键字文件 要查找的文件 输出的目标文件\n"
        echo "参数中如果有通配符，需要将参数用双引号包起来\n"
        exit 1;
    fi

    cat $1 | while read line
    do
        echo "$line $2 >> $3"
        grep "$line" $2 > $3
    done
    if [ ! -s $3 ];
    then
    cat $2 > $3
    fi


