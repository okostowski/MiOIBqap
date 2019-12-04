import sys
import numpy as np
import matplotlib.pyplot as plt

#Argumenty: <sciezka do folderu z wynikami> <sciezka do folderu z rozwiazaniami> <nazwy instancji...>

if __name__ == "__main__":
    folder_path = sys.argv[1]
    optima_path = sys.argv[2]
    instance_names = sys.argv[3:] #niech np 2 pierwsze wchodzą na wykres podobieństwa itp
    '''
    folder_path='../wyniki'
    optima_path='../rozwiazania'
    instance_names=['chr12a', 'rou15', 'chr18a', 'els19', 'nug25', 'chr25a', 'kra32', 'ste36a']'''
    instances = []
    mnoznik_czasu = 1000 / 10
    for instance_name in instance_names:
        file = open(folder_path+"/"+instance_name+"/"+instance_name+"_s.txt")
        steepest_all_data = file.read().split("\n\n")
        steepest = {"start_scores":[], "assignments":[], "scores":[], "steps":[], "mean_time":float(steepest_all_data[-1])*mnoznik_czasu}
        for result in steepest_all_data[:-1]:
            res = result.split("\n")
            steepest["start_scores"].append(int(res[0]))
            steepest["assignments"].append([int(x) for x in res[1].split(" ")[:-1]])
            steepest["scores"].append(int(res[2]))
            steepest["steps"].append(int(res[3]))
        file.close()
        
        file = open(folder_path+"/"+instance_name+"/"+instance_name+"_g.txt")
        greedy_all_data = file.read().split("\n\n")
        greedy = {"start_scores":[], "assignments":[], "scores":[], "steps":[], "mean_time":float(greedy_all_data[-1])*mnoznik_czasu}
        for result in greedy_all_data[:-1]:
            res = result.split("\n")
            greedy["start_scores"].append(int(res[0]))
            greedy["assignments"].append([int(x) for x in res[1].split(" ")[:-1]])
            greedy["scores"].append(int(res[2]))
            greedy["steps"].append(int(res[3]))
        file.close()
        
        file = open(folder_path+"/"+instance_name+"/"+instance_name+"_r.txt")
        random_all_data = file.read().split("\n\n")
        random = {"assignments":[], "scores":[], "mean_time":float(random_all_data[-1])*mnoznik_czasu}
        for result in random_all_data[:-1]:
            res = result.split("\n")
            random["assignments"].append([int(x) for x in res[0].split(" ")[:-1]])
            random["scores"].append(int(res[1]))
        file.close()
        
        file = open(folder_path+"/"+instance_name+"/"+instance_name+"_h.txt")
        heu_all_data = file.read().split("\n\n")
        heu = {"assignments":[], "scores":[], "mean_time":float(heu_all_data[-1])*mnoznik_czasu}
        for result in heu_all_data[:-1]:
            res = result.split("\n")
            heu["assignments"].append([int(x) for x in res[0].split(" ")[:-1]])
            heu["scores"].append(int(res[1]))
        file.close()
        
        file = open(folder_path+"/"+instance_name+"/"+instance_name+"_sa.txt")
        sa_all_data = file.read().split("\n\n")
        sa = {"assignments":[], "scores":[], "steps":[], "mean_time":float(sa_all_data[-1])*mnoznik_czasu}
        for result in sa_all_data[:-1]:
            res = result.split("\n")
            sa["assignments"].append([int(x) for x in res[0].split(" ")[:-1]])
            sa["scores"].append(int(res[1]))
            sa["steps"].append(int(res[2]))
        file.close()
        
        file = open(folder_path+"/"+instance_name+"/"+instance_name+"_ts.txt")
        ts_all_data = file.read().split("\n\n")
        ts = {"assignments":[], "scores":[], "steps":[], "mean_time":float(ts_all_data[-1])*mnoznik_czasu}
        for result in ts_all_data[:-1]:
            res = result.split("\n")
            ts["assignments"].append([int(x) for x in res[0].split(" ")[:-1]])
            ts["scores"].append(int(res[1]))
            ts["steps"].append(int(res[2]))
        file.close()
        
        steepest["start_scores"] = np.array(steepest["start_scores"])
        greedy["start_scores"] = np.array(greedy["start_scores"])
        steepest["steps"] = np.array(steepest["steps"])
        greedy["steps"] = np.array(greedy["steps"])
        sa["steps"] = np.array(sa["steps"])
        ts["steps"] = np.array(ts["steps"])
        steepest["scores"] = np.array(steepest["scores"])
        greedy["scores"] = np.array(greedy["scores"])
        random["scores"] = np.array(random["scores"])
        heu["scores"] = np.array(heu["scores"])
        sa["scores"] = np.array(sa["scores"])
        ts["scores"] = np.array(ts["scores"])
        
        file = open(optima_path+"/"+instance_name+".sln")
        optimum_data = [line.split() for line in file.readlines()]
        solution = [int(x) for x in optimum_data[1]]
        n, optimum = [int(x) for x in optimum_data[0]]
        file.close()
        
        instances.append({"name":instance_name, "n":n, "optimum":optimum, 
                          "solution":solution, "data_s":steepest, 
                          "data_g":greedy, "data_r":random, "data_h":heu, 
                          "data_sa":sa, "data_ts":ts})

    s_meantime, g_meantime, r_meantime, h_meantime, sa_meantime, ts_meantime, names = [],[],[],[],[],[],[]
    s_quality_mean,g_quality_mean,r_quality_mean,h_quality_mean,sa_quality_mean,ts_quality_mean = [],[],[],[],[],[]
    s_quality_max, g_quality_max,r_quality_max,h_quality_max,sa_quality_max,ts_quality_max = [],[],[],[],[],[]
    s_quality_std,g_quality_std,r_quality_std,h_quality_std,sa_quality_std,ts_quality_std = [],[],[],[],[],[]
    s_steps_mean, g_steps_mean, s_steps_std, g_steps_std = [],[],[],[]
    sa_steps_mean, ts_steps_mean, sa_steps_std, ts_steps_std = [],[],[],[]
    for instance in instances:
        n_inst = instance['n']
        s_meantime.append(instance["data_s"]["mean_time"])
        r_meantime.append(instance["data_r"]["mean_time"])
        g_meantime.append(instance["data_g"]["mean_time"])
        h_meantime.append(instance["data_h"]["mean_time"])
        sa_meantime.append(instance["data_sa"]["mean_time"])
        ts_meantime.append(instance["data_ts"]["mean_time"])
        
        s_quality_mean.append(np.divide(instance['optimum'],np.mean(instance["data_s"]["scores"])))
        r_quality_mean.append(np.divide(instance['optimum'],np.mean(instance["data_r"]["scores"])))
        g_quality_mean.append(np.divide(instance['optimum'],np.mean(instance["data_g"]["scores"])))
        h_quality_mean.append(np.divide(instance['optimum'],np.mean(instance["data_h"]["scores"])))
        sa_quality_mean.append(np.divide(instance['optimum'],np.mean(instance["data_sa"]["scores"])))
        ts_quality_mean.append(np.divide(instance['optimum'],np.mean(instance["data_ts"]["scores"])))
        s_quality_std.append(np.divide(np.std(instance["data_s"]["scores"]),np.mean(instance["data_s"]["scores"])))
        r_quality_std.append(np.divide(np.std(instance["data_r"]["scores"]),np.mean(instance["data_r"]["scores"])))
        g_quality_std.append(np.divide(np.std(instance["data_g"]["scores"]),np.mean(instance["data_g"]["scores"])))
        h_quality_std.append(np.divide(np.std(instance["data_h"]["scores"]),np.mean(instance["data_h"]["scores"])))
        sa_quality_std.append(np.divide(np.std(instance["data_sa"]["scores"]),np.mean(instance["data_sa"]["scores"])))
        ts_quality_std.append(np.divide(np.std(instance["data_ts"]["scores"]),np.mean(instance["data_ts"]["scores"])))
        
        s_quality_max.append(np.divide(instance['optimum'],np.min(instance["data_s"]["scores"])))
        r_quality_max.append(np.divide(instance['optimum'],np.min(instance["data_r"]["scores"])))
        g_quality_max.append(np.divide(instance['optimum'],np.min(instance["data_g"]["scores"])))
        h_quality_max.append(np.divide(instance['optimum'],np.min(instance["data_h"]["scores"])))
        sa_quality_max.append(np.divide(instance['optimum'],np.min(instance["data_sa"]["scores"])))
        ts_quality_max.append(np.divide(instance['optimum'],np.min(instance["data_ts"]["scores"])))
        
        s_steps_mean.append(np.mean(instance['data_s']['steps']))
        g_steps_mean.append(np.mean(instance['data_g']['steps']))
        s_steps_std.append(np.std(instance['data_s']['steps']))
        g_steps_std.append(np.std(instance['data_g']['steps']))
        
        sa_steps_mean.append(np.mean(instance['data_sa']['steps']))
        ts_steps_mean.append(np.mean(instance['data_ts']['steps']))
        sa_steps_std.append(np.std(instance['data_sa']['steps']))
        ts_steps_std.append(np.std(instance['data_ts']['steps']))
        names.append(instance["name"])
        
    #Wykres czasu dzialania
    plt.figure()
    plt.plot(s_meantime, "bo-", label="Steepest")
    plt.plot(g_meantime, "rv-", label="Greedy")
    plt.plot(r_meantime, "gs-", label="Random")
    plt.plot(h_meantime, "yp-", label="Heuristic")
    plt.plot(ts_meantime, "kD-", label="TS")
    plt.plot(sa_meantime, "ch-", label="SA")
    
    #plt.title("Czas działania")
    plt.legend()
    plt.xticks(np.arange(len(names)), names)
    
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Czas [ms]")
    plt.yscale('log')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    
    plt.savefig("plot_mean_time.pdf")
    
    #wykres jakosci najlepszego rozwiązania
    plt.figure()
    plt.plot(s_quality_max, "bo-", label="Steepest")
    plt.plot(g_quality_max, "rv-", label="Greedy")
    plt.plot(r_quality_max, "gs-", label="Random")
    plt.plot(h_quality_max, "yp-", label="Heuristic")
    plt.plot(sa_quality_max, "ch-", label="SA")
    plt.plot(ts_quality_max, "kD-", label="TS")
    
    #plt.title("Maksymalna jakość")
    plt.legend()
    plt.xticks(np.arange(len(names)), names)
    
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Najlepsza jakość rozwiązania")#"Średnia jakość rozwiązania")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    
    plt.savefig("plot_quality_best.pdf")
    
    #wykres jakosci sredniego rozwiązania
    plt.figure(figsize=(15,22))
    plt.subplot(3,2,1)
    xs = np.arange(len(instances))
    plt.errorbar(xs, s_quality_mean, s_quality_std, fmt="bo-", label="Steepest")
    plt.title("Steepest")
    plt.xticks(np.arange(len(names)), names)
    plt.ylim(0.0,1.0)
    
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Średnia jakość rozwiązania")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.subplot(3,2,2)
    plt.errorbar(xs, g_quality_mean, g_quality_std, fmt="rv-", label="Greedy")
    plt.title("Greedy")
    plt.xticks(np.arange(len(names)), names)
    plt.ylim(0.0,1.0)
    
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Średnia jakość rozwiązania")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.subplot(3,2,3)
    plt.errorbar(xs, r_quality_mean, r_quality_std, fmt="gs-", label="Random")
    plt.title("Random")
    plt.xticks(np.arange(len(names)), names)
    plt.ylim(0.0,1.0)
    
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Średnia jakość rozwiązania")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.subplot(3,2,4)
    plt.errorbar(xs, h_quality_mean, h_quality_std, fmt="yp-", label="Heuristic")
    
    plt.title("Heuristic")
    plt.xticks(np.arange(len(names)), names)
    plt.ylim(0.0,1.0)
    
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Średnia jakość rozwiązania")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
             
    plt.subplot(3,2,5)
    plt.errorbar(xs, ts_quality_mean, ts_quality_std, fmt="kD-", label="TS")
    
    plt.title("TS")
    plt.xticks(np.arange(len(names)), names)
    plt.ylim(0.0,1.0)
    
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Średnia jakość rozwiązania")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    
    plt.subplot(3,2,6)
    plt.errorbar(xs, sa_quality_mean, sa_quality_std, fmt="ch-", label="SA")
    
    plt.title("SA")
    plt.xticks(np.arange(len(names)), names)
    plt.ylim(0.0,1.0)
    
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Średnia jakość rozwiązania")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    
    plt.savefig("plot_quality_mean.pdf")
    
    #wykres efektywnosci
    plt.figure()
    plt.plot(np.divide(s_quality_mean,s_meantime), "bo-", label="Steepest")
    plt.plot(np.divide(g_quality_mean,g_meantime), "rv-", label="Greedy")
    plt.plot(np.divide(r_quality_mean,r_meantime), "gs-", label="Random")
    plt.plot(np.divide(h_quality_mean,h_meantime), "yp-", label="Heuristic")
    plt.plot(np.divide(sa_quality_mean,sa_meantime), "ch-", label="SA")
    plt.plot(np.divide(ts_quality_mean,ts_meantime), "kD-", label="TS")
    
    #plt.title("Efektywność algorytmów")
    plt.legend()
    plt.xticks(np.arange(len(names)), names)
    
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Efektywność")#"Średnia jakość rozwiązania")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    
    plt.savefig("plot_effectivness.pdf")
    
    #wykres sredniej ilosci krokow G i S
    plt.figure()
    xs = np.arange(len(instances))
    plt.errorbar(xs, s_steps_mean, s_steps_std, fmt="bo-", label="Steepest")
    plt.errorbar(xs, g_steps_mean, g_steps_std, fmt="rv-", label="Greedy")
    #plt.title("Średnia ilość kroków")
    plt.xticks(np.arange(len(names)), names)
    plt.legend()
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Średnia liczba kroków")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    
    plt.savefig("plot_steps_mean.pdf")
    
    #wykres sredniej ilosci krokow SA i TS
    plt.figure()
    xs = np.arange(len(instances))
    plt.errorbar(xs, sa_steps_mean, sa_steps_std, fmt="ch-", label="SA")
    plt.errorbar(xs, ts_steps_mean, ts_steps_std, fmt="kD-", label="TS")
    #plt.title("Średnia ilość kroków")
    plt.xticks(np.arange(len(names)), names)
    plt.legend()
    plt.xlabel("Nazwa instancji")
    plt.ylabel("Średnia liczba kroków")
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    
    plt.savefig("plot_steps_mean_meta.pdf")