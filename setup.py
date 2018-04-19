from distutils.core import setup

setup(
    name='hubstaff',
    version='0.0.1',
    packages=['hubstaff'],
    url='',
    license='',
    author='Andrey Bortnikov',
    author_email='and.bortnik@gmail.com',
    requirements=[
        'requests==2.18.4',
        'dominate==2.3.1',
        'python-dateutil==2.7.2',
    ],
    scripts=['hubstaff_data.py'],
    description=''
)
