---
permalink: /fitting/
title:   "Fitting"
layout:  single
sidebar:
    nav: "fitting"
classes: wide
---

A cut must be applied at a certain value of the BDT response variable to obtain maximum signal yield while minimizing the background. This is established by doing a series of fits on the MC and real data $m_{B^+}$ spectra.

The functional shape of the signal is determined by fitting three different models to the signal MC: a sum of Crystal Ball (CB) distributions, a sum of Gaussians, and a Breit-Wigner distribution. The motivation for fitting a Breit-Wigner comes from theory, as this particular distribution models the resonance curve produced by a particle, in this case the $B$ meson. However, it is found that it performs the worst due to detector resolution effects that appear in the MC simulation. Conversely, the CB model gives the best $\chi^2$ when compared to the other two, and thus it is used in fitting the data spectrum. The Gaussian sum lies in between the other two fits in terms of $\chi^2$ value. All fits are shown in the links in the sidebar. For some of the studied decay chains, the Crystal Ball $\chi^2$ and the Gaussian fit $\chi^2$ were quite close. Thus, for these particular modes, it was considered using the Gaussian sum since it contains fewer parameters. However, the Crystal Ball sum was ultimately used for all the decays because the added complexity of using an inhomogeneous fitting paradigm would lead to more complications than benefits.

Prior to any data fitting, events are selected to contain at least one charged $B$ meson decaying. Thus, the amount of data to be fitted is reduced considerably and the $B$ meson mass resonance is visible even without applying cuts. The data sample is then fitted using a composite model of the previously determined Crystal Ball sum and an exponential. The Crystal Ball parameters are mostly fixed to be the ones obtained from fitting the corresponding Monte Carlo sample. The sole exception is the width which is allowed to vary slightly due to the MC being narrower. The exponential was chosen to fit the combinatorial background, which looks like fake signal.

Overlaid on top of the data signal is the fitted Monte Carlo simulation, scaled for comparison purposes. Notice that the CB sum fits the data spectrum quite well, which means that the fitting procedure was successful.  Additionally, the exponential is plotted separately and shows the amount of combinatorial background present in the data sample.

Both the exponential background and the signal CB sum are integrated in the range of $5230-5305$ MeV/c$^2$. These ntegration limits on the mass were chosen based on the Monte Carlo plot, as they span the full signal range. The exponential integral gives the background yield in the data, denoted by $B$. Alternatively, the integral of the data Crystal Ball sum gives the signal yield, denoted by $S$. The significance $f$ of the signal is defined as

$$
    f = \frac{S}{\sqrt{S+B}}
$$

and is calculated using the previously obtained values.

The value of $f$ is used as a metric to determine the particular cut that must be applied on the BDT response to obtain a maximum amount of signal and a minimum amount of background. The BDT response lies in the range $-0.5 < BDT\_G < 0.5$. Applying no BDT cuts is equivalent with applying a $ > -0.5$ cut. The optimal BDT cut is obtained iteratively. A total of 300 equally spaced values are taken from the BDT response interval. For each of these values, the data sample is cut such that no event has a lower BDT response than the considered one. The previously described fitting process is performed on the obtained data sample, but all the parameters, except the yields, are completely fixed on the values that were obtained from the initial $> -0.5$ BDT cut fit. The significance $f$ is calculated for each of the cut samples and plotted. The results are shown in the left hand side links. The maximum $f$ and the corresponding BDT cut is determined for each decay chain, marked by a red dot in the mentioned figure. Each obtained BDT cut is ultimately applied on the data sample prior to computing the corresponding raw $CP$ asymmetry.
