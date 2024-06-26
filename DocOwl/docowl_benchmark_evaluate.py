import json
import jsonlines
from docowl_infer import DocOwlInfer
from tqdm import tqdm
import os
from icecream import ic
from evaluation.benchmarks_eval import (
    llm_text_localization_eval,
    llm_textcaps_textvqa_eval,
    llm_benchmark_eval,
)
from evaluation.due_benchmarks_eval import llm_duebenchmark_eval
import argparse


def read_jsonl(filename):
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in jsonlines.Reader(f):
            lines.append(line)
    return lines


def save_jsonl(data, filename, print_log=True):
    """data is a list"""
    with open(filename, "w") as f:
        f.write("\n".join([json.dumps(e, ensure_ascii=False) for e in data]))

    if print_log:
        print("save %d samples to %s" % (len(data), filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="docowl1.5 benchmark evaluation")
    parser.add_argument("--model_path", type=str, help="the directory path of model")
    parser.add_argument(
        "--dataset",
        type=str,
        choices=[
            "DocVQA",
            "InfographicsVQA",
            "WikiTableQuestions",
            "DeepForm",
            "KleisterCharity",
            "TabFact",
            "ChartQA",
            "TextVQA",
            "TextCaps",
            "VisualMRC",
        ],
    )
    parser.add_argument(
        "--downstream_dir", type=str, help="the directory path of DocDownstream-1.0"
    )
    parser.add_argument(
        "--save_dir", type=str, help="the directory to save predictions of the model"
    )
    args = parser.parse_args()

    model_path = args.model_path
    dataset = args.dataset
    downstream_dir = args.downstream_dir
    save_dir = args.save_dir

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    test_path = os.path.join(downstream_dir, "test", dataset + "_test.jsonl")
    save_path = os.path.join(save_dir, dataset + "_test_pred.jsonl")

    if os.path.exists(save_path):
        print(save_path + " exists, skip inference. ")
    else:
        docowl = DocOwlInfer(
            ckpt_path=model_path, anchors="grid_9", add_global_img=True
        )
        print("load model from ", model_path)
        # infer the test samples one by one
        test_samples = read_jsonl(test_path)
        infer_results = []
        for sample in tqdm(test_samples):
            image = os.path.join(downstream_dir, sample["image"][0])
            assert os.path.exists(image)
            question = sample["messages"][0]
            answer = sample["messages"][1]
            assert question["role"] == "user"
            assert answer["role"] == "assistant"
            query = question["content"].replace("<|image|>", "")
            gt_answer = answer["content"]
            model_answer = docowl.inference(image, query)
            sample["model_answer"] = model_answer
            sample["gt_answer"] = gt_answer
            ic(model_answer, gt_answer)
            infer_results.append(sample)
        save_jsonl(infer_results, save_path)

    # calculate metrics
    pred_path = save_path

    if not os.path.exists(pred_path):
        print("not exists:", pred_path)
        exit(0)

    meta_dir = os.path.join(downstream_dir, "meta")

    if dataset in [
        "DeepForm",
        "DocVQA",
        "InfographicsVQA",
        "KleisterCharity",
        "WikiTableQuestions",
    ]:
        llm_duebenchmark_eval(
            dataset_name=dataset,
            split="test",
            llm_pred_path=pred_path,
            meta_dir=meta_dir,
        )
    elif dataset in ["TabFact"]:
        llm_benchmark_eval(
            metric_names=["ExactAccuracy"], result_path=pred_path, save_each_eval=True
        )
    elif dataset in ["ChartQA"]:
        llm_benchmark_eval(
            metric_names=["RelaxedAccuracy"], result_path=pred_path, save_each_eval=True
        )
    elif dataset in ["TextCaps", "TextVQA"]:
        llm_textcaps_textvqa_eval(
            result_path=pred_path, dataset=dataset, split="test", meta_dir=meta_dir
        )
    elif dataset in ["VisualMRC"]:
        llm_benchmark_eval(
            metric_names=[
                "BLEU1",
                "BLEU2",
                "BLEU3",
                "BLEU4",
                "Meteor",
                "RougeL",
                "CIDEr",
            ],
            result_path=pred_path,
            save_each_eval=True,
        )

    print("==============================================")
