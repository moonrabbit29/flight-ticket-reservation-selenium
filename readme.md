### This Web Automation build following this scenario
create transaction for flight product from search until
choose payment method with non login user.

### My assumptions
I create my automation script to process one way flight ticket reservation on tiket.com website.
The script will run and select random variables which consist of Number of passenger,cabin class,flight schedule/airline. Some test done on this scripts includes matching number of passengers on display box after passengers number input and cabin class selected

### My Environtment Spesification :
   OS: Windows 10
   python : 3.7.9 64 bit
   java version : 1.8.0_291

### Module/package needed
   pytest
   pytest-xdist
   pytest-rerunfailures
   selenium
   pyptest-repeat

### How to run
   This scripts run automation on chromium web browser, step to run this scripts
   1. Open this cloned repostiory directory on your computer and run => java -jar selenium-server-standalone-3.141.59.jar
   2. Open another terminal to run the script, you can run => pytest -s means you only run one test or simply use => pytest --count=NUMBER OF TEST YOU WANT TO RUN to run multiple test (occur in turn)

