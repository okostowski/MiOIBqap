import sys
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    folder_path = sys.argv[1]
    optima_path = sys.argv[2]
    instance_names = sys.argv[3:] #niech np 2 pierwsze wchodzą na wykres podobieństwa itp
    
    folder_path='../wyniki'
    optima_path='../rozwiazania'
    instance_names=['els19','chr25a']
    instances = []
    mnoznik_czasu = 1000 / 1000
    for instance_name in instance_names:
        file = open(folder_path+"/multistart/"+instance_name+"_s.txt")
        steepest_all_data = file.read().split("\n\n")
        steepest = {"start_scores":[], "assignments":[], "scores":[], "steps":[], "mean_time":float(steepest_all_data[-1])*mnoznik_czasu}
        for result in steepest_all_data[:-1]:
            res = result.split("\n")
            steepest["start_scores"].append(int(res[0]))
            steepest["assignments"].append([int(x) for x in res[1].split(" ")[:-1]])
            steepest["scores"].append(int(res[2]))
            steepest["steps"].append(int(res[3]))
        file.close()
        
        file = open(folder_path+"/multistart/"+instance_name+"_g.txt")
        greedy_all_data = file.read().split("\n\n")
        greedy = {"start_scores":[], "assignments":[], "scores":[], "steps":[], "mean_time":float(greedy_all_data[-1])*mnoznik_czasu}
        for result in greedy_all_data[:-1]:
            res = result.split("\n")
            greedy["start_scores"].append(int(res[0]))
            greedy["assignments"].append([int(x) for x in res[1].split(" ")[:-1]])
            greedy["scores"].append(int(res[2]))
            greedy["steps"].append(int(res[3]))
        file.close()
        steepest["start_scores"] = np.array(steepest["start_scores"])
        greedy["start_scores"] = np.array(greedy["start_scores"])
        steepest["steps"] = np.array(steepest["steps"])
        greedy["steps"] = np.array(greedy["steps"])
        steepest["scores"] = np.array(steepest["scores"])
        greedy["scores"] = np.array(greedy["scores"])
        
        file = open(optima_path+"/"+instance_name+".sln")
        optimum_data = [line.split() for line in file.readlines()]
        solution = [int(x) for x in optimum_data[1]]
        n, optimum = [int(x) for x in optimum_data[0]]
        file.close()
        
        instances.append({"name":instance_name, "n":n, "optimum":optimum, 
                          "solution":solution, "data_s":steepest, 
                          "data_g":greedy})
    
    
    for instance in instances:
        s_similarity, g_similarity = [],[]
        s_solutions, g_solutions = instance['data_s']['assignments'],instance['data_g']['assignments']
        solution = instance['solution']
        for s_s,g_s in zip(s_solutions,g_solutions):
            s_sim, g_sim = 0,0
            for s_i, g_i, i in zip(s_s,g_s,solution):
                if s_i==i: s_sim+=1
                if g_i==i: g_sim+=1
            s_similarity.append(s_sim/instance['n'])
            g_similarity.append(g_sim/instance['n'])
        
        s_quality = instance['optimum']/instance['data_s']['scores']
        g_quality = instance['optimum']/instance['data_g']['scores']
        
        s_quality_start = instance['optimum']/instance['data_s']['start_scores']
        g_quality_start = instance['optimum']/instance['data_g']['start_scores']
        
        plt.figure()
        plt.scatter(s_quality, s_similarity, label="Steepest")
        plt.scatter(g_quality, g_similarity, label="Greedy")
        plt.legend()
        plt.title(instance['name'])
        plt.xlabel("Jakość rozwiązania")
        plt.ylabel("Podobieństwo do optimum")
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        plt.savefig("plot_"+instance['name']+"_similarity_vs_quality.pdf")
        
        plt.figure(figsize=(15,8))
        plt.subplot(1,2,1)
        plt.scatter(s_quality_start, s_quality, label="Steepest")
        plt.title(instance['name']+' - steepest')
        plt.xlabel("Jakość początkowego rozwiązania")
        plt.ylabel("Jakość rozwiązania")
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        plt.subplot(1,2,2)
        plt.scatter(g_quality_start, g_quality, label="Greedy")
        plt.title(instance['name']+' - greedy')
        plt.xlabel("Jakość początkowego rozwiązania")
        plt.ylabel("Jakość rozwiązania")
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        plt.savefig("plot_"+instance['name']+"_startquality_vs_quality.pdf")
        
        s_scores, g_scores = instance['data_s']['scores'],instance['data_g']['scores']
        s_scores_mean, g_scores_mean, s_scores_std, g_scores_std, s_scores_max, g_scores_max = [],[],[],[],[],[]
        for i in np.linspace(50,500,10,endpoint=True):
            i = np.int(i)
            s_scores_mean.append(np.divide(instance['optimum'],np.mean(s_scores[:i])))
            s_scores_std.append(np.divide(np.std(s_scores[:i]),np.mean(g_scores[:i])))
            s_scores_max.append(np.divide(instance['optimum'],np.min(s_scores[:i])))
            g_scores_mean.append(np.divide(instance['optimum'],np.mean(g_scores[:i])))
            g_scores_std.append(np.divide(np.std(g_scores[:i]),np.mean(g_scores[:i])))
            g_scores_max.append(np.divide(instance['optimum'],np.min(g_scores[:i])))
            
        plt.figure()
        plt.plot(s_scores_max, "bo-", label="Steepest")
        plt.plot(g_scores_max, "rv-", label="Greedy")
        
        #plt.title("Jakość najlepszego rozwiązania w zależności od liczby restartów")
        plt.legend()
        plt.xticks(np.arange(10), [np.int(x) for x in np.linspace(50,500,10,endpoint=True)])
        
        plt.xlabel("Liczba restartów")
        plt.ylabel("Jakość rozwiązania")
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        #plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        
        plt.savefig("plot_restarts_vs_solution_max_"+instance['name']+".pdf")
        
        plt.figure(figsize=(15,8))
        xs = np.arange(10)
        plt.subplot(1,2,1)
        plt.errorbar(xs, s_scores_mean, s_scores_std, fmt="bo-", label="Steepest")
        plt.title("Steepest")
        plt.xticks(np.arange(10), [np.int(x) for x in np.linspace(50,500,10,endpoint=True)])
        plt.xlabel("Liczba restartów")
        plt.ylabel("Średnia jakość rozwiązania")
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                 
        plt.subplot(1,2,2)
        plt.errorbar(xs, g_scores_mean, g_scores_std, fmt="rv-", label="Greedy")
        plt.title("Greedy")
        plt.xticks(np.arange(10), [np.int(x) for x in np.linspace(50,500,10,endpoint=True)])
        plt.xlabel("Liczba restartów")
        plt.ylabel("Średnia jakość rozwiązania")
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        
        plt.savefig("plot_restarts_vs_solution_mean_"+instance['name']+".pdf")