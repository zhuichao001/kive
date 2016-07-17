if [ -z $1 ]; then
  echo "usage:./restart [svr | cli]"
  exit
fi

ps -ef | grep main_$1 | awk '{print $2}' | xargs kill -9
nohup python main_$1.py &>log.$1 &
