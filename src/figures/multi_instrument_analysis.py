import config
import astropy.units as u
from gammapy.estimators import FluxPoints
from gammapy.modeling.models import Models
import matplotlib.pyplot as plt

sed_x_label = r"$E\,/\,{\rm TeV}$"
sed_y_label = (
    r"$E^2\,{\rm d}\phi/{\rm d}\phi\,/\,({\rm erg}\,{\rm cm}^{-2}\,{\rm s}^{-1})$"
)

figsize = config.FigureSizeAA(aspect_ratio=1.618, width_aa="intermediate")
fig = plt.figure(figsize=figsize.inch)
ax = fig.add_axes([0.1, 0.1, 0.9, 0.9])

# load the flux points and plot them
fermi_flux_points = FluxPoints.read(
    "../data/multi-instrument/datasets/flux_points/crab_fermi_flux_points.fits"
)
magic_flux_points = FluxPoints.read(
    "../data/multi-instrument/datasets/flux_points/crab_magic_flux_points.fits"
)
hawc_flux_points = FluxPoints.read(
    "../data/multi-instrument/input/hawc/HAWC19_flux_points.fits"
)

# load the best-fit model
models = Models.read("../data/multi-instrument/results/crab_multi_instrument_fit.yaml")
crab_lp = models["Crab Nebula"].spectral_model

plot_kwargs = {
    "energy_bounds": [0.01, 300] * u.TeV,
    "sed_type": "e2dnde",
    "yunits": u.Unit("erg cm-2 s-1"),
    "xunits": u.TeV,
}

crab_lp.plot(ax=ax, ls="-", lw=1.5, color="crimson", label="joint fit", **plot_kwargs)
crab_lp.plot_error(ax=ax, facecolor="crimson", alpha=0.4, **plot_kwargs)

fermi_flux_points.plot(ax=ax, sed_type="e2dnde", color="k", label="Fermi-LAT")
magic_flux_points.plot(ax=ax, sed_type="e2dnde", color="dodgerblue", label="MAGIC")
hawc_flux_points.plot(ax=ax, sed_type="e2dnde", color="goldenrod", label="HAWC")

ax.set_xlim(plot_kwargs["energy_bounds"])
ax.set_xlabel(sed_x_label)
ax.set_ylabel(sed_y_label)
ax.legend()
fig.savefig("multi_instrument_analysis.pdf")
fig.savefig("multi_instrument_analysis.png")
