import glob
import sys
import bashgraph as bg


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + "testcase_dir")
        exit(1)

    test_dir = sys.argv[1]
    bash_files = glob.glob(test_dir + "/*.sh")

    

    for file in bash_files:
        print(file)
