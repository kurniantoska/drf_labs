from __future__ import print_function

__all__ = ('read_pgpass',)


def read_pgpass(dbname, BASE_DIR):
    """
    Reads the pgpass. Returns the postgres settings dict for Django.
    :param str dbname:
    :return dict:
    """
    import os
    import psycopg2.extensions

    try:
        # See http://stackoverflow.com/questions/14742064/python-os-environhome-works-on-idle-but-not-in-a-script
        home_folder = os.path.expanduser('~')
        pgpass = os.path.join(home_folder, '.pgpass')
        pgpass_lines = open(pgpass).read().split()
    except IOError:
        print(
            """
            error read pgpass!
            """
            )
    else:
        for match in (dbname, '*'):
            for line in pgpass_lines:
                words = line.strip().split(':')
                if words[2] == match:
                    return {
                        'ENGINE': 'django.db.backends.postgresql_psycopg2',
                        'NAME': dbname,
                        'USER': words[3],
                        'PASSWORD': words[4],
                        'HOST': words[0],
                        'OPTIONS': {
                            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
                        },
                    }
        ## wanna print something here.. if you want
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
