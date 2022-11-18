pkill -9 python3
export DEVELOP_ENV=prod
nohup python3 /github/web/app.py > /data/log.out 2>&1 &
