from sdk.moveapps_spec import hook_impl
from sdk.moveapps_io import MoveAppsIo
from movingpandas import TrajectoryCollection
import logging
import matplotlib.pyplot as plt

# import the function get_GDF from the file "./app/getGeoDataFrame.py"
from app.getGeoDataFrame import get_GDF

# showcase injecting App settings (parameter `year`)
from dataclasses import dataclass


@dataclass
class AppConfig:
    year: int


class App(object):

    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    # showcase injecting App settings (parameter `year`)
    @staticmethod
    def map_config(config: dict):
        return AppConfig(
            year=config["year"] if "year" in config else 1994
        )

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:

        logging.info(f'Welcome to the {config}')

        """Your app code goes here"""

        # showcase injecting App settings (parameter `year`)
        app_config = self.map_config(config=config)
        data_gdf = get_GDF(data)  # translate the TrajectoryCollection to a GeoDataFrame
        logging.info(f'Subsetting data for {app_config.year}')
        # subset the data to only contain the specified year
        if app_config.year in data_gdf.index.year:
            result = data_gdf[data_gdf.index.year == app_config.year]
        else:
            result = None

        # showcase creating an artifact
        if result is not None:
            result.plot(column=data.get_traj_id_col())
            plot_file = self.moveapps_io.create_artifacts_file("plot.png")
            plt.savefig(plot_file)
            logging.info(f'saved plot to {plot_file}')
        else:
            logging.warning("Nothing to plot")

        # showcase accessing auxiliary files
        # auxiliary_file_a = MoveAppsIo.get_auxiliary_file_path("auxiliary-file-a")
        # with open(auxiliary_file_a, 'r') as f:
        #    logging.info(f.read())

        # Translate the result back to a TrajectoryCollection
        if result is not None:
            result = TrajectoryCollection(
                result,
                traj_id_col=data.get_traj_id_col(),
                t=data.to_point_gdf().index.name,
                crs=data.get_crs()
            )
        logging.info(result)
        # return the resulting data for next Apps in the Workflow
        return result
