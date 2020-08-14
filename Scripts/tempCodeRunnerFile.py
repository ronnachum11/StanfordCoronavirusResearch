    update_plot(f"COVID-19 Cumulative Hospitalizations - {state}", 0, x_ticks=x_ticks, x_tick_labels=x_tick_labels, add_reopenings=False)
    plt.plot(hospitalized, color='k')