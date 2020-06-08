---
permalink: /histos/
title:   "Preliminary Histograms"
layout:  single
sidebar:
  nav: "histos1"
classes: wide
---

A large array of potentially useful variables are selected from the refined analysis data samples described in the [LHCb](../lhcb) section. This initial selection is conducted based on general physical considerations of what would constitute the best training set for a multivariate analysis algorithm (MVA). The main particle properties considered in the selection are in the histograms to the left. Most, but not all of them are applicable for every particle in the studied decay chains.

Thus, if a particle contains one of the properties listed in the histograms you can access to the left, the distribution of that variable is plotted for both real data and the simulation. The two resulting histograms are then normalized with respect to their total number of events and overlaid. The obtained plots are used to determine if the variable under consideration is indeed a good candidate for MVA training. If the shape of the signal MC sample distribution is quite distinct from the real data sample shape, then the variable is deemed as good; if they match, the variable is removed and the BDT will not be trained on it. This is to ensure that the MVA learns how to discriminate between signal and background with high efficiency. All the plots are found on the links to the left of this webpage. These are only for Run I. The Run II histograms are the same, since the increase in statistics is not noticeable as the histograms are normalized.
