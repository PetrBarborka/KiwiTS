from subprocess import call

repo = "../../kiwisources/travelling-salesman/"
# repo = "/repo/"

# n = [5, 10, 15, 20, 30, 40, 50, 60, 70, 100, 200, 300]
n = [5, 10, 100]

files = ["{}real_data/data_{}.txt".format(repo, i) for i in n]

for f in files:
    # print( "calling {}".format(f) )
    call( "cat {} | ./run".format(f), shell=True )
