            hospitalized = [0] * 7 + [np.mean(hospitalized[x - 7: x]) for x in range(7, len(hospitalized))]
