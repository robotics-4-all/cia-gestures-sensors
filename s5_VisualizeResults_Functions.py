"""
This script was created at 20-Sep-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
sns.set()


#  ============== #
#    Functions    #
# =============== #
def visualize_results(screen_path: str, results: pd.DataFrame) -> None:

    plots_path = os.path.join(screen_path, 'results.png')

    if not os.path.exists(plots_path):

        metrics_table = [['NumOfOrgUserTstData', 'FRR', 'FAR'],
                         ['NumOfUnlocks', 'FRR_Conf', 'NumOfAcceptTL']]

        ncols = 3
        nrows = len(metrics_table) * 3 // ncols

        fig, axes = plt.subplots(nrows, ncols, sharey=True, figsize=(ncols * 6.4, nrows * 4.8))
        fig.suptitle('Results')

        for i_row, metrics in enumerate(metrics_table):
            for i_col, metric in enumerate(metrics):
                sns.boxplot(ax=axes[i_row, i_col],
                            data=results, y='Module', x=metric,
                            showmeans=True, meanprops={'marker': 'o', 'markeredgecolor': 'black'})

                axes[i_row, i_col].set_xlabel('')
                axes[i_row, i_col].set_ylabel('')
                axes[i_row, i_col].set_title(metric)

        plt.tight_layout()
        # fig.show()
        plt.savefig(plots_path, bbox_inches='tight')
        plt.close(fig)

        print('     Results plots saved at:', plots_path)

    else:

        print('     Results plots already saved at:', plots_path)

    print('')

    return
