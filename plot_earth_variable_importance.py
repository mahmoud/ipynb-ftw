# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

def plot_evimp(evimp):
    import pylab
    fig = pylab.figure()
    axes1 = fig.add_subplot(111)
    attrs = [a for a, _ in evimp]
    imp = [s for _, s in evimp]
    imp = numpy.array(imp)
    X = range(len(attrs))
    l1 = axes1.plot(X, imp[:, 0], "b-", label="nsubsets")
    axes2 = axes1.twinx()

    l2 = axes2.plot(X, imp[:, 1], "g-", label="gcv")
    l3 = axes2.plot(X, imp[:, 2], "r-", label="rss")

    x_axis = axes1.xaxis
    x_axis.set_ticks(X)
    x_axis.set_ticklabels([a for a in attrs], rotation=90)

    axes1.yaxis.set_label_text("nsubsets")
    axes2.yaxis.set_label_text("normalized gcv or rss")

    axes1.legend((l1[0], l2[0], l3[0]), ("nsubsets", "gcv", "rss"))

    axes1.set_title("Variable importance")
    return fig

# get this with [(v.name, i) for v, i in in_classifier.evimp()]
ev_imps = [('d_Earth_score', (14.0, 100.0, 100.0)), ('rv_t_Earth_abs_error', (13.0, 45.128448423301073, 45.580204569556933)), ('rv_t_Earth_score', (11.0, 25.542997633117885, 26.007005502156545)), ('rv_Earth_score', (10.0, 11.047386277152476, 11.636564532975727)), ('d_rel_Earth_abs_error', (8.0, 4.2512898775610228, 4.7857072329646462)), ('rv_Earth_abs_error', (5.0, 1.6827235926962756, 2.028000469935141))]

x = plot_evimp(ev_imps)

# <codecell>

metamars_v1_evimps = [('d_Earth_score', (9.0, 100.0, 100.0)), ('rv_Earth_score', (8.0, 22.086250105371903, 23.063403196811507)), ('d_rel_Earth_score', (5.0, 0.78695121600693041, 1.6083434492547779)), ('rv_t_Earth_score', (4.0, 0.36353647527114635, 1.0254131229982806))]
x = plot_evimp(metamars_v1_evimps)

