import sys
import numpy as np
import matplotlib.pyplot as plt

#Argumenty: <sciezka do folderu z wynikami> <sciezka do folderu z rozwiazaniami> <nazwy instancji...>

if __name__ == "__main__":
    folder_path = sys.argv[1]
    optima_path = sys.argv[2]
    instance_names = sys.argv[3:] #niech np 2 pierwsze wchodzą na wykres podobieństwa itp
    instances = []
    for instance_name in instance_names:
        file = open(folder_path+"/"+instance_name+"/"+instance_name+"_s.txt")
        steepest_all_data = file.read().split("\n\n")
        steepest = {"start_scores":[], "assignments":[], "scores":[], "steps":[], "mean_time":float(steepest_all_data[-1])/10.0}
        for result in steepest_all_data[:-1]:
            res = result.split("\n")
            steepest["start_scores"].append(int(res[0]))
            steepest["assignments"].append([int(x) for x in res[1].split(" ")[:-1]])
            steepest["scores"].append(int(res[2]))
            steepest["steps"].append(int(res[3]))
        file.close()
        
        file = open(folder_path+"/"+instance_name+"/"+instance_name+"_g.txt")
        greedy_all_data = file.read().split("\n\n")
        greedy = {"start_scores":[], "assignments":[], "scores":[], "steps":[], "mean_time":float(greedy_all_data[-1])/10.0}
        for result in greedy_all_data[:-1]:
            res = result.split("\n")
            greedy["start_scores"].append(int(res[0]))
            greedy["assignments"].append([int(x) for x in res[1].split(" ")[:-1]])
            greedy["scores"].append(int(res[2]))
            greedy["steps"].append(int(res[3]))
        file.close()
        
        file = open(folder_path+"/"+instance_name+"/"+instance_name+"_r.txt")
        random_all_data = file.read().split("\n\n")
        random = {"assignments":[], "scores":[], "mean_time":float(random_all_data[-1])/10.0}
        for result in random_all_data[:-1]:
            res = result.split("\n")
            random["assignments"].append([int(x) for x in res[0].split(" ")[:-1]])
            random["scores"].append(int(res[1]))
        file.close()
        
        steepest["start_scores"] = np.array(steepest["start_scores"])
        greedy["start_scores"] = np.array(greedy["start_scores"])
        steepest["steps"] = np.array(steepest["steps"])
        greedy["steps"] = np.array(greedy["steps"])
        steepest["scores"] = np.array(steepest["scores"])
        greedy["scores"] = np.array(greedy["scores"])
        random["scores"] = np.array(random["scores"])
        
        file = open(optima_path+"/"+instance_name+".sln")
        optimum_data = [line.split() for line in file.readlines()]
        solution = [int(x) for x in optimum_data[1]]
        n, optimum = [int(x) for x in optimum_data[0]]
        file.close()
        
        instances.append({"name":instance_name, "n":n, "optimum":optimum, 
                          "solution":solution, "data_s":steepest, 
                          "data_g":greedy, "data_r":random})

    s, g, r, names = [],[],[],[]
    for instance in instances:
        s.append(instance["data_s"]["mean_time"])
        r.append(instance["data_r"]["mean_time"])
        g.append(instance["data_g"]["mean_time"])
        names.append(instance["name"])
        
    plt.plot(s, "bo-", label="Steepest")
    plt.plot(g, "ro-", label="Greedy")
    plt.plot(r, "go-", label="Random")
    
    plt.title("Czas działania")
    plt.legend()
    plt.xticks(np.arange(len(names)), names)
    
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Czas [s]")
    
    plt.savefig("plot_mean_time.pdf")