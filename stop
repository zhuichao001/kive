if [ -z $1 ]; then
  echo "usage:./stop [svr | cli]"
  exit
fi

ps -ef | grep main_$1 | awk '{print $2}' | xargs kill -9
