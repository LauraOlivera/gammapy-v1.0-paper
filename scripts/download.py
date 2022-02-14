import logging
import click
from pathlib import Path
from gammapy.scripts.download import progress_download

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

BASE_URL = "https://github.com/gammapy/gammapy-data/raw/master/"
PATH = Path(__file__).parent.parent
PATH_DATA = PATH / "src/data"


FILENAMES_FERMI = [
    "fermi-3fhl-gc-counts-cube.fits.gz",
    "fermi-3fhl-gc-background-cube.fits.gz",
    "fermi-3fhl-gc-exposure-cube.fits.gz",
    "fermi-3fhl-gc-psf-cube.fits.gz",
]

FILENAMES_CTA = [
    "index/gps/hdu-index.fits.gz",
    "index/gps/obs-index.fits.gz",
    "data/baseline/gps/gps_baseline_110380.fits",
    "data/baseline/gps/gps_baseline_111140.fits",
    "data/baseline/gps/gps_baseline_111159.fits",
    "caldb/data/cta/1dc/bcf/South_z20_50h/irf_file.fits",
]


def download_cta_data():
    cta_path = PATH_DATA / f"cta-galactic-center/input"
    cta_path.mkdir(exist_ok=True, parents=True)

    for filename in FILENAMES_CTA:
        destination = cta_path / filename
        destination.parent.mkdir(exist_ok=True, parents=True)
        source = BASE_URL + "cta-1dc/" + filename
        log.info(f"Downloading {source}")
        progress_download(source, destination)


def download_fermi_data():
    fermi_path = PATH_DATA / f"fermi-ts-map/input"
    fermi_path.mkdir(exist_ok=True, parents=True)

    for filename in FILENAMES_FERMI:
        destination = fermi_path / filename
        source = BASE_URL + "fermi-3fhl-gc/" + filename
        log.info(f"Downloading {source}")
        progress_download(source, destination)


DATASETS_REGISTRY = {
    "fermi-gc": download_fermi_data,
    "cta-1dc": download_cta_data,
}


@click.command()
@click.argument(
    "dataset", type=click.Choice(list(DATASETS_REGISTRY), case_sensitive=False)
)
def cli(dataset):
    download_method = DATASETS_REGISTRY[dataset]
    download_method()


if __name__ == "__main__":
    cli()
