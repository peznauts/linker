import setuptools


setuptools.setup(
    name='linker',
    version='0.0.1',
    long_description=__doc__,
    packages=[
        'linker'
    ],
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'sqlalchemy',
        'pymysql'
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points = {
        "console_scripts": [
            "linker-debug = linker.entry:start_app_debug",
            "linker-prod = linker.entry:start_app_prod",
            "linker-db-sync = linker.entry:db_sync"
        ]
    }
)
