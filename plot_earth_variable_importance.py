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

# <codecell>

d_evimps = [('d_word_count', (20.0, 100.0, 100.0)), ('d_thumb_right_count', (19.0, 33.776363564361652, 36.542379557760988)), ('d_h2_text_median', (18.0, 27.730815629958929, 30.513915113257422)), ('d_spoken_wp_count', (17.0, 20.668257238057077, 23.536010810717659)), ('d_navbox_word_mean', (16.0, 15.92393475739058, 18.776587616654023)), ('d_reflist_count', (15.0, 12.464754100334925, 15.24758483858623)), ('d_cite_web', (14.0, 9.6051766814164132, 12.295316018491842)), ('d_caption_word_variance', (13.0, 7.72693271996354, 10.277876285713795)), ('d_cite_count', (12.0, 6.5500111045957388, 8.9271667683051081)), ('d_p_count', (11.0, 5.5215397785299212, 7.7196337490168556)), ('d_h3_text_variance', (9.0, 4.53085398853126, 6.3147549368330935)), ('d_int_link_text_median', (8.0, 3.4135129302536971, 5.0313143034491468)), ('d_h3_header_mean', (5.0, 1.5819359033683611, 2.6197452475042859)), ('d_h3_text_skewness_trimmed', (4.0, 0.91900346917035425, 1.770662475344162))]
x = plot_evimp(d_evimps)

# <codecell>

# higher new_var penalty (1)
d_evimps2 = [('d_wiki_file_link_count', (16.0, 100.0, 100.0)), ('d_cite_count', (15.0, 45.960297318926784, 47.710161211021443)), ('d_h2_text_median', (14.0, 30.324428913923111, 32.409346891964589)), ('d_spoken_wp_count', (13.0, 21.861828497587346, 24.023053691756882)), ('d_cite_web', (12.0, 17.630290783811819, 19.70736416920683)), ('d_word_count', (11.0, 13.450484602719232, 15.452889269209757)), ('d_p_count', (10.0, 11.030019146208833, 12.88811125228103)), ('d_navbox_word_mean', (9.0, 8.4173312575838022, 10.147071496439471)), ('d_reflist_count', (8.0, 6.3693723410063532, 7.9504548667335415)), ('d_caption_word_mean', (7.0, 4.7316477899661784, 6.1492145454634999)), ('d_int_link_text_median', (5.0, 2.6584513450550746, 3.6991705594880733))]
x = plot_evimp(d_evimps2)

# <codecell>

d_evimps_test = [('d_word_count', (18.0, 100.0, 100.0)), ('d_h2_text_median', (16.0, 34.982168650891104, 37.358388731923114)), ('d_navbox_word_median', (15.0, 29.206411735822503, 31.567508806550581)), ('d_spoken_wp_count', (14.0, 23.612959807573702, 25.965516683770495)), ('d_ext_link_count', (13.0, 18.98132095549618, 21.290065723096006)), ('d_all_img_count', (12.0, 14.907536364433458, 17.155102665966687)), ('d_h3_text_rel_std_dev', (11.0, 10.909104470417271, 13.102586476404852)), ('d_caption_word_mean', (10.0, 8.6439649090357324, 10.695978132426863)), ('d_cite_per_w', (9.0, 6.709070617926348, 8.6067515540164852)), ('d_cite_journal', (8.0, 5.3378351981749264, 7.0530811857142144)), ('d_p_mean_trimmed', (7.0, 4.0041251657343881, 5.5385577556500429)), ('d_caption_word_variance', (5.0, 2.1370910964557313, 3.2704142906120324)), ('d_p_skewness', (4.0, 1.3064040342775756, 2.2365639142437543))]
x = plot_evimp(d_evimps_test)

# <codecell>

from matplotlib.pyplot import figure
from numpy import linspace
from scipy.stats import beta
 
x = linspace(0,1,75)
 
fig = figure()
ax = fig.add_subplot(111)
ax.plot(x,beta.pdf(x,0.5,0.5),label=r"$\alpha=\beta=0.5$")
ax.plot(x,beta.pdf(x,5,1),label=r"$\alpha=5, \beta=1$")
ax.plot(x,beta.pdf(x,1,3),label=r"$\alpha=1, \beta=3$")
ax.plot(x,beta.pdf(x,2,2),label=r"$\alpha=2, \beta=2$")
ax.plot(x,beta.pdf(x,2,5),label=r"$\alpha=2, \beta=5$")
ax.grid(True)
ax.minorticks_on()
ax.legend(loc=9)
setp(ax.get_legend().get_texts(),fontsize='small')
ax.set_ylim(0,2.6)
ax.set_xlabel("x")
ax.set_ylabel("PDF")

# <codecell>

from matplotlib.pyplot import figure
from numpy import linspace
from scipy import stats
 
old_alpha = 12.1687
old_beta = 7.2045

alpha = 4.34748
beta = 2.9277428

b_pdf = stats.beta.pdf(x,alpha,beta)
b_stats = stats.beta.stats(alpha, beta, moments='mvsk')

x = linspace(0,1,75)
fig = figure()
ax = fig.add_subplot(111)
ax.plot(x, b_pdf,label=r"$\alpha=%s \beta=%s$" % (alpha, beta))
ax.grid(True)
ax.minorticks_on()
ax.legend(loc=9)
setp(ax.get_legend().get_texts(),fontsize='small')
ax.set_ylim(0,6)
ax.set_xlabel("x")
ax.set_ylabel("PDF")

# <codecell>

b_stats

