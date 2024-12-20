from baseline import run_baseline
from main import run_agent
import os, glob, argparse
from tqdm import tqdm


def run_task(task, output_dir, task_type="vision", task_name=None, baseline=False):
    all_task_instances = glob.glob(
        f"../tasks/{task}/processed/*/"
        if task_type == "vision"
        else f"../tasks/{task}/*/"
    )
    output_dir = os.path.join(output_dir, task)

    for task_instance in tqdm(all_task_instances):
        print(f"Running task instance: {task_instance}")
        if baseline:
            run_baseline(
                task_instance, output_dir, task_type=task_type, task_name=task_name
            )
        else:
            run_agent(
                task_instance, output_dir, task_type=task_type, task_name=task_name
            )
        # break


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        type=str,
        choices=[
            "vstar",
            "blink_viscorr",
            "blink_semcorr",
            "blink_depth",
            "blink_jigsaw",
            "blink_spatial",
            "mmvp",
            "geometry",
            "graph_connectivity",
            "graph_isomorphism",
            "graph_maxflow",
            "math_convexity",
            "math_parity",
            "geometry_new",
            "winner_id",
        ],
        help="The task name",
    )
    parser.add_argument(
        "--baseline", action="store_true", help="Run the baseline model"
    )
    args = parser.parse_args()

    if args.task in [
        "vstar",
        "blink_viscorr",
        "blink_semcorr",
        "blink_depth",
        "blink_jigsaw",
        "blink_spatial",
        "mmvp",
    ]:
        task_type = "vision"
        task_name = None

    elif args.task in ["geometry", "geometry_new"]:
        task_type = "geo"
        task_name = None

    else:
        task_type = "math"
        task_name = args.task

    run_task(
        args.task,
        "outputs",
        task_type=task_type,
        task_name=task_name,
        baseline=args.baseline,
    )
