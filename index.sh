a=(master1,slave1,slave2)
for((i=$1;i<=$2;i++));
do
  echo "___now_${a}_____"
  ssh root@${a[i]} "source /etc/profile;"
done
