pg_dump -Fc --no-acl --no-owner kurator > kurator.dump
s3cmd put kurator.dump s3://umc_kurator/db
heroku pgbackups:restore DATABASE 'https://s3.amazonaws.com/umc_kurator/db'
