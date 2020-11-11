# SlackAssistant

To begin:

    extra requirements:
        download rabbitmq: sudo apt-get install rabbitmq-server
        download celery: pip install celery #uses python3 
        download dependencies: pip install -r requirements.txt
    
    1. start rabbitmq (see below) (Note that rabbitmq starts by itself upon install)
    2. start celery (see below)
    3. start assistant (see below)

    You should be able to see incoming events and responses in the window where assistant is running
    
For RabbitMQ:

    starting: sudo rabbitmqctl start_app
    stopping: sudo rabbitmqctl stop_app
    reset: sudo rabbitmqctl reset
    restart: sudo rabbitmqctl restart

For Celery:

    starting: celery -A tasker worker --quiet --without-gossip --without-mingle --without-heartbeat

For Assistant:
    python3 rtm.py
    Theoretically should work with python2 as well but haven't tested
