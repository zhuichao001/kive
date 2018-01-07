ps -ef | grep main_server | awk '{print $2}' | xargs kill -9

cd ..
python -m kive/server/main_server
